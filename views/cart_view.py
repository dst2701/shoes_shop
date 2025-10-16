"""
Cart View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from config.database import get_db_connection

class CartView:
    def __init__(self, root):
        self.root = root

    def show_cart(self, username, role="buyer", on_back_callback=None):
        """Show cart interface - from main.py"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Giỏ hàng")
        self.root.geometry("1000x700")

        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        tk.Label(header_container, text="GIỎ HÀNG", font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        btn_back = tk.Button(header_container, text="← Quay lại",
                            command=lambda: on_back_callback(role, username) if on_back_callback else None,
                            bg='#f39c12', fg='white', relief='flat',
                            font=('Arial', 12, 'bold'), padx=15, pady=5)
        btn_back.pack(side='right', pady=15, padx=(0, 10))

        btn_logout = tk.Button(header_container, text="Đăng xuất",
                              command=lambda: self.logout_callback() if hasattr(self, 'logout_callback') else None,
                              bg='#e74c3c', fg='white', relief='flat',
                              font=('Arial', 15), padx=15, pady=5)
        btn_logout.pack(side='right', pady=15)

        if username:
            tk.Label(header_container, text=f"Khách hàng: {username}",
                     font=('Arial', 14), fg='white', bg='#2c3e50').pack(side='right', pady=15, padx=(0, 15))

        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Load cart data trực tiếp từ database dựa vào username
        cart_products = {}
        total_amount = 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Lấy MaKH từ username
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                tk.Label(main_frame, text="Không tìm thấy thông tin khách hàng",
                        font=('Arial', 18), bg='#f8f9fa', fg='#e74c3c').pack(expand=True)
                return

            ma_kh = result[0]

            # Lấy MaGH từ MaKH
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()

            if not gh_result:
                # Giỏ hàng trống
                tk.Label(main_frame, text="Giỏ hàng trống",
                        font=('Arial', 18), bg='#f8f9fa', fg='#6c757d').pack(expand=True)
                return

            ma_gh = gh_result[0]

            # Lấy chi tiết giỏ hàng với thông tin sản phẩm từ database
            cursor.execute("""
                SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
                       (sp.Gia * ghsp.SoLuong) as ThanhTien
                FROM giohangchuasanpham ghsp
                JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
                WHERE ghsp.MaGH = %s
                ORDER BY sp.TenSP
            """, (ma_gh,))

            cart_items = cursor.fetchall()

            if not cart_items:
                tk.Label(main_frame, text="Giỏ hàng trống",
                        font=('Arial', 18), bg='#f8f9fa', fg='#6c757d').pack(expand=True)
                return

            # Tổ chức dữ liệu giỏ hàng
            for ma_sp, ten_sp, gia, mau_sac, size, so_luong, thanh_tien in cart_items:
                cart_key = f"{ma_sp}_{mau_sac}_{size}"
                cart_products[cart_key] = {
                    'product_id': ma_sp,
                    'name': ten_sp,
                    'price': float(gia),
                    'color': mau_sac,
                    'size': size,
                    'quantity': so_luong,
                    'total': float(thanh_tien)
                }
                total_amount += float(thanh_tien)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu giỏ hàng: {str(e)}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        print(f"Debug: Loaded cart for user {username}: {len(cart_products)} items, total: {total_amount}")

        # Cart title
        tk.Label(main_frame, text="Chi tiết giỏ hàng:", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa').pack(anchor='w', pady=(0, 10))

        # Table header
        header_frame_table = tk.Frame(main_frame, bg='#34495e', height=40)
        header_frame_table.pack(fill='x', pady=(0, 5))
        header_frame_table.pack_propagate(False)

        # Header labels
        tk.Label(header_frame_table, text="Tên sản phẩm", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=25, anchor='w').pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Màu sắc", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=10).pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Size", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=8).pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Số lượng", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=10).pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Đơn giá", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=12).pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Thành tiền", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=12).pack(side='left', padx=5, pady=5)
        tk.Label(header_frame_table, text="Hành động", font=('Arial', 12, 'bold'),
                 bg='#34495e', fg='white', width=10).pack(side='left', padx=5, pady=5)

        # Items container
        items_container = tk.Frame(main_frame, bg='#f8f9fa')
        items_container.pack(fill='both', expand=True, pady=(0, 20))

        # Function to remove item from cart - cập nhật để xóa t�� database
        def remove_from_cart_db(product_id, color, size):
            result = messagebox.askyesno("Xác nhận xóa",
                                       f"Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?")
            if not result:
                return

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Lấy MaKH và MaGH
                cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
                result = cursor.fetchone()
                ma_kh = result[0]

                cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
                result = cursor.fetchone()
                ma_gh = result[0]

                # Xóa sản phẩm khỏi giỏ hàng
                cursor.execute("""
                    DELETE FROM giohangchuasanpham 
                    WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
                """, (ma_gh, product_id, color, size))

                conn.commit()
                messagebox.showinfo("Thành công", "Đã xóa sản phẩm khỏi giỏ hàng!")

                # Refresh cart view
                self.show_cart(username, role, on_back_callback)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Create product rows
        for cart_key, product in cart_products.items():
            # Product row frame
            product_frame = tk.Frame(items_container, bg='white', relief='solid', bd=1, height=60)
            product_frame.pack(fill='x', pady=2)
            product_frame.pack_propagate(False)

            # Product name
            name_label = tk.Label(product_frame, text=product['name'], font=('Arial', 11),
                                 bg='white', width=25, anchor='w', wraplength=180)
            name_label.pack(side='left', padx=5, pady=10)

            # Color
            color_label = tk.Label(product_frame, text=product['color'], font=('Arial', 11),
                                  bg='white', width=10)
            color_label.pack(side='left', padx=5, pady=10)

            # Size
            size_label = tk.Label(product_frame, text=product['size'], font=('Arial', 11),
                                 bg='white', width=8)
            size_label.pack(side='left', padx=5, pady=10)

            # Quantity
            qty_label = tk.Label(product_frame, text=str(product['quantity']), font=('Arial', 11),
                                bg='white', width=10)
            qty_label.pack(side='left', padx=5, pady=10)

            # Unit price
            price_display = f"{product['price']:,.0f} VNĐ"
            price_label = tk.Label(product_frame, text=price_display, font=('Arial', 11),
                                  bg='white', width=12)
            price_label.pack(side='left', padx=5, pady=10)

            # Total price
            total_display = f"{product['total']:,.0f} VNĐ"
            total_label = tk.Label(product_frame, text=total_display, font=('Arial', 11, 'bold'),
                                  bg='white', width=12, fg='#e74c3c')
            total_label.pack(side='left', padx=5, pady=10)

            # Remove button
            btn_remove = tk.Button(product_frame, text="🗑️",
                                  command=lambda pid=product['product_id'], color=product['color'], size=product['size']: remove_from_cart_db(pid, color, size),
                                  bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                  width=8, cursor='hand2', relief='flat')
            btn_remove.pack(side='left', padx=5, pady=5)

        # Total section
        total_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='ridge', bd=2)
        total_frame.pack(fill='x', pady=(20, 0))

        total_container = tk.Frame(total_frame, bg='#ecf0f1')
        total_container.pack(fill='x', padx=20, pady=15)

        tk.Label(total_container, text="TỔNG TIỀN:", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').pack(side='left')

        tk.Label(total_container, text=f"{total_amount:,.0f} VNĐ", font=('Arial', 20, 'bold'),
                 bg='#ecf0f1', fg='#e74c3c').pack(side='right')

        # Action buttons frame
        button_frame = tk.Frame(main_frame, bg='#f8f9fa')
        button_frame.pack(fill='x', pady=(20, 0))

        btn_clear = tk.Button(button_frame, text="🗑️ Xóa tất cả",
                             command=lambda: self.clear_cart_db(username, role, on_back_callback),
                             bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                             padx=20, pady=10, relief='flat', cursor='hand2')
        btn_clear.pack(side='left')

        btn_view_invoice = tk.Button(button_frame, text="📄 Xem hóa đơn",
                               command=lambda: self.view_invoice_from_cart_db(username, role, cart_products, total_amount, on_back_callback),
                               bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=10, relief='flat', cursor='hand2')
        btn_view_invoice.pack(side='right')

    def clear_cart_db(self, username, role="buyer", on_back_callback=None):
        """Xóa toàn bộ giỏ hàng từ database"""
        result = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả sản phẩm trong giỏ hàng?")
        if not result:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Lấy MaKH và MaGH
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return

            ma_kh = result[0]

            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            result = cursor.fetchone()
            if not result:
                return

            ma_gh = result[0]

            # Xóa toàn bộ sản phẩm trong giỏ hàng từ database
            cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))
            conn.commit()

            messagebox.showinfo("Thành công", "Đã xóa tất cả sản phẩm!")
            self.show_cart(username, role, on_back_callback)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa giỏ hàng: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def view_invoice_from_cart_db(self, username, role, cart_products, total_amount, on_back_callback):
        """Xem hóa đơn từ giỏ hàng - sử dụng dữ liệu từ database"""
        if not cart_products:
            messagebox.showwarning("Cảnh báo", "Giỏ hàng trống!")
            return

        # Convert cart_products format để tương thích với show_invoice_page
        converted_products = {}
        for cart_key, product in cart_products.items():
            converted_products[product['product_id']] = {
                'name': product['name'],
                'price': product['price'],
                'quantity': product['quantity'],
                'total': product['total']
            }

        # Import và sử dụng InvoiceView
        from views.invoice_view import InvoiceView
        invoice_view = InvoiceView(self.root)
        invoice_view.show_invoice_page(username, role, converted_products, total_amount, lambda: self.show_cart(username, role, on_back_callback))

    def set_logout_callback(self, callback):
        """Set logout callback"""
        self.logout_callback = callback
