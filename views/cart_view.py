"""
Giao diện giỏ hàng - hiển thị sản phẩm đã thêm vào giỏ hàng
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from utils.image_utils import load_image_safely

class CartView(BaseView):
    def __init__(self, username=None, parent_view=None):
        super().__init__("Shop Shoes - Giỏ hàng", "1200x700")
        self.username = username
        self.parent_view = parent_view
        self.cart_data = {}
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện giỏ hàng"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        tk.Label(header_container, text="🛒 GIỎ HÀNG CỦA BẠN", font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        # Back to products button
        btn_back = tk.Button(header_container, text="← Quay lại mua sắm", command=self.back_to_products,
                            bg='#3498db', fg='white', relief='flat',
                            font=('Arial', 12), padx=15, pady=8, cursor='hand2')
        btn_back.pack(side='right', pady=15)

        # Load cart data
        self.load_cart_data()

        if not self.cart_data:
            # Empty cart message
            empty_frame = tk.Frame(self.root, bg='#f8f9fa')
            empty_frame.pack(fill='both', expand=True, padx=20, pady=50)

            tk.Label(empty_frame, text="🛒", font=('Arial', 80), bg='#f8f9fa', fg='#bdc3c7').pack(pady=20)
            tk.Label(empty_frame, text="Giỏ hàng của bạn đang trống",
                     font=('Arial', 18, 'bold'), bg='#f8f9fa', fg='#7f8c8d').pack(pady=10)
            tk.Label(empty_frame, text="Hãy thêm một số sản phẩm để tiếp tục mua sắm!",
                     font=('Arial', 12), bg='#f8f9fa', fg='#95a5a6').pack(pady=5)

            tk.Button(empty_frame, text="Tiếp tục mua sắm", command=self.back_to_products,
                     bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                     relief='flat', padx=30, pady=12, cursor='hand2').pack(pady=30)
        else:
            # Cart content
            main_frame = tk.Frame(self.root)
            main_frame.pack(fill='both', expand=True, padx=15, pady=15)

            # Cart items frame
            items_frame = tk.Frame(main_frame)
            items_frame.pack(fill='both', expand=True)

            tk.Label(items_frame, text="Sản phẩm trong giỏ hàng:", font=('Arial', 16, 'bold'),
                     fg='#2c3e50').pack(anchor='w', pady=(0, 10))

            # Treeview for cart items
            tree_frame = tk.Frame(items_frame)
            tree_frame.pack(fill='both', expand=True)

            # Configure treeview style
            style = ttk.Style()
            style.configure("Cart.Treeview", rowheight=50)

            self.tree = ttk.Treeview(tree_frame, columns=("Hình ảnh", "Tên sản phẩm", "Màu sắc", "Size", "Số lượng", "Đơn giá", "Thành tiền", "Action"),
                                    show="headings", height=12, style="Cart.Treeview")

            # Configure columns
            self.tree.heading("Hình ảnh", text="Hình ảnh")
            self.tree.heading("Tên sản phẩm", text="Tên sản phẩm")
            self.tree.heading("Màu sắc", text="Màu sắc")
            self.tree.heading("Size", text="Size")
            self.tree.heading("Số lượng", text="SL")
            self.tree.heading("Đơn giá", text="Đơn giá")
            self.tree.heading("Thành tiền", text="Thành tiền")
            self.tree.heading("Action", text="")

            self.tree.column("Hình ảnh", width=80, anchor='center')
            self.tree.column("Tên sản phẩm", width=250)
            self.tree.column("Màu sắc", width=80, anchor='center')
            self.tree.column("Size", width=60, anchor='center')
            self.tree.column("Số lượng", width=60, anchor='center')
            self.tree.column("Đơn giá", width=120, anchor='e')
            self.tree.column("Thành tiền", width=130, anchor='e')
            self.tree.column("Action", width=60, anchor='center')

            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)

            self.tree.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Populate cart items
            self.populate_cart_items()

            # Summary frame
            summary_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='ridge', bd=2)
            summary_frame.pack(fill='x', pady=(15, 0))

            summary_container = tk.Frame(summary_frame, bg='#ecf0f1')
            summary_container.pack(fill='x', padx=20, pady=15)

            # Total calculation
            total_amount = sum(item['total'] for item in self.cart_data.values())

            tk.Label(summary_container, text="TỔNG CỘNG:", font=('Arial', 16, 'bold'),
                     bg='#ecf0f1', fg='#2c3e50').pack(side='left')

            tk.Label(summary_container, text=f"{total_amount:,.0f} VNĐ", font=('Arial', 18, 'bold'),
                     bg='#ecf0f1', fg='#e74c3c').pack(side='right')

            # Action buttons frame
            action_frame = tk.Frame(main_frame)
            action_frame.pack(fill='x', pady=(15, 0))

            # Clear cart button
            btn_clear = tk.Button(action_frame, text="🗑️ Xóa toàn bộ giỏ hàng", command=self.clear_cart,
                                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                 relief='flat', padx=20, pady=10, cursor='hand2')
            btn_clear.pack(side='left')

            # View invoice button (thay thế checkout button)
            btn_view_invoice = tk.Button(action_frame, text="📄 Xem hóa đơn", command=self.view_invoice,
                                       bg='#f39c12', fg='white', font=('Arial', 14, 'bold'),
                                       relief='flat', padx=30, pady=10, cursor='hand2')
            btn_view_invoice.pack(side='right')

        # Bind events
        if hasattr(self, 'tree'):
            self.tree.bind("<Button-1>", self.on_tree_click)

    def load_cart_data(self):
        """Load dữ liệu giỏ hàng từ database"""
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep09102025"
            )
            cursor = conn.cursor()

            # Sửa lại tên cột từ TenDangNhap thành TenDN
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()
            
            if not result:
                return

            ma_kh = result[0]

            # Lấy MaGH từ MaKH
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()
            
            if not gh_result:
                return

            ma_gh = gh_result[0]

            # Lấy chi tiết giỏ hàng với thông tin sản phẩm
            cursor.execute("""
                SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
                       (sp.Gia * ghsp.SoLuong) as ThanhTien, url.URLAnh
                FROM giohangchuasanpham ghsp
                JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
                LEFT JOIN (
                    SELECT MaSP, MIN(URLAnh) as URLAnh 
                    FROM url_sp 
                    GROUP BY MaSP
                ) url ON sp.MaSP = url.MaSP
                WHERE ghsp.MaGH = %s
                ORDER BY sp.TenSP
            """, (ma_gh,))

            cart_items = cursor.fetchall()

            # Tổ chức dữ liệu giỏ hàng
            for ma_sp, ten_sp, gia, mau_sac, size, so_luong, thanh_tien, url_anh in cart_items:
                cart_key = f"{ma_sp}_{mau_sac}_{size}"
                self.cart_data[cart_key] = {
                    'product_id': ma_sp,
                    'name': ten_sp,
                    'price': float(gia),
                    'color': mau_sac,
                    'size': size,
                    'quantity': so_luong,
                    'total': float(thanh_tien),
                    'image_url': url_anh
                }

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu giỏ hàng: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def populate_cart_items(self):
        """Điền dữ liệu vào treeview giỏ hàng"""
        for cart_key, item in self.cart_data.items():
            # Format price
            price_display = f"{item['price']:,.0f} VNĐ"
            total_display = f"{item['total']:,.0f} VNĐ"

            self.tree.insert("", "end", iid=cart_key, values=(
                "📷",  # Placeholder for image
                item['name'],
                item['color'],
                item['size'],
                item['quantity'],
                price_display,
                total_display,
                "🗑️"  # Delete button
            ))

    def on_tree_click(self, event):
        """Handle click trên treeview - xóa sản phẩm"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x, event.y)
            if column == "#8":  # Action column (Delete)
                item = self.tree.identify_row(event.y)
                if item:
                    self.remove_from_cart(item)

    def remove_from_cart(self, cart_key):
        """Xóa sản phẩm khỏi giỏ hàng"""
        if cart_key not in self.cart_data:
            return

        item = self.cart_data[cart_key]

        # Confirm deletion
        result = messagebox.askyesno("Xác nhận",
                                   f"Bạn có chắc muốn xóa '{item['name']}' khỏi giỏ hàng?")
        if not result:
            return

        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep09102025"
            )
            cursor = conn.cursor()

            # Lấy MaKH và MaGH
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()
            ma_kh = result[0]

            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            result = cursor.fetchone()
            ma_gh = result[0]

            # Xóa sản phẩm khỏi giỏ hàng
            cursor.execute("""
                DELETE FROM giohangchuasanpham 
                WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
            """, (ma_gh, item['product_id'], item['color'], item['size']))

            conn.commit()

            # Remove from local data và UI
            del self.cart_data[cart_key]
            self.tree.delete(cart_key)

            # Update parent view cart count
            if self.parent_view:
                self.parent_view.load_cart_count()

            messagebox.showinfo("Thành công", f"Đã xóa '{item['name']}' khỏi giỏ hàng!")

            # Refresh view if cart is empty
            if not self.cart_data:
                self.close()
                new_cart = CartView(username=self.username, parent_view=self.parent_view)
                new_cart.show()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def clear_cart(self):
        """Xóa toàn bộ giỏ hàng"""
        if not self.cart_data:
            return

        # Confirm deletion
        result = messagebox.askyesno("Xác nhận",
                                   "Bạn có chắc muốn xóa toàn bộ sản phẩm trong giỏ hàng?")
        if not result:
            return

        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep09102025"
            )
            cursor = conn.cursor()

            # Lấy MaKH và MaGH
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()
            ma_kh = result[0]

            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            result = cursor.fetchone()
            ma_gh = result[0]

            # Xóa toàn bộ sản phẩm trong giỏ hàng
            cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))
            conn.commit()

            # Update parent view cart count
            if self.parent_view:
                self.parent_view.load_cart_count()

            messagebox.showinfo("Thành công", "Đã xóa toàn bộ sản phẩm trong giỏ hàng!")

            # Refresh view
            self.close()
            new_cart = CartView(username=self.username, parent_view=self.parent_view)
            new_cart.show()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa giỏ hàng: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def view_invoice(self):
        """Xem hóa đơn - mở trang hóa đơn chi tiết"""
        if not self.cart_data:
            messagebox.showwarning("Cảnh báo", "Giỏ hàng trống!")
            return

        # Import và tạo InvoiceView với reload để đảm bảo sử dụng phiên bản mới nhất
        import importlib
        import sys

        # Reload module nếu đã được import trước đó
        if 'views.invoice_view' in sys.modules:
            importlib.reload(sys.modules['views.invoice_view'])

        from views.invoice_view import InvoiceView

        # Đóng cart view hiện tại
        self.close()

        # Mở invoice view với dữ liệu giỏ hàng
        invoice_view = InvoiceView(
            username=self.username,
            cart_data=self.cart_data,
            parent_view=self.parent_view
        )
        invoice_view.show()

    def back_to_products(self):
        """Quay lại trang sản phẩm"""
        self.close()

    def close(self):
        """Đóng view với proper cleanup"""
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass