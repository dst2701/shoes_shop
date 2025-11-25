"""
Cart View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from config.database import get_db_connection
from utils.ui_effects import add_button_hover_effect, get_hover_color

class CartView:
    def __init__(self, root):
        self.root = root

    def show_cart(self, username, role="buyer", on_back_callback=None):
        """Show cart interface - Load from DATABASE giohangchuasanpham"""
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

        # Load cart data from DATABASE giohangchuasanpham
        cart_products = {}
        total_amount = 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get MaKH from username
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                tk.Label(main_frame, text="Không tìm thấy thông tin khách hàng",
                        font=('Arial', 18), bg='#f8f9fa', fg='#e74c3c').pack(expand=True)
                return

            ma_kh = result[0]

            # Load cart items from giohangchuasanpham
            cursor.execute("""
                SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong, sp.GiamGia
                FROM giohangchuasanpham ghsp
                JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
                WHERE ghsp.MaKH = %s
                ORDER BY sp.TenSP
            """, (ma_kh,))

            cart_items = cursor.fetchall()

            # Track if cart is empty for button states
            cart_is_empty = len(cart_items) == 0

            # Convert to cart_products format
            for ma_sp, ten_sp, gia, mau_sac, size, so_luong, giam_gia in cart_items:
                # Convert Decimal to float
                gia_float = float(gia)
                giam_gia_float = float(giam_gia) if giam_gia else 0.0

                price_after_discount = gia_float * (1 - giam_gia_float / 100.0)
                subtotal = price_after_discount * so_luong

                cart_key = f"{ma_sp}|{mau_sac}|{size}"
                cart_products[cart_key] = {
                    'product_id': ma_sp,
                    'name': ten_sp,
                    'price': price_after_discount,
                    'color': mau_sac,
                    'size': size,
                    'quantity': so_luong,
                    'discount': giam_gia_float,
                    'total': subtotal
                }
                total_amount += subtotal

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu giỏ hàng: {str(e)}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        print(f"Debug: Loaded cart from DATABASE for user {username}: {len(cart_products)} items, total: {total_amount:,.0f} VNĐ")

        # Cart title
        tk.Label(main_frame, text="Chi tiết giỏ hàng:", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa').pack(anchor='w', pady=(0, 10))

        # Show empty cart message if no items
        if cart_is_empty:
            empty_msg = tk.Label(main_frame,
                               text="🛒 Giỏ hàng trống\n\nThêm sản phẩm từ trang danh sách hoặc\nxem đơn hàng chưa thanh toán bên dưới",
                               font=('Arial', 14), bg='#f8f9fa', fg='#7f8c8d',
                               justify='center', pady=40)
            empty_msg.pack(fill='both', expand=True)

        # Table header with better alignment - Added checkbox column
        header_frame_table = tk.Frame(main_frame, bg='#34495e', height=45)
        header_frame_table.pack(fill='x', pady=(0, 2))
        header_frame_table.pack_propagate(False)

        # Create header columns with consistent widths - Updated to include Checkbox and MaSP
        header_cols = [
            ("☑", 0.05, 'center'),  # Checkbox column
            ("Mã SP", 0.09, 'center'),
            ("Tên sản phẩm", 0.20, 'w'),
            ("Màu sắc", 0.10, 'center'),
            ("Size", 0.08, 'center'),
            ("Số lượng", 0.10, 'center'),
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

        # Dictionary to store checkbox variables and selected items
        checkbox_vars = {}
        selected_total = tk.DoubleVar(value=0.0)

        # Function to update total based on selected items
        def update_selected_total():
            total = 0
            for cart_key, var in checkbox_vars.items():
                if var.get():
                    total += cart_products[cart_key]['total']
            selected_total.set(total)
            total_label.config(text=f"{total:,.0f} VNĐ")

        # Function to toggle row highlight
        def toggle_row_highlight(frame, var, cart_key):
            if var.get():
                frame.config(bg='#d4edda')  # Light green highlight
                # Update all child widgets background
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#d4edda')
            else:
                frame.config(bg='white')
                # Update all child widgets background
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='white')
            update_selected_total()

        # Function to remove item from cart - cập nhật để xóa từ database
        def remove_from_cart_db(product_id, color, size):
            """Xóa sản phẩm khỏi giỏ hàng database"""
            result = messagebox.askyesno("Xác nhận xóa",
                                       f"Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?")
            if not result:
                return

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Get MaKH
                cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
                result = cursor.fetchone()
                if not result:
                    return
                ma_kh = result[0]

                # Delete from giohangchuasanpham
                cursor.execute("""
                    DELETE FROM giohangchuasanpham 
                    WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
                """, (ma_kh, product_id, color, size))

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

            # Create checkbox variable for this row
            checkbox_var = tk.BooleanVar(value=False)
            checkbox_vars[cart_key] = checkbox_var

            # Create row data with same width ratios as headers (including checkbox)
            row_data = [
                ("", 0.05, 'center', 'checkbox'),  # Checkbox
                (product['product_id'], 0.09, 'center', 'text'),
                (product['name'], 0.20, 'w', 'text'),
                (product['color'], 0.10, 'center', 'text'),
                (product['size'], 0.08, 'center', 'text'),
                (str(product['quantity']), 0.10, 'center', 'text'),
                (f"{product['price']:,.0f} VNĐ", 0.13, 'e', 'text'),
                (f"{product['total']:,.0f} VNĐ", 0.13, 'e', 'price'),
                ("", 0.12, 'center', 'button')
            ]

            for i, (content, width_ratio, anchor, content_type) in enumerate(row_data):
                x_pos = sum(col[1] for col in row_data[:i])

                if content_type == 'checkbox':
                    # Checkbox
                    chk = tk.Checkbutton(product_frame, variable=checkbox_var, bg='white',
                                        command=lambda f=product_frame, v=checkbox_var, k=cart_key:
                                        toggle_row_highlight(f, v, k))
                    chk.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)
                elif content_type == 'button':
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
                    if content_type == 'text' and i == 2:  # Product name - add wrapping (index changed due to checkbox)
                        label.config(wraplength=int(width_ratio * 800))  # Approximate wrapping width
                    label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)

        # Total section - Now shows selected items total
        total_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='ridge', bd=2)
        total_frame.pack(fill='x', pady=(20, 0))

        total_container = tk.Frame(total_frame, bg='#ecf0f1')
        total_container.pack(fill='x', padx=20, pady=15)

        tk.Label(total_container, text="TỔNG TIỀN (Đã chọn):", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').pack(side='left')

        total_label = tk.Label(total_container, text="0 VNĐ", font=('Arial', 20, 'bold'),
                               bg='#ecf0f1', fg='#e74c3c')
        total_label.pack(side='right')

        # Action buttons frame
        button_frame = tk.Frame(main_frame, bg='#f8f9fa')
        button_frame.pack(fill='x', pady=(20, 0))

        # Determine button states based on cart content
        clear_btn_state = 'normal' if not cart_is_empty else 'disabled'
        create_order_btn_state = 'normal' if not cart_is_empty else 'disabled'
        clear_btn_bg = '#e74c3c' if not cart_is_empty else '#95a5a6'
        create_order_btn_bg = '#27ae60' if not cart_is_empty else '#95a5a6'

        btn_clear = tk.Button(button_frame, text="🗑️ Xóa tất cả",
                             command=lambda: self.clear_memory_cart(username, role, on_back_callback, memory_cart),
                             bg=clear_btn_bg, fg='white', font=('Arial', 12, 'bold'),
                             padx=20, pady=10, relief='raised', cursor='hand2' if not cart_is_empty else 'arrow',
                             bd=2, state=clear_btn_state)
        btn_clear.pack(side='left')
        if not cart_is_empty:
            add_button_hover_effect(btn_clear, '#e74c3c', get_hover_color('#e74c3c'))

        # NEW: Nút "Tạo đơn hàng" - Lưu vào database
        btn_create_order = tk.Button(button_frame, text="📦 Tạo đơn hàng",
                               command=lambda: self.create_order_from_db(username, role, cart_products,
                                                                         checkbox_vars, on_back_callback),
                               bg=create_order_btn_bg, fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=10, relief='raised', cursor='hand2' if not cart_is_empty else 'arrow',
                               bd=2, state=create_order_btn_state)
        btn_create_order.pack(side='right', padx=(5, 0))
        if not cart_is_empty:
            add_button_hover_effect(btn_create_order, '#27ae60', get_hover_color('#27ae60'))

        # NEW: Nút "Chưa thanh toán" - LUÔN ENABLED (không phụ thuộc cart)
        btn_unpaid_orders = tk.Button(button_frame, text="📋 Chưa thanh toán",
                               command=lambda: self.show_unpaid_orders(username, role, on_back_callback),
                               bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                               padx=20, pady=10, relief='raised', cursor='hand2', bd=2)
        btn_unpaid_orders.pack(side='right', padx=(5, 0))
        add_button_hover_effect(btn_unpaid_orders, '#f39c12', get_hover_color('#f39c12'))

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

            cursor.execute("SELECT MaDH FROM donhang WHERE MaKH = %s", (ma_kh,))
            result = cursor.fetchone()
            if not result:
                return

            ma_gh = result[0]

            # FIXED: Simply delete cart items without affecting product inventory
            # Cart items are just "reserved" - they don't affect actual inventory until payment
            cursor.execute("DELETE FROM sptrongdon WHERE MaDH = %s", (ma_gh,))

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

    def view_invoice_from_cart_db_selected(self, username, role, cart_products, checkbox_vars, on_back_callback):
        """Xem hóa đơn từ giỏ hàng - CHỈ các sản phẩm được chọn"""
        # Filter only selected products
        selected_products = {}
        selected_total = 0

        for cart_key, var in checkbox_vars.items():
            if var.get():  # Only include checked items
                product = cart_products[cart_key]
                # Use cart_key as unique identifier (includes color and size)
                selected_products[cart_key] = {
                    'product_id': product['product_id'],
                    'name': product['name'],
                    'price': product['price'],
                    'color': product['color'],
                    'size': product['size'],
                    'quantity': product['quantity'],
                    'total': product['total']
                }
                selected_total += product['total']

        if not selected_products:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một sản phẩm để xem hóa đơn!")
            return

        # Import và sử dụng InvoiceView với selected products
        from views.invoice_view import InvoiceView
        invoice_view = InvoiceView(self.root)
        invoice_view.show_invoice_page(username, role, selected_products, selected_total,
                                      lambda: self.show_cart(username, role, on_back_callback))

    def set_logout_callback(self, callback):
        """Set logout callback"""
        self.logout_callback = callback

    def create_order_from_db(self, username, role, cart_products, checkbox_vars, on_back_callback):
        """Tạo đơn hàng mới từ giỏ hàng database - Lưu vào donhang + sptrongdon"""
        # Get selected products
        selected_products = {}
        for cart_key, var in checkbox_vars.items():
            if var.get():  # Only checked items
                product = cart_products[cart_key]
                selected_products[cart_key] = product

        if not selected_products:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một sản phẩm để tạo đơn hàng!")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 1. Get MaKH
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
                return
            ma_kh = result[0]

            # 2. KIỂM TRA SỐ LƯỢNG KHẢ DỤNG - Logic mới
            # Tính toán số lượng khả dụng sau khi trừ đi các đơn chờ thanh toán
            insufficient_products = []

            # Group selected products by MaSP (vì tồn kho không phân biệt màu/size)
            products_by_masp = {}
            for cart_key, item in selected_products.items():
                ma_sp = item['product_id']
                if ma_sp not in products_by_masp:
                    products_by_masp[ma_sp] = {
                        'name': item['name'],
                        'requested_quantity': 0,
                        'items': []
                    }
                products_by_masp[ma_sp]['requested_quantity'] += item['quantity']
                products_by_masp[ma_sp]['items'].append(item)

            # Check each product
            for ma_sp, product_info in products_by_masp.items():
                # Get stock quantity
                cursor.execute("SELECT SoLuong, TenSP FROM sanpham WHERE MaSP = %s", (ma_sp,))
                stock_result = cursor.fetchone()
                if not stock_result:
                    messagebox.showerror("Lỗi", f"Không tìm thấy sản phẩm {ma_sp}!")
                    return

                stock_quantity = stock_result[0]
                product_name = stock_result[1]

                # Get total quantity in pending orders (sptrongdon)
                cursor.execute("""
                    SELECT COALESCE(SUM(SoLuong), 0) 
                    FROM sptrongdon 
                    WHERE MaSP = %s
                """, (ma_sp,))
                pending_result = cursor.fetchone()
                total_in_pending = pending_result[0] if pending_result else 0

                # Calculate available quantity
                available_quantity = stock_quantity - total_in_pending
                requested_quantity = product_info['requested_quantity']

                # Check if insufficient
                if requested_quantity > available_quantity:
                    insufficient_products.append({
                        'ma_sp': ma_sp,
                        'name': product_name,
                        'requested': requested_quantity,
                        'available': available_quantity,
                        'stock': stock_quantity,
                        'pending': total_in_pending
                    })

            # If any product is insufficient, show error and abort
            if insufficient_products:
                error_msg = "⚠️ KHÔNG THỂ TẠO ĐƠN HÀNG!\n\n"
                error_msg += "Một số sản phẩm không đủ số lượng:\n\n"

                for i, prod in enumerate(insufficient_products, 1):
                    error_msg += f"{i}. {prod['name']} (Mã: {prod['ma_sp']})\n"
                    error_msg += f"   • Bạn muốn: {prod['requested']} sản phẩm\n"
                    error_msg += f"   • Số lượng khả dụng: {prod['available']} sản phẩm\n"
                    error_msg += f"   • Tồn kho: {prod['stock']} | Đang trong đơn chờ: {prod['pending']}\n\n"

                error_msg += "Vui lòng:\n"
                error_msg += "• Giảm số lượng sản phẩm trong giỏ hàng\n"
                error_msg += "• Hoặc xóa sản phẩm không đủ hàng\n"
                error_msg += "• Sau đó thử tạo đơn lại"

                messagebox.showerror("Không đủ hàng", error_msg)
                return

            # 3. Generate new MaDH (GHxxx)
            cursor.execute("SELECT MAX(CAST(SUBSTRING(MaDH, 3) AS UNSIGNED)) FROM donhang")
            max_result = cursor.fetchone()
            max_id = max_result[0] if max_result[0] else 0
            ma_dh = f"GH{max_id + 1:03d}"

            # 4. Insert into donhang with current datetime
            ngay_lap = datetime.now()
            cursor.execute("""
                INSERT INTO donhang (MaDH, MaKH, NgayLap)
                VALUES (%s, %s, %s)
            """, (ma_dh, ma_kh, ngay_lap))

            # 5. Insert selected products into sptrongdon
            for cart_key, item in selected_products.items():
                cursor.execute("""
                    INSERT INTO sptrongdon (MaDH, MaSP, MauSac, Size, SoLuong)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ma_dh, item['product_id'], item['color'], item['size'], item['quantity']))

            conn.commit()

            # 6. Remove selected items from giohangchuasanpham database
            for cart_key, item in selected_products.items():
                cursor.execute("""
                    DELETE FROM giohangchuasanpham 
                    WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
                """, (ma_kh, item['product_id'], item['color'], item['size']))

            conn.commit()

            messagebox.showinfo("Thành công",
                              f"✅ Đã tạo đơn hàng {ma_dh}!\n\n"
                              f"📅 Thời gian: {ngay_lap.strftime('%d/%m/%Y %H:%M')}\n"
                              f"📦 Số sản phẩm: {len(selected_products)}\n\n"
                              f"💡 Bạn có thể xem và thanh toán đơn này tại 'Chưa thanh toán'")

            # Refresh cart view
            self.show_cart(username, role, on_back_callback)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo đơn hàng: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_unpaid_orders(self, username, role, on_back_callback):
        """Hiển thị danh sách đơn hàng chưa thanh toán"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Đơn hàng chưa thanh toán")
        self.root.geometry("1200x700")

        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        tk.Label(header_container, text="ĐƠN HÀNG CHƯA THANH TOÁN", font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        btn_back = tk.Button(header_container, text="← Quay lại",
                            command=lambda: on_back_callback(role, username) if on_back_callback else None,
                            bg='#f39c12', fg='white', relief='raised',
                            font=('Arial', 12, 'bold'), padx=15, pady=5, cursor='hand2', bd=2)
        btn_back.pack(side='right', pady=15)
        add_button_hover_effect(btn_back, '#f39c12', get_hover_color('#f39c12'))

        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get MaKH
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                tk.Label(main_frame, text="Không tìm thấy thông tin khách hàng",
                        font=('Arial', 18), bg='#f8f9fa', fg='#e74c3c').pack(expand=True)
                return
            ma_kh = result[0]

            # Get unpaid orders (orders that are NOT in hoadon table)
            cursor.execute("""
                SELECT dh.MaDH, dh.NgayLap
                FROM donhang dh
                WHERE dh.MaKH = %s
                  AND dh.MaDH NOT IN (SELECT DISTINCT MaHD FROM hoadon WHERE MaKH = %s)
                ORDER BY dh.NgayLap DESC
            """, (ma_kh, ma_kh))

            unpaid_orders = cursor.fetchall()

            if not unpaid_orders:
                tk.Label(main_frame, text="Không có đơn hàng chưa thanh toán\n\nTạo đơn hàng từ giỏ hàng tạm để bắt đầu!",
                        font=('Arial', 18), bg='#f8f9fa', fg='#6c757d',
                        justify='center').pack(expand=True)
                return

            # Display orders
            tk.Label(main_frame, text=f"Có {len(unpaid_orders)} đơn hàng chưa thanh toán:",
                    font=('Arial', 16, 'bold'), bg='#f8f9fa').pack(anchor='w', pady=(0, 10))

            # Create scrollable frame for orders
            canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
            scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Display each order
            for ma_dh, ngay_lap in unpaid_orders:
                # Get order details
                cursor.execute("""
                    SELECT sp.MaSP, sp.TenSP, sp.Gia, st.MauSac, st.Size, st.SoLuong, sp.GiamGia
                    FROM sptrongdon st
                    JOIN sanpham sp ON st.MaSP = sp.MaSP
                    WHERE st.MaDH = %s
                """, (ma_dh,))

                order_items = cursor.fetchall()

                # Calculate total - Convert Decimal to float to avoid errors
                total = 0
                for _, _, gia, _, _, so_luong, giam_gia in order_items:
                    gia_float = float(gia)
                    giam_gia_float = float(giam_gia) if giam_gia else 0.0
                    price_after_discount = gia_float * (1 - giam_gia_float / 100.0)
                    total += price_after_discount * so_luong

                # Order card
                order_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', bd=2)
                order_frame.pack(fill='x', pady=5, padx=5)

                # Order header
                header = tk.Frame(order_frame, bg='#3498db', height=40)
                header.pack(fill='x')

                tk.Label(header, text=f"📦 {ma_dh}", font=('Arial', 14, 'bold'),
                        bg='#3498db', fg='white').pack(side='left', padx=10, pady=5)

                ngay_str = ngay_lap.strftime('%d/%m/%Y %H:%M') if isinstance(ngay_lap, datetime) else str(ngay_lap)
                tk.Label(header, text=f"🕒 {ngay_str}", font=('Arial', 12),
                        bg='#3498db', fg='white').pack(side='left', padx=10)

                tk.Label(header, text=f"💰 {total:,.0f} VNĐ", font=('Arial', 12, 'bold'),
                        bg='#3498db', fg='white').pack(side='left', padx=10)

                # Order items summary
                items_frame = tk.Frame(order_frame, bg='white')
                items_frame.pack(fill='x', padx=10, pady=5)

                tk.Label(items_frame, text=f"Số lượng sản phẩm: {len(order_items)}",
                        font=('Arial', 11), bg='white').pack(anchor='w')

                # Buttons
                btn_frame = tk.Frame(order_frame, bg='white')
                btn_frame.pack(fill='x', padx=10, pady=10)

                btn_pay = tk.Button(btn_frame, text="💳 Thanh toán",
                                   command=lambda m=ma_dh: self.pay_order(username, role, m, on_back_callback),
                                   bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                                   padx=15, pady=5, cursor='hand2')
                btn_pay.pack(side='right', padx=5)
                add_button_hover_effect(btn_pay, '#27ae60', get_hover_color('#27ae60'))

                btn_delete = tk.Button(btn_frame, text="🗑️ Xóa",
                                      command=lambda m=ma_dh: self.delete_order(username, role, m, on_back_callback),
                                      bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                      padx=15, pady=5, cursor='hand2')
                btn_delete.pack(side='right', padx=5)
                add_button_hover_effect(btn_delete, '#e74c3c', get_hover_color('#e74c3c'))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải đơn hàng: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def pay_order(self, username, role, ma_dh, on_back_callback):
        """Thanh toán đơn hàng"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get order details
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, st.MauSac, st.Size, st.SoLuong, sp.GiamGia
                FROM sptrongdon st
                JOIN sanpham sp ON st.MaSP = sp.MaSP
                WHERE st.MaDH = %s
            """, (ma_dh,))

            order_items = cursor.fetchall()

            # Convert to cart_products format for invoice
            cart_products = {}
            total = 0
            for ma_sp, ten_sp, gia, mau_sac, size, so_luong, giam_gia in order_items:
                # Convert Decimal to float to avoid calculation errors
                gia_float = float(gia)
                giam_gia_float = float(giam_gia) if giam_gia else 0.0

                price_after_discount = gia_float * (1 - giam_gia_float / 100.0)
                subtotal = price_after_discount * so_luong

                cart_key = f"{ma_sp}|{mau_sac}|{size}"
                cart_products[cart_key] = {
                    'product_id': ma_sp,
                    'name': ten_sp,
                    'price': price_after_discount,
                    'color': mau_sac,
                    'size': size,
                    'quantity': so_luong,
                    'discount': giam_gia_float,
                    'total': subtotal
                }
                total += subtotal

            # Show invoice view for payment
            from views.invoice_view import InvoiceView
            invoice_view = InvoiceView(self.root)
            invoice_view.show_invoice_page(username, role, cart_products, total,
                                          lambda: self.show_unpaid_orders(username, role, on_back_callback),
                                          ma_dh_to_delete=ma_dh)  # Pass MaDH to delete after payment

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thanh toán: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_order(self, username, role, ma_dh, on_back_callback):
        """Xóa đơn hàng chưa thanh toán"""
        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa đơn hàng {ma_dh}?")
        if not result:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Delete from sptrongdon first (foreign key constraint)
            cursor.execute("DELETE FROM sptrongdon WHERE MaDH = %s", (ma_dh,))

            # Delete from donhang
            cursor.execute("DELETE FROM donhang WHERE MaDH = %s", (ma_dh,))

            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa đơn hàng {ma_dh}!")

            # Refresh
            self.show_unpaid_orders(username, role, on_back_callback)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa đơn hàng: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

