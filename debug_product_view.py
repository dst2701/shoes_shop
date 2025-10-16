"""
DEBUG VERSION - Product View với chỉ search và cart để test layout
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView

class ProductViewDebug(BaseView):
    def __init__(self, role=None, username=None):
        super().__init__("DEBUG - Shop Shoes", "1400x800")
        self.role = role
        self.username = username
        self.cart_count = 0
        self.setup_debug_ui()

    def setup_debug_ui(self):
        """DEBUG UI - chỉ test search và cart"""
        print("=== THIẾT LẬP DEBUG UI ===")

        # 1. HEADER với CART - MÀU ĐỎ ĐỂ DỄ THẤY
        print("1. Tạo header...")
        header_frame = tk.Frame(self.root, bg='red', height=80)  # Màu đỏ để dễ thấy
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='red')
        header_container.pack(fill='both', expand=True, padx=10)

        # Logo
        tk.Label(header_container, text="SHOP GIÀY DEBUG", font=('Arial', 20, 'bold'),
                 fg='white', bg='red').pack(side='left', pady=20)

        # CART BUTTON - VÀNG ĐỂ NỔI BẬT
        print("2. Tạo cart button...")
        self.cart_btn = tk.Button(header_container, text=f"🛒 GIỎ HÀNG DEBUG ({self.cart_count})",
                                 command=self.test_cart,
                                 bg='yellow', fg='black', relief='solid', bd=3,
                                 font=('Arial', 14, 'bold'), padx=20, pady=10,
                                 cursor='hand2')
        self.cart_btn.pack(side='right', pady=20)

        # 2. THANH TÌM KIẾM - MÀU XANH ĐỂ DỄ THẤY
        print("3. Tạo search bar...")
        search_frame = tk.Frame(self.root, bg='blue', height=100)  # Màu xanh để dễ thấy
        search_frame.pack(fill='x', padx=10, pady=10)
        search_frame.pack_propagate(False)

        search_container = tk.Frame(search_frame, bg='blue')
        search_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Search label
        tk.Label(search_container, text="🔍 THANH TÌM KIẾM DEBUG:",
                 font=('Arial', 16, 'bold'), bg='blue', fg='white').pack(side='left')

        # Search entry
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var,
                               font=('Arial', 14), width=30, relief='solid', bd=3)
        search_entry.pack(side='right', padx=10)

        # 3. BỘ LỌC - MÀU TÍM ĐỂ DỄ THẤY
        print("4. Tạo filter...")
        filter_frame = tk.Frame(self.root, bg='purple', height=80)  # Màu tím để dễ thấy
        filter_frame.pack(fill='x', padx=10, pady=10)
        filter_frame.pack_propagate(False)

        filter_container = tk.Frame(filter_frame, bg='purple')
        filter_container.pack(fill='both', expand=True, padx=20, pady=15)

        tk.Label(filter_container, text="BỘ LỌC DEBUG: Nike | Adidas | Tất cả",
                 font=('Arial', 14, 'bold'), bg='purple', fg='white').pack()

        # 4. CONTENT AREA - MÀU XANH LÁ ĐỂ DỄ THẤY
        print("5. Tạo content area...")
        content_frame = tk.Frame(self.root, bg='green')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(content_frame, text="DANH SÁCH SẢN PHẨM DEBUG\n\n"
                                   "Nếu bạn thấy được:\n"
                                   "- Header đỏ với nút giỏ hàng vàng\n"
                                   "- Thanh search xanh\n" 
                                   "- Bộ lọc tím\n"
                                   "- Content xanh lá này\n\n"
                                   "Thì layout đang hoạt động bình thường!",
                 font=('Arial', 16), bg='green', fg='white',
                 justify='center').pack(expand=True, pady=50)

        print("=== HOÀN THÀNH DEBUG UI ===")

    def test_cart(self):
        """Test mở giỏ hàng"""
        messagebox.showinfo("DEBUG", "Nút giỏ hàng hoạt động!\nSẽ mở cart view...")

        # Test import cart view
        try:
            from views.cart_view import CartView
            messagebox.showinfo("DEBUG", "CartView import thành công!")
        except Exception as e:
            messagebox.showerror("DEBUG ERROR", f"Lỗi import CartView: {e}")

    def show(self):
        """Override show để thêm debug info"""
        print("=== HIỂN THỊ DEBUG WINDOW ===")
        self.root.mainloop()

# Test function
def test_debug_view():
    """Function để test debug view"""
    print("=== BẮT ĐẦU TEST DEBUG ===")
    debug_view = ProductViewDebug(role="customer", username="test_user")
    debug_view.show()

if __name__ == "__main__":
    test_debug_view()
