"""Processing pipeline: file → knowledge graph → HTML/JSON/article."""
from __future__ import annotations

from pathlib import Path

from core.extractor import extract_knowledge_graph
from core.html_renderer import kg_to_article, kg_to_html
from core.knowledge_graph import KnowledgeGraph
from core.pdf_reader import chunk_text, extract_text_from_pdf, merge_knowledge_graphs

MODE_MAP: dict[str, str] = {
    "concept-map": "force_directed",
    "mind-map": "radial",
    "flowchart": "hierarchical",
    "timeline": "timeline",
    "auto": "auto",
}


def process_file(filepath: Path, output_dir: Path, provider: str = "auto",
                 mode: str = "auto", status_callback=None) -> dict | None:
    cb = status_callback or (lambda m: None)
    stem = filepath.stem
    suffix = filepath.suffix.lower()

    cb("📖 读取文件...")
    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(filepath)
    else:
        raw_text = filepath.read_text(encoding="utf-8")

    if not raw_text.strip():
        return None

    cb("🤖 调用 AI 提取概念...")
    if suffix == ".pdf":
        chunks = chunk_text(raw_text)
        graphs = []
        for chunk in chunks:
            try:
                kg = extract_knowledge_graph(chunk, provider=provider)
                graphs.append(kg)
            except Exception:
                pass
        if not graphs:
            return None
        merged = merge_knowledge_graphs(graphs, title=stem)
        kg = KnowledgeGraph.from_json(merged)
    else:
        kg = extract_knowledge_graph(raw_text, provider=provider)
        kg.title = stem

    if mode != "auto":
        kg.layout_hint = MODE_MAP.get(mode, "force_directed")

    json_path = output_dir / f"{stem}.json"
    html_path = output_dir / f"{stem}.html"
    article_path = output_dir / f"{stem}_article.md"

    cb("📄 生成交互网页...")
    kg.save(json_path)
    html_content = kg_to_html(kg)
    html_path.write_text(html_content, encoding="utf-8")
    article_content = kg_to_article(kg)
    article_path.write_text(article_content, encoding="utf-8")

    cb("✓ 完成")
    return {
        "input": filepath.name, "html": str(html_path),
        "json": str(json_path), "article": str(article_path),
        "concepts": len(kg.concepts), "relations": len(kg.relations),
    }
