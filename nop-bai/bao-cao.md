# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Tạ Kim Ngân |
| MSSV | 2A202601258 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/kinmgan/Track2_Day21_2A202601258_TaKimNgan |
| Ngày nộp | 06/09/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=100`, `learning_rate=0.1`, `max_depth=3`.

**Lý do:** Bộ tham số `n_estimators=100, learning_rate=0.1, max_depth=3` đạt sự cân bằng tối ưu giữa F1-score (0.7109) và Accuracy (0.8780). Mặc dù lần 3 có F1 cao hơn không đáng kể (0.7149), nhưng Accuracy thấp hơn (0.8740) và mô hình phức tạp gấp đôi (`n_estimators=200, max_depth=5`), tốn tài nguyên và dễ quá khớp. Lần 1 có Accuracy cao nhất (0.8780) không trùng với lần có F1 cao nhất (lần 3), phản ánh bản chất dữ liệu mất cân bằng khi Accuracy bị chi phối bởi lớp đa số. Sự đánh đổi giữa `n_estimators` và `learning_rate` cho thấy việc tăng quá mức số lượng cây không cải thiện hiệu năng khi tham số đã hội tụ.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult bị mất cân bằng lớp nghiêm trọng (lớp thu nhập <= 50K chiếm ~75.2%, lớp > 50K chiếm ~24.8%). Nếu mô hình ngây thơ luôn đoán tất cả là thu nhập thấp, Accuracy vẫn đạt 75.2% nhưng hoàn toàn vô dụng vì không nhận diện được ai có thu nhập cao. Chỉ số F1-score trên lớp dương đo lường trung bình hài hòa giữa Precision và Recall, phản ánh chính xác khả năng phát hiện lớp thu nhập cao. Ta không dùng `average="weighted"` hay `macro` khi tính F1-score vì các dạng này bị pha loãng bởi lớp đa số, làm che khuất hiệu năng thực tế trên lớp mục tiêu cần dự đoán.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Runner GitHub Actions không SSH được tới máy chủ EC2. | Private key SSH chưa chuẩn định dạng hoặc Security Group EC2 chặn port 22/8080. | Thêm private key `income_deploy` vào GitHub Secrets và mở port 22, 8080 trong Security Group AWS. |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7109 | 0.8780 |
| Bước 3 (thêm `train_batch2`) | 0.7014 | 0.8740 |

**Nhận xét:** Khi bổ sung 22.361 mẫu từ `train_batch2` (tổng 44.722 mẫu), điểm F1-score giảm nhẹ từ 0.7109 xuống 0.7014 và Accuracy giảm từ 0.8780 xuống 0.8740. Điều này cho thấy dữ liệu bổ sung có cùng phân phối nhưng chứa nhiều nhiễu hơn, làm giảm khả năng tổng quát hóa nếu giữ nguyên siêu tham số. Kết quả chứng minh việc tăng dữ liệu không tự động cải thiện điểm số nếu không đi kèm với tinh chỉnh mô hình.

