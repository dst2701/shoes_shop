import tkinter as tk
from tkinter import ttk
import mysql.connector

# Debug version để kiểm tra layout
def debug_product_view():
    root = tk.Tk()
    root.title("DEBUG - Shop Shoes")
    root.geometry("1400x800")
    root.configure(bg='red')  # Background đỏ để dễ debug

    print("=== DEBUGGING LAYOUT ===")

    # Header
    print("1. Tạo header...")
    header_frame = tk.Frame(root, bg='#2c3e50', height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)
    tk.Label(header_frame, text="SHOP GIÀY (DEBUG)", font=('Arial', 20, 'bold'),
             fg='white', bg='#2c3e50').pack(pady=15)

    # THANH TÌM KIẾM - MÀU ĐỎ ĐỂ DỄ THẤY
    print("2. Tạo thanh tìm kiếm...")
    search_frame = tk.Frame(root, bg='red', height=100)
    search_frame.pack(fill='x', padx=10, pady=10)
    search_frame.pack_propagate(False)

    tk.Label(search_frame, text="🔍 THANH TÌM KIẾM NÀY CÓ HIỂN THỊ KHÔNG?",
             font=('Arial', 20, 'bold'), bg='red', fg='white').pack(pady=30)

    # THANH BỘ LỌC - MÀU XANH ĐỂ DỄ THẤY
    print("3. Tạo thanh bộ lọc...")
    filter_frame = tk.Frame(root, bg='blue', height=80)
    filter_frame.pack(fill='x', padx=10, pady=10)
    filter_frame.pack_propagate(False)

    tk.Label(filter_frame, text="🔧 BỘ LỌC NÀY CÓ HIỂN THỊ KHÔNG?",
             font=('Arial', 18, 'bold'), bg='blue', fg='white').pack(pady=20)

    # Nội dung chính
    print("4. Tạo nội dung chính...")
    main_frame = tk.Frame(root, bg='yellow')
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    tk.Label(main_frame, text="NỘI DUNG CHÍNH Ở ĐÂY",
             font=('Arial', 16, 'bold'), bg='yellow').pack(expand=True)

    print("5. Hoàn thành layout debug!")
    print("Nếu bạn thấy:")
    print("- Header đen: SHOP GIÀY (DEBUG)")
    print("- Thanh đỏ: 🔍 THANH TÌM KIẾM...")
    print("- Thanh xanh: 🔧 BỘ LỌC...")
    print("- Vùng vàng: NỘI DUNG CHÍNH")
    print("Thì layout đang hoạt động đúng!")

    root.mainloop()

if __name__ == "__main__":
    debug_product_view()
