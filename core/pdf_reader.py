"""PDF text extraction and cleaning with PyMuPDF"""

from __future__ import annotations

import re
from pathlib import Path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract and clean text from a PDF file.

    Uses PyMuPDF for fast, accurate text extraction.
    Handles common PDF artifacts: headers/footers, hyphenation, whitespace.
    Falls back to a temp copy if the path contains characters that trip the C layer.
    """
    import fitz
    path_str = str(pdf_path)

    try:
        doc = fitz.open(path_str)
    except Exception:
        import tempfile, shutil
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        try:
            shutil.copy2(path_str, tmp.name)
            doc = fitz.open(tmp.name)
        finally:
            tmp.close()
            try: Path(tmp.name).unlink(missing_ok=True)
            except Exception: pass
    pages: list[str] = []

    for page in doc:
        text = page.get_text("text")
        pages.append(text)

    doc.close()

    full_text = "\n".join(pages)
    return _clean_pdf_text(full_text)


def _clean_pdf_text(text: str) -> str:
    """Clean common PDF extraction artifacts."""
    # Remove hyphenation at line breaks (word-\nword → wordword)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Collapse 3+ newlines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove lines that are likely headers/footers
    # (short lines with only numbers, page numbers, etc.)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip page numbers
        if re.fullmatch(r"\d{1,4}", stripped):
            continue
        # Skip lines that are just "Page X" or similar
        if re.fullmatch(r"[Pp]age\s+\d+", stripped):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def chunk_text(text: str, max_chars: int = 6000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks for individual processing.

    Splits on paragraph boundaries when possible. Each chunk stays
    under max_chars to fit within Claude API context limits.
    """
    if len(text) <= max_chars:
        return [text]

    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        para_len = len(para)

        if current_len + para_len > max_chars and current:
            chunks.append("\n\n".join(current))
            # Keep last paragraph for overlap
            overlap_text = current[-1] if current else ""
            current = [overlap_text, para] if overlap_text else [para]
            current_len = len(overlap_text) + para_len if overlap_text else para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def merge_knowledge_graphs(graphs: list, title: str = "Combined Knowledge Graph") -> dict:
    """Merge multiple KnowledgeGraph results into one, removing duplicates.

    Deduplication strategy: concepts with highly similar names are merged.
    Relations are reconnected to the merged concept IDs.
    """
    if len(graphs) == 1:
        merged = graphs[0].model_dump()
        merged["source"] = "pdf"
        return merged

    seen_names: dict[str, str] = {}  # lower_name → id
    concepts: list[dict] = []
    relations: list[dict] = []
    id_map: dict[str, str] = {}  # old_id → new_id

    counter = 1
    for g in graphs:
        for c in g.concepts:
            name_key = c.name.strip().lower()
            if name_key in seen_names:
                id_map[c.id] = seen_names[name_key]
            else:
                new_id = f"c{counter}"
                id_map[c.id] = new_id
                seen_names[name_key] = new_id
                concepts.append({
                    "id": new_id,
                    "name": c.name,
                    "description": c.description,
                    "category": c.category,
                    "difficulty": c.difficulty,
                })
                counter += 1

    for g in graphs:
        for r in g.relations:
            new_source = id_map.get(r.source, r.source)
            new_target = id_map.get(r.target, r.target)
            if new_source == new_target:
                continue
            # Skip duplicate relations
            dup = any(
                existing["source"] == new_source
                and existing["target"] == new_target
                and existing["type"] == r.type.value
                for existing in relations
            )
            if not dup:
                relations.append({
                    "source": new_source,
                    "target": new_target,
                    "type": r.type.value,
                    "label": r.label,
                })

    return {
        "title": title,
        "source": "pdf",
        "layout_hint": "force_directed",
        "concepts": concepts,
        "relations": relations,
    }
