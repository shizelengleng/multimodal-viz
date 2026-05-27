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
