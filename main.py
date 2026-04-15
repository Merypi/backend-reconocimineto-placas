from fastapi import FastAPI, File, UploadFile
import boto3

app = FastAPI()

# Cliente AWS
rekognition = boto3.client("rekognition", region_name="us-east-1")

@app.post("/reconocer")
async def reconocer(file: UploadFile = File(...)):
    contenido = await file.read()

    response = rekognition.detect_text(
        Image={
            "Bytes": contenido
        }
    )

    textos = []

    for item in response["TextDetections"]:
        if item["Type"] == "LINE":
            textos.append(item["DetectedText"])

    return {
        "textos_detectados": textos
    }