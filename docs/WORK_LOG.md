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

## 加强协议与预检

- 在正式运行前锁定三条件、真实检测损失、官方分组 optimizer、六排列、10,000 次 bootstrap 和 `<10%` 主判据。
- 第一次全步预检在 loss 初始化前失败：高层 YAML 构造保留了字典型 `model.args`，而真实 loss 需要训练器注入的属性配置。修复为调用官方 `get_cfg`，不修改上游 runtime。
- 第二次预检跑通真实 loss/反传/optimizer，并证明三条件参数轨迹等价；复核原始 JSONL 时发现 collector 在每个 step 后被清空，导致 `sequence` 重置。该预检保留为问题发现证据，不用于正式结论。
- collector 改为 family 全程保留事件，容量提升到 4096，并新增事件总数和 `0..N-1` 连续序号 hard-fail。
- 第三次 MoT 预检通过：两个观察条件均得到 48 条事件、序号 0 至 47 且无重复；状态标记为 `PREFLIGHT_COMPLETE`、`formal_verdict_eligible=false`。
- 正式模式若任一 family 主中位数不满足 `<10%`，会在写完 summary、failure、日志与 manifest 后非零退出，不更新 `LATEST.txt`。
