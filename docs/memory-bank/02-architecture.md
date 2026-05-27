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
