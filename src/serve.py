from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "")
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """
    Tải file model.joblib từ cloud storage (AWS S3 / GCP GCS) về máy khi server khởi động.
    """
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    if not ARTIFACT_BUCKET:
        print("ARTIFACT_BUCKET chưa được thiết lập. Bỏ qua tải model từ Cloud Storage.")
        return

    # Thử tải từ AWS S3 bằng boto3 trước
    try:
        import boto3
        s3 = boto3.client("s3")
        s3.download_file(ARTIFACT_BUCKET, MODEL_KEY, MODEL_PATH)
        print("Model đã được tải xuống từ AWS S3.")
        return
    except Exception as e:
        print(f"Không thể tải từ S3: {e}")

    # Thử tải từ GCP GCS
    try:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(ARTIFACT_BUCKET)
        blob = bucket.blob(MODEL_KEY)
        blob.download_to_filename(MODEL_PATH)
        print("Model đã được tải xuống từ GCP GCS.")
    except Exception as e:
        print(f"Không thể tải từ GCS: {e}")


download_model()

# Nếu ~/models/model.joblib chưa tồn tại nhưng có file cục bộ models/model.joblib thì dùng file cục bộ
if not os.path.exists(MODEL_PATH) and os.path.exists("models/model.joblib"):
    MODEL_PATH = "models/model.joblib"

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Không thể nạp model từ {MODEL_PATH}: {e}")
        model = None
else:
    model = None


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """
    Endpoint kiểm tra sức khỏe server.
    GitHub Actions gọi endpoint này sau khi deploy để xác nhận server đang chạy.

    Trả về: {"status": "ok"}
    """
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luận chính.

    Đầu vào : JSON {"features": [f1, f2, ..., f10]}
    Đầu ra  : JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}

    Thứ tự 10 đặc trưng (khớp với thứ tự trong FEATURE_NAMES của test):
        age, workclass, education_num, marital_status, occupation,
        relationship, sex, capital_gain, capital_loss, hours_per_week
    """
    if len(req.features) != 10:
        raise HTTPException(
            status_code=400,
            detail="Expected 10 features (adult income)"
        )

    if model is None:
        raise HTTPException(
            status_code=500,
            detail="Model file not found or not loaded yet."
        )

    pred = int(model.predict([req.features])[0])
    label = "thu_nhap_cao" if pred == 1 else "thu_nhap_thap"
    return {"prediction": pred, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

