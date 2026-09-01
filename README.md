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
run_p1_dashboard.cmd
```

`run_p1_benchmark.cmd` 默认创建新的 `repro-*` 证据目录，不覆盖正式结果，也不修改正式 `LATEST.txt`。`run_p1_dashboard.cmd` 默认读取相邻 P0 仓库的正式 `LATEST.txt`，在 `127.0.0.1:8765` 启动只读面板。

## 当前状态

代码、测试与两次失败证据已从混合仓库中独立出来。正式 split-repo 结果将在同一代码 commit 固定后重新运行并写入 `artifacts/p1/`，避免沿用路径归属不清的旧正式产物。

## 导航

- [`docs/REQUIREMENTS.md`](docs/REQUIREMENTS.md)：P1 完成口径和统计判据。
- [`docs/DESIGN.md`](docs/DESIGN.md)：实时 consumer 与 paired benchmark 设计。
- [`docs/WORK_LOG.md`](docs/WORK_LOG.md)：失败、修复与验证记录。
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md)：当前不能外推的结论。
- [`configs/p1.yaml`](configs/p1.yaml)：固定实验配置。
- [`src/e3_p1/`](src/e3_p1/)：P1 实现。
