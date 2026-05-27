"""Multi-provider extraction: text → KnowledgeGraph JSON.

Supports DeepSeek and MiMo APIs — both OpenAI-compatible.
"""
from __future__ import annotations

import os
from typing import Literal

from .knowledge_graph import KnowledgeGraph

Provider = Literal["deepseek", "mimo", "auto"]

DEFAULT_MODELS: dict[str, str] = {
    "deepseek": "deepseek-chat",
    "mimo": "mimo-v2.5",
}

MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"

EXTRACTION_PROMPT = """You are a knowledge graph extraction engine for educational content. Analyze the input and extract a structured knowledge graph.

## Output Format (JSON)

Return ONLY valid JSON with this exact structure:
```json
{
  "title": "short descriptive title",
  "concepts": [
    {
      "id": "c1",
      "name": "Concept Name",
      "description": "1-2 sentence clear explanation in Chinese",
      "category": "one of: definition|principle|example|application|theory|person|event|process|other",
      "difficulty": "basic|intermediate|advanced"
    }
  ],
  "relations": [
    {
      "source": "c1",
      "target": "c2",
      "type": "one of: influences|prerequisite_of|part_of|contrasts_with|example_of|leads_to|relates_to",
      "label": "short label in Chinese describing the relationship"
    }
  ],
  "layout_hint": "one of: force_directed|radial|hierarchical|timeline"
}
```

## Guidelines

- Extract 5-20 concepts (enough to capture key ideas, not too granular)
- Each concept name should be short (2-8 characters)
- Every concept must have at least one relation unless there's only one concept
- Use meaningful relationship labels in Chinese
- Choose layout_hint based on content:
  - "radial" if there's a clear central topic with branches
  - "hierarchical" if there's a clear parent-child or step-by-step structure
  - "timeline" if there are chronological events
  - "force_directed" for general interconnected concepts
- Prefer Chinese for names, descriptions, and labels
- Category mapping: 概念定义→definition, 原理规律→principle, 例子案例→example, 实际应用→application, 理论学派→theory, 人物学者→person, 历史事件→event, 流程步骤→process

## Input Text

__TEXT__"""


def _resolve_provider(provider: Provider) -> str:
    if provider != "auto":
        return provider
    if os.environ.get("DEEPSEEK_API_KEY"):
        return "deepseek"
    if os.environ.get("MIMO_API_KEY"):
        return "mimo"
    raise ValueError(
        "No API key found. Set DEEPSEEK_API_KEY or MIMO_API_KEY."
    )


def _extract_via_openai_compatible(text: str, api_key: str | None, model: str,
                                    base_url: str) -> KnowledgeGraph:
    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = EXTRACTION_PROMPT.replace("__TEXT__", text[:8000])

    response = client.chat.completions.create(
        model=model,
        max_tokens=8192,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_response(response.choices[0].message.content or "")


def _extract_via_deepseek(text: str, api_key: str | None, model: str) -> KnowledgeGraph:
    key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise ValueError("DEEPSEEK_API_KEY not set")
    return _extract_via_openai_compatible(text, key, model, "https://api.deepseek.com")


def _extract_via_mimo(text: str, api_key: str | None, model: str) -> KnowledgeGraph:
    key = api_key or os.environ.get("MIMO_API_KEY")
    if not key:
        raise ValueError("MIMO_API_KEY not set")
    return _extract_via_openai_compatible(text, key, model, MIMO_BASE_URL)


def _parse_response(raw: str) -> KnowledgeGraph:
    """Parse LLM response, handling markdown code fences and common JSON issues."""
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    # Try direct parse first
    try:
        kg = KnowledgeGraph.from_json(raw)
        kg.source = "text"
        concept_ids = {c.id for c in kg.concepts}
        kg.relations = [r for r in kg.relations
                        if r.source in concept_ids and r.target in concept_ids]
        return kg
    except Exception:
        pass

    # Repair common AI JSON issues
    import re
    repaired = raw

    # 1. Truncate to last complete key-value or list element
    repaired = _truncate_to_last_complete(repaired)

    # 2. Close all open brackets/braces in correct nesting order
    closing_stack = []
    escape = False
    in_string = False
    for ch in repaired:
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            closing_stack.append('}')
        elif ch == '[':
            closing_stack.append(']')
        elif ch == '}':
            if closing_stack and closing_stack[-1] == '}':
                closing_stack.pop()
        elif ch == ']':
            if closing_stack and closing_stack[-1] == ']':
                closing_stack.pop()
    repaired += ''.join(reversed(closing_stack))

    # 3. Remove trailing commas (now that brackets are closed)
    repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
    # Also strip bare trailing commas
    repaired = repaired.rstrip().rstrip(',')

    kg = KnowledgeGraph.from_json(repaired)
    kg.source = "text"

    # Drop relations referencing concepts that don't exist (truncated JSON)
    concept_ids = {c.id for c in kg.concepts}
    kg.relations = [r for r in kg.relations
                    if r.source in concept_ids and r.target in concept_ids]
    return kg


def _truncate_to_last_complete(s: str) -> str:
    """Find the last position where a JSON key-value pair or list element ends cleanly,
    then truncate there so we can close the structure ourselves."""
    in_string = False
    escape = False
    depth = 0  # {} depth
    array_depth = 0  # [] depth
    last_safe = 0

    for i, ch in enumerate(s):
        if escape:
            escape = False
            continue
        if ch == '\\':
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == '[':
            array_depth += 1
        elif ch == ']':
            array_depth -= 1
        elif ch == ',' and depth > 0:
            # A comma at depth > 0 means we just finished a key:value or list element
            last_safe = i

    # If the JSON ends cleanly, don't truncate
    if not in_string and depth >= 0:
        return s

    # Try cutting at last_safe (after which we can close ourselves)
    if last_safe > 0:
        return s[:last_safe]

    return s


_EXTRACTORS = {
    "deepseek": _extract_via_deepseek,
    "mimo": _extract_via_mimo,
}


def extract_knowledge_graph(
    text: str,
    api_key: str | None = None,
    model: str | None = None,
    provider: Provider = "auto",
) -> KnowledgeGraph:
    provider = _resolve_provider(provider)
    model = model or DEFAULT_MODELS[provider]
    extract_fn = _EXTRACTORS[provider]
    return extract_fn(text, api_key=api_key, model=model)
