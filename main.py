import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import boto3

from db import vehicles_collection, users_collection

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    if len(texts) < 2:
        return {"registrado": False}

    placa = (texts[0] + texts[1]).replace(" ", "").upper()

    vehiculo = vehicles_collection.find_one({"placa": placa})

    if not vehiculo:
        return False

    usuario = users_collection.find_one({"_id": vehiculo["usuario_id"]})

    return {
        "autorizado": vehiculo.get("autorizado"),
        "placa": placa,
        "modelo": vehiculo.get("modelo"),
        "usuario": {
            "nombre": usuario.get("nombre") if usuario else None,
            "documento": usuario.get("documento") if usuario else None
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )