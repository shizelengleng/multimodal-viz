"""一键知识图谱生成工具 —— 放入文件 → 运行 → 得到可视化结果"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Add parent to path so we can import multimodal_viz
sys.path.insert(0, str(Path(__file__).parent))

from multimodal_viz.extractor import extract_knowledge_graph
from multimodal_viz.html_renderer import kg_to_article, kg_to_html
from multimodal_viz.knowledge_graph import KnowledgeGraph
from multimodal_viz.pdf_reader import chunk_text, extract_text_from_pdf, merge_knowledge_graphs


def setup_project(project_name: str) -> tuple[Path, Path]:
    """Create project folder structure under E:\\知识图谱生成"""
    base = Path("E:/知识图谱生成")
    base.mkdir(parents=True, exist_ok=True)

    project_dir = base / project_name
    input_dir = project_dir / "input"
    output_dir = project_dir / "output"

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    return input_dir, output_dir


def process_file(filepath: Path, output_dir: Path, provider: str) -> dict | None:
    """Process a single file: extract KG, generate HTML + JSON + article."""
    stem = filepath.stem
    suffix = filepath.suffix.lower()
    print(f"\n{'─'*50}")
    print(f"处理: {filepath.name}")

    # Step 1: Extract text
    if suffix == ".pdf":
        print(f"  [PDF] 提取文本...")
        raw_text = extract_text_from_pdf(filepath)
        source_type = "pdf"
    else:
        print(f"  [TEXT] 读取文本...")
        raw_text = filepath.read_text(encoding="utf-8")
        source_type = "text_file"

    print(f"  文本长度: {len(raw_text)} 字符")

    # Step 2: Extract knowledge graph
    if source_type == "pdf":
        chunks = chunk_text(raw_text)
        print(f"  [提取] {len(chunks)} 个文本块...")
        graphs = []
        for i, chunk in enumerate(chunks):
            print(f"    块 {i + 1}/{len(chunks)} ({len(chunk)} 字符)")
            try:
                kg = extract_knowledge_graph(chunk, provider=provider)
                graphs.append(kg)
            except Exception as e:
                print(f"    [警告] 块 {i + 1} 失败: {e}")
        if not graphs:
            print("[错误] 未能从 PDF 提取知识图谱")
            return None
        merged = merge_knowledge_graphs(graphs, title=stem)
        kg = KnowledgeGraph.from_json(merged)
    else:
        print(f"  [提取] 调用 LLM API...")
        kg = extract_knowledge_graph(raw_text, provider=provider)
        kg.title = stem

    print(f"  提取: {len(kg.concepts)} 个概念, {len(kg.relations)} 条关系")

    # Step 3: Generate outputs
    json_path = output_dir / f"{stem}.json"
    html_path = output_dir / f"{stem}.html"
    article_path = output_dir / f"{stem}_article.md"

    kg.save(json_path)
    print(f"  [JSON] {json_path.name}")

    html_content = kg_to_html(kg)
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  [HTML] {html_path.name}")

    article_content = kg_to_article(kg)
    article_path.write_text(article_content, encoding="utf-8")
    print(f"  [文章] {article_path.name}")

    return {
        "input": filepath.name,
        "html": str(html_path),
        "json": str(json_path),
        "article": str(article_path),
        "concepts": len(kg.concepts),
        "relations": len(kg.relations),
    }


def main():
    print("╔══════════════════════════════════════╗")
    print("║   多模态知识图谱可视化生成器       ║")
    print("║   Multimodal Knowledge Graph Viz    ║")
    print("╚══════════════════════════════════════╝")
    print()

    # Project name
    project_name = input("\n项目名称 (例: my_research): ").strip()
    if not project_name:
        project_name = "untitled"
    project_name = project_name.replace(" ", "_")

    input_dir, output_dir = setup_project(project_name)

    print(f"\n文件夹已创建:")
    print(f"  输入: {input_dir}")
    print(f"  输出: {output_dir}")

    # Copy example files if input is empty
    existing = list(input_dir.glob("*.txt")) + list(input_dir.glob("*.md")) + list(input_dir.glob("*.pdf"))
    if not existing:
        print(f"\ninput 文件夹为空，你可以放入自己的 .txt / .md / .pdf 文件。")
        print(f"或者输入 'demo' 使用示例文件...")

    action = input(f"\n按 Enter 开始处理 input 文件夹中的文件\n输入 'demo' 复制示例文件到 input: ").strip()

    if action.lower() == "demo":
        examples = Path(__file__).parent / "examples"
        for f in ["docker_agent_deploy.txt", "learning_theories.txt"]:
            src = examples / f
            if src.exists():
                dst = input_dir / f
                dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"  复制: {f}")
        print("示例文件已放入 input 文件夹。")

    # Find files to process
    files = list(input_dir.glob("*.txt")) + list(input_dir.glob("*.md")) + list(input_dir.glob("*.pdf"))
    if not files:
        print(f"\n[提示] input 文件夹中没有 .txt / .md / .pdf 文件。")
        print(f"   请将文件放入: {input_dir}")
        print(f"   然后重新运行本程序。")
        input("\n按 Enter 退出...")
        return

    print(f"\n找到 {len(files)} 个文件，开始处理...")

    results = []
    for f in files:
        result = process_file(f, output_dir, provider="auto")
        if result:
            results.append(result)

    # Summary
    if results:
        print(f"\n{'='*50}")
        print(f"完成! 共处理 {len(results)} 个文件")
        print(f"{'='*50}")
        print(f"\n产物在: {output_dir}")
        print()
        for r in results:
            print(f"  {r['input']} → {r['concepts']} 概念, {r['relations']} 关系")
            print(f"    打开: {Path(r['html']).name}")
            print(f"    数据: {Path(r['json']).name}")
        print(f"\n双击 .html 文件即可在浏览器中探索知识图谱。")
    else:
        print("\n没有文件被成功处理。")

    input(f"\n按 Enter 退出...")


if __name__ == "__main__":
    main()
