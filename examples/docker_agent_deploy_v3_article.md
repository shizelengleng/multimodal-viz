# Docker容器本地部署AI Agent完整指南

本文档由知识图谱自动生成，用于 web-video-presentation 导览生成。

## 知识图谱概览

本知识图谱包含 14 个核心概念和 15 条概念关系，推荐使用 层级图 布局展示。

## 核心概念

### Docker Model Runner

- **类别**: 概念定义
- **难度**: 基础
- **说明**: Docker推出的本地运行LLM模型的工具，兼容OpenAI API，支持多种模型如ai/smollm2、ai/gemma3等

### Docker MCP Gateway

- **类别**: 概念定义
- **难度**: 进阶
- **说明**: 通过Model Context Protocol连接外部工具和服务的网关组件，支持duckduckgo、filesystem等工具

### Docker cagent

- **类别**: 概念定义
- **难度**: 基础
- **说明**: 声明式YAML多Agent运行时，无需手写代码，支持定义多个Agent角色和工具集

### Docker Offload

- **类别**: 概念定义
- **难度**: 进阶
- **说明**: 提供GPU加速云端环境的工具，用于提升AI Agent运行性能

### Docker Compose

- **类别**: 概念定义
- **难度**: 基础
- **说明**: 定义和运行多容器AI应用的统一编排工具，支持集成模型、工具网关和Web UI

### 方案一：自定义Agent

- **类别**: 例子案例
- **难度**: 进阶
- **说明**: 适合Python开发者，使用Docker Model Runner加自定义代码编写Agent逻辑

### 方案二：零代码cagent

- **类别**: 例子案例
- **难度**: 基础
- **说明**: 推荐方案，通过YAML声明式定义多Agent，无需编写代码即可运行

### 方案三：Compose多服务

- **类别**: 例子案例
- **难度**: 进阶
- **说明**: 适合完整Agent应用，通过Docker Compose集成模型、工具网关和Web界面

### 方案四：Goose简易方案

- **类别**: 例子案例
- **难度**: 基础
- **说明**: 使用Goose开源框架加Docker快速构建带浏览器界面的AI助手

### 硬件要求

- **类别**: 原理规律
- **难度**: 基础
- **说明**: 不同模型对显存和存储的需求，从ai/smollm2的1GB显存到ai/qwen3-30b的16GB以上显存

### MCP协议

- **类别**: 原理规律
- **难度**: 进阶
- **说明**: Model Context Protocol，通过--servers参数启用duckduckgo、context7、filesystem等工具

### 安全沙盒

- **类别**: 原理规律
- **难度**: 高级
- **说明**: Agent生成的代码应在隔离容器中运行，可禁用网络防止数据泄露

### 混合AI模式

- **类别**: 原理规律
- **难度**: 高级
- **说明**: 本地小模型处理常规任务，远程大模型处理复杂推理，可降低5至30倍成本

### 推荐学习路径

- **类别**: 流程步骤
- **难度**: 基础
- **说明**: 从安装Docker Desktop开始，逐步体验模型运行、零代码Agent、多Agent架构和自定义配置


## 概念关系

- **Docker Model Runner** 构成方案一的核心 **方案一：自定义Agent**
- **Docker cagent** 构成方案二的核心 **方案二：零代码cagent**
- **Docker Compose** 构成方案三的核心 **方案三：Compose多服务**
- **Docker MCP Gateway** 用于方案三的工具网关 **方案三：Compose多服务**
- **Docker Model Runner** 依赖硬件资源 **硬件要求**
- **Docker MCP Gateway** 基于MCP协议 **MCP协议**
- **安全沙盒** 安全策略与混合模式相关 **混合AI模式**
- **推荐学习路径** 学习路径第一步 **Docker Model Runner**
- **推荐学习路径** 学习路径后续步骤 **方案二：零代码cagent**
- **推荐学习路径** 学习路径进阶步骤 **方案三：Compose多服务**
- **方案一：自定义Agent** 编码方案对比零代码方案 **方案二：零代码cagent**
- **方案二：零代码cagent** 单Agent对比多服务架构 **方案三：Compose多服务**
- **方案四：Goose简易方案** 简易方案对比自定义方案 **方案一：自定义Agent**
- **Docker Model Runner** 可配合GPU加速 **Docker Offload**
- **Docker cagent** 通过MCP协议引用工具 **Docker MCP Gateway**
