# Desktop Packaging Design Spec

**Date:** 2026-05-26
**Status:** Draft

## 1. Purpose

Package `multimodal-viz` as a standalone Windows desktop application (EXE) with a clean, minimal GUI. Non-technical users can double-click to launch, drop in files, and get interactive knowledge graph HTML output — no Python installation required.

## 2. User Flow

```
首次启动
  → 检测 .env 不存在
  → 弹窗："请粘贴你的 DeepSeek API Key"
  → 用户粘贴 → 写入 .env → 主界面

日常使用
  → 双击 EXE → 主界面
  → 拖放 .txt/.md/.pdf 到拖放区
  → 选择输出目录（默认上次选择）
  → 点击"开始生成"
  → 进度条 + 实时日志
  → 完成 → 按钮打开 HTML / 打开文件夹

已有 .env 时
  → 直接进入主界面
  → API 状态灯绿色 "DeepSeek ✓"
```

## 3. Architecture

```
gui_app.py (NEW — tkinter + ttkbootstrap)
  ├── FirstRunDialog     — API Key 输入弹窗
  ├── MainWindow         — 主界面布局 + 事件绑定
  │   ├── DropZone       — 拖放区域组件
  │   ├── FileList       — 文件列表 + 移除
  │   ├── ProgressBar    — 进度条 + 状态文本
  │   └── OutputPanel    — 输出结果展示
  └── ProcessingThread   — 后台线程，调用 process_file()

multimodal_viz/ (EXISTING — 复用)
  ├── extractor.py       — LLM 知识图谱提取
  ├── knowledge_graph.py — 数据模型
  ├── html_renderer.py   — HTML 生成 (MODIFIED: vis-network 内联)
  ├── pdf_reader.py      — PDF 文本提取
  └── __init__.py        — .env 加载 (MODIFIED: frozen 路径)
```

## 4. Visual Design — 小清新风格

**Theme:** ttkbootstrap `litera`
- Background: `#FAFAFA` (warm off-white)
- Primary: `#4CAF50` (mint green — buttons, progress bar)
- Accent: `#F26B1D` (warm orange — highlights, links)
- Card bg: `#FFFFFF` with `#E8E8E8` border, 8px radius

**Typography:**
- Title: Microsoft YaHei 12pt bold
- Body: Microsoft YaHei 10pt
- Monospace: Consolas 9pt (status log)

**Layout (500×650px default, resizable):**

```
┌─────────────────────────────────────────────┐
│  📊 多模态知识图谱可视化生成器               │
│             小清新 · 知识探索               │
├─────────────────────────────────────────────┤
│  API: ● DeepSeek ✓               [⚙ 设置]  │
├─────────────────────────────────────────────┤
│  输出目录:                                  │
│  [_____________________________] [📁 浏览]  │
├─────────────────────────────────────────────┤
│  ┌─ 📂 拖放文件到此处 ───────────────────┐  │
│  │        .txt  .md  .pdf                │  │
│  │    点击或拖放以添加文件               │  │
│  └───────────────────────────────────────┘  │
│  文件列表 (2):                              │
│  ├ 📄 docker_agent_deploy.txt    [✕ 移除]  │
│  └ 📄 learning_theories.txt      [✕ 移除]  │
├─────────────────────────────────────────────┤
│  [▶ 开始生成]    [📁 打开输出目录]         │
│                                             │
│  ████████████████░░░░░░ 65%                │
│  ↳ 处理中: docker_agent.txt · 12 概念      │
│                                             │
│  已生成:                                    │
│  ✓ docker_agent.html · 12 概念, 8 关系     │
│  ✓ docker_agent.json · [查看]              │
├─────────────────────────────────────────────┤
│  ● DeepSeek 已连接      已处理 1/2 个文件  │
└─────────────────────────────────────────────┘
```

## 5. Component Specs

### 5.1 DropZone

- `tkinterdnd2` for native drag-and-drop on Windows
- Dashed border `#4CAF50` on white background
- Hover: border goes solid, bg shifts to `#E8F5E9`
- Click opens `filedialog.askopenfilenames()`
- Accepts: `.txt`, `.md`, `.pdf`

### 5.2 FileList

- Scrollable frame showing added files
- Each row: file icon emoji + filename + [✕ 移除] button
- Remove updates list and refreshes UI

### 5.3 ProgressBar

- ttkbootstrap `Striped` + `info` color
- Percentage text overlaid
- Below: status text "处理中: xxx · N 概念, M 关系"
- After completion: "✓ 全部完成"

### 5.4 FirstRunDialog

- Toplevel modal window
- Title: "欢迎使用 · API 配置"
- Description: "请输入你的 DeepSeek API Key 以开始使用"
- Input: password-masked Entry field
- Buttons: [跳过] [保存并开始]
- On save: write `.env`, reload `os.environ`

### 5.5 ProcessingThread

- `threading.Thread(daemon=True)`
- Iterates files, calls existing `process_file()` from `run_pipeline.py`
- Communicates via `queue.Queue` to main thread
- Main thread polls queue every 100ms via `root.after()`
- Messages: `("progress", value)`, `("status", text)`, `("done", result_dict)`, `("error", msg)`

## 6. Existing Code Changes

### 6.1 html_renderer.py — vis-network offline

```python
# Before (line 154):
<script src="https://unpkg.com/vis-network@9.1.6/dist/vis-network.min.js"></script>

# After:
<script>{vis_js_content}</script>

# Where vis_js_content is loaded from assets/vis-network.min.js
# using _get_asset_path() helper that handles sys._MEIPASS
```

### 6.2 __init__.py — frozen-aware .env path

```python
# Before:
_env_path = Path(__file__).parent.parent / ".env"

# After:
def _get_env_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / ".env"
    return Path(__file__).parent.parent / ".env"
```

### 6.3 requirements.txt — fix deps

```
click>=8.0.0
pydantic>=2.0.0
anthropic>=0.40.0
openai>=1.0.0
PyMuPDF>=1.23.0
python-dotenv>=1.0.0
ttkbootstrap>=1.10.0
tkinterdnd2>=0.4.0
```

Remove: `jinja2>=3.1.0` (unused)

## 7. PyInstaller Config

```python
# multimodal-viz.spec
# OneDir, console=False (Windows GUI app)
# Hidden imports: fitz, openai, anthropic, pydantic, ttkbootstrap, tkinterdnd2
# Data: multimodal_viz/assets/vis-network.min.js
# Excludes: numpy, pandas, scipy, matplotlib, tensorflow, torch, tkinter.test
```

## 8. Distribution

```
multimodal-viz-v0.2.0.zip
├── multimodal-viz.exe
├── .env.example
├── README.txt        (Chinese, simple setup + usage)
└── _internal/        (PyInstaller bundled deps)
```

README content:
```
多模态知识图谱可视化生成器 v0.2

使用步骤：
1. 双击 multimodal-viz.exe 启动
2. 首次使用会提示输入 DeepSeek API Key
   （在 platform.deepseek.com 注册获取）
3. 拖放 .txt / .md / .pdf 文件
4. 选择输出目录
5. 点击"开始生成"
6. 双击生成的 .html 文件在浏览器中查看

API Key 申请：https://platform.deepseek.com
联系作者：[your email]

祝你探索知识愉快 🌱
```

## 9. Files Changed / Created

| File | Action | Scope |
|---|---|---|
| `multimodal_viz/html_renderer.py` | Modify | vis-network CDN → inline |
| `multimodal_viz/__init__.py` | Modify | frozen-aware .env path |
| `multimodal_viz/assets/vis-network.min.js` | Create | JS lib file |
| `gui_app.py` | Create | ~400 lines, tkinter GUI |
| `requirements.txt` | Modify | add openai, dotenv, ttkbootstrap, tkinterdnd2; remove jinja2 |
| `multimodal-viz.spec` | Create | PyInstaller config |
| `build_exe.bat` | Create | Build script |
| `README.txt` | Create | User guide |
| `.env.example` | Modify | Add instructions |

Unchanged: `cli.py`, `extractor.py`, `knowledge_graph.py`, `pdf_reader.py`, `run_pipeline.py`, `一键生成.bat`

## 10. Edge Cases & Error Handling

- **No .env & user clicks "跳过"**: Enter main interface, API status shows "未配置", disable "开始生成" button, show hint "请点击 ⚙ 设置配置 API Key"
- **Invalid API Key**: First file fails with "401 Unauthorized" → show error dialog "API Key 无效，请重新设置" → re-open FirstRunDialog
- **Empty file**: Skip with log "跳过空文件: xxx"
- **PDF with no text layer**: Show warning "PDF 可能为扫描件，无文本层: xxx"
- **Network error during API call**: Show error "网络连接失败: xxx", continue with remaining files
- **Processing error mid-file**: Log error, continue with next file, don't crash
- **Output directory deleted mid-processing**: Recreate via `mkdir(parents=True)`
- **Output directory default**: Stored in `output_dir.cfg` next to `.env`, defaults to user's Desktop on first run
- **tkinterdnd2 + PyInstaller**: Copy `tkinterdnd2/tkdnd` folder to dist root in build script; add `--collect-all tkinterdnd2` in spec

## 11. Build Prerequisites

Before running PyInstaller:
```bash
# Download vis-network standalone UMD
npm install vis-network@9.1.6
# Copy to assets
copy node_modules\vis-network\standalone\umd\vis-network.min.js multimodal_viz\assets\
```

## 12. Verification

```bash
# Dev test
python gui_app.py
# → GUI launches, drag-drop works, processing works, output files valid

# Build
pyinstaller --clean multimodal-viz.spec
# → dist/multimodal-viz/ created with EXE

# EXE test
Remove DEEPSEEK_API_KEY from env
Launch dist/multimodal-viz/multimodal-viz.exe
# → FirstRunDialog appears
Paste key → save
# → MainWindow appears
Drop test .txt file
Click start
# → Processing completes, HTML opens offline in browser
```
