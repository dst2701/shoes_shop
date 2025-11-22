"""
Invoice View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from config.database import get_db_connection
from datetime import datetime
from utils.ui_effects import add_button_hover_effect, get_hover_color

class InvoiceView:
    def __init__(self, root):
        self.root = root

    def show_invoice_page(self, username, role, cart_products, total_amount, on_back_callback=None, ma_dh_to_delete=None):
        """Show invoice page - from main.py
        ma_dh_to_delete: Mã đơn hàng cần xóa sau khi thanh toán (nếu thanh toán từ đơn chưa thanh toán)
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Hóa đơn chi tiết")
        self.root.geometry("1200x800")

        # Get customer info from database
        customer_address = "Chưa cập nhật địa chỉ"
        customer_phone = "Chưa cập nhật số điện thoại"

        # Display order ID instead of invoice ID
        display_order_id = ma_dh_to_delete if ma_dh_to_delete else "Đang tạo..."

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get customer address and phone
            cursor.execute("SELECT DiaChi, SDT, MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if result:
                customer_address = result[0] if result[0] else "Chưa cập nhật địa chỉ"
                customer_phone = result[1] if result[1] else "Chưa cập nhật số điện thoại"
                ma_kh = result[2]

        except Exception as e:
            print(f"Error getting customer info: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Header frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        # Add order ID to header (GHxxx instead of HDxxx)
        header_title = f"📄 ĐƠN HÀNG CHI TIẾT - {display_order_id}"

        tk.Label(header_container, text=header_title, font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        # Back button
        btn_back = tk.Button(header_container, text="← Quay lại giỏ hàng",
                            command=lambda: on_back_callback() if on_back_callback else None,
                            bg='#95a5a6', fg='white', relief='raised',
                            font=('Arial', 12), padx=15, pady=8, cursor='hand2', bd=2)
        btn_back.pack(side='right', pady=15)
        # Add hover effect
        add_button_hover_effect(btn_back, '#95a5a6', get_hover_color('#95a5a6'))

        # Main content frame
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Invoice header info
        info_frame = tk.Frame(main_frame, bg='white', relief='ridge', bd=2)
        info_frame.pack(fill='x', pady=(0, 20))

        info_container = tk.Frame(info_frame, bg='white')
        info_container.pack(fill='x', padx=20, pady=15)

        # Shop info
        tk.Label(info_container, text="SHOP SHOES", font=('Arial', 18, 'bold'),
                 bg='white', fg='#2c3e50').pack(anchor='w')
        tk.Label(info_container, text=f"Địa chỉ: {customer_address}", font=('Arial', 12),
                 bg='white', fg='#7f8c8d').pack(anchor='w')
        tk.Label(info_container, text=f"Điện thoại: {customer_phone}", font=('Arial', 12),
                 bg='white', fg='#7f8c8d').pack(anchor='w')

        # Divider
        tk.Frame(info_container, height=1, bg='#bdc3c7').pack(fill='x', pady=10)

        # Invoice info
        current_time = datetime.now()

        invoice_info_frame = tk.Frame(info_container, bg='white')
        invoice_info_frame.pack(fill='x')

        # Left column - Invoice details
        left_info = tk.Frame(invoice_info_frame, bg='white')
        left_info.pack(side='left', fill='x', expand=True)

        # Display order ID (GHxxx from donhang table)
        tk.Label(left_info, text=f"Mã đơn hàng: {display_order_id}",
                 font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')

        tk.Label(left_info, text=f"Ngày lập: {current_time.strftime('%d/%m/%Y %H:%M')}",
                 font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')
        tk.Label(left_info, text=f"Khách hàng: {username}",
                 font=('Arial', 12), bg='white', fg='#7f8c8d').pack(anchor='w')

        # Right column - Status
        right_info = tk.Frame(invoice_info_frame, bg='white')
        right_info.pack(side='right')

        tk.Label(right_info, text="TRẠNG THÁI: CHƯA THANH TOÁN",
                 font=('Arial', 12, 'bold'), bg='white', fg='#e74c3c').pack()

        # Products table
        products_frame = tk.Frame(main_frame, bg='white')
        products_frame.pack(fill='both', expand=True)

        tk.Label(products_frame, text="Chi tiết sản phẩm:", font=('Arial', 16, 'bold'),
                 bg='white', fg='#2c3e50').pack(anchor='w', pady=(0, 10))

        # Create scrollable table for products with better alignment including size and color
        table_scroll_frame = tk.Frame(products_frame, bg='white')
        table_scroll_frame.pack(fill='both', expand=True)

        # Canvas and scrollbar for scrollable table
        table_canvas = tk.Canvas(table_scroll_frame, bg='white', highlightthickness=0)
        table_scrollbar = tk.Scrollbar(table_scroll_frame, orient='vertical', command=table_canvas.yview)
        table_frame = tk.Frame(table_canvas, bg='white')

        # Pack scrollbar and canvas
        table_scrollbar.pack(side='right', fill='y')
        table_canvas.pack(side='left', fill='both', expand=True)

        # Create window in canvas with width binding
        canvas_window = table_canvas.create_window((0, 0), window=table_frame, anchor='nw')

        # Update scroll region when content changes
        def update_scroll_region(event=None):
            table_canvas.configure(scrollregion=table_canvas.bbox('all'))

        table_frame.bind('<Configure>', update_scroll_region)

        # Bind canvas width to container width
        def configure_canvas_width(event):
            canvas_width = event.width
            table_canvas.itemconfig(canvas_window, width=canvas_width)

        table_canvas.bind('<Configure>', configure_canvas_width)
        table_canvas.configure(yscrollcommand=table_scrollbar.set)

        # Mouse wheel scrolling
        def on_invoice_mousewheel(event):
            table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Only bind mousewheel when mouse is over the canvas
        table_canvas.bind("<Enter>", lambda e: table_canvas.bind_all("<MouseWheel>", on_invoice_mousewheel))
        table_canvas.bind("<Leave>", lambda e: table_canvas.unbind_all("<MouseWheel>"))

        # Table header with size and color columns
        header_table = tk.Frame(table_frame, bg='#34495e', height=45)
        header_table.pack(fill='x', pady=(0, 2))
        header_table.pack_propagate(False)

        # Define header columns with size and color included - Thu hẹp để fit content
        header_cols = [
            ("STT", 0.05, 'center'),
            ("Mã SP", 0.09, 'center'),
            ("Tên sản phẩm", 0.27, 'w'),
            ("Màu sắc", 0.09, 'center'),
            ("Size", 0.06, 'center'),
            ("Số lượng", 0.09, 'center'),
            ("Đơn giá", 0.16, 'e'),
            ("Thành tiền", 0.16, 'e')
        ]

        for i, (text, width_ratio, anchor) in enumerate(header_cols):
            header_label = tk.Label(header_table, text=text, font=('Arial', 12, 'bold'),
                                   bg='#34495e', fg='white', anchor=anchor)
            header_label.place(relx=sum(col[1] for col in header_cols[:i]), rely=0,
                              relwidth=width_ratio, relheight=1)

        # Use cart_products directly - cart_products now contains selected items only
        # cart_products format from cart_view:
        # {cart_key: {'product_id': ..., 'name': ..., 'price': ..., 'color': ..., 'size': ..., 'quantity': ..., 'total': ...}}

        # Group products by product_id, name, size, and color (should already be unique by cart_key)
        grouped_products = {}

        for cart_key, product in cart_products.items():
            # cart_key is already unique (MaSP_color_size), so we can use it directly
            # But we need to structure it for display
            grouped_products[cart_key] = {
                'ma_sp': product.get('product_id', ''),
                'name': product.get('name', ''),
                'price': product.get('price', 0),
                'quantity': product.get('quantity', 0),
                'color': product.get('color', ''),
                'size': product.get('size', ''),
                'total': product.get('total', 0)
            }

        # Product rows with size and color
        stt = 1
        for key, product in grouped_products.items():
            # Product row frame with consistent height
            row_frame = tk.Frame(table_frame, bg='white', relief='solid', bd=1, height=50)
            row_frame.pack(fill='x', pady=1)
            row_frame.pack_propagate(False)

            # Create row data with EXACT SAME width ratios as headers - CRITICAL FOR ALIGNMENT!
            row_data = [
                (str(stt), 0.05, 'center', 'text'),           # Match header: 0.05
                (product['ma_sp'], 0.09, 'center', 'text'),   # Match header: 0.09
                (product['name'], 0.27, 'w', 'name'),         # Match header: 0.27
                (product['color'], 0.09, 'center', 'text'),   # Match header: 0.09
                (str(product['size']), 0.06, 'center', 'text'), # Match header: 0.06
                (str(product['quantity']), 0.09, 'center', 'text'), # Match header: 0.09
                (f"{product['price']:,.0f}", 0.16, 'e', 'text'),    # Match header: 0.16
                (f"{product['total']:,.0f}", 0.16, 'e', 'price')    # Match header: 0.16
            ]

            for i, (content, width_ratio, anchor, content_type) in enumerate(row_data):
                x_pos = sum(col[1] for col in row_data[:i])

                if content_type == 'price':
                    # Price labels with special formatting
                    price_label = tk.Label(row_frame, text=content, font=('Arial', 11, 'bold'),
                                          bg='white', anchor=anchor, fg='#27ae60')
                    price_label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)
                elif content_type == 'name':
                    # Product name with text wrapping
                    name_label = tk.Label(row_frame, text=content, font=('Arial', 11),
                                         bg='white', anchor=anchor, wraplength=int(width_ratio * 1000))
                    name_label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)
                else:
                    # Regular text labels
                    label = tk.Label(row_frame, text=content, font=('Arial', 11),
                                    bg='white', anchor=anchor)
                    label.place(relx=x_pos, rely=0, relwidth=width_ratio, relheight=1)

            stt += 1

        # Total frame
        total_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='ridge', bd=2)
        total_frame.pack(fill='x', pady=(20, 0))

        total_container = tk.Frame(total_frame, bg='#ecf0f1')
        total_container.pack(fill='x', padx=20, pady=15)

        tk.Label(total_container, text="TỔNG TIỀN THANH TOÁN:", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').pack(side='left')

        tk.Label(total_container, text=f"{total_amount:,.0f} VNĐ", font=('Arial', 20, 'bold'),
                 bg='#ecf0f1', fg='#e74c3c').pack(side='right')

        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg='white')
        action_frame.pack(fill='x', pady=(20, 0))

        # Payment button with enhanced hover effect
        btn_payment = tk.Button(action_frame, text="💳 THANH TOÁN",
                               command=lambda: self.process_payment_main(username, role, cart_products, total_amount, on_back_callback, ma_dh_to_delete),
                               bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                               relief='raised', padx=40, pady=12, cursor='hand2', bd=3)
        btn_payment.pack(side='right')
        # Add hover effect with extra prominence for payment button
        add_button_hover_effect(btn_payment, '#27ae60', get_hover_color('#27ae60'))

        # Print button
        btn_print = tk.Button(action_frame, text="🖨️ In hóa đơn",
                             command=lambda: messagebox.showinfo("Thông báo", "Chức năng in hóa đơn sẽ được cập nhật!"),
                             bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                             relief='raised', padx=20, pady=10, cursor='hand2', bd=2)
        btn_print.pack(side='left')
        # Add hover effect
        add_button_hover_effect(btn_print, '#3498db', get_hover_color('#3498db'))

    def process_payment_main(self, username, role, cart_products, total_amount, on_back_callback, ma_dh_to_delete=None):
        """Process payment from invoice page - from main.py
        ma_dh_to_delete: Mã đơn hàng cần xóa sau khi thanh toán thành công
        """
        if not cart_products:
            messagebox.showwarning("Cảnh báo", "Không có sản phẩm để thanh toán!")
            return

        result = messagebox.askyesno("Xác nhận thanh toán",
                                   f"Tổng tiền: {total_amount:,.0f} VNĐ\n\n"
                                   f"Bạn có muốn tiến hành thanh toán?")
        if not result:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Lấy mã khách hàng
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
                return

            ma_kh = result[0]

            # Tạo mã hóa đơn mới
            cursor.execute(
                "SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'"
            )
            result = cursor.fetchone()
            next_number = ((result[0] or 0) + 1) if result else 1
            ma_hd = f"HD{next_number:03d}"

            # Tạo hóa đơn mới (chỉ lưu ngày)
            current_date = datetime.now().date()
            cursor.execute(
                """
                INSERT INTO hoadon (MaHD, MaKH, NgayLap)
                VALUES (%s, %s, %s)
                """,
                (ma_hd, ma_kh, current_date)
            )

            # Use cart_products passed from cart_view (already selected items only)
            # Convert cart_products to grouped_items format
            grouped_items = {}
            for cart_key, product in cart_products.items():
                grouped_items[cart_key] = {
                    'ma_sp': product.get('product_id', ''),
                    'ten_sp': product.get('name', ''),
                    'price': product.get('price', 0),
                    'quantity': product.get('quantity', 0),
                    'color': product.get('color', ''),
                    'size': product.get('size', ''),
                    'total': product.get('total', 0)
                }

            # Insert grouped items into cthoadon and decrease product quantities
            for item in grouped_items.values():
                    # First check current stock before processing
                    cursor.execute("SELECT SoLuong FROM sanpham WHERE MaSP = %s", (item['ma_sp'],))
                    stock_result = cursor.fetchone()
                    current_stock = stock_result[0] if stock_result else 0

                    # Validate stock availability
                    if current_stock < item['quantity']:
                        conn.rollback()
                        messagebox.showerror("Lỗi",
                                           f"Không đủ hàng trong kho!\n"
                                           f"Sản phẩm: {item['ten_sp']}\n"
                                           f"Số lượng yêu cầu: {item['quantity']}\n"
                                           f"Số lượng còn lại: {current_stock}")
                        return

                    cursor.execute(
                        """
                        INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (ma_hd, item['ma_sp'], item['ten_sp'], item['color'], item['size'],
                         item['quantity'], item['price'], item['total'])
                    )

                    # Decrease product quantity in sanpham table with explicit validation
                    cursor.execute(
                        """
                        UPDATE sanpham 
                        SET SoLuong = GREATEST(0, SoLuong - %s)
                        WHERE MaSP = %s
                        """,
                        (item['quantity'], item['ma_sp'])
                    )

                    # Double-check that the update succeeded and quantity is not negative
                    cursor.execute("SELECT SoLuong FROM sanpham WHERE MaSP = %s", (item['ma_sp'],))
                    new_stock_result = cursor.fetchone()
                    new_stock = new_stock_result[0] if new_stock_result else 0

                    if new_stock < 0:
                        # This should not happen with GREATEST function, but extra safety
                        conn.rollback()
                        messagebox.showerror("Lỗi",
                                           f"Lỗi hệ thống: Số lượng sản phẩm bị âm!\n"
                                           f"Sản phẩm: {item['ten_sp']}")
                        return

            # NEW: Xóa đơn hàng nếu thanh toán từ "Chưa thanh toán"
            if ma_dh_to_delete:
                # Delete all items in order
                cursor.execute("DELETE FROM sptrongdon WHERE MaDH = %s", (ma_dh_to_delete,))
                # Delete order itself
                cursor.execute("DELETE FROM donhang WHERE MaDH = %s", (ma_dh_to_delete,))
                print(f"✅ Deleted order {ma_dh_to_delete} after payment")

            conn.commit()

            messagebox.showinfo("Thành công",
                              f"Thanh toán thành công!\n"
                              f"Mã hóa đơn: {ma_hd}\n"
                              f"Cảm ơn bạn đã mua hàng!")

            # Return to product page
            if hasattr(self, 'show_products_callback') and self.show_products_callback:
                self.show_products_callback(role, username)
            elif on_back_callback:
                on_back_callback()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xử lý thanh toán: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def set_show_products_callback(self, callback):
        """Set callback to return to products page"""
        self.show_products_callback = callback
