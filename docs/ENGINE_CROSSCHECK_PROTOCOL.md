# P1 DetectionTrainer 交叉验证协议

本协议在三族正式交叉验证运行前冻结。它只回答“P1 观察器能否无侵入地进入真实 Ultralytics 训练生命周期”，不替换 `STRENGTHENED_PROTOCOL.md` 已完成的 108 对正式 `<10%` 开销结论。

## 目的与边界

首轮和加强基准已经覆盖真实模型 forward、检测 loss、backward、官方分组 optimizer 与 JSONL writer，但为了隔离观察器开销，数据在计时前预加载。交叉验证进一步接入官方 `DetectionTrainer`，覆盖 coco8 train dataloader、batch preprocess、检测损失、反传、optimizer step、EMA、训练回调和面板 consumer。

每次执行为 CPU、batch=2、imgsz=64、连续 5 个 coco8 train epoch（共 10 个 batch）。关闭会随机改变输入的几何、颜色和翻转增强，使同一 pair 的原始 collated batch 可逐字节比较。关闭 validation、plot 和 checkpoint 序列化；这些不是 P1 路由观察链路，且会把不相关 I/O 混入交叉验证。

## 条件与顺序

- `off`：不注册 collector，不写事件。
- `capture_jsonl`：在 `on_train_start` 注册 P0 collector，每个 batch 设置上下文，事件产生时立即 JSON 编码和写入，并在 `on_train_batch_end` flush。
- 每族 2 对 warmup，不进入结果；6 对 measured，AB/BA 各 3 对。
- 每个 pair 两个条件使用同一 seed；不同 pair 改变 seed。

## 两个计时窗口

1. epoch window：累加 5 次 `on_train_epoch_start` 到 `on_train_epoch_end`。包含 dataloader 迭代、preprocess、forward、检测 loss、backward、optimizer step，以及观察条件中的 JSON 编码、write、每 batch flush。连续 10 个 batch 用于降低单个 2-batch epoch 的 CPU 调度噪声。
2. full lifecycle：Trainer 构造开始到训练完成。它包含模型和数据集准备，只作诊断，不用于 P1 正式判据。

## 等价性 hard-fail

每一对均必须满足：

1. 初始模型和 optimizer 状态哈希完全一致；
2. 两个 collated batch 的图像、标签、框、batch index 和文件路径哈希完全一致；
3. epoch 结束后的模型、optimizer momentum 和 EMA 状态哈希完全一致；
4. loss items 在 `rtol=atol=1e-6` 内一致，batch 数与 optimizer step 数一致；
5. 观察条件事件数等于“发现模块数 × batch 数”，且 `sequence` 从 0 连续；
6. 合并后的三族 Trainer 事件流能被真实 dashboard HTTP 主页、健康检查和 API 消费。

任一项不满足，运行写出 `failure.json` 和 manifest 后非零退出，不更新 `LATEST.txt`。

## 结果解释

6 对/族只用于描述真实 Trainer 集成后的量级和发现异常，不计算新的置信区间，也不产生新的正式 `<10%` 结论。正式结论仍以 `p1s-20260901-cpu-fullstep-v1` 的 108 个 preregistered pair 为准，避免用更小样本事后替换既有判据。

运行时若存在 `.git`，同时核对官方 commit/tree 和关键文件哈希；当前官方源码为无 `.git` 的冻结快照，因此强制核对 Trainer、detect trainer、routing protocol 和三份模型 YAML 的预注册 SHA-256。

## 已知 Latent 启动缺陷与限定处理

冻结源码的 Latent 模型在构造时为 stride 推断执行 forward，三个 `LatentMixture` 各保留 `_last_routing_logits`、`_last_routing_probs`、`_last_routing_summary` 非叶张量。官方 `_setup_train` 随后的 `ModelEMA(deepcopy(model))` 因而无法启动；该问题在全新 Python 进程中也可复现，不是 P1 hook 或跨族污染。

证据 Trainer 只在 `get_model` 返回后清空这 9 个临时快照字段，并逐项记录 module、字段、shape 以及它是否属于 `state_dict`。限定条件是：仅清理上述三种字段、仅清理非叶 tensor、不得改动参数或 buffer；同一 pair 的 off/on 清理清单必须完全一致。正式训练的首个 forward 会重新发布当前快照。
