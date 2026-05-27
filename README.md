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
