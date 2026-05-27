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
