"""
Giao diện hóa đơn chi tiết - hiển thị thông tin chi tiết hóa đơn từ giỏ hàng
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from datetime import datetime

class InvoiceView(BaseView):
    def __init__(self, username=None, cart_data=None, parent_view=None):
        super().__init__("Shop Shoes - Hóa đơn chi tiết", "1000x800")
        self.username = username
        self.cart_data = cart_data or {}
        self.parent_view = parent_view
        self.ma_kh = None
        self.ma_hd = None
        self.customer_info = {}

        # Lấy thông tin khách hàng và tạo mã hóa đơn trước khi setup UI
        self.get_customer_info()
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện hóa đơn"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        # Hiển thị mã hóa đơn trong header
        header_text = f"📄 HÓA ĐƠN CHI TIẾT - {self.ma_hd}" if self.ma_hd else "📄 HÓA ĐƠN CHI TIẾT"
        tk.Label(header_container, text=header_text, font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        # Back button
        btn_back = tk.Button(header_container, text="← Quay lại giỏ hàng", command=self.back_to_cart,
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
        tk.Label(info_container, text="Địa chỉ: 123 Đường ABC, Quận XYZ, TP.HCM", font=('Arial', 12),
                 bg='white', fg='#7f8c8d').pack(anchor='w')
        tk.Label(info_container, text="Điện thoại: 0123.456.789", font=('Arial', 12),
                 bg='white', fg='#7f8c8d').pack(anchor='w')

        # Divider
        tk.Frame(info_container, height=1, bg='#bdc3c7').pack(fill='x', pady=10)

        # Invoice info
        invoice_info_frame = tk.Frame(info_container, bg='white')
        invoice_info_frame.pack(fill='x')

        # Left column - Invoice details
        left_info = tk.Frame(invoice_info_frame, bg='white')
        left_info.pack(side='left', fill='x', expand=True)

        current_time = datetime.now()

        # Hiển thị mã hóa đơn
        if self.ma_hd:
            tk.Label(left_info, text=f"Mã hóa đơn: {self.ma_hd}",
                     font=('Arial', 12, 'bold'), bg='white', fg='#e74c3c').pack(anchor='w')

        tk.Label(left_info, text=f"Ngày lập: {current_time.strftime('%d/%m/%Y %H:%M')}",
                 font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w')

        if self.ma_kh:
            tk.Label(left_info, text=f"Mã khách hàng: {self.ma_kh}",
                     font=('Arial', 12), bg='white', fg='#7f8c8d').pack(anchor='w')

        # Hiển thị tên khách hàng
        if self.customer_info.get('TenKH'):
            tk.Label(left_info, text=f"Tên khách hàng: {self.customer_info['TenKH']}",
                     font=('Arial', 12), bg='white', fg='#7f8c8d').pack(anchor='w')

        # Hiển thị địa chỉ chính xác từ cột DiaChi trong database
        if self.customer_info.get('DiaChi'):
            tk.Label(left_info, text=f"Địa chỉ: {self.customer_info['DiaChi']}",
                     font=('Arial', 12), bg='white', fg='#7f8c8d').pack(anchor='w')

        # Hiển thị số điện thoại
        if self.customer_info.get('SDT'):
            tk.Label(left_info, text=f"Số điện thoại: {self.customer_info['SDT']}",
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

        # Treeview for products
        tree_frame = tk.Frame(products_frame)
        tree_frame.pack(fill='both', expand=True)

        # Configure treeview style
        style = ttk.Style()
        style.configure("Invoice.Treeview", rowheight=35)

        self.tree = ttk.Treeview(tree_frame,
                                columns=("STT", "Mã SP", "Tên sản phẩm", "Số lượng", "Đơn giá", "Thành tiền"),
                                show="headings", height=15, style="Invoice.Treeview")

        # Configure columns
        self.tree.heading("STT", text="STT")
        self.tree.heading("Mã SP", text="Mã SP")
        self.tree.heading("Tên sản phẩm", text="Tên sản phẩm")
        self.tree.heading("Số lượng", text="Số lượng")
        self.tree.heading("Đơn giá", text="Đơn giá")
        self.tree.heading("Thành tiền", text="Thành tiền")

        self.tree.column("STT", width=50, anchor='center')
        self.tree.column("Mã SP", width=80, anchor='center')
        self.tree.column("Tên sản phẩm", width=300)
        self.tree.column("Số lượng", width=80, anchor='center')
        self.tree.column("Đơn giá", width=120, anchor='e')
        self.tree.column("Thành tiền", width=130, anchor='e')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Populate invoice items
        self.populate_invoice_items()

        # Total frame
        total_frame = tk.Frame(main_frame, bg='#ecf0f1', relief='ridge', bd=2)
        total_frame.pack(fill='x', pady=(20, 0))

        total_container = tk.Frame(total_frame, bg='#ecf0f1')
        total_container.pack(fill='x', padx=20, pady=15)

        # Calculate total
        total_amount = sum(item['total'] for item in self.cart_data.values())

        tk.Label(total_container, text="TỔNG TIỀN THANH TOÁN:", font=('Arial', 16, 'bold'),
                 bg='#ecf0f1', fg='#2c3e50').pack(side='left')

        tk.Label(total_container, text=f"{total_amount:,.0f} VNĐ", font=('Arial', 20, 'bold'),
                 bg='#ecf0f1', fg='#e74c3c').pack(side='right')

        # Action buttons frame
        action_frame = tk.Frame(main_frame, bg='white')
        action_frame.pack(fill='x', pady=(20, 0))

        # Payment button
        btn_payment = tk.Button(action_frame, text="💳 THANH TOÁN", command=self.process_payment,
                               bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                               relief='flat', padx=40, pady=12, cursor='hand2')
        btn_payment.pack(side='right')

        # Print button
        btn_print = tk.Button(action_frame, text="🖨️ In hóa đơn", command=self.print_invoice,
                             bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                             relief='flat', padx=20, pady=10, cursor='hand2')
        btn_print.pack(side='left')

    def get_customer_info(self):
        """Lấy thông tin khách hàng từ database và tạo mã hóa đơn"""
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep09102025"
            )
            cursor = conn.cursor()

            # Lấy thông tin khách hàng bao gồm địa chỉ chính xác
            cursor.execute("SELECT MaKH, TenKH, SDT, DiaChi FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()

            if result:
                self.ma_kh = result[0]
                self.customer_info = {
                    'MaKH': result[0],
                    'TenKH': result[1],
                    'SDT': result[2],
                    'DiaChi': result[3]
                }

                # Tạo mã hóa đơn mới dựa trên số lượng hóa đơn hiện có
                cursor.execute(
                    "SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'"
                )
                hd_result = cursor.fetchone()
                next_number = ((hd_result[0] or 0) + 1) if hd_result else 1
                self.ma_hd = f"HD{next_number:03d}"

        except Exception as e:
            print(f"Lỗi khi lấy thông tin khách hàng: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def populate_invoice_items(self):
        """Điền dữ liệu sản phẩm vào bảng hóa đơn"""
        stt = 1
        for cart_key, item in self.cart_data.items():
            # Format price
            price_display = f"{item['price']:,.0f}"
            total_display = f"{item['total']:,.0f}"

            self.tree.insert("", "end", values=(
                stt,
                item['product_id'],
                item['name'],
                item['quantity'],
                price_display,
                total_display
            ))
            stt += 1

    def process_payment(self):
        """Xử lý thanh toán và tạo hóa đơn trong database"""
        if not self.cart_data:
            messagebox.showwarning("Cảnh báo", "Không có sản phẩm để thanh toán!")
            return

        total_amount = sum(item['total'] for item in self.cart_data.values())

        result = messagebox.askyesno("Xác nhận thanh toán",
                                   f"Tổng tiền: {total_amount:,.0f} VNĐ\n\n"
                                   f"Bạn có muốn tiến hành thanh toán?")
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
                (ma_hd, self.ma_kh, current_date)
            )

            # Thêm chi tiết hóa đơn
            for item in self.cart_data.values():
                cursor.execute(
                    """
                    INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (ma_hd, item['product_id'], item['name'], item['color'], item['size'],
                     item['quantity'], item['price'], item['total'])
                )

            # Xóa sản phẩm khỏi giỏ hàng sau khi thanh toán
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (self.ma_kh,))
            gh_result = cursor.fetchone()
            if gh_result:
                ma_gh = gh_result[0]
                cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))

            conn.commit()

            messagebox.showinfo("Thành công",
                              f"Thanh toán thành công!\n"
                              f"Mã hóa đơn: {ma_hd}\n"
                              f"Cảm ơn bạn đã mua hàng!")

            # Update parent view cart count
            if self.parent_view:
                self.parent_view.load_cart_count()

            # Close invoice view
            self.close()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xử lý thanh toán: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def print_invoice(self):
        """In hóa đơn (placeholder)"""
        messagebox.showinfo("Thông báo", "Chức năng in hóa đơn sẽ được cập nhật trong phiên bản tiếp theo!")

    def back_to_cart(self):
        """Quay lại giỏ hàng"""
        self.close()

    def close(self):
        """Đóng view với proper cleanup"""
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass
