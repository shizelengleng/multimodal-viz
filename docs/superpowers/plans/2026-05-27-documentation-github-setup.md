# Documentation System & GitHub Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish Memory-Bank documentation system and push project to `github.com/shizelengleng/multimodal-viz`

**Architecture:** Create 8 documentation/config files across 4 directories (root, docs/memory-bank/, .github/, .claude/), clean sensitive data, init git, and push. All files are markdown — no code changes.

**Tech Stack:** Markdown, Git, GitHub

---

### Task 1: .gitignore — Protect sensitive files

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/.gitignore`

- [ ] **Step 1: Create .gitignore**

Write the file:

```gitignore
# Environment — API keys
.env

# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.egg

# Virtual environments
venv/
.venv/
env/

# PyInstaller
dist/
build/
*.spec.bak

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
Thumbs.db
.DS_Store
Desktop.ini

# Config with potential secrets
config/settings.cfg
```

- [ ] **Step 2: Verify .env won't be tracked**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git init && git status
```

Expected: .env does NOT appear in untracked files (it's gitignored).

- [ ] **Step 3: Commit .gitignore**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add .gitignore && git commit -m "chore: add .gitignore"
```

---

### Task 2: README.md — Project homepage

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/README.md`
- Delete: `C:/Users/123/Desktop/project/multimodal-viz/README.txt`

- [ ] **Step 1: Write README.md**

```markdown
# 多模态知识图谱可视化生成器

<div align="center">

**文本/PDF → AI 提取 → 交互式知识图谱 HTML**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green)](https://customtkinter.tomschimansky.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v0.5.3-brightgreen)]()

</div>

## 简介

将文本或 PDF 文档自动转化为**交互式知识图谱网页**。支持三种可视化模式：**概念图**、**思维导图**、**时间线/流程图**。

底层由 **DeepSeek V4** 和 **MiMo v2.5** 双 AI 模型驱动，自动提取关键概念及其关系，生成可在浏览器中拖拽、缩放、探索的交互式 HTML。

## 功能

- 📄 **多格式输入** — 支持 .txt / .md / .pdf 文件，支持拖放
- 🧠 **AI 提取** — DeepSeek + MiMo 双模型，中文优化
- 🗺️ **三模式可视化** — 力导向图 / 放射图 / 分层图 / 时间线
- 📝 **文章生成** — 自动将概念重组为叙事文章
- 📊 **JSON 输出** — 结构化知识图谱数据，可二次处理
- 🎨 **暗色主题** — 完整深色 UI，自定义窗口框架

## 快速开始

### 下载

1. 从 [Releases](https://github.com/shizelengleng/multimodal-viz/releases) 下载最新 `multimodal-viz-vX.X.X.zip`
2. 解压到任意文件夹
3. 双击 `multimodal-viz.exe`

### 配置 API Key

| 提供商 | 注册地址 | 模型 |
|--------|----------|------|
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com) → API Keys | deepseek-chat |
| MiMo | [platform.xiaomimimo.com](https://platform.xiaomimimo.com) → API Keys | mimo-v2.5 |

至少配置一个即可使用。打开程序 → ⚙ API 设置 → 输入 Key → 保存。

### 使用

1. 将 .txt / .md / .pdf 文件拖入程序
2. 选择输出目录
3. 点击「开始生成」
4. 在浏览器中打开生成的 .html 文件

## 从源码运行

```bash
git clone https://github.com/shizelengleng/multimodal-viz.git
cd multimodal-viz
pip install -r requirements.txt
python main.py
```

## 项目结构

```
multimodal-viz/
├── main.py                    # 启动入口 + SplashScreen
├── app/
│   ├── main_window.py         # 主窗口 + 导航 + 处理管道
│   └── services.py            # 文件处理逻辑
├── gui/
│   ├── theme.py               # 设计令牌
│   ├── sidebar.py             # 折叠侧边栏
│   ├── toast.py               # Toast 通知
│   ├── widgets.py             # DropZone + FileList
│   └── pages/                 # 4 个页面
├── core/
│   ├── extractor.py           # AI 提取引擎 + JSON 修复
│   ├── knowledge_graph.py     # 数据模型
│   ├── pdf_reader.py          # PDF 解析
│   ├── html_renderer.py       # vis-network HTML 生成
│   ├── cli.py                 # 命令行接口
│   └── assets/
├── docs/memory-bank/          # 设计文档
└── requirements.txt
```

## 技术栈

| 层 | 技术 |
|----|------|
| UI | CustomTkinter 5.2 + tkinterdnd2 |
| AI | DeepSeek API / MiMo API (OpenAI 兼容协议) |
| PDF | PyMuPDF |
| 图谱 | vis-network.js |
| 数据模型 | Pydantic v2 |
| 打包 | PyInstaller |

## License

MIT
```

- [ ] **Step 2: Delete outdated README.txt**

```bash
rm "C:/Users/123/Desktop/project/multimodal-viz/README.txt"
```

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add README.md && git rm README.txt && git commit -m "docs: add README.md for v0.5.3"
```

---

### Task 3: CHANGELOG.md — Version history

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/CHANGELOG.md`

- [ ] **Step 1: Write CHANGELOG.md**

```markdown
# Changelog

## v0.5.3 (2026-05-27)

**修复：** MiMo JSON 解析容错

- 栈式括号闭合算法 — 修复嵌套结构的 JSON 补齐顺序
- 无效关系自动过滤 — 截断 JSON 中孤立 relations 不再抛异常，改为自动丢弃
- max_tokens 增大至 8192 减少截断概率

## v0.5.2 (2026-05-26)

**新增：** SplashScreen + MiMo API + 处理进度改进

- 启动 SplashScreen — 深色 360×200 加载窗口 + 进度条
- MiMo API 支持 — Xiaomi MiMo v2.5 模型 (api.xiaomimimo.com/v1)
- 移除 Anthropic Claude 接口
- 处理进度条改为 indeterminate — 阶段式状态：📖 读取 → 🤖 AI提取 → 📄 生成网页 → ✓ 完成
- 修复自定义窗口框架回归 — 双 root 窗口、任务栏图标 (WS_EX_APPWINDOW)、侧边栏排序
- API 状态检测修复 — load_dotenv(override=True)

## v0.5.1 (2026-05-25)

**修复：** 网络 + 滚动

- PyInstaller 打包加入 certifi CA 证书 + httpx/httpcore/h11/anyio 解决其他电脑网络错误
- 结果页增加 CTkScrollableFrame 滚动支持

## v0.5.0 (2026-05-24)

**重构：** ttkbootstrap → CustomTkinter

- 全界面迁移至 CustomTkinter 5.2 — 原生圆角组件
- 自定义窗口框架 — overrideredirect + 深色标题栏
- 折叠侧边栏 — ☰ 汉堡菜单 280↔72px
- 模块化页面结构 — input / output / results / settings
- 可视化模式选择 — concept-map / mind-map / flowchart / timeline / auto

## v0.2 (2026-05)

**初始版本：** 基础功能

- 文本/PDF 输入 → DeepSeek API 提取 → vis-network HTML 输出
- JSON + 文章两种输出格式
- ttkbootstrap 界面
- 命令行接口
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add CHANGELOG.md && git commit -m "docs: add CHANGELOG.md with milestone history"
```

---

### Task 4: Memory-Bank docs — 5 core documents

**Files:**
- Create: `docs/memory-bank/01-product-design.md`
- Create: `docs/memory-bank/02-architecture.md`
- Create: `docs/memory-bank/03-implementation-plan.md`
- Create: `docs/memory-bank/04-progress.md`
- Create: `docs/memory-bank/05-conventions.md`

- [ ] **Step 1: Write 01-product-design.md**

```markdown
# 01 — 产品设计文档 (Product Design)

## 产品定位

**多模态知识图谱可视化生成器** — 将文本/PDF 文档自动转化为交互式知识图谱网页的桌面工具。

## 目标用户

- 学生：快速梳理论文/教材的知识结构
- 教师：将课程内容可视化，辅助教学
- 研究者：文献综述、概念关系分析
- 内容创作者：将长文转化为结构化图谱

## 核心功能

| 功能 | 描述 | v0.5.3 状态 |
|------|------|-------------|
| 文本输入 | .txt / .md 文件，拖放或浏览添加 | ✓ |
| PDF 输入 | 文字型 PDF 文本提取 (PyMuPDF) | ✓ |
| AI 概念提取 | DeepSeek + MiMo 双模型，中文优化 | ✓ |
| 关系提取 | 7 种关系类型 (influences, part_of, example_of 等) | ✓ |
| 多布局 | force_directed / radial / hierarchical / timeline | ✓ |
| 交互 HTML | vis-network.js 可视化网页 | ✓ |
| 文章生成 | 概念重组的叙事文章 (.md) | ✓ |
| JSON 输出 | 结构化知识图谱数据 | ✓ |
| 暗色主题 | 完整深色 UI | ✓ |
| 拖放 | 文件拖放到程序 | ✓ |

## 用户流程

```
启动 → SplashScreen → 主窗口
                          ├─ 📥 输入页：拖放/浏览文件
                          ├─ 📤 输出页：选择目录 + 模式 + 开始
                          ├─ ✅ 结果页：查看处理结果
                          └─ ⚙ 设置页：配置 API Key
```

## 平台约束

- Windows 10/11 桌面应用
- 需要网络连接（调用 AI API）
- 需要至少一个 API Key（DeepSeek 或 MiMo）
```

- [ ] **Step 2: Write 02-architecture.md**

```markdown
# 02 — 架构文档 (Architecture)

## 分层结构

```
┌─────────────────────────────────────┐
│  main.py — 入口 + SplashScreen      │
├─────────────────────────────────────┤
│  app/ — 应用层                       │
│  ├── main_window.py  # 窗口 + 导航   │
│  └── services.py     # 处理管道      │
├─────────────────────────────────────┤
│  gui/ — 界面层                       │
│  ├── theme.py        # 设计令牌      │
│  ├── sidebar.py      # 折叠侧边栏    │
│  ├── toast.py        # 通知          │
│  ├── widgets.py      # 通用组件      │
│  └── pages/          # 4 个页面      │
├─────────────────────────────────────┤
│  core/ — 核心引擎                     │
│  ├── knowledge_graph.py  # 数据模型   │
│  ├── extractor.py        # AI 提取    │
│  ├── pdf_reader.py       # PDF 解析   │
│  ├── html_renderer.py    # HTML 生成  │
│  └── cli.py              # 命令行     │
└─────────────────────────────────────┘
```

## 数据流

```
文件 (.txt/.md/.pdf)
  │
  ▼
pdf_reader.py / 直接读取 ──→ 文本
  │
  ▼
extractor.py ──→ DeepSeek/MiMo API
  │
  ▼
raw JSON ──→ _parse_response()
  │            ├── code fence 去除
  │            ├── 直接解析尝试
  │            ├── 截断不完整部分
  │            ├── 栈式括号补齐
  │            ├── 去除尾随逗号
  │            └── 过滤孤立 relations
  ▼
KnowledgeGraph (Pydantic model)
  │
  ├──→ .json 文件 (原始数据)
  ├──→ .html 文件 (vis-network 交互图)
  └──→ .md 文章
```

## 关键设计决策

| 决策 | 原因 |
|------|------|
| OpenAI 兼容协议 | DeepSeek 和 MiMo 都兼容，共用 `_extract_via_openai_compatible()` |
| JSON 修复而非重试 | MiMo 经常截断 JSON，修复比重试更可靠 |
| overrideredirect 自定义窗口 | 实现暗色标题栏，统一设计语言 |
| WS_EX_APPWINDOW | 无原生标题栏的窗口不会自动出现在任务栏 |
| hierarchical → 物理启用的布局策略 | hierarchical 布局禁用物理 → 初始定位后启用自由物理 |
| CTkProgressBar indeterminate | API 调用时间不确定，滚动条比假百分比诚实 |

## 模块边界

| 模块 | 职责 | 依赖 |
|------|------|------|
| `core/knowledge_graph.py` | 数据结构定义 (Concept, Relation, KnowledgeGraph) | pydantic |
| `core/extractor.py` | AI 调用 + JSON 解析修复 | openai, knowledge_graph |
| `core/pdf_reader.py` | PDF → 文本 | fitz (PyMuPDF) |
| `core/html_renderer.py` | 知识图谱 → HTML | Jinja2 模板 (内嵌) |
| `app/services.py` | 文件处理编排 | pdf_reader, extractor, html_renderer |
| `app/main_window.py` | 窗口管理 + 导航 + 线程调度 | gui/*, services |
```

- [ ] **Step 3: Write 03-implementation-plan.md**

```markdown
# 03 — 实施计划 (Implementation Plan)

## v0.5.3 之后

### 已完成
- [x] 双 AI 提供商 (DeepSeek + MiMo)
- [x] SplashScreen 启动画面
- [x] 处理进度 indeterminate + stage-based 状态
- [x] JSON 修复 (栈式括号闭合 + 孤立关系过滤)
- [x] 自定义窗口框架 + 任务栏图标
- [x] 折叠侧边栏
- [x] PyInstaller 打包 (SSL/HTTP 依赖完整)

### 待规划

#### 优先级 1 — 体验改进
- [ ] 批量文件并行处理
- [ ] 处理进度 per-file 细化
- [ ] 拖放区域支持更多格式 (.docx, .epub)
- [ ] 生成后自动打开 HTML

#### 优先级 2 — 功能扩展
- [ ] 用户自定义提示词模板
- [ ] 图布局参数可调 (节点大小、颜色映射)
- [ ] 导出 PNG/SVG 静态图
- [ ] 多文件合并为一个知识图谱
- [ ] 本地模型支持 (Ollama)

#### 优先级 3 — 工程改进
- [ ] 自动化测试 (pytest)
- [ ] GitHub Actions CI 自动构建 EXE
- [ ] 自动更新检查
- [ ] 国际化 (英文界面)
```

- [ ] **Step 4: Write 04-progress.md**

```markdown
# 04 — 进度跟踪 (Progress)

**当前版本：** v0.5.3
**最后更新：** 2026-05-27

## 当前状态

✅ 稳定可用。DeepSeek 和 MiMo 双模型均可正常工作，JSON 解析容错完善。

## 已完成功能

- 文本 + PDF 输入
- DeepSeek + MiMo API 提取
- 4 种图布局模式
- 交互式 HTML + JSON + 文章三种输出
- 暗色 UI + 自定义窗口框架
- SplashScreen + 处理进度条
- PyInstaller 打包分发

## 已知问题

| 问题 | 影响 | 状态 |
|------|------|------|
| 扫描版 PDF 无文字 | 无法提取 | 设计限制，非 bug |
| 极长文档 (8000+ 字符) 截断 | 概念可能不完整 | extractor.py 已截断 text[:8000] |
| MiMo 偶尔返回截断 JSON | 丢失部分概念 | 已通过 JSON 修复缓解 |

## 下次会话起点

1. 读取 `04-progress.md` (本文件)
2. 读取 `03-implementation-plan.md` 选择下一个任务
3. 读取 `02-architecture.md` 了解模块边界
4. 读取 `05-conventions.md` 遵守编码规范
```

- [ ] **Step 5: Write 05-conventions.md**

```markdown
# 05 — 开发规范 (Conventions)

## 代码风格

- Python >= 3.11
- `from __future__ import annotations` 在每个文件首行
- 类型注解：所有函数参数和返回值
- 不写 docstring (代码自解释)
- 注释只用中文，只在非显而易见的逻辑处

## 命名约定

| 元素 | 风格 | 示例 |
|------|------|------|
| 文件名 | snake_case | `knowledge_graph.py` |
| 类名 | PascalCase | `KnowledgeGraph` |
| 函数/方法 | snake_case | `extract_knowledge_graph()` |
| 私有方法 | _leading_underscore | `_parse_response()` |
| 常量 | UPPER_SNAKE | `EXTRACTION_PROMPT` |
| Tkinter 变量 | _trailing_underscore | `self._processing` |

## UI 约定

- 所有 UI 用 CustomTkinter (ctk)，不用标准 tkinter
- 颜色从 `gui/theme.py` 的 `C` 字典取，不硬编码
- 字体用 `Microsoft YaHei`，大小从 `gui/theme.py` 的 `FONT_*` 常量取
- 间距从 `gui/theme.py` 的 `SPACING_*` 常量取

## 禁止使用

- ❌ `tkinter.ttk` 组件 — 全部用 ctk
- ❌ `pack()` 和 `grid()` 混用 — 统一用 `pack()`
- ❌ 硬编码颜色值 (`"#FF0000"`) — 用 theme 令牌
- ❌ `print()` 调试 — 用 logging 或去掉
- ❌ `except Exception: pass` — 至少记录日志
- ❌ 任何 Anthropic / Claude 相关代码

## Git 约定

- commit message: 英文，`type: description` 格式
  - `feat:` 新功能
  - `fix:` 修复
  - `docs:` 文档
  - `chore:` 工程配置
  - `refactor:` 重构
- 不提交 .env / dist/ / build/ / .spec.bak

## 安全规则

- API Key 只存 .env，硬编码等同于泄露
- 用户输入的文件路径用 pathlib.Path，不拼接字符串
- HTML 输出中的用户文本做基本转义 (vis-network 无 XSS 风险)
```

- [ ] **Step 6: Commit all memory-bank docs**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add docs/memory-bank/ && git commit -m "docs: add memory-bank documentation system"
```

---

### Task 5: GitHub issue template

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/.github/ISSUE_TEMPLATE/bug-report.md`

- [ ] **Step 1: Write bug-report.md**

```markdown
---
name: Bug 报告
about: 报告一个问题帮助改进项目
title: "[Bug] "
labels: bug
assignees: shizelengleng
---

## 描述

<!-- 清晰简洁地描述这个 bug -->

## 复现步骤

1. 
2. 
3. 

## 期望行为

<!-- 你期望发生什么 -->

## 实际行为

<!-- 实际发生了什么 -->

## 环境

- 操作系统: Windows 10 / 11
- 应用版本: v0.5.x
- API 提供商: DeepSeek / MiMo
- 文件类型: .txt / .md / .pdf

## 截图/日志

<!-- 如有，粘贴错误信息或截图 -->
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add .github/ && git commit -m "docs: add bug report issue template"
```

---

### Task 6: CLAUDE.md — Claude Code project instructions

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/.claude/CLAUDE.md`

- [ ] **Step 1: Create .claude directory**

```bash
mkdir -p "C:/Users/123/Desktop/project/multimodal-viz/.claude"
```

- [ ] **Step 2: Write CLAUDE.md**

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add .claude/ && git commit -m "chore: add Claude Code project instructions"
```

---

### Task 7: LICENSE — MIT

**Files:**
- Create: `C:/Users/123/Desktop/project/multimodal-viz/LICENSE`

- [ ] **Step 1: Write LICENSE**

```markdown
MIT License

Copyright (c) 2026 shizelengleng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add LICENSE && git commit -m "chore: add MIT license"
```

---

### Task 8: Clean requirements.txt — Remove Anthropic

**Files:**
- Modify: `C:/Users/123/Desktop/project/multimodal-viz/requirements.txt`

- [ ] **Step 1: Remove anthropic from requirements.txt**

Edit `requirements.txt` and remove the line `anthropic>=0.40.0`.

Final file:
```
click>=8.0.0
pydantic>=2.0.0
openai>=1.0.0
PyMuPDF>=1.23.0
python-dotenv>=1.0.0
customtkinter>=5.2.0
tkinterdnd2>=0.4.0
```

- [ ] **Step 2: Commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add requirements.txt && git commit -m "chore: remove anthropic dependency"
```

---

### Task 9: Stage and commit all project source files

**Files:** All source code under `C:/Users/123/Desktop/project/multimodal-viz/` (excluded by .gitignore: .env, dist/, build/, etc.)

- [ ] **Step 1: Review what will be committed**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git status
```

Verify: .env, dist/, build/, __pycache__ are NOT listed. Everything else IS listed.

- [ ] **Step 2: Stage and commit all source code**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git add -A && git commit -m "feat: multimodal knowledge graph visualizer v0.5.3"
```

- [ ] **Step 3: Verify commit**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git log --oneline
```

---

### Task 10: Push to GitHub

**Prerequisite:** GitHub repo `shizelengleng/multimodal-viz` must exist. If not, create it first.

- [ ] **Step 1: Create GitHub repo (if not exists)**

```bash
gh repo create multimodal-viz --public --description "多模态知识图谱可视化生成器 — 文本/PDF → AI 提取 → 交互式知识图谱 HTML" --source=. --remote=origin --push
```

If `gh` CLI is not authenticated, the user should:
1. Run `gh auth login`
2. Then re-run the above command

If user prefers manual creation:
1. Go to https://github.com/new
2. Name: `multimodal-viz`
3. Description: `多模态知识图谱可视化生成器 — 文本/PDF → AI 提取 → 交互式知识图谱 HTML`
4. Public, no README/license/gitignore (we already have them)
5. Then run: `git remote add origin https://github.com/shizelengleng/multimodal-viz.git && git push -u origin main`

- [ ] **Step 2: Verify remote and push**

```bash
cd "C:/Users/123/Desktop/project/multimodal-viz" && git remote -v && git push -u origin main
```

- [ ] **Step 3: Verify on GitHub**

Open `https://github.com/shizelengleng/multimodal-viz` in browser. Confirm README.md renders, all files are present, no .env or sensitive files visible.
```

