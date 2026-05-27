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
