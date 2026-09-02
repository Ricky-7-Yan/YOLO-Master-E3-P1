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

## 加强正式验证

- 从冻结源码 commit 执行三族正式加强运行，计时纳入真实检测 loss、backward、梯度裁剪、官方分组 SGD step 和逐 step JSONL 写入/flush。
- MoE 30 对中位 slowdown `2.113%`、95% CI `[-2.514%, 8.361%]`；MoT 48 对 `-0.050%`、`[-6.374%, 9.451%]`；Latent 30 对 `-5.741%`、`[-16.195%, 1.570%]`。
- 三族主中位数和 CI 上界均低于 10%，总状态为 `PASS / STRONG`；负值不作加速解释。
- 108 个正式 pair 的 loss、梯度、模型参数和 optimizer 状态等价；两个观察条件的事件数与全局连续序号均通过 hard-fail。
- writer 事件为 MoE 432、MoT 432、Latent 216，共 1,080 条；12 项正式证据 manifest 独立重算 0 mismatch。

## Trainer 集成交叉验证准备

- 新增独立的 `DetectionTrainer` 交叉验证层，不改动 108 对正式判据与结论。
- 第一次 MoT 预检在训练前因官方源码快照没有 `.git` 元数据而 hard-fail；没有使用文件夹名冒充 commit 校验。
- 修复为预注册并核对 Trainer、detect trainer、routing protocol 和三份模型 YAML 的 SHA-256；若运行目录未来带 `.git`，还会同时校验 commit/tree。
- 第二次 MoT 预检完成 2 对 AB/BA、4 次真实 epoch。每次 2 个 batch、2 次 optimizer update；输入、loss、模型、optimizer 和 EMA 轨迹均等价，产生 16 条连续事件，dashboard HTTP smoke 通过。
- 冻结三族正式交叉验证协议：每族 2 对 warmup + 6 对 measured；小样本数字只作描述，不替换正式开销结论。
- 第一次三族运行完成 MoE 与 MoT 后在 Latent `ModelEMA(deepcopy)` 启动阶段失败；单独新进程复现同样错误，排除跨族残留。
- 属性检查定位到三个 `LatentMixture` 共 9 个 constructor forward 遗留的非叶 `_last_routing_*` 张量。证据 harness 增加限定 setup guard：只清空这些不属于 `state_dict` 的瞬时快照，并把逐项清单纳入 off/on 等价性检查。
- 三族 v2 完成 48 次单 epoch Trainer 运行、208 条事件和 dashboard HTTP smoke，但每次只有 2 个 batch，6 对描述的波动范围达到 `-54%～+231%`，不足以稳定描述开销量级；该运行只留本地诊断。
- v3 在不改正式 108 对判据的前提下，把每次 Trainer 执行扩为连续 5 epoch、10 个 batch，按 5 个 epoch window 之和比较，降低过短计时窗造成的调度噪声。

## Trainer 集成交叉验证完成

- v3 完成三族各 2 对 warmup、6 对 measured，AB/BA=3/3，共 48 次真实 `DetectionTrainer` 执行；每次 5 epoch、10 batch、10 optimizer step。
- 18 个 measured pair 的初始/最终 model、optimizer、EMA、原始 collated batch、loss item 序列和步数均完全等价。
- measured writer 产生 MoE 360、MoT 240、Latent 180 条事件；含 warmup 的原始流共 1,040 条，序号连续，dashboard HTTP 返回 200 并识别三族。
- 发现 dashboard 默认最近窗口为 1,000 条；补充源事件总量、窗口上限与截断标记，避免将滑动窗口误读为事件丢失，并新增中间损坏行 hard-fail。
- 运行时无 `.git` 元数据，改用预注册的 6 个关键文件 SHA-256 验证官方冻结快照，全部匹配；36 项归档证据独立重算 0 mismatch。
- v3 描述性 epoch-window 中位数为 MoE `4.948%`、MoT `-33.209%`、Latent `13.629%`，逐对范围约 `-84%～+284%`。由于小数据 CPU 波动过大，结果不重新裁定 `<10%`，正式结论仍使用 108 对加强实验。
- 修正交叉验证图：事件数量柱改为中性 family 配色，不再错误复用时延阈值的通过/失败颜色。
