import cv2
from ultralytics import YOLO

def detect_people(video_path):
    # Load YOLOv8 model
    model = YOLO('yolov8n.pt')  # You can use yolov8s.pt, yolov8m.pt, etc. based on your requirements

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    
    frame_number = 0
    people_count = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Perform detection
        results = model(frame)
        detections = results.pandas().xyxy[0]
        
        # Count the number of people detected
        count = len(detections[detections['name'] == 'person'])
        people_count.append((frame_number, count))
        frame_number += 1

    cap.release()
    return people_count
