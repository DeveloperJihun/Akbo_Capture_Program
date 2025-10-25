import tkinter as tk
from tkinter import messagebox
import state  # 기존 전역 상태 사용

def open_resizable_overlay():
    """크기/위치 조절 가능한 캡처 영역 박스"""
    overlay = tk.Toplevel()
    overlay.title("캡처 영역 조절")
    overlay.geometry("300x200+100+100")  # 기본 크기
    overlay.configure(bg="red")
    
    # 창 투명도 (테두리 느낌)
    overlay.attributes("-alpha", 0.3)
    
    # 기본적으로 드래그 이동 + 크기조절 가능
    overlay.resizable(True, True)

    def save_region():
        # 현재 위치와 크기 가져오기
        overlay.update_idletasks()
        geo = overlay.geometry()  # "WxH+X+Y"
        size, x, y = geo.split("+")
        w, h = size.split("x")
        state.capture_region = (int(x), int(y), int(w), int(h))
        messagebox.showinfo("완료", f"캡처 영역 저장됨: {state.capture_region}")
        overlay.destroy()

    btn = tk.Button(overlay, text="이 영역으로 저장", command=save_region)
    btn.pack(side="bottom", fill="x")

    # 메인 윈도우와 독립적으로 동작
    overlay.transient()
    overlay.grab_set()
    overlay.focus_force()
