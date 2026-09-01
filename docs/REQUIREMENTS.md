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
