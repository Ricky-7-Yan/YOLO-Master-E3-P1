# YOLO-Master E3 P1：实时路由面板与开销验证

本仓库只承载 E3 P1：消费 P0 的统一 routing JSONL，提供本地实时面板，并对 MoE、MoT、Latent 三族执行 hook off/on 成对训练路径开销实验。

P0 的 schema、collector、多样本与 batch 证据位于独立仓库：[YOLO-Master-E3-P0](https://github.com/Ricky-7-Yan/YOLO-Master-E3-P0)。P1 将它作为明确的前置合同，不重复提交 P0 正式产物。

## 目录约定

以下目录应位于同一父目录：

```text
YOLO-Master-E3-P0/
YOLO-Master-E3-P1/
YOLO-Master-main-07d3303/
YOLO-Master-baseline/
```

## 复现命令

```bat
run_tests.cmd
run_p1_benchmark.cmd
run_p1_strengthened.cmd
run_p1_dashboard.cmd
```

`run_p1_benchmark.cmd` 默认创建新的 `repro-*` 证据目录，不覆盖正式结果，也不修改正式 `LATEST.txt`。`run_p1_dashboard.cmd` 默认读取相邻 P0 仓库的正式 `LATEST.txt`，在 `127.0.0.1:8765` 启动只读面板。

`run_p1_strengthened.cmd` 是加强协议入口：以 coco8 真实标签执行 `DetectionModel.loss + backward + 官方分组 SGD step`，分层比较关闭观察器、仅内存采集、采集并逐 step 写入 JSONL 三种条件。正式结论与原 surrogate 基线分开归档，不混用数字。

## 当前状态

加强正式运行 `p1s-20260901-cpu-fullstep-v1` 已通过。它使用 4 张 coco8 val 图及真实标签，计时覆盖检测 loss、backward、梯度裁剪、官方分组 SGD step 和逐 step JSONL 写入/flush：

- MoE：30 对，中位 slowdown `2.113%`，95% CI `[-2.514%, 8.361%]`。
- MoT：48 对，中位 slowdown `-0.050%`，95% CI `[-6.374%, 9.451%]`。
- Latent：30 对，中位 slowdown `-5.741%`，95% CI `[-16.195%, 1.570%]`。
- 三族均满足中位数 `<10%`，且区间上界也 `<10%`，总体为 `PASS / STRONG`。
- 108 对 loss、梯度、模型和 optimizer 轨迹等价；三族 writer 共 1,080 条事件，序号连续；12 项正式文件 manifest 重算无误。

正式加强证据见 [`artifacts/p1-strengthened/p1s-20260901-cpu-fullstep-v1/`](artifacts/p1-strengthened/p1s-20260901-cpu-fullstep-v1/)。负 slowdown 只表示本次 CPU 噪声下未检出正向开销，不能解释为观察器加速。

### 首轮隔离微基准

独立仓库正式运行 `p1-20260901-cpu-split` 已通过：

- 面板 HTTP smoke：`PASS`，读取 P0 的 52 条事件，覆盖 3 个 family、13 个模块。
- MoE：30 对，AB/BA=15/15，中位成对 slowdown `-0.903%`，bootstrap 95% CI `[-7.987%, 8.097%]`。
- MoT：30 对，AB/BA=15/15，中位成对 slowdown `5.087%`，bootstrap 95% CI `[-5.648%, 9.510%]`。
- Latent：30 对，AB/BA=15/15，中位成对 slowdown `1.196%`，bootstrap 95% CI `[-5.536%, 5.670%]`。
- 90 对 loss 全部等价，所有 hook 均已清理；14 个正式文件已写入 SHA-256 manifest。

负 slowdown 仅表示本次 CPU 噪声下的观测值，不解释为 hook 带来加速。正式证据见 [`artifacts/p1/p1-20260901-cpu-split/`](artifacts/p1/p1-20260901-cpu-split/)。

## 导航

- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md)：P1 完成口径和统计判据。
- [`docs/DESIGN.md`](docs/DESIGN.md)：实时 consumer 与 paired benchmark 设计。
- [`docs/STRENGTHENED_PROTOCOL.md`](docs/STRENGTHENED_PROTOCOL.md)：正式加强运行前锁定的协议。
- [`docs/EXPERIMENT_REPORT.md`](docs/EXPERIMENT_REPORT.md)：正式实验结果与证据索引。
- [`docs/WORK_LOG.md`](docs/WORK_LOG.md)：失败、修复与验证记录。
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md)：当前不能外推的结论。
- [`configs/p1.yaml`](configs/p1.yaml)：固定实验配置。
- [`src/e3_p1/`](src/e3_p1/)：P1 实现。
