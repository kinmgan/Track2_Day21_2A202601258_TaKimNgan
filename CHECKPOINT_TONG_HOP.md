# CHECKPOINT TỔNG HỢP LAB 21: TỪ THỰC NGHIỆM CỤC BỘ ĐẾN TRIỂN KHAI LIÊN TỤC (MLOps)
*(Dành cho người mới bắt đầu / Non-Tech — Hướng dẫn chuẩn hóa 100% cho Windows)*

---

## 💡 1. GIẢI THÍCH THUẬT NGỮ & BẢN CHẤT (BẮT BUỘC ĐỌC ĐỂ HIỂU VÌ SAO PHẢI LÀM)

Nếu bạn là người mới (non-tech), các từ ngữ chuyên ngành MLOps có thể làm bạn hoang mang. Hãy hiểu chúng qua các ví dụ đời thường sau:

| Thuật ngữ | Giải thích bình dân | Ví dụ thực tế dễ hiểu |
|---|---|---|
| **Mô hình AI / ML (Model)** | Một "học sinh" học bài từ dữ liệu quá khứ để đi thi dự đoán. | Ở bài lab này: Học sinh sẽ xem thông tin tuổi, số năm học, nghề nghiệp... để dự đoán người đó thu nhập **> 50.000$/năm** hay **<= 50.000$/năm**. |
| **MLOps (ML Operations)** | Dây chuyền sản xuất công nghiệp cho AI. | Thay vì làm bánh thủ công ở nhà (chạy code trên máy cá nhân), MLOps tạo ra nhà máy tự động: tự trộn bột, tự nướng, tự kiểm tra bánh ngon không, rồi tự đóng gói bán. |
| **MLflow (Sổ tay thí nghiệm)** | Nhật ký ghi chép lại điểm số của các lần thử nghiệm. | Khi bạn thay đổi cách dạy học sinh (thay đổi siêu tham số / hyperparameter), MLflow sẽ ghi lại: Lần 1 điểm bao nhiêu, Lần 2 điểm bao nhiêu. |
| **DVC (Data Version Control)** | "Quản lý kho" cho dữ liệu lớn. | Git chỉ lưu được file code chữ nhẹ, không lưu nổi file dữ liệu nặng hàng triệu dòng. DVC sẽ cất dữ liệu nặng vào "Kho mây", chỉ để lại một "Thẻ kho" siêu nhẹ (`.dvc`) cho Git giữ. |
| **Cloud Storage / Bucket** | Tủ Locker bảo mật trên mây (Google Cloud / AWS / Azure). | Nơi cất giữ dữ liệu thô và mô hình AI đã hoàn thành để dùng chung cho cả team. |
| **VM (Virtual Machine - Máy chủ ảo)** | Chiếc máy tính chạy 24/7 trên trung tâm dữ liệu. | Giống như thuê một chiếc máy tính trên mây để cài ứng dụng trả kết quả cho người dùng bất kể ngày đêm. |
| **FastAPI / REST API / Endpoint** | Quầy giao dịch nhận yêu cầu và trả kết quả. | Khách gửi thông tin qua cửa `/score`, máy chủ dùng mô hình AI tính toán rồi trả về kết quả `thu_nhap_cao` hoặc `thu_nhap_thap`. |
| **CI/CD (GitHub Actions)** | Robot vận hành dây chuyền tự động. | Mỗi khi bạn đẩy code/dữ liệu mới lên GitHub (`git push`), robot GitHub Actions tự bật máy lên, lấy dữ liệu, dạy học sinh, chấm điểm, và mang học sinh đi phục vụ. |
| **Quality Gate (Cổng kiểm định)** | Thanh chắn chất lượng trước khi xuất xưởng. | Nếu điểm thi của mô hình mới dưới 0.65, robot hủy ngay việc triển khai, không cho phép đưa mô hình kém lên máy chủ. |

---

## 🎯 2. TẠI SAO BÀI LAB DÙNG ĐIỂM F1 THAY VÌ ACCURACY (ĐỘ CHÍNH XÁC CHUNG)?

> **Cạm bẫy thực tế:** 
> Tập dữ liệu có **75.2%** người thu nhập thấp và chỉ **24.8%** người thu nhập cao. 
> - Nếu mô hình lười biếng, **luôn đoán tất cả mọi người là thu nhập thấp**, nó sẽ đúng 75.2% trường hợp! 
> - Điểm **Accuracy = 0.752 (75.2%)** nghe có vẻ cao, nhưng mô hình này **HOÀN TOÀN VÔ DỤNG** vì không tìm ra được bất kỳ ai có thu nhập cao.

* **F1-score (của lớp thu nhập cao)**: Đo lường chính xác khả năng "bắt trúng" người thu nhập cao mà không bị đoán nhầm. Nếu đoán bừa tất cả là thu nhập thấp, **F1-score = 0.0**.
* **Tiêu chuẩn đạt bài lab**: Chỉ số `f1_score >= 0.65`.

---

## 🗺️ 3. LỘ TRÌNH TỔNG QUAN (3 BƯỚC THỰC HIỆN)

```
[BƯỚC 1: CỤC BỘ (LOCAL)]          [BƯỚC 2: TỰ ĐỘNG HÓA (CI/CD)]        [BƯỚC 3: HUẤN LUYỆN LIÊN TỤC]
Chạy code trên máy Windows         Đẩy code/dữ liệu lên GitHub         Bổ sung dữ liệu mới
Thử 3+ siêu tham số               GitHub Actions tự động chạy 4 jobs   Git Push -> Pipeline tự động
Lưu nhật ký bằng MLflow           Kiểm tra F1 >= 0.65 -> Đưa lên VM   Cập nhật mô hình mới trên VM
```

---

## 🛠️ 4. BẢNG CHECKPOINT CHI TIẾT THEO CÁC TASK (CHUẨN WINDOWS)

### 📌 TASK 0: CHUẨN BỊ MÔI TRƯỜNG TRÊN WINDOWS
**Mục tiêu:** Cài đặt các công cụ cần thiết và tạo môi trường ảo Python.
**Kiến thức thu được:** Biết cách quản lý môi trường ảo cô lập trên Windows, không làm hỏng Python hệ thống.

* **Thao tác chi tiết (Thực hiện trên PowerShell):**
  1. Mở **PowerShell** tại thư mục dự án `Track2_Day21_2A202601258_TaKimNgan`:
     ```powershell
     # Tạo môi trường ảo
     python -m venv .venv

     # Kích hoạt môi trường ảo trên Windows PowerShell
     .\.venv\Scripts\Activate.ps1
     ```
     *(Lưu ý: Nếu gặp lỗi PowerShell chặn script ExecutionPolicy, chạy lệnh: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` rồi kích hoạt lại).*
  2. Cài đặt các thư viện phụ thuộc:
     ```powershell
     pip install -r requirements.txt
     ```
  3. Kiểm tra các lệnh chuẩn bị:
     ```powershell
     python prepare_data.py
     ```
     *Kết quả mong đợi:* Hiển thị `train_batch1.csv : 22361 mau`, `holdout.csv : 500 mau`, `train_batch2.csv : 22361 mau`.

---

### 📌 TASK 1: BƯỚC 1 - THỰC NGHIỆM CỤC BỘ VỚI MLFLOW
**Mục tiêu:** Viết code huấn luyện `src/train.py`, chạy ít nhất 3 thí nghiệm với các siêu tham số khác nhau trong `params.yaml`, so sánh bằng MLflow.
**Kiến thức thu được:** Hiểu cách log thông số, lưu mô hình artifact và giải thích vì sao F1-score phản ánh đúng bản chất dữ liệu mất cân bằng.

* **Thao tác chi tiết:**
  1. **Đặt biến môi trường MLflow trên Windows PowerShell:**
     ```powershell
     $env:MLFLOW_TRACKING_URI="sqlite:///mlflow.db"
     $env:MLFLOW_ARTIFACT_ROOT="./mlartifacts"
     ```
  2. **Hoàn thiện file `src/train.py`:**
     * Đọc `data/train_batch1.csv` và `data/holdout.csv`.
     * Huấn luyện `GradientBoostingClassifier`.
     * Log `f1_score` (lớp dương, không dùng average) và `accuracy` vào MLflow.
     * Lưu kết quả ra `outputs/report.json` và mô hình ra `models/model.joblib`.
  3. **Chạy thí nghiệm 3 lần (mỗi lần sửa `params.yaml`):**
     * *Lần 1:* `n_estimators: 100`, `learning_rate: 0.1`, `max_depth: 3` -> Chạy: `python src/train.py`
     * *Lần 2:* `n_estimators: 50`, `learning_rate: 0.05`, `max_depth: 2` -> Sửa `params.yaml` -> Chạy: `python src/train.py`
     * *Lần 3:* `n_estimators: 200`, `learning_rate: 0.1`, `max_depth: 5` -> Sửa `params.yaml` -> Chạy: `python src/train.py`
  4. **Bật MLflow UI để soi kết quả:**
     ```powershell
     mlflow ui --backend-store-uri sqlite:///mlflow.db
     ```
     Mở trình duyệt truy cập: `http://localhost:5000`. Chọn bộ tham số tốt nhất (đạt `f1_score >= 0.65`) cập nhật lại vào `params.yaml`.

* **📸 CHỨNG CỨ CẦN LƯU GIAO ĐOẠN 1:**
  * File ảnh: `nop-bai/anh-chup-man-hinh/01-mlflow-ui.png`
  * *Yêu cầu:* Chụp giao diện MLflow UI (thấy rõ URL `http://localhost:5000`), hiển thị ít nhất 3 runs, thấy rõ cột `f1_score` và `accuracy`.

---

### 📌 TASK 2: BƯỚC 2 - THIẾT LẬP KHO MÂY DVC & MÁY CHỦ VM
**Mục tiêu:** Đưa dữ liệu lên Cloud Storage (GCP/AWS/Azure) bằng DVC và tạo máy chủ ảo VM trên mây (GCP GCE hoặc AWS EC2).
**Kiến thức thu được:** Hiểu cách phiên bản hóa dữ liệu lớn mà không làm nặng Git, cấu hình phân quyền Cloud Security (Service Account trên GCP hoặc Access Key / IAM Role trên AWS).

* **Thao tác chi tiết:**

  #### 🔹 PHƯƠNG ÁN 1: NẾU DÙNG AWS (S3 & EC2)
  1. **Cài đặt DVC S3 plugin:**
     ```powershell
     pip install dvc-s3 boto3
     ```
  2. **Tạo AWS S3 Bucket:**
     ```powershell
     aws s3 mb s3://<TEN_BUCKET_CUA_BAN> --region us-east-1
     ```
     *(Hoặc vào AWS Console > S3 > Create bucket)*
  3. **Tạo AWS IAM Credentials:**
     * Vào AWS Console > IAM > Users > Create user (ví dụ: `dvc-user`).
     * Cấp quyền `AmazonS3FullAccess` (hoặc policy S3 phù hợp).
     * Tạo Access Key (tải/lưu `AWS_ACCESS_KEY_ID` và `AWS_SECRET_ACCESS_KEY`).
  4. **Cấu hình DVC trỏ tới S3 Bucket:**
     ```powershell
     dvc init
     dvc remote add -d labstore s3://<TEN_BUCKET_CUA_BAN>/dvc
     
     # Cấu hình Access Key cho DVC remote
     dvc remote modify labstore access_key_id <AWS_ACCESS_KEY_ID>
     dvc remote modify labstore secret_access_key <AWS_SECRET_ACCESS_KEY>
     dvc remote modify labstore region us-east-1
     
     # Thêm dữ liệu & đẩy lên S3
     dvc add data/train_batch1.csv data/holdout.csv data/train_batch2.csv
     dvc push
     ```
   5. **Tạo và Cấu hình Máy Chủ Âỏ AWS EC2 (Chi tiết cho người mới):**
      * **Bước 5.1 (Đăng nhập & Chọn Region):** Truy cập [AWS Management Console](https://console.aws.amazon.com/), chọn Region `us-east-1` (N. Virginia) ở góc trên bên phải.
      * **Bước 5.2 (Vào dịch vụ EC2):** Tìm kiếm **EC2** trong thanh tìm kiếm -> Click **Launch Instance**.
      * **Bước 5.3 (Cấu hình Instance):**
        - **Name:** Nhập `income-prediction-api`
        - **OS / AMI:** Chọn **Ubuntu** -> **Ubuntu Server 22.04 LTS (HVM)** (*Free tier eligible*).
        - **Instance type:** Chọn `t2.micro` (hoặc `t3.micro` - thuộc gói Miễn phí / Free Tier).
      * **Bước 5.4 (Cấu hình Network & Firewall / Security Group):**
        - Nhấn **Edit** tại phần *Network settings*.
        - Đảm bảo **Auto-assign Public IP** là `Enable`.
        - Tại **Inbound security groups rules**:
          - *Rule 1 (SSH):* Type = `SSH`, Port = `22`, Source = `Anywhere` (`0.0.0.0/0`).
          - *Rule 2 (API Port):* Click **Add security group rule**, chọn Type = `Custom TCP`, Port Range = `8080`, Source = `Anywhere` (`0.0.0.0/0`).
      * **Bước 5.5 (Launch):** Nhấn **Launch Instance**, chờ 1-2 phút rồi lưu lại địa chỉ **Public IPv4 Address** của EC2 (ví dụ: `54.210.12.34`).

   6. **Tạo SSH Key Pair trên Windows & Kết nối vào EC2:**
      * **Bước 6.1 (Tạo SSH Key trên Windows PowerShell):**
        ```powershell
        ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\income_deploy" -N '""'
        ```
        Lệnh trên tạo ra 2 file tại `C:\Users\<Tên_User>\.ssh\`:
        - `income_deploy` (Private Key - Lưu bảo mật trên Windows).
        - `income_deploy.pub` (Public Key - Dán lên EC2).
      * **Bước 6.2 (Thêm Public Key vào EC2):**
        - Trên AWS Console > EC2 > Instances > Chọn Instance vừa tạo -> Nhấn **Connect** -> Chọn **EC2 Instance Connect** -> Nhấn **Connect** để mở terminal web.
        - Mở file `.ssh/authorized_keys` trên EC2 và dán nội dung của `income_deploy.pub` vào:
          ```bash
          mkdir -p ~/.ssh
          nano ~/.ssh/authorized_keys
          # Dán toàn bộ nội dung file income_deploy.pub từ Windows vào đây, ấn Ctrl+O (Enter) để save, Ctrl+X để thoát.
          chmod 600 ~/.ssh/authorized_keys
          chmod 700 ~/.ssh
          ```
      * **Bước 6.3 (Kiểm tra kết nối SSH từ Windows PowerShell):**
        ```powershell
        ssh -i "$env:USERPROFILE\.ssh\income_deploy" ubuntu@<PUBLIC_IP_CUA_EC2>
        ```

   7. **Cài đặt Môi trường, Viết `src/serve.py` (FastAPI) & Deploy Systemd Service trên EC2:**
      * **Bước 7.1 (Cài đặt Packages trên EC2 qua SSH):**
        ```bash
        sudo apt update && sudo apt install -y python3-pip python3-venv awscli
        mkdir -p ~/app/src ~/models
        cd ~/app
        python3 -m venv venv
        source venv/bin/activate
        pip install fastapi uvicorn boto3 joblib scikit-learn pandas pydantic
        ```
      * **Bước 7.2 (Hoàn thiện `src/serve.py` hỗ trợ AWS S3):**
        File `src/serve.py` trên máy local/EC2 sử dụng `boto3` để tự động tải `model.joblib` từ S3 Bucket `ARTIFACT_BUCKET` khi server khởi động và mở 2 endpoint: `GET /healthz` và `POST /score`.
      * **Bước 7.3 (Copy code từ Windows lên EC2):**
        ```powershell
        scp -i "$env:USERPROFILE\.ssh\income_deploy" src/serve.py ubuntu@<PUBLIC_IP_CUA_EC2>:~/app/src/serve.py
        ```
      * **Bước 7.4 (Tạo & Kích hoạt `systemd service` `income-api.service` trên EC2):**
        Tạo file dịch vụ chạy ẩn:
        ```bash
        sudo nano /etc/systemd/system/income-api.service
        ```
        Nội dung file `income-api.service`:
        ```ini
        [Unit]
        Description=Income Prediction FastAPI Service
        After=network.target

        [Service]
        User=ubuntu
        WorkingDirectory=/home/ubuntu/app
        Environment="PATH=/home/ubuntu/app/venv/bin"
        Environment="ARTIFACT_BUCKET=<TEN_BUCKET_S3_CUA_BAN>"
        Environment="AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>"
        Environment="AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>"
        Environment="AWS_REGION=us-east-1"
        ExecStart=/home/ubuntu/app/venv/bin/python /home/ubuntu/app/src/serve.py

        Restart=always
        RestartSec=5

        [Install]
        WantedBy=multi-user.target
        ```
        Khởi chạy dịch vụ:
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl enable income-api
        sudo systemctl start income-api
        sudo systemctl status income-api
        ```
      * **Bước 7.5 (Kiểm tra Endpoint):**
        ```powershell
        curl http://<PUBLIC_IP_CUA_EC2>:8080/healthz
        ```
        Kết quả trả về `{"status": "ok"}` chứng tỏ API đã hoạt động thành công!

  ---

  #### 🔹 PHƯƠNG ÁN 2: NẾU DÙNG GCP (GCS & GCE)
  1. **Tạo Cloud Storage Bucket:**
     ```powershell
     gcloud storage buckets create gs://<TEN_BUCKET_CUA_BAN> --location=us-central1
     ```
  2. **Tạo Service Account & Tải key `sa-key.json`** lưu vào thư mục dự án (Lưu ý: `sa-key.json` nằm trong `.gitignore`, KHÔNG push lên Git).
  3. **Cấu hình DVC trỏ tới GCS Bucket:**
     ```powershell
     dvc init
     dvc remote add -d labstore gs://<TEN_BUCKET_CUA_BAN>/dvc
     dvc remote modify labstore credentialpath sa-key.json
     dvc add data/train_batch1.csv data/holdout.csv data/train_batch2.csv
     dvc push
     ```
  4. **Tạo máy chủ ảo VM GCE** và mở cổng firewall `8080`.
  5. **Viết `src/serve.py` (FastAPI)** mở 2 endpoint: `GET /healthz` và `POST /score`.
  6. Copy `sa-key.json` và `src/serve.py` lên VM, cấu hình `systemd service` (`income-api.service`).
  7. Tạo SSH Key pair dán `.pub` vào `~/.ssh/authorized_keys` trên VM.

---

### 📌 TASK 3: BƯỚC 2 - THIẾT LẬP GITHUB ACTIONS CI/CD PIPELINE
**Mục tiêu:** Xây dựng file `.github/workflows/cicd.yml` với 4 jobs liên hoàn: `Unit Test` -> `Train` -> `Quality Gate` -> `Release`.
**Kiến thức thu được:** Hiểu nguyên lý CI/CD trong AI: tự động kiểm thử code, kéo dữ liệu từ DVC, huấn luyện mô hình trên môi trường sạch, chặn deployment nếu không đạt điểm chuẩn, tự động deploy lên VM.

* **Thao tác chi tiết:**
  1. **Cấu hình Secrets trên GitHub Repo** (Settings > Secrets and variables > Actions):
     * **Đối với AWS:**
       - `AWS_ACCESS_KEY_ID`: Key ID của AWS IAM User
       - `AWS_SECRET_ACCESS_KEY`: Secret Key của AWS IAM User
       - `AWS_REGION`: Region S3 (vd: `us-east-1`)
       - `ARTIFACT_BUCKET`: Tên S3 Bucket
       - `SERVER_HOST`: IP công khai (Public IP) của AWS EC2
       - `SERVER_USER`: `ubuntu` (user mặc định trên AWS Ubuntu EC2)
       - `SERVER_SSH_KEY`: Nội dung file private key `income_deploy`
     * **Đối với GCP:**
       - `STORAGE_CREDENTIALS`: Nội dung file `sa-key.json`
       - `ARTIFACT_BUCKET`: Tên GCS Bucket
       - `SERVER_HOST`: IP công khai của GCE VM
       - `SERVER_USER`: Tên user trên VM
       - `SERVER_SSH_KEY`: Nội dung file private key `income_deploy`
  2. **Viết unit test `tests/test_train.py`** và chạy kiểm thử cục bộ: `pytest tests/ -v`.
  3. **Hoàn thiện file `.github/workflows/cicd.yml`**.
  4. **Push code lên GitHub để kích hoạt Pipeline:**
     ```powershell
     git add .
     git commit -m "feat: add CI/CD pipeline, tests, and serving API"
     git push origin main
     ```
  5. **Kiểm tra kết quả trên VM (Dùng `curl.exe` chuẩn Windows PowerShell):**
     ```powershell
     # Kiểm tra sức khỏe API
     curl.exe http://<IP_VM>:8080/healthz

     # Thử nghiệm dự đoán
     curl.exe -X POST http://<IP_VM>:8080/score -H "Content-Type: application/json" -d "{\"features\": [60, 2, 5, 2, 4, 0, 1, 0, 0, 45]}"
     ```

* **📸 CHỨNG CỨ CẦN LƯU GIAO ĐOẠN 2:**
  * File ảnh 1: `nop-bai/anh-chup-man-hinh/02-actions-buoc-2.png` (Tab GitHub Actions cả 4 jobs màu xanh: Unit Test, Train, Quality Gate, Release).
  * File ảnh 2: `nop-bai/anh-chup-man-hinh/04-curl-api.png` (Màn hình PowerShell chạy 2 lệnh `curl.exe`, thấy rõ IP VM và kết quả trả về JSON).
  * File ảnh 3: `nop-bai/anh-chup-man-hinh/05-cloud-storage.png` (Trình duyệt xem Cloud Console thấy rõ thư mục `dvc/` và `artifacts/current/model.joblib`).

---

### 📌 TASK 4: BƯỚC 3 - HUẤN LUYỆN LIÊN TỤC (CONTINUOUS TRAINING)
**Mục tiêu:** Mô phỏng việc có dữ liệu mới thu thập thêm. Chỉ cần cập nhật dữ liệu và `git push`, toàn bộ hệ thống tự huấn luyện lại và cập nhật mô hình trên VM.
**Kiến thức thu được:** Hiểu bản chất vòng lặp MLOps thực tế sản xuất: Dữ liệu mới -> DVC track -> Git trigger CI/CD -> Auto Retrain -> Auto Deploy.

* **Thao tác chi tiết:**
  1. Ghép 22.361 mẫu mới từ `train_batch2.csv` vào tập huấn luyện:
     ```powershell
     python append_batch.py
     ```
  2. Báo cho DVC biết dữ liệu đã thay đổi & Đẩy dữ liệu mới lên Cloud Storage:
     ```powershell
     dvc add data/train_batch1.csv
     git add data/train_batch1.csv.dvc
     git commit -m "data: bổ sung 22361 mẫu dữ liệu mới (train_batch2)"
     
     # QUAN TRỌNG: Phải dvc push TRƯỚC khi git push!
     dvc push
     git push origin main
     ```
  3. Mở tab GitHub Actions xem robot tự kích hoạt quy trình huấn luyện lại trên 44.722 mẫu.
  4. Tải file `outputs/report.json` của cả 2 lần chạy (Bước 2 vs Bước 3) để so sánh chỉ số F1.

* **📸 CHỨNG CỨ CẦN LƯU GIAO ĐOẠN 3:**
  * File ảnh: `nop-bai/anh-chup-man-hinh/03-actions-buoc-3.png`
  * *Yêu cầu:* Tên của lần chạy Actions hiển thị đúng commit message dữ liệu (`data: bổ sung 22361 mẫu dữ liệu mới...`), cả 4 jobs màu xanh.

---

### 📌 TASK 5: HOÀN THIỆN BÁO CÁO & NỘP BÀI
**Mục tiêu:** Điền báo cáo tổng hợp `nop-bai/bao-cao.md`, kiểm tra lại checklist và nộp link Repo.

* **Thao tác chi tiết:**
  1. Mở file `nop-bai/bao-cao.md` và điền 3 nội dung:
     * Bộ siêu tham số đã chọn ở Bước 1 & Lý do chọn F1 thay vì Accuracy.
     * So sánh điểm F1 giữa Bước 2 (22.361 mẫu) và Bước 3 (44.722 mẫu).
     * Khó khăn gặp phải và giải pháp.
  2. Kiểm tra checklist trong `nop-bai/README.md`.
  3. Git push toàn bộ thư mục `nop-bai/` lên GitHub:
     ```powershell
     git add nop-bai/
     git commit -m "docs: complete report and screenshots for submission"
     git push origin main
     ```
  4. Lấy link GitHub Repo Public dán vào hệ thống nộp bài `https://codelabs.vlearn.dev`.

---

## 📊 5. TIÊU CHUẨN ĐÁNH GIÁ ĐẠT (RUBRIC CHẤM ĐIỂM 80-100 ĐIỂM)

| Tiêu chí | Điều kiện ĐẠT | Điểm tối đa |
|---|---|---|
| **1. MLflow Tracking (Bước 1)** | MLflow UI có ít nhất 3 runs, hiển thị đủ `f1_score` và `accuracy`. | **20 điểm** |
| **2. Phân tích chỉ số (Bước 1)** | Chọn đúng bộ tham số đạt F1 >= 0.65, giải thích chuẩn vì sao chọn F1 thay vì Accuracy. | **4 điểm** |
| **3. DVC Remote (Bước 2)** | Data đã được lưu trữ trên Cloud Storage theo cấu trúc `dvc/`. | **12 điểm** |
| **4. GitHub Actions CI/CD (Bước 2)** | Cả 4 jobs (`Unit Test`, `Train`, `Quality Gate`, `Release`) xanh lá cây. | **16 điểm** |
| **5. Quality Gate (Bước 2)** | Đặt ngưỡng chăn F1 < 0.65 chính xác trong CI workflow. | **4 điểm** |
| **6. Serving API (Bước 2)** | Máy chủ VM trả về kết quả đúng qua endpoint `POST /score`. | **12 điểm** |
| **7. Continuous Training (Bước 3)** | Một commit dữ liệu tự kích hoạt pipeline chạy lại thành công. | **12 điểm** |
| **TỔNG ĐIỂM CHÍNH** | **Hoàn thiện đầy đủ 5 ảnh minh chứng + 1 báo cáo A4** | **80/80 điểm** |
| **THÁCH THỨC BONUS** | Làm thêm các bài tập nâng cao (DagsHub, Threshold tuning, Drift detection...) | **+20 điểm** |

---

## ⚡ QUICK REFERENCE: LỆNH BÀN THỜ CHO WINDOWS POWERSHELL

```powershell
# 1. Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# 2. Đặt biến môi trường MLflow
$env:MLFLOW_TRACKING_URI="sqlite:///mlflow.db"
$env:MLFLOW_ARTIFACT_ROOT="./mlartifacts"

# 3. Chạy huấn luyện & Bật UI MLflow
python src/train.py
mlflow ui --backend-store-uri sqlite:///mlflow.db

# 4. Kiểm tra Unit Test
pytest tests/ -v

# 5. DVC Push & Git Push Dữ liệu mới
dvc add data/train_batch1.csv
git add data/train_batch1.csv.dvc
git commit -m "data: update dataset"
dvc push
git push origin main

# 6. Test API trên VM bằng PowerShell
curl.exe http://<VM_IP>:8080/healthz
curl.exe -X POST http://<VM_IP>:8080/score -H "Content-Type: application/json" -d "{\"features\": [60, 2, 5, 2, 4, 0, 1, 0, 0, 45]}"
```
