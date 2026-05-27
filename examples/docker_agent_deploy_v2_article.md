# Docker容器本地部署AI Agent完全指南

本文档由知识图谱自动生成，用于 web-video-presentation 导览生成。

## 知识图谱概览

本知识图谱包含 14 个核心概念和 15 条概念关系，推荐使用 层级图 布局展示。

## 核心概念

### Docker Model Runner

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: Docker推出的本地运行LLM模型的工具，兼容OpenAI API，支持拉取和运行多种AI模型。

### Docker MCP Gateway

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: 通过Model Context Protocol连接外部工具和服务的网关，使AI Agent能够调用搜索、文件系统等工具。

### Docker cagent

- **类别**: 实际应用
- **难度**: 基础
- **说明**: 声明式YAML多Agent运行时，无需手写代码即可定义和运行AI Agent。

### Docker Offload

- **类别**: 实际应用
- **难度**: 高级
- **说明**: 提供GPU加速云端环境，用于增强本地AI Agent的计算能力。

### Docker Compose

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: 定义和运行多容器AI应用的统一编排工具，用于集成模型、工具网关和Web界面。

### 本地模型

- **类别**: 概念定义
- **难度**: 基础
- **说明**: 在本地Docker环境中运行的AI模型，如ai/smollm2、ai/gemma3、ai/llama3.2等，各有不同的硬件需求。

### MCP协议

- **类别**: 原理规律
- **难度**: 进阶
- **说明**: Model Context Protocol，用于连接AI Agent与外部工具的通信协议，支持duckduckgo、filesystem等工具。

### YAML声明式Agent

- **类别**: 例子案例
- **难度**: 基础
- **说明**: 通过YAML文件定义Agent的角色、模型、指令和工具集，无需编写代码即可创建多Agent系统。

### 多Agent协作

- **类别**: 原理规律
- **难度**: 高级
- **说明**: 多个AI Agent（如审查者、批评者、修订者）协同工作，完成复杂任务。

### 硬件要求

- **类别**: 其他
- **难度**: 基础
- **说明**: 运行不同AI模型所需的显存和存储空间，从轻量模型（1GB显存）到高端模型（16GB以上显存）。

### 安全沙盒

- **类别**: 原理规律
- **难度**: 进阶
- **说明**: Agent生成的代码在隔离容器中运行，可禁用网络以防止数据泄露的安全机制。

### 混合AI模式

- **类别**: 实际应用
- **难度**: 高级
- **说明**: 本地小模型处理常规任务，远程大模型处理复杂推理，可降低5至30倍成本的部署策略。

### Goose框架

- **类别**: 实际应用
- **难度**: 进阶
- **说明**: 开源AI助手框架，结合Docker Model Runner和MCP Gateway，快速构建带浏览器界面的私有AI助手。

### 学习路径

- **类别**: 流程步骤
- **难度**: 基础
- **说明**: 从安装Docker Desktop、拉取轻量模型、使用cagent体验零代码Agent，到学习完整多Agent架构的推荐步骤。


## 概念关系

- **Docker Model Runner** 运行本地模型 **本地模型**
- **Docker Model Runner** 工具链组成部分 **Docker MCP Gateway**
- **Docker cagent** 使用YAML声明式定义 **YAML声明式Agent**
- **Docker cagent** 支持多Agent协作 **多Agent协作**
- **Docker MCP Gateway** 基于MCP协议 **MCP协议**
- **Docker Compose** 编排模型服务 **Docker Model Runner**
- **Docker Compose** 编排工具网关 **Docker MCP Gateway**
- **本地模型** 依赖硬件要求 **硬件要求**
- **安全沙盒** 保障多Agent安全 **多Agent协作**
- **混合AI模式** 结合本地和远程模型 **Docker Model Runner**
- **Goose框架** 集成Model Runner **Docker Model Runner**
- **Goose框架** 集成MCP Gateway **Docker MCP Gateway**
- **学习路径** 先启用Model Runner **Docker Model Runner**
- **学习路径** 体验cagent **Docker cagent**
- **学习路径** 学习Compose架构 **Docker Compose**
