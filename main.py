from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from utils import extract_frames, compute_resnet_vector
import os
import shutil
import uuid


app = FastAPI()
FRAME_DIR = "frames"
COLLECTION_NAME = "video_frames"

# Init Qdrant (in-memory)
qdrant = QdrantClient(":memory:")

qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frames = extract_frames(temp_path, FRAME_DIR)

    points = []
    for path in frames:
        vector = compute_resnet_vector(path)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"image_path": path}
        ))

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    os.remove(temp_path)

    return {"frames_stored": len(frames)}

@app.post("/search-similar/")
async def search_similar(file: UploadFile = File(...)):
    temp_path = f"query_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    vector = compute_resnet_vector(temp_path)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=5,
        with_payload=True
    )

    response = []
    for result in results:
        image_path = result.payload["image_path"]
        response.append({
            "score": result.score,
            "image_path": image_path,
            
        })

    os.remove(temp_path)
    return JSONResponse(content=response)

@app.get("/frame/{filename}")
def get_frame(filename: str):
    filepath = os.path.join("frames", filename)
    return FileResponse(filepath)

@app.get("/list-frames/")
def list_frames():
    frames_dir = "frames"
    if not os.path.exists(frames_dir):
        return {"error": "Frames directory not found"}
    
    files = [
        f for f in os.listdir(frames_dir)
        if f.endswith(".jpg") or f.endswith(".png")
    ]
    return JSONResponse(content={"frame_files": files})


app.mount("/", StaticFiles(directory="static", html=True), name="static")
