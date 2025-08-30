import cv2
from cvzone.HandTrackingModule import HandDetector
from directkeys import PressKey, ReleaseKey, space_pressed, up_arrow_pressed, down_arrow_pressed, left_arrow_pressed, right_arrow_pressed
import time

detector = HandDetector(detectionCon=0.8, maxHands=1)
 
#  Phím đang bấm là gì
current_key_pressed = set()

time.sleep(1.5)

video = cv2.VideoCapture(0)

move_threshold = 100
upper_threshold = 200
lower_threshold = 300

# Hàm kiểm tra và nhấn phím
def press_key_if_needed(key, action):
    if action == 'press' and key not in current_key_pressed:
        PressKey(key)
        current_key_pressed.add(key)
    elif action == 'release' and key in current_key_pressed:
        ReleaseKey(key)
        current_key_pressed.remove(key)

while True:
    ret, frame = video.read()
    hands, img = detector.findHands(frame)

    if hands:
        lmList = hands[0]['lmList']
        fingers = detector.fingersUp(hands[0])

        hand_x = lmList[9][0]
        hand_y = lmList[9][1]
        
        height, width, _ = frame.shape
        center_x = width // 2
        
        # Xử lý các tình huống dựa trên vị trí tay
        if fingers == [0, 0, 0, 0, 0]: # Kích hoạt nắm tay
            cv2.putText(frame, 'Skill Activated', (380, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            press_key_if_needed(space_pressed, 'press')

        elif hand_y < upper_threshold:  # Nhảy
            cv2.putText(frame, 'Jumping', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            press_key_if_needed(up_arrow_pressed, 'press')
            press_key_if_needed(down_arrow_pressed, 'release')

        elif hand_y > lower_threshold:  # Cúi người
            cv2.putText(frame, 'Crouching', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            press_key_if_needed(down_arrow_pressed, 'press')
            press_key_if_needed(up_arrow_pressed, 'release')

        elif hand_x > center_x + move_threshold:  # Di chuyển sang trái
            cv2.putText(frame, 'Moving Left', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            press_key_if_needed(left_arrow_pressed, 'press')
            press_key_if_needed(right_arrow_pressed, 'release')

        elif hand_x < center_x - move_threshold:  # Di chuyển sang phải
            cv2.putText(frame, 'Moving Right', (420, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            press_key_if_needed(right_arrow_pressed, 'press')
            press_key_if_needed(left_arrow_pressed, 'release')

        else:  # Vị trí trung lập
            cv2.putText(frame, 'Neutral Position', (350, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            # Release tất cả phím nếu ở vị trí trung lập
            for key in [up_arrow_pressed, down_arrow_pressed, left_arrow_pressed, right_arrow_pressed, space_pressed]:
                press_key_if_needed(key, 'release')

    cv2.imshow("Hand Detector", frame)
    
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Giải phóng tài nguyên
video.release()
cv2.destroyAllWindows()
