"""
Giao diện đăng nhập và đăng ký - thiết kế giống hệt file gốc
"""
import tkinter as tk
from tkinter import messagebox
from views.base_view import BaseView
from models.user import authenticate_user, register_user
from utils.validators import validate_login_data, validate_registration_data

class LoginView(BaseView):
    def __init__(self, on_login_success=None):
        super().__init__("Shop Shoes - Đăng nhập", "500x600")
        self.on_login_success = on_login_success
        # Initialize global variables như file gốc
        self.entry_user = None
        self.entry_pass = None
        self.btn_eye = None
        self.reg_entry_user = None
        self.reg_entry_pass = None
        self.reg_entry_confirm_pass = None
        self.reg_entry_phone = None
        self.reg_entry_address = None
        self.reg_entry_name = None
        self.reg_role_var = None
        self.reg_btn_eye = None
        self.reg_btn_eye_confirm = None
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện đăng nhập giống hệt file gốc"""
        self.show_login()

    def show_login(self):
        """Hiển thị giao diện đăng nhập - copy từ file gốc"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Đăng nhập")
        self.root.geometry("500x600")

        # Main frame với background giống file gốc
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True)

        # Login form - căn giữa như file gốc
        login_frame = tk.Frame(main_frame, bg='white', padx=30, pady=30)
        login_frame.pack(expand=True)

        # Header giống file gốc
        tk.Label(login_frame, text="ĐĂNG NHẬP", font=('Arial', 20, 'bold'),
                 bg='white', fg='#2c3e50').pack(pady=(0, 30))

        # Username - design giống file gốc
        tk.Label(login_frame, text="Tên đăng nhập:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.entry_user = tk.Entry(login_frame, font=('Arial', 14), width=28)
        self.entry_user.pack(pady=(5, 15))

        # Password với eye button - design giống file gốc
        tk.Label(login_frame, text="Mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
        frame_pass = tk.Frame(login_frame, bg='white')
        frame_pass.pack(pady=(5, 30))

        self.entry_pass = tk.Entry(frame_pass, show='*', font=('Arial', 14), width=23)
        self.entry_pass.pack(side='left')

        self.btn_eye = tk.Button(frame_pass, text='👁‍🗨', command=self.toggle_password,
                                relief='flat', bg='white', font=('Arial', 14))
        self.btn_eye.pack(side='left', padx=(8, 0))

        # Login button - style giống file gốc
        btn_login = tk.Button(login_frame, text="ĐĂNG NHẬP", command=self.handle_login,
                             bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                             width=20, height=2, relief='flat', cursor='hand2')
        btn_login.pack(pady=(0, 15))

        # Register link - style giống file gốc
        tk.Label(login_frame, text="Chưa có tài khoản?", font=('Arial', 12),
                 bg='white', fg='#7f8c8d').pack()

        btn_register = tk.Button(login_frame, text="Đăng ký ngay", command=self.show_register,
                                bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                relief='flat', cursor='hand2', padx=20, pady=5)
        btn_register.pack(pady=(5, 0))

        # Focus và bind Enter giống file gốc
        self.entry_user.focus()

        def on_enter_user(event):
            self.entry_pass.focus()
        def on_enter_pass(event):
            self.handle_login()

        self.entry_user.bind('<Return>', on_enter_user)
        self.entry_pass.bind('<Return>', on_enter_pass)

    def show_register(self):
        """Hiển thị giao diện đăng ký - copy từ file gốc"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Đăng ký")
        self.root.geometry("720x900")

        # Frame chính - căn giữa giống trang đăng nhập
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True)

        # Register form - căn giữa với expand=True
        register_frame = tk.Frame(main_frame, bg='white', padx=30, pady=20)
        register_frame.pack(expand=True)

        # Header với nút quay về - căn giữa
        header_row = tk.Frame(register_frame, bg='white')
        header_row.pack(fill='x', pady=(0, 15))

        tk.Button(header_row, text="← Quay về đăng nhập", command=self.show_login,
                  bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'),
                  relief='flat', padx=12, pady=6, cursor='hand2').pack(side='left')

        tk.Label(header_row, text="ĐĂNG KÝ TÀI KHOẢN", font=('Arial', 18, 'bold'),
                 bg='white', fg='#2c3e50').pack(expand=True)

        # Username - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Tên đăng nhập:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_user = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_user.pack(pady=(5, 15))

        # Full name - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Họ tên:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_name = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_name.pack(pady=(5, 15))

        # Password - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
        reg_frame_pass = tk.Frame(register_frame, bg='white')
        reg_frame_pass.pack(pady=(5, 15))

        self.reg_entry_pass = tk.Entry(reg_frame_pass, show='*', font=('Arial', 14), width=23)
        self.reg_entry_pass.pack(side='left')

        self.reg_btn_eye = tk.Button(reg_frame_pass, text='👁‍🗨', command=self.toggle_reg_password,
                               relief='flat', bg='white', font=('Arial', 14))
        self.reg_btn_eye.pack(side='left', padx=(8, 0))

        # Confirm Password - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Xác nhận mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
        reg_frame_confirm_pass = tk.Frame(register_frame, bg='white')
        reg_frame_confirm_pass.pack(pady=(5, 15))

        self.reg_entry_confirm_pass = tk.Entry(reg_frame_confirm_pass, show='*', font=('Arial', 14), width=23)
        self.reg_entry_confirm_pass.pack(side='left')

        self.reg_btn_eye_confirm = tk.Button(reg_frame_confirm_pass, text='👁‍🗨', command=self.toggle_reg_confirm_password,
                                       relief='flat', bg='white', font=('Arial', 14))
        self.reg_btn_eye_confirm.pack(side='left', padx=(8, 0))

        # Role - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Vai trò:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_role_var = tk.StringVar(value="buyer")
        role_frame = tk.Frame(register_frame, bg='white')
        role_frame.pack(pady=(5, 15))

        tk.Radiobutton(role_frame, text="Người mua", variable=self.reg_role_var, value="buyer",
                       bg='white', font=('Arial', 14)).pack(side='left', padx=(0, 30))
        tk.Radiobutton(role_frame, text="Người bán", variable=self.reg_role_var, value="seller",
                       bg='white', font=('Arial', 14)).pack(side='left')

        # Phone - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Số điện thoại:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_phone = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_phone.pack(pady=(5, 15))

        # Address - căn trái như trang đăng nhập
        tk.Label(register_frame, text="Địa chỉ (tùy chọn):", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_address = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_address.pack(pady=(5, 20))

        # Buttons - căn giữa theo kiểu trang đăng nhập
        btn_frame = tk.Frame(register_frame, bg='white')
        btn_frame.pack()

        btn_register = tk.Button(btn_frame, text="ĐĂNG KÝ", command=self.handle_register,
                                bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                                width=15, height=2, relief='flat', cursor='hand2')
        btn_register.pack(pady=(0, 8))

        btn_back = tk.Button(btn_frame, text="HỦY BỎ", command=self.show_login,
                            bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                            width=15, height=2, relief='flat', cursor='hand2')
        btn_back.pack()

        # Focus và bind Enter
        self.reg_entry_user.focus()

        def on_enter_reg_user(event):
            self.reg_entry_name.focus()
        def on_enter_reg_name(event):
            self.reg_entry_pass.focus()
        def on_enter_reg_pass(event):
            self.reg_entry_confirm_pass.focus()
        def on_enter_reg_confirm(event):
            self.reg_entry_phone.focus()
        def on_enter_reg_phone(event):
            self.reg_entry_address.focus()
        def on_enter_reg_address(event):
            self.handle_register()

        self.reg_entry_user.bind('<Return>', on_enter_reg_user)
        self.reg_entry_name.bind('<Return>', on_enter_reg_name)
        self.reg_entry_pass.bind('<Return>', on_enter_reg_pass)
        self.reg_entry_confirm_pass.bind('<Return>', on_enter_reg_confirm)
        self.reg_entry_phone.bind('<Return>', on_enter_reg_phone)
        self.reg_entry_address.bind('<Return>', on_enter_reg_address)

    def toggle_password(self):
        """Toggle hiển thị mật khẩu - giống file gốc"""
        if self.entry_pass.cget('show') == '':
            self.entry_pass.config(show='*')
            self.btn_eye.config(text='👁‍🗨')
        else:
            self.entry_pass.config(show='')
            self.btn_eye.config(text='👁')

    def toggle_reg_password(self):
        """Toggle hiển thị mật khẩu đăng ký - giống file gốc"""
        if self.reg_entry_pass.cget('show') == '':
            self.reg_entry_pass.config(show='*')
            self.reg_btn_eye.config(text='👁‍🗨')
        else:
            self.reg_entry_pass.config(show='')
            self.reg_btn_eye.config(text='👁')

    def toggle_reg_confirm_password(self):
        """Toggle hiển thị mật khẩu xác nhận - giống file gốc"""
        if self.reg_entry_confirm_pass.cget('show') == '':
            self.reg_entry_confirm_pass.config(show='*')
            self.reg_btn_eye_confirm.config(text='👁‍🗨')
        else:
            self.reg_entry_confirm_pass.config(show='')
            self.reg_btn_eye_confirm.config(text='👁')

    def handle_login(self):
        """Xử lý đăng nhập - giống file gốc"""
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Import mysql connector để kết nối database trực tiếp như file gốc
        import mysql.connector

        conn = None
        cursor = None
        try:
            # Kết nối database giống file gốc
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep"
            )
            cursor = conn.cursor()

            # Kiểm tra khách hàng trước
            cursor.execute(
                "SELECT MaKH FROM khachhang WHERE TenDN=%s AND MatKhau=%s",
                (username, password)
            )
            if cursor.fetchone():
                # Gọi show_shoes từ file gốc với role buyer
                if self.on_login_success:
                    self.on_login_success("buyer", username)
                else:
                    # Import và gọi trực tiếp show_shoes như file gốc
                    from views.product_view import ProductView
                    self.root.destroy()
                    product_view = ProductView(role="buyer", username=username)
                    product_view.run()
                return

            # Kiểm tra nhân viên
            cursor.execute(
                "SELECT MaNV FROM nhanvien WHERE TenDN=%s AND MatKhau=%s",
                (username, password)
            )
            if cursor.fetchone():
                # Gọi show_shoes từ file gốc với role seller
                if self.on_login_success:
                    self.on_login_success("seller", username)
                else:
                    # Import và gọi trực tiếp show_shoes như file gốc
                    from views.product_view import ProductView
                    self.root.destroy()
                    product_view = ProductView(role="seller", username=username)
                    product_view.run()
                return

            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def handle_register(self):
        """Xử lý đăng ký - giống file gốc"""
        username = self.reg_entry_user.get().strip()
        password = self.reg_entry_pass.get()
        confirm_password = self.reg_entry_confirm_pass.get()
        role = self.reg_role_var.get()
        phone = self.reg_entry_phone.get().strip()
        address = self.reg_entry_address.get().strip()
        full_name = self.reg_entry_name.get().strip()

        if not all([username, password, confirm_password, role, phone, full_name]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
            return

        if role not in ("buyer", "seller"):
            messagebox.showerror("Lỗi", "Vui lòng chọn vai trò hợp lệ!")
            return

        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        if len(password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
            return

        if not phone.isdigit() or len(phone) not in (10, 11):
            messagebox.showerror("Lỗi", "Số điện thoại phải gồm 10 hoặc 11 chữ số!")
            return

        # Import mysql connector để kết nối database trực tiếp như file gốc
        import mysql.connector

        conn = None
        cursor = None
        try:
            # Kết nối database giống file gốc
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep"
            )
            cursor = conn.cursor()

            # Kiểm tra tên đăng nhập đã tồn tại chưa
            cursor.execute("SELECT 1 FROM khachhang WHERE TenDN=%s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại trong danh sách khách hàng!")
                return

            cursor.execute("SELECT 1 FROM nhanvien WHERE TenDN=%s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại trong danh sách nhân viên!")
                return

            if role == "buyer":
                # Kiểm tra số điện thoại đã tồn tại chưa
                cursor.execute("SELECT 1 FROM khachhang WHERE SDT=%s", (phone,))
                if cursor.fetchone():
                    messagebox.showerror("Lỗi", "Số điện thoại đã được sử dụng!")
                    return

                # Tạo ID khách hàng mới
                cursor.execute(
                    "SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) FROM khachhang WHERE MaKH LIKE 'KH%'"
                )
                result = cursor.fetchone()
                next_number = ((result[0] or 0) + 1) if result else 1
                customer_id = f"KH{next_number:03d}"

                cursor.execute(
                    """
                    INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (customer_id, full_name, phone, address if address else None, username, password)
                )

                # Tự động tạo giỏ hàng cho khách hàng mới
                cart_id = f"GH{next_number:03d}"
                cursor.execute(
                    """
                    INSERT INTO giohang (MaGH, MaKH)
                    VALUES (%s, %s)
                    """,
                    (cart_id, customer_id)
                )
            else:
                # Tạo ID nhân viên mới
                cursor.execute(
                    "SELECT MAX(CAST(SUBSTRING(MaNV, 3) AS UNSIGNED)) FROM nhanvien WHERE MaNV LIKE 'NV%'"
                )
                result = cursor.fetchone()
                next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
                staff_id = f"NV{next_number:03d}"

                cursor.execute(
                    """
                    INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (staff_id, full_name, username, password)
                )

            conn.commit()
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            self.show_login()

        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Lỗi", f"Không thể đăng ký do trùng dữ liệu: {str(err)}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đăng ký: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def close(self):
        """Đóng view với proper cleanup"""
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass
