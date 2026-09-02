# P1 设计说明

## 仓库边界

`YOLO-Master-E3-P0` 是 producer/contract，负责模型路由到统一事件；本仓库是 P1 consumer/benchmark，负责实时展示和观察器开销验证。两者通过 JSONL schema 和 Python package 边界连接，正式证据分别归档。

## 实时面板

`P0 routing-all.jsonl → 每次请求重新读取 → family/module 聚合 → /api/snapshot → 浏览器定时刷新`

- 默认只绑定 `127.0.0.1`，不提供写操作。
- JSONL 最后一条不完整行会等待下一轮刷新，防止 writer/reader 并发导致页面崩溃。
- 默认窗口为最新 1,000 条；API 同时返回源有效事件总数、窗口上限和是否截断，避免把滑动窗口误认成事件丢失。
- 仅容忍正在写入的最后一条不完整行；更早位置的 JSON 损坏会 hard-fail，防止静默掩盖证据破损。
- 页面显示事件数、三族摘要、逐模块 entropy/Gini/dominant share 和最近事件。

## 成对开销实验

- 每族分别构造 hook-off 与 hook-on 模型，固定 seed 并递归哈希完整 `state_dict`。
- 固定两张 coco8 图片组成 batch=2。
- 5 对 warmup 排除在统计外；30 对正式测量按 AB/BA 交替。
- 计时覆盖 train-mode forward 与可微 surrogate backward，不含构造、注册、I/O、HTTP 和 optimizer step。
- 每对 loss 必须在 `rtol=atol=1e-6` 内一致；on 条件采集事件数必须等于发现模块数。
- 逐对 slowdown 中位数为主统计量，5000 次固定 seed bootstrap 提供 95% 区间。

## Hard-fail

模型状态不同、loss 不等、事件数错误、hook 未移除、HTTP smoke 失败或证据目录覆盖都会立即失败。部分 family 完成后失败的运行不进入正式 P1 结论。

## 加强路径

加强 benchmark 独立于原 surrogate benchmark，避免事后改变已完成实验的口径。它把两个 batch 的 4 张 coco8 val 图片和真实标签预加载后，比较三个并行、初态相同的训练轨迹：关闭采集、内存采集、采集并写 JSONL。计时覆盖真实检测损失、反传、梯度裁剪、官方分组 SGD 更新以及可选 writer；模型/optimizer 哈希、schema 校验与绘图仍在计时外完成。

六种条件排列解决三条件测试的位置偏差；事件 stream 在整个 family 内保留并强制验证全局连续序号。预检与正式状态通过 `formal_verdict_eligible` 分开，防止小样本诊断被误读为验收结果。完整预注册口径见 [`STRENGTHENED_PROTOCOL.md`](STRENGTHENED_PROTOCOL.md)。

## Trainer 集成交叉验证层

交叉验证不重新实现训练循环，而是通过官方 `DetectionTrainer` callbacks 装配观察器：`on_train_start` 注册、`on_train_batch_start` 注入样本上下文、事件产生时写 JSONL、`on_train_batch_end` flush、`teardown` 移除 hook。证据 harness 只覆写 checkpoint 保存方法，避免把权重序列化 I/O 混入观察器集成验证；dataloader、preprocess、检测 loss、backward、optimizer、EMA 和主训练回调顺序保持官方实现。

同一 pair 的 off/on 独立构造 Trainer，但强制比较原始 collated batch、初始与最终模型、optimizer、EMA、loss 和 step 数；合并的三族事件随后交给现有 dashboard 的真实 HTTP server smoke。完整冻结口径见 [`ENGINE_CROSSCHECK_PROTOCOL.md`](ENGINE_CROSSCHECK_PROTOCOL.md)。
