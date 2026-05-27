"""CLI entry point for multimodal learning content visualization."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from .extractor import extract_knowledge_graph
from .html_renderer import kg_to_article, kg_to_html
from .knowledge_graph import KnowledgeGraph, auto_detect_layout
from .pdf_reader import chunk_text, extract_text_from_pdf, merge_knowledge_graphs


@click.command()
@click.argument(
    "input",
    type=str,
)
@click.option(
    "-m", "--mode",
    type=click.Choice(["concept-map", "mind-map", "timeline", "flowchart", "auto"]),
    default="auto",
    help="Visualization mode (default: auto-detect)",
)
@click.option(
    "-o", "--output",
    type=click.Path(),
    default=None,
    help="Output HTML file path (default: <input_stem>.html)",
)
@click.option(
    "--json-only",
    is_flag=True,
    help="Only output knowledge graph JSON, skip HTML generation",
)
@click.option(
    "--provider",
    "-p",
    type=click.Choice(["deepseek", "anthropic", "auto"]),
    default="auto",
    help="LLM provider (default: auto-detect from env vars)",
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="API key (or set DEEPSEEK_API_KEY / ANTHROPIC_API_KEY env var)",
)
@click.option(
    "--model",
    type=str,
    default=None,
    help="Model name (default: provider's recommended model)",
)
@click.option(
    "--save-json",
    type=click.Path(),
    default=None,
    help="Save intermediate knowledge graph JSON to file",
)
def main(
    input: str,
    mode: str,
    output: str | None,
    json_only: bool,
    provider: str,
    api_key: str | None,
    model: str | None,
    save_json: str | None,
):
    """Extract knowledge graphs from text or PDF and generate interactive visualizations.

    INPUT can be:
      - A text string (inline):  multimodal-viz "建构主义是..."
      - A .txt file path:        multimodal-viz notes.txt
      - A .pdf file path:        multimodal-viz paper.pdf
    """

    # --- Step 1: Determine input type and extract text ---
    potential_path = Path(input)

    if potential_path.suffix.lower() == ".pdf":
        click.echo(f"[PDF] Reading: {potential_path}")
        raw_text = extract_text_from_pdf(potential_path)
        source_type = "pdf"
    elif potential_path.exists() and potential_path.suffix.lower() in (".txt", ".md"):
        click.echo(f"[FILE] Reading text file: {potential_path}")
        raw_text = potential_path.read_text(encoding="utf-8")
        source_type = "text_file"
    else:
        click.echo("[TEXT] Processing inline text input")
        raw_text = input
        source_type = "text"

    click.echo(f"   Text length: {len(raw_text)} chars")

    # --- Step 2: Extract knowledge graph(s) via Claude API ---
    if source_type == "pdf":
        chunks = chunk_text(raw_text)
        click.echo(f"[EXTRACT] Processing {len(chunks)} text chunks...")

        graphs = []
        for i, chunk in enumerate(chunks):
            click.echo(f"   Chunk {i + 1}/{len(chunks)} ({len(chunk)} chars)")
            try:
                kg = extract_knowledge_graph(chunk, api_key=api_key, model=model, provider=provider)
                graphs.append(kg)
                click.echo(f"   -> {len(kg.concepts)} concepts, {len(kg.relations)} relations")
            except Exception as e:
                click.echo(f"   [WARN] Failed: {e}", err=True)

        if not graphs:
            click.echo("[ERROR] No knowledge graphs extracted from PDF.", err=True)
            sys.exit(1)

        merged = merge_knowledge_graphs(graphs, title=potential_path.stem)
        kg = KnowledgeGraph.from_json(merged)
        click.echo(f"[MERGED] {len(kg.concepts)} concepts, {len(kg.relations)} relations")
    else:
        click.echo("[EXTRACT] Extracting knowledge graph via Claude API...")
        kg = extract_knowledge_graph(raw_text, api_key=api_key, model=model, provider=provider)
        click.echo(f"   Extracted: {len(kg.concepts)} concepts, {len(kg.relations)} relations")

    kg.source = source_type

    # --- Step 3: Auto-detect layout if needed ---
    if mode == "auto":
        detected = auto_detect_layout(kg)
        kg.layout_hint = detected
        click.echo(f"[LAYOUT] Auto-detected: {detected}")
    else:
        mode_map = {
            "concept-map": "force_directed",
            "mind-map": "radial",
            "timeline": "timeline",
            "flowchart": "hierarchical",
        }
        kg.layout_hint = mode_map[mode]

    # --- Step 4: Output ---
    if save_json:
        kg.save(save_json)
        click.echo(f"[SAVED] Knowledge graph JSON: {save_json}")

    if json_only:
        click.echo(kg.to_json())
        return

    # Determine output base path
    if output is None:
        stem = potential_path.stem if potential_path.exists() and potential_path.suffix else "knowledge_graph"
        output = f"{stem}.html"
    output_path = Path(output).resolve()
    base_name = output_path.stem
    base_dir = output_path.parent

    # 1. Save knowledge graph JSON
    json_path = base_dir / f"{base_name}.json"
    kg.save(json_path)
    click.echo(f"\n[JSON] Knowledge graph: {json_path}")

    # 2. Generate interactive vis.js HTML (quick preview)
    html_content = kg_to_html(kg)
    html_path = base_dir / f"{base_name}.html"
    html_path.write_text(html_content, encoding="utf-8")
    click.echo(f"[HTML] Interactive concept map: {html_path}")

    # 3. Generate article.md for web-video-presentation
    article_content = kg_to_article(kg)
    article_path = base_dir / f"{base_name}_article.md"
    article_path.write_text(article_content, encoding="utf-8")
    click.echo(f"[ARTICLE] For web-video-presentation: {article_path}")

    # Print summary
    click.echo(f"\n{'='*50}")
    click.echo(f"Title: {kg.title}")
    click.echo(f"Concepts: {len(kg.concepts)}")
    click.echo(f"Relations: {len(kg.relations)}")
    click.echo(f"Layout: {kg.layout_hint}")
    click.echo(f"\nOutput files:")
    click.echo(f"  1. {json_path.name}  - raw knowledge graph data")
    click.echo(f"  2. {html_path.name}  - interactive concept map (open in browser)")
    click.echo(f"  3. {article_path.name}  - feed to web-video-presentation skill")
    click.echo(f"\nConcepts:")
    for c in kg.concepts:
        click.echo(f"  [{c.id}] {c.name} ({c.category}, {c.difficulty})")
    if kg.relations:
        click.echo(f"\nRelations:")
        for r in kg.relations:
            click.echo(f"  {r.source} --[{r.type.value}]--> {r.target}: {r.label}")


if __name__ == "__main__":
    main()
