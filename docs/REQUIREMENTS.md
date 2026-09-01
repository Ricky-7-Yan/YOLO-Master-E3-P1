# E3 P1 完成口径

P1 只有在以下条件全部成立时标记为完成：

1. 提供 TensorBoard/W&B 或可实时刷新的面板，本仓库选择本地只读 Web 面板。
2. 面板消费 P0 `e3.routing/v1.0.0` JSONL，不依赖三族内部类。
3. 覆盖 MoE、MoT、Latent 至少三个真实 routing family。
4. 主页、`/healthz`、`/api/snapshot` 真实 HTTP smoke 通过。
5. hook off/on 模型初始状态一致，固定输入和 pair seed，预热不计时，AB/BA 顺序均衡。
6. 每对 loss 数值等价，事件数与模块数一致，hook 执行后全部清理。
7. 主统计量在运行前固定为逐对 slowdown 中位数；每族中位数 `<10%` 判 PASS，同时报告 bootstrap 95% 区间。
8. 保留原始 pair、配置、输入、环境、完整日志、图、摘要和 SHA-256 manifest。

P1 的前置 P0 仓库只提供统一事件合同和固定事件源；P1 不复制或重新计入 P0 多样本、重复与 batch 结果。

## 加强验证的附加要求

加强运行不降低上述完成口径，并额外要求：

1. 使用真实 coco8 图像与 YOLO 标签，通过 `DetectionModel.loss` 执行 backward 和官方分组 optimizer step。
2. 分离 `off`、`capture`、`capture_jsonl` 三个条件，六排列均衡执行顺序，并把逐 step JSONL 编码、写入与 flush 纳入主条件计时。
3. 三条件不仅 loss/梯度等价，而且每个 pair 后模型参数和 optimizer momentum 轨迹的递归哈希完全一致。
4. 事件总数必须精确匹配，`sequence` 必须从 0 全局连续；正式判据失败时进程非零退出且保留证据。
5. 预检只验证机制和暴露问题，必须标记为不可用于正式结论；正式三族运行仍按每族主中位数 `<10%` 判定。
