# LangGraph 生产级学习计划

> 基于 Boss 直聘 JD 和 2026 年 AI Agent 最佳实践

## Level 1 — 基础 (001/) ✅ 已完成
- StateGraph + 节点 + 边
- 条件边 (conditional edge)
- Tool calling (手动 JSON schema)

## Level 2 — Prebuilt Agent ← 当前步骤
- `create_react_agent` — 一行代码建立 ReAct 循环
- `@tool` 装饰器 — 自动生成 tool schema
- 对比手写图 vs Prebuilt 的区别

## Level 3 — Persistence / 记忆
- MemorySaver checkpointing
- 多轮对话上下文
- 断点续跑 (pause/resume)

## Level 4 — Human-in-the-loop
- 关键步骤等待人工确认
- interrupt / Command
- 审批流程

## Level 5 — Multi-Agent
- Supervisor + Worker 模式
- Agent 间消息传递
- 子图 (Subgraph)

## Level 6 — 生产级进阶
- MCP 协议集成
- Streaming 与事件
- 错误处理与重试
- 测试与评测
