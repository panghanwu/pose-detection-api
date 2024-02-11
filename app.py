from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from pathlib import Path
import shutil

from data import Point, Rectangle, PoseData

def save_temp_video(video: UploadFile) -> str:
    suffix = Path(video.filename).suffix
    path = f'temp{suffix}'
    with open(path, 'wb') as f:
        shutil.copyfileobj(video.file, f)
    return path

    
    
yolo = YOLO('yolov8n-pose.pt')
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Good"}

@app.post('/run')
async def run_yolov8_pose(video: UploadFile = File(...)):
    video_path = save_temp_video(video)
    frame_results = yolo(video_path, stream=True, verbose=False)
    frame_data = []
    for index, result in enumerate(frame_results):
        persons = []
        for i in range(len(result.boxes)):
            pose = PoseData()
            box = result.boxes.xyxy[i]
            conf = result.boxes.conf[i]
            pose.player = Rectangle(
                x1=box[0].item(),
                y1=box[1].item(),
                x2=box[2].item(),
                y2=box[3].item(),
                confidence=conf.item()
            )
            keypoints = result.keypoints.data[i]
            for j in range(17):
                kp = keypoints[j].tolist()
                pose[j+1] = Point(
                    x=kp[0],
                    y=kp[1],
                    confidence=kp[2]
                )
            persons.append(pose)
        frame_data.append({'frame_index': index, 'persons': persons})
            
    return frame_data
