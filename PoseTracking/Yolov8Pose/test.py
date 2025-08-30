from ultralytics import YOLO

model = YOLO("yolov8n-pose.pt")
result = model.predict(source ="0")