"""Extra integrity cases beyond the public vectors: duplicated rows, crashed graders, relabelled slices."""
import copy

import pytest

pytestmark = pytest.mark.student

ROWS = [{"item_id": f"E-{i:03d}", "seed": s, "pass_rate": True, "slices": ["money_movement"] if i == 0 else []}
        for i in range(4) for s in (1, 2)]
SPEC = {"eval_set_version": "v2", "metrics": [{"id": "pass_rate", "kind": "capability", "blocking": True,
                                               "threshold": {"min": 0.8}}]}


def rep(rows, metrics=None, failures=()):
    return {"manifest": {"eval_set_sha": "x", "items": 4, "seeds": [1, 2]}, "rows": rows,
            "metrics": metrics or {"pass_rate": 1.0}, "evaluator_failures": list(failures)}


def test_duplicate_rows_with_right_count_are_flagged():
    from lab9 import gate

    base = rep(copy.deepcopy(ROWS))
    rows = copy.deepcopy(ROWS)
    rows[-1] = copy.deepcopy(rows[0])          # same length, one (item, seed) twice, one missing
    assert gate.integrity_check(rep(rows), base, SPEC)


def test_evaluator_failures_and_none_values_are_flagged():
    from lab9 import gate

    base = rep(copy.deepcopy(ROWS))
    assert gate.integrity_check(rep(copy.deepcopy(ROWS), failures=["E-001@1:Grader:boom"]), base, SPEC)
    rows = copy.deepcopy(ROWS)
    rows[0]["pass_rate"] = None
    assert gate.integrity_check(rep(rows, {"pass_rate": 1.0}), base, SPEC)


def test_relabelled_slice_and_edited_metric_are_flagged():
    from lab9 import gate

    base = rep(copy.deepcopy(ROWS))
    rows = copy.deepcopy(ROWS)
    for r in rows:
        r["slices"] = []
    assert gate.integrity_check(rep(rows), base, SPEC)
    rows = copy.deepcopy(ROWS)
    rows[1]["pass_rate"] = False
    assert gate.integrity_check(rep(rows, {"pass_rate": 1.0}), base, SPEC)   # metric does not match rows


def test_dropping_a_slice_or_blocking_is_a_ratchet_violation():
    from lab9 import gate

    base = rep(copy.deepcopy(ROWS))
    old = dict(SPEC, slices=[{"name": "money_movement", "metric": "pass_rate", "min": 0.9, "blocking": True}])
    new = dict(SPEC, slices=[])
    assert gate.integrity_check(base, base, new, old)
    soft = dict(SPEC, slices=[{"name": "money_movement", "metric": "pass_rate", "min": 0.9, "blocking": False}])
    assert gate.integrity_check(base, base, soft, old)
    assert gate.integrity_check(base, base, old, old) == []
