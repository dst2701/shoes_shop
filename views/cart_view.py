"""
Cart View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from config.database import get_db_connection
from utils.ui_effects import add_button_hover_effect, get_hover_color

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
                            bg='#f39c12', fg='white', relief='raised',
                            font=('Arial', 12, 'bold'), padx=15, pady=5, cursor='hand2', bd=2)
        btn_back.pack(side='right', pady=15, padx=(0, 10))
        # Add hover effect
        add_button_hover_effect(btn_back, '#f39c12', get_hover_color('#f39c12'))

        btn_logout = tk.Button(header_container, text="Đăng xuất",
                              command=lambda: self.logout_callback() if hasattr(self, 'logout_callback') else None,
                              bg='#e74c3c', fg='white', relief='raised',
                              font=('Arial', 15), padx=15, pady=5, cursor='hand2', bd=2)
        btn_logout.pack(side='right', pady=15)
        # Add hover effect
        add_button_hover_effect(btn_logout, '#e74c3c', get_hover_color('#e74c3c'))

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

            # Lấy chi tiết giỏ hàng với thông tin sản phẩm từ database (bao gồm GiamGia)
            cursor.execute("""
                SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
                       sp.GiamGia
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

            # Tổ chức dữ liệu giỏ hàng - Áp dụng giảm giá
            for ma_sp, ten_sp, gia, mau_sac, size, so_luong, giam_gia in cart_items:
                # Tính giá sau giảm (GiamGia là int: 0, 10, 15,...)
                discount_percent = int(giam_gia) if giam_gia else 0
                original_price = float(gia)
                discounted_price = original_price * (1 - discount_percent / 100)
                thanh_tien = discounted_price * so_luong

                cart_key = f"{ma_sp}_{mau_sac}_{size}"
                cart_products[cart_key] = {
                    'product_id': ma_sp,
                    'name': ten_sp,
                    'price': discounted_price,  # Giá đã giảm
                    'color': mau_sac,
                    'size': size,
                    'quantity': so_luong,
                    'total': thanh_tien
                }
                total_amount += thanh_tien

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

        # Table header with better alignment
        header_frame_table = tk.Frame(main_frame, bg='#34495e', height=45)
        header_frame_table.pack(fill='x', pady=(0, 2))
        header_frame_table.pack_propagate(False)

        # Create header columns with consistent widths - Updated to include MaSP
        header_cols = [
            ("Mã SP", 0.1, 'center'),
            ("Tên sản phẩm", 0.22, 'w'),
            ("Màu sắc", 0.11, 'center'),
            ("Size", 0.08, 'center'),
            ("Số lượng", 0.11, 'center'),
            ("Đơn giá", 0.13, 'e'),
            ("Thành tiền", 0.13, 'e'),
            ("Hành động", 0.12, 'center')
        ]

        for i, (text, width_ratio, anchor) in enumerate(header_cols):
            header_label = tk.Label(header_frame_table, text=text, font=('Arial', 12, 'bold'),
                                   bg='#34495e', fg='white', anchor=anchor)
            header_label.place(relx=sum(col[1] for col in header_cols[:i]), rely=0,
                              relwidth=width_ratio, relheight=1)

        # Create scrollable items container
        items_scroll_frame = tk.Frame(main_frame, bg='#f8f9fa')
        items_scroll_frame.pack(fill='both', expand=True, pady=(0, 20))

        # Canvas and scrollbar for scrollable content
        items_canvas = tk.Canvas(items_scroll_frame, bg='#f8f9fa', highlightthickness=0)
        items_scrollbar = tk.Scrollbar(items_scroll_frame, orient='vertical', command=items_canvas.yview)
        items_container = tk.Frame(items_canvas, bg='#f8f9fa')

        # Pack scrollbar and canvas
        items_scrollbar.pack(side='right', fill='y')
        items_canvas.pack(side='left', fill='both', expand=True)

        # Create window in canvas with width binding
        canvas_window = items_canvas.create_window((0, 0), window=items_container, anchor='nw')

        # Update scroll region when content changes
        def update_scroll_region(event=None):
            items_canvas.configure(scrollregion=items_canvas.bbox('all'))

        items_container.bind('<Configure>', update_scroll_region)

        # Bind canvas width to container width
        def configure_canvas_width(event):
            canvas_width = event.width
            items_canvas.itemconfig(canvas_window, width=canvas_width)

        items_canvas.bind('<Configure>', configure_canvas_width)
        items_canvas.configure(yscrollcommand=items_scrollbar.set)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            items_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Only bind mousewheel when mouse is over the canvas
        items_canvas.bind("<Enter>", lambda e: items_canvas.bind_all("<MouseWheel>", on_mousewheel))
        items_canvas.bind("<Leave>", lambda e: items_canvas.unbind_all("<MouseWheel>"))

        # Function to remove item from cart - cập nhật để xóa từ database
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

        # Create product rows with consistent alignment
        for cart_key, product in cart_products.items():
            # Product row frame with consistent height
            product_frame = tk.Frame(items_container, bg='white', relief='solid', bd=1, height=65)
            product_frame.pack(fill='x', pady=1)
            product_frame.pack_propagate(False)

            # Create row data with same width ratios as headers
            row_data = [
                (product['product_id'], 0.1, 'center', 'text'),
                (product['name'], 0.22, 'w', 'text'),
                (product['color'], 0.11, 'center', 'text'),
                (product['size'], 0.08, 'center', 'text'),
                (str(product['quantity']), 0.11, 'center', 'text'),
                (f"{product['price']:,.0f} VNĐ", 0.13, 'e', 'text'),
                (f"{product['total']:,.0f} VNĐ", 0.13, 'e', 'price'),
                ("", 0.12, 'center', 'button')
            ]

            for i, (content, width_ratio, anchor, content_type) in enumerate(row_data):
                x_pos = sum(col[1] for col in row_data[:i])

                if content_type == 'button':
                    # Remove button with hover effect - Thu hẹp để align tốt hơn
                    btn_remove = tk.Button(product_frame, text="🗑️",
                                          command=lambda pid=product['product_id'], color=product['color'],
                                          size=product['size']: remove_from_cart_db(pid, color, size),
                                          bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                          cursor='hand2', relief='raised', width=4, height=1, bd=2)
                    # Thu hẹp button: 0.08 -> 0.06, center trong column 0.12
                    btn_remove.place(relx=x_pos + (width_ratio - 0.06)/2, rely=0.25,
                                    relwidth=0.06, relheight=0.5)
                    # Add hover effect
                    add_button_hover_effect(btn_remove, '#e74c3c', get_hover_color('#e74c3c'))
                elif content_type == 'price':
                    # Price labels with special formatting
                    price_label = tk.Label(product_frame, text=content, font=('Arial', 11, 'bold'),
                                          bg='white', anchor=anchor, fg='#e74c3c')
                    price_label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)
                else:
                    # Regular text labels
                    label = tk.Label(product_frame, text=content, font=('Arial', 11),
                                    bg='white', anchor=anchor)
                    if content_type == 'text' and i == 1:  # Product name - add wrapping
                        label.config(wraplength=int(width_ratio * 800))  # Approximate wrapping width
                    label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)

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
                             padx=20, pady=10, relief='raised', cursor='hand2', bd=2)
        btn_clear.pack(side='left')
        # Add hover effect
        add_button_hover_effect(btn_clear, '#e74c3c', get_hover_color('#e74c3c'))

        btn_view_invoice = tk.Button(button_frame, text="📄 Xem hóa đơn",
                               command=lambda: self.view_invoice_from_cart_db(username, role, cart_products, total_amount, on_back_callback),
                               bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=10, relief='raised', cursor='hand2', bd=2)
        btn_view_invoice.pack(side='right')
        # Add hover effect
        add_button_hover_effect(btn_view_invoice, '#f39c12', get_hover_color('#f39c12'))

    def clear_cart_db(self, username, role="buyer", on_back_callback=None):
        """Xóa toàn bộ giỏ hàng từ database - FIXED: không trả lại số lượng cho kho"""
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

            # FIXED: Simply delete cart items without affecting product inventory
            # Cart items are just "reserved" - they don't affect actual inventory until payment
            cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))

            conn.commit()

            messagebox.showinfo("Thành công", "Đã xóa tất cả sản phẩm khỏi giỏ hàng!")
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
