# Multimodal-Viz Project Instructions

## Project
CustomTkinter desktop app that converts text/PDF documents into interactive knowledge graph HTML. Powered by DeepSeek and MiMo AI models via OpenAI-compatible API.

## Key Paths
- Entry: `main.py`
- Main window: `app/main_window.py`
- Processing: `app/services.py`
- AI extraction: `core/extractor.py`
- Data models: `core/knowledge_graph.py`
- HTML render: `core/html_renderer.py`
- Theme tokens: `gui/theme.py`
- PyInstaller spec: `multimodal-viz.spec`

## Before Making Changes
1. Read `docs/memory-bank/02-architecture.md` for module boundaries
2. Read `docs/memory-bank/05-conventions.md` for code style
3. Read `docs/memory-bank/04-progress.md` for current state

## Rules
- All UI uses CustomTkinter (ctk), never tkinter directly
- Colors/fonts/spacing from `gui/theme.py` tokens only
- Chinese comments only when necessary, no docstrings
- API keys always from .env, never hardcoded
- Commit messages in English: `type: description`
- Never commit .env, dist/, build/, __pycache__

## Build
```bash
pyinstaller -y multimodal-viz.spec
```

## Test
```bash
python -c "from core.extractor import _parse_response; ..."
```
