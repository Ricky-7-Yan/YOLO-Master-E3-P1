"""Evidence plots for the P1 paired training-path benchmark."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def save_benchmark_plot(families: dict[str, dict[str, Any]], path: Path, target_percent: float) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = list(families)
    figure, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), constrained_layout=True)
    x = np.arange(len(names))
    off = [families[name]["off_ms"]["median"] for name in names]
    on = [families[name]["on_ms"]["median"] for name in names]
    width = 0.34
    axes[0].bar(x - width / 2, off, width, label="Hook off", color="#61758A")
    axes[0].bar(x + width / 2, on, width, label="Hook on", color="#2F6FAE")
    axes[0].set_xticks(x, [name.upper() for name in names])
    axes[0].set_ylabel("Median train-path forward+backward (ms)")
    axes[0].set_title("Paired observer timing")
    axes[0].grid(axis="y", color="#D8DEE6")
    axes[0].legend()

    slowdowns = [families[name]["paired_slowdown_percent"]["median"] for name in names]
    lower = [families[name]["paired_slowdown_percent"]["bootstrap_95_ci"][0] for name in names]
    upper = [families[name]["paired_slowdown_percent"]["bootstrap_95_ci"][1] for name in names]
    errors = np.asarray([[value - low for value, low in zip(slowdowns, lower)], [high - value for value, high in zip(slowdowns, upper)]])
    colors = ["#50A47B" if value < target_percent else "#C83E4D" for value in slowdowns]
    axes[1].bar(x, slowdowns, yerr=errors, capsize=5, color=colors)
    axes[1].axhline(target_percent, color="#C83E4D", linestyle="--", label=f"Target < {target_percent:g}%")
    axes[1].axhline(0.0, color="#61758A", linewidth=0.9)
    axes[1].set_xticks(x, [name.upper() for name in names])
    axes[1].set_ylabel("Paired slowdown (%)")
    axes[1].set_title("Median and bootstrap 95% CI")
    axes[1].grid(axis="y", color="#D8DEE6")
    axes[1].legend()
    figure.suptitle("E3 P1 observer-overhead benchmark · real train-mode forward+backward")
    figure.savefig(path, dpi=180)
    plt.close(figure)
