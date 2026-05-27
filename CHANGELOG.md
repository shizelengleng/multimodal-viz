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
