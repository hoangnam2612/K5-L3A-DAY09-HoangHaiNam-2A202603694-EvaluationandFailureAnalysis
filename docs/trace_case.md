# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `<shape> <claim>@<seed>`, run ID trong report |
| Triệu chứng | Grader nào fail; reply nói gì so với ledger ghi gì |
| Bước sai đầu tiên | Số thứ tự event + kind + trích payload (≤1 dòng) |
| Vì sao là bước *đầu tiên* | Các bước trước đó đúng ra sao (dẫn số event) |
| Failure mode | Mã FM-xx trong `docs/failure_taxonomy.md` |
| Đối chứng | Cùng claim@seed trên shape `fixed`: bước đó khác thế nào |
| Regression test | Tên test + grader/assert nào bắt được; đã thấy fail trên variant lỗi và pass trên `fixed` chưa |
| Chưa chắc chắn | Điều trace không chứng minh được |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.


---
## Case của nhóm: C-002@11 (FM-03 ticket_trust)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, trong `E-seeded_regression-20261117-948e` (item E-002, 5/5 seed đều fail) |
| Triệu chứng | `pass_rate` fail (`status resolved != denied`), `refund_amount_correct` fail, `db_fact_kept` fail. Reply trôi chảy "LogiX đã hoàn 20.000đ cho đơn O-202" nhưng nhãn là `denied`, ledger đã ghi 20.000 (nhãn 0) |
| Bước sai đầu tiên | **Event 3** `model_override {"delay_days": 5}`: ticket ghi "trễ 5 ngày" còn DB ghi 3 ngày; agent lấy số của ticket |
| Vì sao là bước *đầu tiên* | Event 1 `handoff` và event 2 `investigator` (lookup_order, delay_days của DB) đều đúng. Từ event 3, quote (event 4: 20.000, clause SHIP-LATE-03), refund và reply chỉ là hệ quả của số ngày sai |
| Failure mode | FM-03 (ticket_trust) |
| Đối chứng | `fixed C-002@11`: không có `model_override`; event 3 `quote` = 0 `no_entitlement`; reply "chưa đủ điều kiện", ledger 0, đúng nhãn |
| Regression test | `tests/test_lab9_trace_case.py`: `test_seeded_regression_overrides_db_and_refunds` (bắt lỗi trên `seeded_regression`: event 3 là `model_override`, `DbFactKept` và `RefundAmountCorrect` đều False) và `test_fixed_keeps_the_db_fact` (pass trên `fixed`). Đã chạy cả hai |
| Chưa chắc chắn | MockLLM tất định nên trace không cho biết một LLM thật tin ticket với xác suất bao nhiêu; chỉ chứng minh cơ chế lỗi và việc grader bắt được nó |
