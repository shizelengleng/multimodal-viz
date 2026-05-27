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

## Rules
- All UI uses CustomTkinter (ctk), never tkinter directly
- Colors/fonts/spacing from `gui/theme.py` tokens only
- Chinese comments only when necessary, no docstrings
- API keys always from .env, never hardcoded
- Commit messages in English: `type: description`
- Never commit .env, dist/, build/, __pycache__

## Development Workflow

### Git Strategy — Trunk-based
- `main` branch always shippable
- New feature → `feature/<name>` branch → merge to `main`
- Bug fix → `fix/<name>` branch → merge to `main`
- Tag releases: `v0.5.4`, `v0.6.0`, etc.
- No force push to main ever

### Daily Flow
1. Make changes directly — skip plan mode unless the task touches 3+ files or changes architecture
2. If modifying `core/` logic, add a test in `tests/`
3. Manual verification: run `python main.py`
4. Commit: `type: description` (feat/fix/chore/docs)
5. Push to GitHub

### When to Update Docs
| File | When |
|------|------|
| `CHANGELOG.md` | Each release |
| `docs/memory-bank/03-implementation-plan.md` | Plans change |
| `docs/memory-bank/04-progress.md` | End of each dev session |
| `docs/memory-bank/02-architecture.md` | Module structure changes (rare) |
| `docs/memory-bank/01-product-design.md` | Product direction changes (very rare) |

### Autonomous Execution
- Execute tasks without pausing to confirm each step
- Only stop for: blocked (can't resolve), ambiguity that prevents progress, or all tasks complete
- Don't ask "should I continue?" — just continue

### Before Making Changes
1. Read `docs/memory-bank/02-architecture.md` for module boundaries
2. Read `docs/memory-bank/05-conventions.md` for code style
3. Read `docs/memory-bank/04-progress.md` for current state

## Build
```bash
pyinstaller -y multimodal-viz.spec
```

## Test
```bash
python -c "from core.extractor import _parse_response; ..."
```
