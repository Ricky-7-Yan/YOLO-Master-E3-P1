# P1 设计说明

## 仓库边界

`YOLO-Master-E3-P0` 是 producer/contract，负责模型路由到统一事件；本仓库是 P1 consumer/benchmark，负责实时展示和观察器开销验证。两者通过 JSONL schema 和 Python package 边界连接，正式证据分别归档。

## 实时面板

`P0 routing-all.jsonl → 每次请求重新读取 → family/module 聚合 → /api/snapshot → 浏览器定时刷新`

- 默认只绑定 `127.0.0.1`，不提供写操作。
- JSONL 最后一条不完整行会等待下一轮刷新，防止 writer/reader 并发导致页面崩溃。
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
