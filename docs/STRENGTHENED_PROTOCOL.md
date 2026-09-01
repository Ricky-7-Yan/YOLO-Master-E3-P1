# P1 加强实验预注册协议

本协议在正式加强运行前固定，目的不是修改 P1 原判据，而是补足真实检测损失、optimizer、更多 MoT 重复和端到端写入层的证据。

## 1. 正式比较条件

每个 family 同时维护三份完全相同初始状态的模型与 optimizer：

1. `off`：不注册观察 hook。
2. `capture`：注册 P0 collector，事件只保存在内存。
3. `capture_jsonl`：注册相同 collector，每个 step 将新增事件 JSON 编码、写入并 flush；不执行 `fsync`。

三条件使用六种排列循环，确保每 6 对中每个条件在第一、第二、第三执行位置各出现两次。MoE/Latent 正式 30 对，MoT 加强至 48 对；warmup 为 6 对且不进入统计。

## 2. 计时区域

每个条件的单个 measured unit 包含固定两批 coco8 图像，每批 2 张，覆盖全部 4 张 val 图。每个 step 的计时区域包括：

`zero_grad → 真实 DetectionModel.loss → loss.sum → backward → clip_grad_norm_(10) → SGD optimizer.step → 可选 JSONL 编码/写入/flush`

模型构造、hook 注册/移除、状态哈希、事件 schema 校验、绘图、manifest、dashboard HTTP 不计时。图片和 YOLO 标签在计时前确定性加载，以免与 observer 无关的文件 I/O 稀释 slowdown；输入文件路径、图像哈希、标签哈希和解析后目标数全部落盘。

## 3. 透明性 hard-fail

- 三条件初始模型状态哈希必须一致，optimizer 初始状态哈希必须一致。
- 每个 pair 的每个 batch 都要比较总检测损失、box/cls/dfl 分量和裁剪前梯度范数。
- 每个 pair 完成后，三份模型状态哈希和 optimizer 状态哈希必须完全一致，证明观察器未改变参数轨迹或 momentum。
- `capture` 与 `capture_jsonl` 每个 step 的事件数必须等于发现的叶级 routed module 数；首个 measured step 通过 P0 JSON Schema。
- 执行结束后所有 hook 必须移除；证据目录不得覆盖；任一条件失败则整个 run 失败并保留 `failure.json`、日志和 manifest。

## 4. 统计与判读

对每个 pair 分别计算：

- `capture` 相对 `off` 的 slowdown；
- `capture_jsonl` 相对 `off` 的 slowdown；
- `capture_jsonl` 相对 `capture` 的 writer 增量。

运行前固定主统计量为逐对 slowdown 中位数，并用固定 seed、10,000 次 bootstrap 报告中位数 95% CI。

- **任务判据**：每个 family 的 `capture_jsonl vs off` 中位数 `<10%` 才 PASS。
- **加强证据等级**：若对应 95% CI 上界也 `<10%`，标记 `STRONG`；否则标记 `INCONCLUSIVE`，但不得看结果后修改任务判据。
- `capture vs off` 和 writer 增量用于定位，不替代主判据。

## 5. 结论边界

当前本机是 CPU-only PyTorch，无 NVIDIA CUDA。加强运行可证明真实检测 loss 与 optimizer 路径上的本机结果，但不能代替统一 GPU、AMP、真实训练增强、长 epoch 或不同硬件。GPU 数据必须来自真实设备并单独记录，不能推算。
