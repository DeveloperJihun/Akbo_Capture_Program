import tkinter as tk
from tkinter import messagebox, simpledialog
import pyautogui
import os
import state

def ask_song_title():
    """곡 제목 입력받고 폴더 생성"""
    state.song_title = simpledialog.askstring("곡 제목 입력", "곡 제목을 입력하세요:")
    if not state.song_title:
        messagebox.showwarning("경고", "곡 제목을 입력해야 합니다!")
        return False

    state.SAVE_DIR = os.path.join("captures", state.song_title)
    os.makedirs(state.SAVE_DIR, exist_ok=True)
    state.count = 1
    return True


def select_area(root):
    """캡처 영역 지정"""
    if not state.song_title:
        if not ask_song_title():
            return

    root.withdraw()
    # messagebox.showinfo("영역 선택", "마우스로 드래그하여 캡처 영역을 지정하세요.")

    sel = tk.Toplevel()
    sel.attributes("-fullscreen", True)
    sel.attributes("-alpha", 0.3)
    sel.configure(bg="gray")

    start = {"x": 0, "y": 0}
    rect = None

    def on_mouse_down(event):
        start["x"], start["y"] = event.x, event.y

    def on_mouse_drag(event):
        nonlocal rect
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start["x"], start["y"], event.x, event.y, outline="red", width=2)

    def on_mouse_up(event):
        x1, y1, x2, y2 = start["x"], start["y"], event.x, event.y
        sel.destroy()

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        state.capture_region = (x1, y1, x2 - x1, y2 - y1)
        messagebox.showinfo("완료", f"캡처 영역: {state.capture_region}")
        root.deiconify()

    canvas = tk.Canvas(sel, bg="gray")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)


def capture_area():
    """캡처 실행"""
    if not state.capture_region:
        messagebox.showwarning("경고", "먼저 캡처할 영역을 지정하세요!")
        return

    img = pyautogui.screenshot(region=state.capture_region)
    filename = os.path.join(state.SAVE_DIR, f"{state.song_title}_{state.count}.png")
    img.save(filename)
    print(f"저장됨: {filename}")
    state.count += 1


def toggle_overlay():
    """캡처 영역 미리보기 토글"""
    if not state.capture_region:
        messagebox.showwarning("경고", "먼저 캡처할 영역을 지정하세요!")
        return

    if state.overlay_window and tk.Toplevel.winfo_exists(state.overlay_window):
        state.overlay_window.destroy()
        state.overlay_window = None
    else:
        state.overlay_window = tk.Toplevel()
        state.overlay_window.overrideredirect(True)
        state.overlay_window.attributes("-alpha", 0.3)
        state.overlay_window.configure(bg="red")

        x, y, w, h = state.capture_region
        state.overlay_window.geometry(f"{w}x{h}+{x}+{y}")
