# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5` (backend replay, 100 mẫu mỗi tiêu chí, nhãn người có sẵn trong CSV).
FAIL là lớp dương (judge phải *tìm ra* lỗi). Tỉ lệ lỗi hiệu chỉnh bằng Rogan-Gladen.

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có (tp 24, fp 4, fn 6, tn 66) | **dùng** (tầng theo dõi, không thay grader code về tiền/approval) |
| helpful | 100 | 0.375 | 1.000 | 0.300 | **Không** (tp 9, fp 0, fn 21, tn 70) | **loại**, không được dùng làm gate |

Tỉ lệ FAIL quan sát → hiệu chỉnh: tone 0.28 → 0.30; helpful 0.09 → **0.30**. Judge `helpful` báo 9% lỗi trong khi thực tế khoảng 30%.

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú / sửa rubric |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha, anh check giúp em." (tone) | PASS | FAIL | Người | Xưng "em/anh", suồng sã. Rubric thêm: bắt buộc "Dạ… anh/chị", cấm "em/nha/nhé" khi nói với khách |
| 2 | H-017 "Dạ, bạn ơi LogiX đã hoàn 25.000đ… rồi nha." (tone) | PASS | FAIL | Người | Có "Dạ" nên judge bị đánh lừa, nhưng "bạn ơi… nha" sai giọng CSKH. Rubric: một từ suồng sã là FAIL dù có "Dạ" |
| 3 | H-029 "Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm." (tone) | PASS | FAIL | Người | Câu cụt, chặn khách nhắn tiếp. Rubric thêm: không được từ chối nhận thêm tin nhắn của khách |
| 4 | H-063 "Dạ, LogiX đã hoàn 20.000đ và sẽ hoàn thêm cho anh/chị ạ." (tone) | PASS | FAIL | Người | Hứa hoàn thêm không có căn cứ. Đây là lỗi nội dung (FM-08), không giao cho judge tone: kiểm bằng grader code `ReplyMatchesLedger` |
| 5 | H-042 "Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ." (tone) | FAIL | PASS | Người | Lịch sự, đúng giọng. Judge phạt vì thiếu cảm ơn/xin lỗi. Rubric: cảm ơn/xin lỗi không bắt buộc với thông báo hoàn tiền |
| 6 | H-051 "Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ." (tone) | FAIL | PASS | Người | Từ "refund" không làm sai giọng. Rubric: thuật ngữ vay mượn phổ biến chấp nhận được |
| 7 | HL-015 "Dạ, LogiX đã hoàn 55.000đ cho đơn O-112 ạ." (helpful) | PASS | FAIL | Người | Judge chỉ đọc văn phong, không đối chiếu số tiền với ledger. Tiền phải chấm bằng code |
| 8 | HL-016 / HL-028 "…thành thật xin lỗi… rất trân trọng sự kiên nhẫn…" (helpful) | PASS | FAIL | Người | Đủ lời xin lỗi nhưng không nói đã làm gì. Judge thưởng sự lịch sự. Rubric: "hữu ích" = nêu hành động + số tiền + thời hạn |
| 9 | HL-047 "Ok bạn, đơn O-515 xử lý rồi nhé." (helpful) | PASS | FAIL | Người | Không nói kết quả (hoàn bao nhiêu? từ chối?) |

Người đúng ở cả 9 case: `tone_ok` hơi dễ dãi với giọng suồng sã (fn 6) và khắt khe với cách diễn đạt lệch mẫu (fp 4); `helpful` gần như luôn PASS.

## Kết luận
- **Loại `helpful`**: recall 0.30 < 0.70 và κ 0.375 < 0.6; judge bỏ sót 21/30 reply thực sự không hữu ích (fn = 21). Dùng làm gate sẽ cho lọt phần lớn bản tệ (báo 9% lỗi so với ~30% sau hiệu chỉnh). P = 1.0 không cứu được: judge không bao giờ báo nhầm, nhưng gần như không báo. Nếu sửa rubric theo hàng 7-9 thì phải calibrate lại trên nhãn mới trước khi đưa vào.
- **Giữ `tone_ok`** (κ 0.757, P 0.857, R 0.8) ở tầng theo dõi; sau khi sửa rubric theo hàng 1-6 cần calibrate lại. Tiền và approval không bao giờ giao cho judge.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới (held-out) để có kết luận thật. Judge hằng số làm κ không xác định: `cohen_kappa` raise `ValueError`, `calibrate` coi là FAIL.
