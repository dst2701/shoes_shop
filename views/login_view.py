"""
Login and Registration View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox
from models.user import authenticate_user, register_user

class LoginView:
    def __init__(self, root):
        self.root = root
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
        self.on_login_success = None

    def set_login_callback(self, callback):
        """Set callback function for successful login"""
        self.on_login_success = callback

    def login(self):
        """Login function from main.py"""
        username = self.entry_user.get().strip()
        password = self.entry_pass.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            role = authenticate_user(username, password)
            if role:
                if self.on_login_success:
                    self.on_login_success(role, username)
            else:
                messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database: {str(e)}")

    def register(self):
        """Register function from main.py"""
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

        try:
            success = register_user(username, password, role, phone, address, full_name)
            if success:
                messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
                self.show_login()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đăng ký: {str(e)}")

    def toggle_password(self):
        """Toggle password visibility"""
        if self.entry_pass.cget('show') == '':
            self.entry_pass.config(show='*')
            self.btn_eye.config(text='👁‍🗨')
        else:
            self.entry_pass.config(show='')
            self.btn_eye.config(text='👁')

    def toggle_reg_password(self):
        """Toggle registration password visibility"""
        if self.reg_entry_pass.cget('show') == '':
            self.reg_entry_pass.config(show='*')
            self.reg_btn_eye.config(text='👁‍🗨')
        else:
            self.reg_entry_pass.config(show='')
            self.reg_btn_eye.config(text='👁')

    def toggle_reg_confirm_password(self):
        """Toggle registration confirm password visibility"""
        if self.reg_entry_confirm_pass.cget('show') == '':
            self.reg_entry_confirm_pass.config(show='*')
            self.reg_btn_eye_confirm.config(text='👁‍🗨')
        else:
            self.reg_entry_confirm_pass.config(show='')
            self.reg_btn_eye_confirm.config(text='👁')

    def show_login(self):
        """Show login interface - from main.py"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Đăng nhập")
        self.root.geometry("720x720")

        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True)

        login_frame = tk.Frame(main_frame, bg='white', padx=30, pady=30)
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="ĐĂNG NHẬP", font=('Arial', 18, 'bold'),
                 bg='white', fg='#2c3e50').pack(pady=(0, 20))

        tk.Label(login_frame, text="Tên đăng nhập:", font=('Arial', 15), bg='white').pack(anchor='w')
        self.entry_user = tk.Entry(login_frame, font=('Arial', 15), width=25)
        self.entry_user.pack(pady=(5, 15))

        tk.Label(login_frame, text="Mật khẩu:", font=('Arial', 15), bg='white').pack(anchor='w')
        frame_pass = tk.Frame(login_frame, bg='white')
        frame_pass.pack(pady=(5, 20))

        self.entry_pass = tk.Entry(frame_pass, show='*', font=('Arial', 15), width=20)
        self.entry_pass.pack(side='left')

        self.btn_eye = tk.Button(frame_pass, text='👁‍🗨', command=self.toggle_password,
                               relief='flat', bg='white', font=('Arial', 12))
        self.btn_eye.pack(side='left', padx=(5, 0))

        # Buttons
        btn_frame = tk.Frame(login_frame, bg='white')
        btn_frame.pack()

        btn_login = tk.Button(btn_frame, text="Đăng nhập", command=self.login,
                             bg='#3498db', fg='white', font=('Arial', 15, 'bold'),
                             width=15, height=2, relief='flat')
        btn_login.pack(pady=(0, 10))

        btn_register_link = tk.Button(btn_frame, text="Đăng ký tài khoản", command=self.show_register,
                                     bg='#27ae60', fg='white', font=('Arial', 15, 'bold'),
                                     width=15, height=2, relief='flat')
        btn_register_link.pack()

        def on_enter(event):
            self.login()

        self.entry_user.bind('<Return>', on_enter)
        self.entry_pass.bind('<Return>', on_enter)
        self.entry_user.focus()

    def show_register(self):
        """Show registration interface - from main.py"""
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

        # Username
        tk.Label(register_frame, text="Tên đăng nhập:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_user = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_user.pack(pady=(5, 15))

        # Full name
        tk.Label(register_frame, text="Họ tên:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_name = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_name.pack(pady=(5, 15))

        # Password
        tk.Label(register_frame, text="Mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
        reg_frame_pass = tk.Frame(register_frame, bg='white')
        reg_frame_pass.pack(pady=(5, 15))

        self.reg_entry_pass = tk.Entry(reg_frame_pass, show='*', font=('Arial', 14), width=23)
        self.reg_entry_pass.pack(side='left')

        self.reg_btn_eye = tk.Button(reg_frame_pass, text='👁‍🗨', command=self.toggle_reg_password,
                               relief='flat', bg='white', font=('Arial', 14))
        self.reg_btn_eye.pack(side='left', padx=(8, 0))

        # Confirm Password
        tk.Label(register_frame, text="Xác nhận mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
        reg_frame_confirm_pass = tk.Frame(register_frame, bg='white')
        reg_frame_confirm_pass.pack(pady=(5, 15))

        self.reg_entry_confirm_pass = tk.Entry(reg_frame_confirm_pass, show='*', font=('Arial', 14), width=23)
        self.reg_entry_confirm_pass.pack(side='left')

        self.reg_btn_eye_confirm = tk.Button(reg_frame_confirm_pass, text='👁‍🗨', command=self.toggle_reg_confirm_password,
                                       relief='flat', bg='white', font=('Arial', 14))
        self.reg_btn_eye_confirm.pack(side='left', padx=(8, 0))

        # Role
        tk.Label(register_frame, text="Vai trò:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_role_var = tk.StringVar(value="buyer")
        role_frame = tk.Frame(register_frame, bg='white')
        role_frame.pack(pady=(5, 15))

        tk.Radiobutton(role_frame, text="Người mua", variable=self.reg_role_var, value="buyer",
                       bg='white', font=('Arial', 14)).pack(side='left', padx=(0, 30))
        tk.Radiobutton(role_frame, text="Người bán", variable=self.reg_role_var, value="seller",
                       bg='white', font=('Arial', 14)).pack(side='left')

        # Phone
        tk.Label(register_frame, text="Số điện thoại:", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_phone = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_phone.pack(pady=(5, 15))

        # Address
        tk.Label(register_frame, text="Địa chỉ (tùy chọn):", font=('Arial', 14), bg='white').pack(anchor='w')
        self.reg_entry_address = tk.Entry(register_frame, font=('Arial', 14), width=28)
        self.reg_entry_address.pack(pady=(5, 20))

        # Buttons
        btn_frame = tk.Frame(register_frame, bg='white')
        btn_frame.pack()

        btn_register = tk.Button(btn_frame, text="ĐĂNG KÝ", command=self.register,
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
            self.register()

        self.reg_entry_user.bind('<Return>', on_enter_reg_user)
        self.reg_entry_name.bind('<Return>', on_enter_reg_name)
        self.reg_entry_pass.bind('<Return>', on_enter_reg_pass)
        self.reg_entry_confirm_pass.bind('<Return>', on_enter_reg_confirm)
        self.reg_entry_phone.bind('<Return>', on_enter_reg_phone)
        self.reg_entry_address.bind('<Return>', on_enter_reg_address)
