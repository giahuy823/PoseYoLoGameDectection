import tkinter as tk
import subprocess
import os

current_process = None

HAND_SCRIPT = os.path.join("HandGesture (Endless Run) 2", "main.py")
POSE_SCRIPT = os.path.join("DetectPose",
"DetectPose",
"main.py")

def start_process(script_path):
    global current_process
    stop_process()
    current_process = subprocess.Popen(["python", script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

def stop_process():
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None

def exit_program():
    stop_process()
    root.quit()
    root.destroy()

root = tk.Tk()
root.title("PHƯƠNG THỨC ĐIỀU KHIỂN")
root.geometry("400x200")

label = tk.Label(root, text="Chọn phương thức điều khiển", font=("Arial", 14))
label.pack(pady=10)

btn_pose = tk.Button(root, text="Nhận diện từ cơ thể(YOLOv8)", command=lambda: start_process(POSE_SCRIPT), width=30)
btn_pose.pack(pady=5)

btn_hand = tk.Button(root, text="Nhận diện bàn tay (Hand Gesture)", command=lambda: start_process(HAND_SCRIPT), width=30)
btn_hand.pack(pady=10)

btn_stop = tk.Button(root, text="Dừng", command=stop_process, width=30, bg="orange", fg="white")
btn_stop.pack(pady=5)

btn_exit = tk.Button(root, text="Thoát", command=exit_program, width=30, bg="red", fg="white")
btn_exit.pack(pady=5)

root.mainloop()