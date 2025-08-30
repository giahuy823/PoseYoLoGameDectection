# Pose Detect and Hand Detect for Endless Run Game

## Giới Thiệu
Chào mừng bạn đến với Pose Detect và Hand Detect cho trò chơi Endless Run Game! Đây là ứng dụng được xây dựng để giúp người chơi có thể điều khiển nhân vật trò chơi Subway Suffer nhảy cúi và qua trái qua phải. Và hiện tại chỉ có thể chơi Subway Suffer.

## Tính Năng Chính
- Phần camera tracking: Tracking theo khung xương người dùng nếu là pose và tracking theo điểm giữa lòng bàn tay.
- Di chuyển: Pose thì di chuyển theo hướng di chuyển của cơ thể. Người chơi qua trái, phải thì nhân vật trong game cũng sẽ chạy qua trái, phải tương ứng với hướng di chuyển của người chơi và tương tự cho phần nhảy lên ngồi xuống.
- Sử dụng ván trượt trong Subway Suffer: Đối với HandDetect thì nắm bàn tay lại thì sẽ sử dụng ván trượt và cũng có thể start màn chơi khi nắm tay lại.
Đối với PoseDetect thì dơ bàn tay lên thì sẽ sử dụng ván trượt và cũng có thể start màn chơi khi dơ tay lên.

## Công nghệ sử dụng
- Trình biên dịch: Python
- Thư viện hỗ trợ: Pygame, random, opencv-python, cvzone, ultralytics, numpy, torch, mediapipe

## Yêu cầu hệ thống
- Game vẫn chưa có .exe nên vẫn phải chạy trong trình biên dịch VSCode, truy cập đường dẫn sau để tải về: https://code.visualstudio.com/.
- Tải python trên trang chủ pyhon về, truy cập đường dẫn sau để truy cập: https://www.python.org/downloads/.

## Khởi động Game
- Mở VSCode và mở thư mục PoseDetect&HandDetect trong VSCode, chạy main.py trong HandGesture để chạy HandDetect và chạy main.py trong Yolov8Pose để chạy PoseDetect.
- Cũng có thể chạy phần chọn cách Tracking trong phần control_selector.py trong để mở menu chọn cách Tracking để chơi có Pose và Hand để chọn lựa,

## Thông tin liên hệ
Gmail: nguyenhoangphongsupham@gmail.com, giahuy.823948@gmail.com
