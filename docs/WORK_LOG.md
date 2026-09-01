# P1 技术工作日志

## 实时 consumer

- 建立本地只读 HTTP 面板、健康检查和聚合 API。
- 增加 JSONL 不完整尾行容错与真实 HTTP smoke。

## 第一次失败：MoE 训练态无外层快照

- warmup 预期每步 6 个 MoE 事件，实际为 0，运行在正式计时前停止。
- 根因是错误假设训练态总会发布外层 snapshot。
- 修复为保留带明确来源标记的 nested-router fallback，从真实 weights/indices 构造观察快照。

## 第二次失败：Latent 字典型 extra state

- MoE/MoT 局部测量后，Latent model state hash 遇到字典 value。
- 局部数字只作为诊断，不进入正式结论。
- 状态指纹改为递归覆盖 tensor、dict、list、tuple 和 scalar。

## 仓库拆分

- P1 代码、测试、配置和失败证据迁入独立仓库。
- P0 通过相邻仓库路径提供统一事件合同，P1 不复制 P0 正式证据。
- split-repo 正式结果必须从固定 P1 commit 重新生成。
