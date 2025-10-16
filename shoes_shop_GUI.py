import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import urllib.request
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_IMAGE_DIR = os.path.join(BASE_DIR, "images")

# Kết nối MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="tungds270105",
        database="shopgiaydep"
    )


def generate_customer_id(cursor):
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) FROM khachhang WHERE MaKH LIKE 'KH%'"
    )
    result = cursor.fetchone()
    next_number = ((result[0] or 0) + 1) if result else 1
    return f"KH{next_number:03d}"


def generate_staff_id(cursor):
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaNV, 3) AS UNSIGNED)) FROM nhanvien WHERE MaNV LIKE 'NV%'"
    )
    result = cursor.fetchone()
    next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
    return f"NV{next_number:03d}"


entry_user = None
entry_pass = None
reg_entry_user = None
reg_entry_pass = None
reg_entry_confirm_pass = None
reg_entry_phone = None
reg_entry_address = None
reg_entry_name = None
reg_role_var = None

# Đăng nhập
def login():
    username = entry_user.get().strip()
    password = entry_pass.get()

    if not username or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT MaKH FROM khachhang WHERE TenDN=%s AND MatKhau=%s",
            (username, password)
        )
        if cursor.fetchone():
            show_shoes(role="buyer", username=username)
            return

        cursor.execute(
            "SELECT MaNV FROM nhanvien WHERE TenDN=%s AND MatKhau=%s",
            (username, password)
        )
        if cursor.fetchone():
            show_shoes(role="seller", username=username)
            return

        messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# THÊM FUNCTION ĐĂNG KÝ
def register():
    username = reg_entry_user.get().strip()
    password = reg_entry_pass.get()
    confirm_password = reg_entry_confirm_pass.get()
    role = reg_role_var.get()
    phone = reg_entry_phone.get().strip()
    address = reg_entry_address.get().strip()
    full_name = reg_entry_name.get().strip()

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

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM khachhang WHERE TenDN=%s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại trong danh sách khách hàng!")
            return

        cursor.execute("SELECT 1 FROM nhanvien WHERE TenDN=%s", (username,))
        if cursor.fetchone():
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại trong danh sách nhân viên!")
            return

        if role == "buyer":
            cursor.execute("SELECT 1 FROM khachhang WHERE SDT=%s", (phone,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Số điện thoại đã được sử dụng!")
                return

            customer_id = generate_customer_id(cursor)
            cursor.execute(
                """
                INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (customer_id, full_name, phone, address if address else None, username, password)
            )
        else:
            staff_id = generate_staff_id(cursor)
            cursor.execute(
                """
                INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
                VALUES (%s, %s, %s, %s)
                """,
                (staff_id, full_name, username, password)
            )

        conn.commit()
        messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
        show_login()

    except mysql.connector.IntegrityError as err:
        messagebox.showerror("Lỗi", f"Không thể đăng ký do trùng dữ liệu: {str(err)}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đăng ký: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Toggle password
def toggle_password():
    if entry_pass.cget('show') == '':
        entry_pass.config(show='*')
        btn_eye.config(text='👁‍🗨')
    else:
        entry_pass.config(show='')
        btn_eye.config(text='👁')

def toggle_reg_password():
    if reg_entry_pass.cget('show') == '':
        reg_entry_pass.config(show='*')
        reg_btn_eye.config(text='👁‍🗨')
    else:
        reg_entry_pass.config(show='')
        reg_btn_eye.config(text='👁')

def toggle_reg_confirm_password():
    if reg_entry_confirm_pass.cget('show') == '':
        reg_entry_confirm_pass.config(show='*')
        reg_btn_eye_confirm.config(text='👁‍🗨')
    else:
        reg_entry_confirm_pass.config(show='')
        reg_btn_eye_confirm.config(text='👁')
        

# Load ảnh an toàn
def load_image_safely(path_or_url):
    source = (path_or_url or "").strip()
    if not source:
        return None

    image = None
    try:
        if source.lower().startswith(("http://", "https://")):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(source, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() != 200:
                    return None
                raw_data = response.read()
            with Image.open(io.BytesIO(raw_data)) as img:
                image = img.copy()
        else:
            candidate_paths = []
            if os.path.isabs(source):
                candidate_paths.append(source)
            else:
                candidate_paths.append(os.path.join(LOCAL_IMAGE_DIR, source))
                candidate_paths.append(os.path.join(BASE_DIR, source))

            for file_path in candidate_paths:
                if os.path.isfile(file_path):
                    with Image.open(file_path) as img:
                        image = img.copy()
                    break

            if image is None:
                return None

        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')

        image = image.resize((300, 300), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    except Exception as e:
        print(f"Lỗi tải ảnh từ {source}: {e}")
        return None

# Hiển thị danh sách giày
def show_shoes(role=None, username=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shop Shoes - Danh sách sản phẩm")
    root.geometry("1200x700")  # Tăng width để chứa gallery

    header_frame = tk.Frame(root, bg='#2c3e50', height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)

    header_container = tk.Frame(header_frame, bg='#2c3e50')
    header_container.pack(fill='both', expand=True, padx=10)

    tk.Label(header_container, text="SHOP GIÀY", font=('Arial', 20, 'bold'),
             fg='white', bg='#2c3e50').pack(side='left', pady=15)

    btn_logout = tk.Button(header_container, text="Đăng xuất", command=show_login,
                          bg='#e74c3c', fg='white', relief='flat',
                          font=('Arial', 15), padx=15, pady=5)
    btn_logout.pack(side='right', pady=15)

    if username:
        role_label = "Người bán" if role == "seller" else "Khách hàng"
        tk.Label(header_container, text=f"{role_label}: {username}",
                 font=('Arial', 14), fg='white', bg='#2c3e50').pack(side='right', pady=15, padx=(0, 15))

    # Load product data và images
    product_rows = []
    product_images = {}  # Dictionary để lưu tất cả ảnh của mỗi sản phẩm
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Lấy thông tin sản phẩm
        cursor.execute("""
            SELECT MaSP, TenSP, Gia, MoTa
            FROM sanpham
            ORDER BY TenSP
        """)
        product_rows = cursor.fetchall()
        
        # Lấy tất cả ảnh của từng sản phẩm
        cursor.execute("""
            SELECT MaSP, URLAnh
            FROM url_sp
            ORDER BY MaSP
        """)
        image_rows = cursor.fetchall()
        
        # Tổ chức ảnh theo sản phẩm
        for ma_sp, url_anh in image_rows:
            if ma_sp not in product_images:
                product_images[ma_sp] = []
            product_images[ma_sp].append(url_anh)
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
        return
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Left panel: Product list
    list_frame = tk.Frame(main_frame, width=400)
    list_frame.pack(side='left', fill='y', padx=(0, 10))
    list_frame.pack_propagate(False)

    tk.Label(list_frame, text="Danh sách giày", font=('Arial', 18, 'bold')).pack(anchor='w', pady=(0, 10))

    tree_frame = tk.Frame(list_frame)
    tree_frame.pack(fill='both', expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Tên", "Giá"), show="headings", height=15)
    tree.heading("Tên", text="Tên giày")
    tree.heading("Giá", text="Giá")
    tree.column("Tên", width=250)
    tree.column("Giá", width=120, anchor='e')

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Populate treeview và product data
    product_data = {}
    for ma_sp, ten_sp, gia, mo_ta in product_rows:
        price_display = f"{float(gia):,.0f} VNĐ" if gia is not None else "N/A"
        tree.insert("", "end", iid=ma_sp, values=(ten_sp, price_display))
        product_data[ma_sp] = {
            "name": ten_sp,
            "price": price_display,
            "description": (mo_ta or "Chưa có mô tả cho sản phẩm này.").strip(),
            "images": product_images.get(ma_sp, [])
        }

    # Right panel: Product details và image gallery
    detail_frame = tk.Frame(main_frame, bg='#f8f9fa')
    detail_frame.pack(side='right', fill='both', expand=True)

    # Product name
    product_name_label = tk.Label(detail_frame, text="Chọn sản phẩm để xem chi tiết", 
                                  font=('Arial', 18, 'bold'), bg='#f8f9fa', fg='#2c3e50')
    product_name_label.pack(pady=(15, 10))

    # Main image display area
    main_image_frame = tk.Frame(detail_frame, bg='white', relief='solid', bd=1, height=350)
    main_image_frame.pack(fill='x', padx=15, pady=(0, 10))
    main_image_frame.pack_propagate(False)

    main_image_label = tk.Label(main_image_frame, text="Hình ảnh sản phẩm", 
                               font=('Arial', 14), bg='white', fg='#6c757d')
    main_image_label.pack(expand=True)

    # Thumbnail gallery section
    gallery_section = tk.Frame(detail_frame, bg='#f8f9fa')
    gallery_section.pack(fill='x', padx=15, pady=(0, 10))

    tk.Label(gallery_section, text="Các ảnh khác:", font=('Arial', 12, 'bold'), 
             bg='#f8f9fa').pack(anchor='w', pady=(0, 5))

    # Scrollable thumbnail container
    thumbnail_frame = tk.Frame(gallery_section, bg='white', height=80, relief='solid', bd=1)
    thumbnail_frame.pack(fill='x')
    thumbnail_frame.pack_propagate(False)

    # Canvas để scroll thumbnails
    thumbnail_canvas = tk.Canvas(thumbnail_frame, bg='white', height=78)
    thumbnail_scrollbar = ttk.Scrollbar(thumbnail_frame, orient='horizontal', command=thumbnail_canvas.xview)
    thumbnail_scrollable = tk.Frame(thumbnail_canvas, bg='white')

    thumbnail_scrollable.bind("<Configure>", 
                             lambda e: thumbnail_canvas.configure(scrollregion=thumbnail_canvas.bbox("all")))
    thumbnail_canvas.create_window((0, 0), window=thumbnail_scrollable, anchor="nw")
    thumbnail_canvas.configure(xscrollcommand=thumbnail_scrollbar.set)

    thumbnail_canvas.pack(side='top', fill='both', expand=True)
    thumbnail_scrollbar.pack(side='bottom', fill='x')

    # Description area
    desc_section = tk.Frame(detail_frame, bg='#f8f9fa')
    desc_section.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    tk.Label(desc_section, text="Mô tả sản phẩm:", font=('Arial', 12, 'bold'), 
             bg='#f8f9fa').pack(anchor='w', pady=(0, 5))

    desc_text = tk.Text(desc_section, height=6, wrap='word', font=('Arial', 11), 
                       state='disabled', bg='white', relief='solid', bd=1)
    desc_text.pack(fill='both', expand=True)

    # Functions để handle images
    def show_main_image(image_url):
        """Hiển thị ảnh chính"""
        try:
            # Clear current image
            for widget in main_image_frame.winfo_children():
                widget.destroy()
            
            if image_url:
                img = load_image_safely(image_url)
                if img:
                    # Resize để fit main display area
                    main_image_label = tk.Label(main_image_frame, image=img, bg='white')
                    main_image_label.image = img  # Keep reference
                    main_image_label.pack(expand=True)
                else:
                    tk.Label(main_image_frame, text="❌ Không thể tải hình ảnh", 
                           font=('Arial', 14), bg='white', fg='#e74c3c').pack(expand=True)
            else:
                tk.Label(main_image_frame, text="Không có hình ảnh", 
                       font=('Arial', 14), bg='white', fg='#6c757d').pack(expand=True)
        except Exception as e:
            tk.Label(main_image_frame, text="Lỗi tải hình ảnh", 
                   font=('Arial', 14), bg='white', fg='#e74c3c').pack(expand=True)

    def update_thumbnail_gallery(images):
        """Cập nhật gallery thumbnails"""
        # Clear current thumbnails
        for widget in thumbnail_scrollable.winfo_children():
            widget.destroy()
        
        if not images:
            tk.Label(thumbnail_scrollable, text="Không có ảnh khác", 
                   font=('Arial', 10), bg='white', fg='#6c757d').pack(side='left', padx=10, pady=20)
            return
        
        for i, image_url in enumerate(images):
            try:
                # Load thumbnail image
                img = load_image_safely(image_url)
                if img:
                    # Resize to thumbnail size (70x70)
                    thumb_img = load_thumbnail_image(image_url)
                    
                    # Create thumbnail button
                    thumb_btn = tk.Button(thumbnail_scrollable, image=thumb_img, 
                                         command=lambda url=image_url: show_main_image(url),
                                         relief='solid', bd=2, cursor='hand2',
                                         bg='white', activebackground='#e9ecef')
                    thumb_btn.image = thumb_img  # Keep reference
                    thumb_btn.pack(side='left', padx=3, pady=3)
                    
                    # Hover effects
                    def on_enter(e, btn=thumb_btn):
                        btn.config(bd=3, bg='#dee2e6')
                    def on_leave(e, btn=thumb_btn):
                        btn.config(bd=2, bg='white')
                    
                    thumb_btn.bind("<Enter>", on_enter)
                    thumb_btn.bind("<Leave>", on_leave)
                    
                else:
                    # Fallback button nếu không load được ảnh
                    thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}", 
                                         command=lambda url=image_url: show_main_image(url),
                                         width=8, height=4, cursor='hand2',
                                         relief='solid', bd=2, bg='white')
                    thumb_btn.pack(side='left', padx=3, pady=3)
                    
            except Exception as e:
                print(f"Lỗi tạo thumbnail {i+1}: {e}")
                # Tạo placeholder button
                thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}", 
                                     command=lambda url=image_url: show_main_image(url),
                                     width=8, height=4, cursor='hand2',
                                     relief='solid', bd=2, bg='white')
                thumb_btn.pack(side='left', padx=3, pady=3)

    def on_product_select(event):
        """Handle khi chọn sản phẩm"""
        selection = tree.selection()
        if not selection:
            return

        ma_sp = selection[0]
        if ma_sp not in product_data:
            return

        product = product_data[ma_sp]
        
        # Update product name
        product_name_label.config(text=product["name"])
        
        # Update description
        desc_text.config(state='normal')
        desc_text.delete(1.0, tk.END)
        desc_text.insert(1.0, product["description"])
        desc_text.config(state='disabled')
        
        # Update images
        images = product["images"]
        if images:
            show_main_image(images[0])  # Show first image as main
            update_thumbnail_gallery(images)
        else:
            show_main_image(None)
            update_thumbnail_gallery([])

    # Bind events
    tree.bind("<<TreeviewSelect>>", on_product_select)
    
    # Mouse wheel scroll cho thumbnail canvas
    def on_mousewheel(event):
        thumbnail_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    
    thumbnail_canvas.bind("<MouseWheel>", on_mousewheel)

#LOAD ẢNH THUMBNAIL
def load_thumbnail_image(path_or_url):
    """Load ảnh thumbnail kích thước 70x70"""
    source = (path_or_url or "").strip()
    if not source:
        return None

    image = None
    try:
        if source.lower().startswith(("http://", "https://")):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(source, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() != 200:
                    return None
                raw_data = response.read()
            with Image.open(io.BytesIO(raw_data)) as img:
                image = img.copy()
        else:
            candidate_paths = []
            if os.path.isabs(source):
                candidate_paths.append(source)
            else:
                candidate_paths.append(os.path.join(LOCAL_IMAGE_DIR, source))
                candidate_paths.append(os.path.join(BASE_DIR, source))

            for file_path in candidate_paths:
                if os.path.isfile(file_path):
                    with Image.open(file_path) as img:
                        image = img.copy()
                    break

            if image is None:
                return None

        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')

        # Resize to thumbnail size
        image = image.resize((70, 70), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    except Exception as e:
        print(f"Lỗi tải thumbnail từ {source}: {e}")
        return None

# FUNCTION HIỂN THỊ ĐĂNG KÝ
def show_register():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Shop Shoes - Đăng ký")
    root.geometry("720x900")
    
    # Frame chính - căn giữa giống trang đăng nhập
    main_frame = tk.Frame(root, bg='#ecf0f1')
    main_frame.pack(fill='both', expand=True)
    
    # Register form - căn giữa với expand=True
    register_frame = tk.Frame(main_frame, bg='white', padx=30, pady=20)
    register_frame.pack(expand=True)

    # Header với nút quay về - căn giữa
    header_row = tk.Frame(register_frame, bg='white')
    header_row.pack(fill='x', pady=(0, 15))

    tk.Button(header_row, text="← Quay về đăng nhập", command=show_login,
              bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'),
              relief='flat', padx=12, pady=6, cursor='hand2').pack(side='left')

    tk.Label(header_row, text="ĐĂNG KÝ TÀI KHOẢN", font=('Arial', 18, 'bold'),
             bg='white', fg='#2c3e50').pack(expand=True)

    # Username - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Tên đăng nhập:", font=('Arial', 14), bg='white').pack(anchor='w')
    global reg_entry_user, reg_entry_name
    reg_entry_user = tk.Entry(register_frame, font=('Arial', 14), width=28)
    reg_entry_user.pack(pady=(5, 15))

    # Full name - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Họ tên:", font=('Arial', 14), bg='white').pack(anchor='w')
    reg_entry_name = tk.Entry(register_frame, font=('Arial', 14), width=28)
    reg_entry_name.pack(pady=(5, 15))
    
    # Password - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
    reg_frame_pass = tk.Frame(register_frame, bg='white')
    reg_frame_pass.pack(pady=(5, 15))
    
    global reg_entry_pass, reg_btn_eye
    reg_entry_pass = tk.Entry(reg_frame_pass, show='*', font=('Arial', 14), width=23)
    reg_entry_pass.pack(side='left')
    
    reg_btn_eye = tk.Button(reg_frame_pass, text='👁‍🗨', command=toggle_reg_password, 
                           relief='flat', bg='white', font=('Arial', 14))
    reg_btn_eye.pack(side='left', padx=(8, 0))
    
    # Confirm Password - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Xác nhận mật khẩu:", font=('Arial', 14), bg='white').pack(anchor='w')
    reg_frame_confirm_pass = tk.Frame(register_frame, bg='white')
    reg_frame_confirm_pass.pack(pady=(5, 15))
    
    global reg_entry_confirm_pass, reg_btn_eye_confirm
    reg_entry_confirm_pass = tk.Entry(reg_frame_confirm_pass, show='*', font=('Arial', 14), width=23)
    reg_entry_confirm_pass.pack(side='left')
    
    reg_btn_eye_confirm = tk.Button(reg_frame_confirm_pass, text='👁‍🗨', command=toggle_reg_confirm_password, 
                                   relief='flat', bg='white', font=('Arial', 14))
    reg_btn_eye_confirm.pack(side='left', padx=(8, 0))
    
    # Role - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Vai trò:", font=('Arial', 14), bg='white').pack(anchor='w')
    global reg_role_var
    reg_role_var = tk.StringVar(value="buyer")
    role_frame = tk.Frame(register_frame, bg='white')
    role_frame.pack(pady=(5, 15))
    
    tk.Radiobutton(role_frame, text="Người mua", variable=reg_role_var, value="buyer",
                   bg='white', font=('Arial', 14)).pack(side='left', padx=(0, 30))
    tk.Radiobutton(role_frame, text="Người bán", variable=reg_role_var, value="seller",
                   bg='white', font=('Arial', 14)).pack(side='left')
    
    # Phone - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Số điện thoại:", font=('Arial', 14), bg='white').pack(anchor='w')
    global reg_entry_phone
    reg_entry_phone = tk.Entry(register_frame, font=('Arial', 14), width=28)
    reg_entry_phone.pack(pady=(5, 15))
    
    # Address - căn trái như trang đăng nhập
    tk.Label(register_frame, text="Địa chỉ (tùy chọn):", font=('Arial', 14), bg='white').pack(anchor='w')
    global reg_entry_address
    reg_entry_address = tk.Entry(register_frame, font=('Arial', 14), width=28)
    reg_entry_address.pack(pady=(5, 20))
    
    # Buttons - căn giữa theo kiểu trang đăng nhập
    btn_frame = tk.Frame(register_frame, bg='white')
    btn_frame.pack()
    
    btn_register = tk.Button(btn_frame, text="ĐĂNG KÝ", command=register,
                            bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                            width=15, height=2, relief='flat', cursor='hand2')
    btn_register.pack(pady=(0, 8))
    
    btn_back = tk.Button(btn_frame, text="HỦY BỎ", command=show_login,
                        bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                        width=15, height=2, relief='flat', cursor='hand2')
    btn_back.pack()
    
    # Focus và bind Enter
    reg_entry_user.focus()
    
    def on_enter_reg_user(event):
        reg_entry_name.focus()
    def on_enter_reg_name(event):
        reg_entry_pass.focus()
    def on_enter_reg_pass(event):
        reg_entry_confirm_pass.focus()
    def on_enter_reg_confirm(event):
        reg_entry_phone.focus()
    def on_enter_reg_phone(event):
        reg_entry_address.focus()
    def on_enter_reg_address(event):
        register()
    
    reg_entry_user.bind('<Return>', on_enter_reg_user)
    reg_entry_name.bind('<Return>', on_enter_reg_name)
    reg_entry_pass.bind('<Return>', on_enter_reg_pass)
    reg_entry_confirm_pass.bind('<Return>', on_enter_reg_confirm)
    reg_entry_phone.bind('<Return>', on_enter_reg_phone)
    reg_entry_address.bind('<Return>', on_enter_reg_address)


# Hiển thị giao diện đăng nhập
def show_login():
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Shop Shoes - Đăng nhập")
    root.geometry("720x720")  # Tăng height cho nút đăng ký
    
    main_frame = tk.Frame(root, bg='#ecf0f1')
    main_frame.pack(fill='both', expand=True)
    
    login_frame = tk.Frame(main_frame, bg='white', padx=30, pady=30)
    login_frame.pack(expand=True)
    
    tk.Label(login_frame, text="ĐĂNG NHẬP", font=('Arial', 18, 'bold'), 
             bg='white', fg='#2c3e50').pack(pady=(0, 20))
    
    tk.Label(login_frame, text="Tên đăng nhập:", font=('Arial', 15), bg='white').pack(anchor='w')
    global entry_user
    entry_user = tk.Entry(login_frame, font=('Arial', 15), width=25)
    entry_user.pack(pady=(5, 15))
    
    tk.Label(login_frame, text="Mật khẩu:", font=('Arial', 15), bg='white').pack(anchor='w')
    frame_pass = tk.Frame(login_frame, bg='white')
    frame_pass.pack(pady=(5, 20))
    
    global entry_pass, btn_eye
    entry_pass = tk.Entry(frame_pass, show='*', font=('Arial', 15), width=20)
    entry_pass.pack(side='left')
    
    btn_eye = tk.Button(frame_pass, text='👁‍🗨', command=toggle_password, 
                       relief='flat', bg='white', font=('Arial', 12))
    btn_eye.pack(side='left', padx=(5, 0))
    
    # THÊM BUTTONS
    btn_frame = tk.Frame(login_frame, bg='white')
    btn_frame.pack()
    
    btn_login = tk.Button(btn_frame, text="Đăng nhập", command=login,
                         bg='#3498db', fg='white', font=('Arial', 15, 'bold'),
                         width=15, height=2, relief='flat')
    btn_login.pack(pady=(0, 10))
    
    btn_register_link = tk.Button(btn_frame, text="Đăng ký tài khoản", command=show_register,
                                 bg='#27ae60', fg='white', font=('Arial', 15, 'bold'),
                                 width=15, height=2, relief='flat')
    btn_register_link.pack()
    
    def on_enter(event):
        login()
    
    entry_user.bind('<Return>', on_enter)
    entry_pass.bind('<Return>', on_enter)
    entry_user.focus()

# THÊM FUNCTION XỬ LÝ FULL SCREEN
def toggle_fullscreen(event=None):
    """Toggle giữa full screen và window mode"""
    current_state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not current_state)
    
    # Nếu thoát fullscreen, về kích thước window bình thường
    if current_state:  # Đang fullscreen -> về window
        if root.title().startswith("Shop Shoes - Đăng nhập"):
            root.geometry("720x720")
        elif root.title().startswith("Shop Shoes - Đăng ký"):
            root.geometry("720x900")
        elif root.title().startswith("Shop Shoes - Danh sách"):
            root.geometry("1200x700")  # Cập nhật kích thước mới

def exit_fullscreen(event=None):
    """Thoát fullscreen khi nhấn Escape"""
    root.attributes('-fullscreen', False)
    # Trả về kích thước bình thường
    if root.title().startswith("Shop Shoes - Đăng nhập"):
        root.geometry("720x720")
    elif root.title().startswith("Shop Shoes - Đăng ký"):
        root.geometry("720x900")
    elif root.title().startswith("Shop Shoes - Danh sách"):
        root.geometry("1200x700")  # Cập nhật kích thước mới

# Khởi tạo giao diện

root = tk.Tk()
icon = tk.PhotoImage(file=r'd:\codeptit\Python\bangiay\image.png')
root.iconphoto(True,icon)
root.configure(bg='#ecf0f1')
root.resizable(True, True)
root.bind('<F11>', toggle_fullscreen)    # F11 để toggle fullscreen
root.bind('<Escape>', exit_fullscreen)   # Escape để thoát fullscreen

show_login()
root.mainloop()