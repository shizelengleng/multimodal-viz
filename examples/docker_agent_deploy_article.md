# Docker容器本地部署AI Agent完全指南

本文档由知识图谱自动生成，用于 web-video-presentation 导览生成。

## 知识图谱概览

本知识图谱包含 14 个核心概念和 15 条概念关系，推荐使用 层级图 布局展示。

## 核心概念

### Docker Model Runner

- **类别**: 实际应用
- **难度**: 基础
- **说明**: Docker推出的本地运行LLM模型的工具，兼容OpenAI API，支持多种模型拉取和调用。

### Docker MCP Gateway

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: 通过Model Context Protocol连接外部工具和服务的网关组件，实现Agent与工具交互。

### Docker cagent

- **类别**: 实际应用
- **难度**: 基础
- **说明**: 声明式YAML多Agent运行时，无需手写代码即可定义和运行AI Agent。

### Docker Offload

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: 提供GPU加速云端环境的工具，用于提升模型推理性能。

### Docker Compose

- **类别**: 实际应用
- **难度**: 基础
- **说明**: 定义和运行多容器AI应用的统一编排工具，支持一键启动完整Agent架构。

### 零代码Agent方案

- **类别**: 例子案例
- **难度**: 基础
- **说明**: 使用Docker cagent通过YAML声明式定义Agent，无需编写代码即可创建多角色Agent。

### 自定义Agent方案

- **类别**: 例子案例
- **难度**: 进阶
- **说明**: 适合Python开发者，通过Docker Model Runner和HTTP请求编写自定义Agent逻辑。

### 多服务Agent架构

- **类别**: 例子案例
- **难度**: 高级
- **说明**: 使用Docker Compose集成模型、工具网关和Web UI的完整Agent应用方案。

### Goose简易Agent

- **类别**: 例子案例
- **难度**: 进阶
- **说明**: 基于Goose开源框架和Docker工具链的简易AI助手方案，提供浏览器界面。

### MCP协议

- **类别**: 原理规律
- **难度**: 进阶
- **说明**: Model Context Protocol，用于连接Agent与外部工具和服务的通信协议。

### 安全沙盒

- **类别**: 原理规律
- **难度**: 高级
- **说明**: Agent生成代码在隔离容器中运行的安全机制，可禁用网络防止数据泄露。

### 混合AI模式

- **类别**: 原理规律
- **难度**: 高级
- **说明**: 本地小模型处理常规任务，远程大模型处理复杂推理，可降低5至30倍成本。

### 硬件要求

- **类别**: 概念定义
- **难度**: 基础
- **说明**: 不同模型对显存和存储的需求，从1GB到16GB以上显存不等。

### 推荐学习路径

- **类别**: 流程步骤
- **难度**: 基础
- **说明**: 从安装Docker Desktop到自定义YAML配置的逐步学习路线。


## 概念关系

- **Docker Model Runner** 构成自定义Agent方案 **自定义Agent方案**
- **Docker MCP Gateway** 基于MCP协议 **MCP协议**
- **Docker cagent** 实现零代码Agent方案 **零代码Agent方案**
- **Docker Compose** 实现多服务Agent架构 **多服务Agent架构**
- **Goose简易Agent** 使用Docker Model Runner **Docker Model Runner**
- **Goose简易Agent** 使用Docker MCP Gateway **Docker MCP Gateway**
- **MCP协议** 作为网关协议 **Docker MCP Gateway**
- **安全沙盒** 应用于多服务架构 **多服务Agent架构**
- **混合AI模式** 优化模型运行 **Docker Model Runner**
- **硬件要求** 决定模型选择 **Docker Model Runner**
- **推荐学习路径** 从安装开始 **Docker Model Runner**
- **推荐学习路径** 进阶使用cagent **Docker cagent**
- **推荐学习路径** 学习Compose架构 **Docker Compose**
- **零代码Agent方案** 零代码与多服务对比 **多服务Agent架构**
- **自定义Agent方案** 自定义与零代码对比 **零代码Agent方案**
