from __future__ import annotations

import json

from e3_p1.dashboard import build_snapshot, load_jsonl, render_dashboard_html, smoke_test_server


def _event(family="mot"):
    return {
        "family": family,
        "module": {"name": "route"},
        "routing": {
            "expert_load": [0.6, 0.4],
            "entropy_normalized": 0.9,
            "load_gini": 0.1,
            "dominant_expert_share": 0.6,
            "mixing_weights": {"state": "observed"},
        },
        "aux_loss": {"state": "observed"},
        "runtime": {"batch_size": 1, "sample_indices": [0]},
    }


def test_jsonl_loader_ignores_partial_tail_and_dashboard_updates(tmp_path):
    source = tmp_path / "events.jsonl"
    source.write_text(json.dumps(_event()) + "\n{partial", encoding="utf-8")

    first = build_snapshot(load_jsonl(source))
    source.write_text(json.dumps(_event()) + "\n" + json.dumps(_event("moe")) + "\n", encoding="utf-8")
    second = build_snapshot(load_jsonl(source))

    assert first["event_count"] == 1
    assert second["event_count"] == 2
    assert sorted(second["families"]) == ["moe", "mot"]


def test_dashboard_html_and_real_http_smoke(tmp_path):
    source = tmp_path / "events.jsonl"
    source.write_text(json.dumps(_event()) + "\n", encoding="utf-8")

    html = render_dashboard_html(refresh_ms=250)
    smoke = smoke_test_server(source)

    assert "fetch('/api/snapshot'" in html
    assert "refresh 250 ms" in html
    assert smoke == {
        "status": "PASS",
        "health_status": 200,
        "html_contains_dashboard": True,
        "api_event_count": 1,
        "api_families": ["mot"],
    }
