import tkinter as tk
from tkinter import ttk

# Test giao diện để kiểm tra layout
def test_layout():
    root = tk.Tk()
    root.title("Test Layout - Thanh tìm kiếm")
    root.geometry("1400x800")

    # Header
    header = tk.Frame(root, bg='#2c3e50', height=60)
    header.pack(fill='x')
    tk.Label(header, text="TEST LAYOUT", font=('Arial', 20, 'bold'),
             fg='white', bg='#2c3e50').pack(pady=15)

    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Left panel
    left_panel = tk.Frame(main_frame, width=400, bg='lightblue')
    left_panel.pack(side='left', fill='y', padx=(0, 10))
    left_panel.pack_propagate(False)

    # Search section - KIỂM TRA XEM CÓ HIỂN THỊ KHÔNG
    search_frame = tk.Frame(left_panel, bg='#f8f9fa', relief='solid', bd=2)
    search_frame.pack(fill='x', pady=(0, 10))

    tk.Label(search_frame, text="🔍 TÌM KIẾM SẢN PHẨM", font=('Arial', 14, 'bold'),
             bg='#f8f9fa', fg='red').pack(pady=10)

    search_entry = tk.Entry(search_frame, font=('Arial', 12), width=25)
    search_entry.pack(pady=10)
    search_entry.insert(0, "Test thanh tìm kiếm...")

    # Filter section
    filter_frame = tk.Frame(left_panel, bg='#e8f5e8', relief='solid', bd=2)
    filter_frame.pack(fill='x', pady=(0, 10))

    tk.Label(filter_frame, text="🔧 BỘ LỌC", font=('Arial', 14, 'bold'),
             bg='#e8f5e8', fg='blue').pack(pady=10)

    tk.Label(filter_frame, text="Nike ○ Adidas ○ Tất cả",
             bg='#e8f5e8').pack(pady=5)

    # Product list
    list_frame = tk.Frame(left_panel, bg='lightyellow')
    list_frame.pack(fill='both', expand=True)

    tk.Label(list_frame, text="DANH SÁCH SẢN PHẨM", font=('Arial', 16, 'bold')).pack(pady=10)

    # Right panel
    right_panel = tk.Frame(main_frame, bg='lightcoral')
    right_panel.pack(side='right', fill='both', expand=True)

    tk.Label(right_panel, text="CHI TIẾT S���N PHẨM\n(Hình ảnh và mô tả)",
             font=('Arial', 16, 'bold'), fg='white', bg='lightcoral').pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    test_layout()
