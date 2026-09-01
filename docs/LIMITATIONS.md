# 限制与加强项

1. 当前 benchmark 是 CPU、batch=2、imgsz=64 的 train-mode forward + surrogate backward，不是完整 detector epoch。
2. 不包含真实标签 loss、optimizer、dataloader、JSONL 写入和 dashboard HTTP。
3. CPU 调度、缓存与频率会产生明显噪声，负 slowdown 不能解释为 hook 加速。
4. 随机初始化模型只验证观测合同，不证明训练后路由质量或检测精度。
5. 本地面板无鉴权、远程多用户和数据库，不作为生产服务。
6. 需要在统一 NVIDIA GPU 或更稳定环境补充完整 train step/epoch，才能形成更强性能结论。
7. MoT 中位数为 5.087%，但 95% bootstrap 区间上界为 9.510%，接近 10% 判据；当前 PASS 仅按预注册的中位数规则成立，不代表已在所有硬件和负载下留出充分余量。
