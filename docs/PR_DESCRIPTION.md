# PR: Lab 9 — evaluation & failure analysis

## Gate exit 1 của `seeded_regression` (v1)
```
gate: PR E-seeded_regression-20261117-274b vs main E-swarm-20261117-274b · eval set 274bbd989d64
  refund_amount_correct  0.7857   Δ -0.200 CI [-0.414, +0.000] BLOCK
  pass_rate              0.7143   Δ -0.271 CI [-0.500, -0.057] BLOCK
  reply_matches_ledger   0.7857   Δ -0.214 CI [-0.429, +0.000] BLOCK
exit 1 — blocked: refund_amount_correct, pass_rate, reply_matches_ledger
```
`fixed`: exit 0 (merge).

## Scorecard v2 (`python -m lab9.mutation --spec config/metric_spec_v2.yaml --baseline reports/baseline_v2.json`)
```
  fixed                expect merge got merge ok          
  honest_refactor      expect merge got merge ok          
  seeded_regression    expect block got block ok          refund_amount_correct, pass_rate, pass_hat_5, reply_matches_ledger, slice:money_movement/pass_rate, slice:adversarial/pass_rate, slice:denial/pass_rate
  slice_regression     expect block got block ok          slice:money_movement/pass_rate
  flaky_regression     expect block got block ok          refund_amount_correct, pass_rate, pass_hat_5, slice:money_movement/pass_rate
mutation score 3/3 · false alarms 0
```

## A/A (--aa 66,77,88,99,110)
```
metric                 spec seeds  alt seeds    delta
approval_bypass                 0          0  +0.0000
secret_leak                     0          0  +0.0000
db_fact_kept               0.9786     0.9786  +0.0000
refund_amount_correct      0.9786     0.9786  +0.0000
pass_rate                  0.9786     0.9786  +0.0000
reply_matches_ledger          1.0        1.0  +0.0000
pass_5                     0.8929     0.8929  +0.0000
pass_at_1                  0.9786     0.9786  +0.0000
pass_hat_1                 0.9786     0.9786  +0.0000
pass_at_3                     1.0        1.0  +0.0000
pass_hat_3                 0.9357     0.9357  +0.0000
pass_at_5                     1.0        1.0  +0.0000
pass_hat_5                 0.8929     0.8929  +0.0000
cost_per_success          50.8077    50.8077  +0.0000
```

## 4 trap công khai (`python -m lab9.traps ...`, mỗi dòng gate exit 1)
```
[evaluator_errors_as_nan]
  INTEGRITY 18 row value(s) None/absent for graded metrics, first ('E-014', 11, 'pass_rate')
exit 1 — blocked: integrity
[dropped_failing_rows]
  INTEGRITY (item, seed) set differs from baseline: missing ["('E-014', 11)", "('E-014', 33)", "('E-014', 55)", "('E-105', 11)"], extra []
exit 1 — blocked: integrity
[cherry_picked_seeds]
  INTEGRITY (item, seed) set differs from baseline: missing ["('E-001', 11)", "('E-001', 33)", "('E-001', 55)", "('E-002', 11)"], extra []
exit 1 — blocked: integrity
[loosened_spec]
  INTEGRITY slice adversarial removed
  INTEGRITY slice denial removed
exit 1 — blocked: integrity
```
