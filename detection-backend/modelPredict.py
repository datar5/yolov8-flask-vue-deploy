from ultralytics import YOLO

model_path = './weights/yolov8n_bdd.pt'
video_path = 'video/save/2.mp4'

model = YOLO(model_path)
results = model(video_path, show=True, save=True)

