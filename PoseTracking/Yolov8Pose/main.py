import cv2
import cvzone
from ultralytics import YOLO
import numpy as np
from directkeys import PressKey, ReleaseKey, up_arrow_pressed, down_arrow_pressed, left_arrow_pressed, right_arrow_pressed, space_pressed
import time
import torch
import mediapipe as mp

# Khởi tạo webcam và model YOLO
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
model = YOLO('yolov8n-pose.pt').to("cuda")
current_key_pressed = set()

# Tọa độ gốc ban đầu (origin)
origin_x, origin_y = 320, 360
neutral_radius = 50  # Bán kính vùng trung tâm

# Biến đếm thời gian để cập nhật tọa độ gốc
last_update_time = time.time()
update_interval = 0.6

# Khởi tạo biến đếm khung hình
frame_counter = 0

# Lưu trữ keypoints của khung hình trước
previous_keypoints = None

def update_keys(new_keys):
    """Cập nhật trạng thái các phím dựa trên vùng mới."""
    global current_key_pressed
    keys_to_press = set(new_keys)

    for key in current_key_pressed - keys_to_press:
        ReleaseKey(key)
    for key in keys_to_press - current_key_pressed:
        PressKey(key)

    current_key_pressed = keys_to_press

def count_fingers(hand_landmarks):
    """Đếm số ngón tay giơ lên dựa trên landmark của MediaPipe."""
    finger_tips = [4, 8, 12, 16, 20]  # Các đầu ngón tay
    finger_bottoms = [3, 6, 10, 14, 18]  # Đốt ngón gần lòng bàn tay

    count = 0
    for tip, bottom in zip(finger_tips, finger_bottoms):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[bottom].y:
            count += 1

    return count

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể truy cập webcam hoặc luồng video.")
        break

    frame = cv2.resize(frame, (640, 720))
    height, width = frame.shape[:2]

    blank_image = np.zeros((height, width, 3), dtype=np.uint8)

    if frame_counter % 2 == 0:
        results = model(frame)
    frame_counter += 1

    # Bỏ qua việc vẽ lên frame gốc
    # frame = results[0].plot()

    # Xử lý nhận diện bàn tay
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)

    position = "NEUTRAL"
    keys_to_press = []

    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            finger_count = count_fingers(hand_landmarks)

            # FingerCount
            cv2.putText(blank_image, f'Fingers: {finger_count}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            mp_draw.draw_landmarks(blank_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Kiểm tra nếu giơ 5 ngón tay
            if finger_count == 5:
                position = "SPACE"
                keys_to_press.append(space_pressed)

    
    if results[0].keypoints is not None and len(results[0].keypoints.data) > 0:
        for keypoints in results[0].keypoints.data:
            keypoints = keypoints.cpu().numpy()

            if keypoints.shape[0] < 17:
                continue

            center_x, center_y, conf = keypoints[0]
            if conf > 0.5:
                current_time = time.time()
                if current_time - last_update_time > update_interval:
                    origin_x, origin_y = int(center_x), int(center_y)
                    last_update_time = current_time
                    

                dx = int(center_x) - origin_x
                dy = origin_y - int(center_y)

                if abs(dx) <= neutral_radius and abs(dy) <= neutral_radius:
                    if position == "NEUTRAL":
                        position = "NEUTRAL"
                else:
                    if abs(dy) > abs(dx):
                        if dy > 0:
                            position = "UP"
                            keys_to_press.append(up_arrow_pressed)
                        else:
                            position = "DOWN"
                            keys_to_press.append(down_arrow_pressed)
                    else:
                        if dx > 0:
                            position = "RIGHT"
                            keys_to_press.append(left_arrow_pressed)
                        else:
                            position = "LEFT"
                            keys_to_press.append(right_arrow_pressed)

                update_keys(keys_to_press)

                if position:
                    cv2.putText(blank_image, position, (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Vẽ trục cố định tại gốc tọa độ
                cv2.line(blank_image, (origin_x, 0), (origin_x, height), (0, 255, 0), 2)
                cv2.line(blank_image, (0, origin_y), (width, origin_y), (0, 255, 0), 2)

                # Vẽ vùng neutral
                cv2.rectangle(blank_image,
                              (origin_x - neutral_radius, origin_y - neutral_radius),
                              (origin_x + neutral_radius, origin_y + neutral_radius),
                              (255, 255, 0), 2)

            if previous_keypoints is not None:
                for i, keypoint in enumerate(keypoints):
                    x, y, confidence = keypoint
                    if confidence > 0.7 and i < len(previous_keypoints):
                        prev_x, prev_y, prev_confidence = previous_keypoints[i]
                        if abs(x - prev_x) > 2 or abs(y - prev_y) > 2:
                            cv2.circle(blank_image, (int(x), int(y)), radius=5, color=(255, 0, 0), thickness=1)
                            cv2.putText(blank_image, f'{i}', (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.4, (255, 255, 255), 1, cv2.LINE_AA)

            previous_keypoints = keypoints
            # Vẽ kết nối keypoints OverLay
            connections = [
                (3, 1), (1, 0), (0, 2), (2, 4), (1, 2), (4, 6), (3, 5),
                (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
                (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
                (5, 11), (6, 12)
            ]
            for part_a, part_b in connections:
                if part_a >= keypoints.shape[0] or part_b >= keypoints.shape[0]:
                    continue
                x1, y1, conf1 = keypoints[part_a]
                x2, y2, conf2 = keypoints[part_b]

                if conf1 > 0.5 and conf2 > 0.5:
                    cv2.line(blank_image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255),
                             thickness=2)


    # Chỉ hiển thị blank_image
    cv2.imshow('Pose Tracking Overlay', blank_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

update_keys([])
cap.release()
cv2.destroyAllWindows()
torch.cuda.empty_cache()