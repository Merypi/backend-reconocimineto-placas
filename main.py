import uvicorn
from fastapi import FastAPI, File, UploadFile
import boto3

app = FastAPI()

# Cliente AWS
rekognition = boto3.client("rekognition", region_name="us-east-1")

@app.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    content = await file.read()

    response = rekognition.detect_text(
        Image={
            "Bytes": content
        }
    )

    texts = []

    for item in response["TextDetections"]:
        if item["Type"] == "LINE":
            texts.append(item["DetectedText"])

    return {
        "textos_detectados": texts
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )