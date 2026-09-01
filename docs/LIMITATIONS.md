# 限制与后续复核项

1. 加强 benchmark 已包含真实标签检测 loss、backward、梯度裁剪、官方分组 optimizer step 和逐 step JSONL 写入/flush，但仍不是完整 detector epoch。
2. 图片与标签在计时前预加载，目的是避免无关磁盘读取稀释 observer slowdown；dataloader、数据增强和 dashboard HTTP 不在主计时内。
3. CPU 调度、缓存与频率会产生明显噪声，负 slowdown 不能解释为 hook 加速。
4. 随机初始化模型只验证观测合同，不证明训练后路由质量或检测精度。
5. 本地面板无鉴权、远程多用户和数据库，不作为生产服务。
6. 当前 PyTorch 为 CPU build，没有 NVIDIA CUDA、AMP、显存或多卡证据；这些只能在真实 GPU 上单独复测，不能推算。
7. MoT 加强结果的 95% CI 上界为 9.451%，仍低于但接近 10% 阈值；本机正式结论成立，不代表所有硬件和负载都留有相同余量。
8. 后续最有价值的是统一 GPU 上的完整 epoch/多轮交叉验证，以及在训练后权重上复核路由质量；不应为了补数字而虚构 GPU 结果。
