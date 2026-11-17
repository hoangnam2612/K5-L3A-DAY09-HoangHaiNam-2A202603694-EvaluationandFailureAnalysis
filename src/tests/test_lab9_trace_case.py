"""Regression test for docs/trace_case.md: C-002@11, first wrong step = model_override (FM-03).

Runs the real shapes on a temp store (cwd must be src/, like the other lab9 tests)."""
import pytest

pytestmark = pytest.mark.student


@pytest.fixture(scope="module")
def trial_of():
    from lab9 import trace_case

    return lambda shape: trace_case.investigate(shape, "C-002", 11)["trial"]


def _ctx(trial, label):
    from pydantic_evals.evaluators import EvaluatorContext

    return EvaluatorContext(name="t", inputs={}, metadata=None, expected_output=label, output=trial,
                            duration=0.0, _span_tree=None, attributes={}, metrics={})


def test_seeded_regression_overrides_db_and_refunds(trial_of):
    from lab9 import graders, trace_case

    t = trial_of("seeded_regression")
    label = trace_case.investigate("seeded_regression", "C-002", 11)["label"]
    first_bad = next(i for i, e in enumerate(t["events"], 1) if e["kind"] == "model_override")
    assert first_bad == 3                                    # the first wrong step
    assert graders.DbFactKept().evaluate(_ctx(t, label)).value is False
    assert graders.RefundAmountCorrect().evaluate(_ctx(t, label)).value is False


def test_fixed_keeps_the_db_fact(trial_of):
    from lab9 import graders, trace_case

    t = trial_of("fixed")
    label = trace_case.investigate("fixed", "C-002", 11)["label"]
    assert not [e for e in t["events"] if e["kind"] == "model_override"]
    assert graders.DbFactKept().evaluate(_ctx(t, label)).value is True
    assert graders.RefundAmountCorrect().evaluate(_ctx(t, label)).value is True
