"""
Base class cho các view
"""
import tkinter as tk
from tkinter import messagebox
import os

class BaseView:
    """Base class cho tất cả các view"""

    def __init__(self, title="Shoes Shop", size="800x600"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)

        # Thiết lập icon giống file gốc
        self.setup_icon()

        # Center window
        self.center_window()

        # Proper cleanup khi đóng cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_icon(self):
        """Thiết lập icon cho app giống file gốc"""
        try:
            # Đường dẫn tới file icon giống file gốc
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'image.png')
            if os.path.exists(icon_path):
                icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Không thể tải icon: {e}")

    def center_window(self):
        """Căn giữa cửa sổ trên màn hình"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def show(self):
        """Hiển thị view - method bị thiếu"""
        self.root.mainloop()

    def close(self):
        """Đóng view"""
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass

    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass
