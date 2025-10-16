"""
Invoice View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from config.database import get_db_connection
from datetime import datetime

class InvoiceView:
    def __init__(self, root):
        self.root = root

    def show_invoice_page(self, username, role, cart_products, total_amount, on_back_callback=None):
        """Show invoice page - from main.py"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Hóa đơn chi tiết")
        self.root.geometry("1000x800")

        # Get customer info from database
        customer_address = "Chưa cập nhật địa chỉ"
        customer_phone = "Chưa cập nhật số điện thoại"
        invoice_id = ""

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

                # Generate preview invoice ID
                cursor.execute(
                    "SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'"
                )
                result = cursor.fetchone()
                next_number = ((result[0] or 0) + 1) if result else 1
                invoice_id = f"HD{next_number:03d}"

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

        # Add invoice ID to header
        header_title = f"📄 HÓA ĐƠN CHI TIẾT"
        if invoice_id:
            header_title += f" - {invoice_id}"

        tk.Label(header_container, text=header_title, font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        # Back button
        btn_back = tk.Button(header_container, text="← Quay lại giỏ hàng",
                            command=lambda: on_back_callback() if on_back_callback else None,
                            bg='#95a5a6', fg='white', relief='flat',
                            font=('Arial', 12), padx=15, pady=8, cursor='hand2')
        btn_back.pack(side='right', pady=15)

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

        # Display invoice ID if available
        if invoice_id:
            tk.Label(left_info, text=f"Mã hóa đơn: {invoice_id}",
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

        # Create table for products with better alignment
        table_frame = tk.Frame(products_frame, bg='white')
        table_frame.pack(fill='both', expand=True)

        # Table header with consistent layout
        header_table = tk.Frame(table_frame, bg='#34495e', height=45)
        header_table.pack(fill='x', pady=(0, 2))
        header_table.pack_propagate(False)

        # Define header columns with consistent widths
        header_cols = [
            ("STT", 0.08, 'center'),
            ("Mã SP", 0.12, 'center'),
            ("Tên sản phẩm", 0.35, 'w'),
            ("Số lượng", 0.12, 'center'),
            ("Đơn giá", 0.165, 'e'),
            ("Thành tiền", 0.165, 'e')
        ]

        for i, (text, width_ratio, anchor) in enumerate(header_cols):
            header_label = tk.Label(header_table, text=text, font=('Arial', 12, 'bold'),
                                   bg='#34495e', fg='white', anchor=anchor)
            header_label.place(relx=sum(col[1] for col in header_cols[:i]), rely=0,
                              relwidth=width_ratio, relheight=1)

        # Product rows with consistent alignment
        stt = 1
        for ma_sp, product in cart_products.items():
            # Product row frame with consistent height
            row_frame = tk.Frame(table_frame, bg='white', relief='solid', bd=1, height=50)
            row_frame.pack(fill='x', pady=1)
            row_frame.pack_propagate(False)

            # Create row data with same width ratios as headers
            row_data = [
                (str(stt), 0.08, 'center', 'text'),
                (ma_sp, 0.12, 'center', 'text'),
                (product['name'], 0.35, 'w', 'name'),
                (str(product['quantity']), 0.12, 'center', 'text'),
                (f"{product['price']:,.0f}", 0.165, 'e', 'text'),
                (f"{product['total']:,.0f}", 0.165, 'e', 'price')
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
                                         bg='white', anchor=anchor, wraplength=int(width_ratio * 700))
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

        # Payment button
        btn_payment = tk.Button(action_frame, text="💳 THANH TOÁN",
                               command=lambda: self.process_payment_main(username, role, cart_products, total_amount, on_back_callback),
                               bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                               relief='flat', padx=40, pady=12, cursor='hand2')
        btn_payment.pack(side='right')

        # Print button
        btn_print = tk.Button(action_frame, text="🖨️ In hóa đơn",
                             command=lambda: messagebox.showinfo("Thông báo", "Chức năng in hóa đơn sẽ được cập nhật!"),
                             bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                             relief='flat', padx=20, pady=10, cursor='hand2')
        btn_print.pack(side='left')

    def process_payment_main(self, username, role, cart_products, total_amount, on_back_callback):
        """Process payment from invoice page - from main.py"""
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

            # Tạo hóa đơn mới
            current_date = datetime.now().date()
            cursor.execute(
                """
                INSERT INTO hoadon (MaHD, MaKH, NgayLap)
                VALUES (%s, %s, %s)
                """,
                (ma_hd, ma_kh, current_date)
            )

            # Thêm chi tiết hóa đơn
            for ma_sp, product in cart_products.items():
                cursor.execute(
                    """
                    INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (ma_hd, ma_sp, product['name'], 'Mặc định', 'Mặc định',
                     product['quantity'], product['price'], product['total'])
                )

            # Clear cart from database after payment
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()
            if gh_result:
                ma_gh = gh_result[0]
                cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))

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
