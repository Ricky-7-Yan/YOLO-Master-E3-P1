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
- 在固定 P1 源码 commit 后重新执行正式运行，环境记录中的工具仓库状态仅包含尚未归档的运行目录。

## 独立仓库正式验证

- 面板从相邻 P0 仓库的正式 `LATEST.txt` 解析事件源，并记录源仓库、相对路径、SHA-256、事件数和 family。
- 真实 HTTP smoke 返回 200，API 读取 52 条事件并识别 MoE、MoT、Latent。
- 三族各执行 30 对测量，AB/BA 各 15 对，共 90 对；loss 等价、事件数和 hook 清理均通过。
- 三族预注册主统计量均低于 10% 阈值，正式状态为 PASS；同时保留 bootstrap 区间，避免用单点估计掩盖 CPU 抖动。
- 浏览器实测页面显示 52 条事件、3 个 family 和 13 个模块，并保存新仓库生成的截图。
