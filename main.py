import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import urllib.request
import io
import os

# Import các module đã tạo
from config.database import get_db_connection, BASE_DIR, LOCAL_IMAGE_DIR
from models.user import authenticate_user, register_user, generate_customer_id, generate_staff_id
from utils.image_utils import load_image_safely, load_thumbnail_image

# Global variables
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

    try:
        role = authenticate_user(username, password)
        if role:
            show_shoes(role=role, username=username)
        else:
            messagebox.showerror("Lỗi", "Sai thông tin đăng nhập!")
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối database: {str(e)}")

# Đăng ký
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

    try:
        success = register_user(username, password, role, phone, address, full_name)
        if success:
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            show_login()
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đăng ký: {str(e)}")

# Toggle password functions
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
        

# Function để load giỏ hàng từ database khi đăng nhập
def load_cart_from_database(username):
    """Load dữ liệu giỏ hàng từ database vào memory cart"""
    if not username:
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Lấy MaKH từ username
        cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
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

        # Lấy tất cả sản phẩm trong giỏ hàng từ database
        cursor.execute("""
            SELECT MaSP, SoLuong FROM giohangchuasanpham 
            WHERE MaGH = %s
        """, (ma_gh,))

        cart_items = cursor.fetchall()

        # Clear và load lại cart từ database
        if hasattr(show_shoes, 'cart'):
            show_shoes.cart.clear()
        else:
            show_shoes.cart = {}

        for ma_sp, so_luong in cart_items:
            show_shoes.cart[ma_sp] = so_luong

        print(f"Debug: Loaded cart from database: {show_shoes.cart}")

    except Exception as e:
        print(f"Error loading cart from database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Hiển thị danh sách giày
def show_shoes(role=None, username=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shop Shoes - Danh sách sản phẩm")
    root.geometry("1200x750")  # Tăng height để chứa search bar

    # Global cart storage (only for buyers) - Load từ database
    if role == "buyer" and not hasattr(show_shoes, 'cart'):
        show_shoes.cart = {}
        # Load cart data từ database khi đăng nhập
        load_cart_from_database(username)

    header_frame = tk.Frame(root, bg='#2c3e50', height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)

    header_container = tk.Frame(header_frame, bg='#2c3e50')
    header_container.pack(fill='both', expand=True, padx=10)

    tk.Label(header_container, text="SHOP GIÀY", font=('Arial', 20, 'bold'),
             fg='white', bg='#2c3e50').pack(side='left', pady=15)

    # Role-specific buttons
    if role == "buyer":
        # Cart button for buyers
        def update_cart_button():
            """Calculate cart count from database for current user"""
            if not username:
                return "🛒 Giỏ hàng (0)"

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Get MaKH from username
                cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
                result = cursor.fetchone()
                if not result:
                    return "🛒 Giỏ hàng (0)"

                ma_kh = result[0]

                # Get MaGH from MaKH
                cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
                gh_result = cursor.fetchone()
                if not gh_result:
                    return "🛒 Giỏ hàng (0)"

                ma_gh = gh_result[0]

                # Calculate total quantity from giohangchuasanpham
                cursor.execute("SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))
                count_result = cursor.fetchone()
                cart_count = count_result[0] if count_result and count_result[0] else 0

                return f"🛒 Giỏ hàng ({cart_count})"

            except Exception as e:
                print(f"Error calculating cart count: {e}")
                return "🛒 Giỏ hàng (0)"
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        btn_cart = tk.Button(header_container, text=update_cart_button(), command=lambda: show_cart(username, role),
                            bg='#f39c12', fg='white', relief='flat',
                            font=('Arial', 12, 'bold'), padx=15, pady=5)
        btn_cart.pack(side='right', pady=15, padx=(0, 10))
    else:
        # Product management button for employees
        btn_add_product = tk.Button(header_container, text="➕ Thêm sản phẩm", command=lambda: show_add_product_form(),
                                   bg='#27ae60', fg='white', relief='flat',
                                   font=('Arial', 12, 'bold'), padx=15, pady=5)
        btn_add_product.pack(side='right', pady=15, padx=(0, 10))

    btn_logout = tk.Button(header_container, text="Đăng xuất", command=show_login,
                          bg='#e74c3c', fg='white', relief='flat',
                          font=('Arial', 15), padx=15, pady=5)
    btn_logout.pack(side='right', pady=15)

    if username:
        role_label = "Người bán" if role == "seller" else "Khách hàng"
        tk.Label(header_container, text=f"{role_label}: {username}",
                 font=('Arial', 14), fg='white', bg='#2c3e50').pack(side='right', pady=15, padx=(0, 15))

    # Search and Filter Frame
    search_frame = tk.Frame(root, bg='#ecf0f1', height=80)
    search_frame.pack(fill='x', padx=10, pady=(5, 0))
    search_frame.pack_propagate(False)

    # Search bar
    search_container = tk.Frame(search_frame, bg='#ecf0f1')
    search_container.pack(side='left', fill='y', pady=10)

    tk.Label(search_container, text="Tìm kiếm:", font=('Arial', 12, 'bold'),
             bg='#ecf0f1').pack(side='left', padx=(10, 5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_container, textvariable=search_var, font=('Arial', 12), width=25)
    search_entry.pack(side='left', padx=5)

    btn_search = tk.Button(search_container, text="🔍",
                          bg='#3498db', fg='white', font=('Arial', 12, 'bold'), padx=10)
    btn_search.pack(side='left', padx=5)

    # Filter frame
    filter_container = tk.Frame(search_frame, bg='#ecf0f1')
    filter_container.pack(side='right', fill='y', pady=10, padx=(0, 10))

    # Brand filter
    tk.Label(filter_container, text="Thương hiệu:", font=('Arial', 12, 'bold'),
             bg='#ecf0f1').pack(side='left', padx=(10, 5))

    brand_var = tk.StringVar(value="Tất cả")
    brand_combo = ttk.Combobox(filter_container, textvariable=brand_var, width=12, state='readonly')
    brand_combo.pack(side='left', padx=5)

    # Price filter
    tk.Label(filter_container, text="Giá:", font=('Arial', 12, 'bold'),
             bg='#ecf0f1').pack(side='left', padx=(10, 5))

    price_var = tk.StringVar(value="Tất cả")
    price_combo = ttk.Combobox(filter_container, textvariable=price_var, width=12, state='readonly',
                              values=["Tất cả", "Dưới 500k", "500k - 1tr", "1tr - 2tr", "Trên 2tr"])
    price_combo.pack(side='left', padx=5)

    btn_filter = tk.Button(filter_container, text="Lọc",
                          bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), padx=10)
    btn_filter.pack(side='left', padx=5)

    # Load product data và images
    all_products = []
    product_images = {}
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Lấy thông tin sản phẩm với thương hiệu
        cursor.execute("""
            SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong
            FROM sanpham sp
            LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
            ORDER BY sp.TenSP
        """)
        all_products = cursor.fetchall()

        # Lấy danh sách thương hiệu cho combobox
        cursor.execute("SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH")
        brands = ["Tất cả"] + [row[0] for row in cursor.fetchall()]
        brand_combo['values'] = brands

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
    main_frame.pack(fill='both', expand=True, padx=10, pady=5)

    # Left panel: Product list
    list_frame = tk.Frame(main_frame, width=400)
    list_frame.pack(side='left', fill='y', padx=(0, 10))
    list_frame.pack_propagate(False)

    tk.Label(list_frame, text="Danh sách giày", font=('Arial', 18, 'bold')).pack(anchor='w', pady=(0, 10))

    tree_frame = tk.Frame(list_frame)
    tree_frame.pack(fill='both', expand=True)

    # Add quantity column for sellers
    if role == "seller":
        tree = ttk.Treeview(tree_frame, columns=("Tên", "Giá", "SL"), show="headings", height=12)
        tree.heading("Tên", text="Tên giày")
        tree.heading("Giá", text="Giá")
        tree.heading("SL", text="SL")
        tree.column("Tên", width=200)
        tree.column("Giá", width=100, anchor='e')
        tree.column("SL", width=50, anchor='e')
    else:
        tree = ttk.Treeview(tree_frame, columns=("Tên", "Giá"), show="headings", height=12)
        tree.heading("Tên", text="Tên giày")
        tree.heading("Giá", text="Giá")
        tree.column("Tên", width=250)
        tree.column("Giá", width=130, anchor='e')

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Action button frame
    action_button_frame = tk.Frame(list_frame)
    action_button_frame.pack(fill='x', pady=(5, 0))

    if role == "buyer":
        # Add to cart button for buyers
        btn_add_to_cart = tk.Button(action_button_frame, text="➕ Thêm vào giỏ hàng",
                                   bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                                   padx=10, pady=8, relief='raised', state='disabled',
                                   cursor='hand2', bd=2)
        btn_add_to_cart.pack(anchor='w', pady=5)

        status_label = tk.Label(action_button_frame, text="Chọn sản phẩm để kích hoạt nút",
                               font=('Arial', 10), fg='#7f8c8d')
        status_label.pack(anchor='w')
    else:
        # Delete product button for sellers
        btn_delete_product = tk.Button(action_button_frame, text="🗑️ Xóa sản phẩm",
                                      bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                      padx=10, pady=8, relief='raised', state='disabled',
                                      cursor='hand2', bd=2)
        btn_delete_product.pack(anchor='w', pady=5)

        status_label = tk.Label(action_button_frame, text="Chọn sản phẩm để xóa",
                               font=('Arial', 10), fg='#7f8c8d')
        status_label.pack(anchor='w')

    # Functions
    def add_to_cart(ma_sp, ten_sp):
        if role != "buyer":
            return

        print(f"Debug: Adding {ten_sp} to cart")

        # Lưu vào database thay vì chỉ lưu trong memory
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Lấy MaKH từ username
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
                return

            ma_kh = result[0]

            # Kiểm tra và tạo giỏ hàng nếu chưa có
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()

            if not gh_result:
                # Tạo mã giỏ hàng mới
                cursor.execute("SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang")
                max_result = cursor.fetchone()
                next_id = (max_result[0] + 1) if max_result[0] else 1
                ma_gh = f"GH{next_id:03d}"

                cursor.execute("INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)", (ma_gh, ma_kh))
            else:
                ma_gh = gh_result[0]

            # Kiểm tra sản phẩm đã có trong giỏ hàng chưa (với màu sắc và size mặc định)
            cursor.execute("""
                SELECT SoLuong FROM giohangchuasanpham 
                WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
            """, (ma_gh, ma_sp))

            existing = cursor.fetchone()

            if existing:
                # Tăng số lượng
                new_quantity = existing[0] + 1
                cursor.execute("""
                    UPDATE giohangchuasanpham 
                    SET SoLuong = %s 
                    WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
                """, (new_quantity, ma_gh, ma_sp))
            else:
                # Thêm sản phẩm mới với màu sắc và size mặc định
                cursor.execute("""
                    INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
                    VALUES (%s, %s, 'Đen', '42', 1)
                """, (ma_gh, ma_sp))

            conn.commit()

            # Cập nhật memory cart để đồng bộ với UI (tạm thời)
            if ma_sp in show_shoes.cart:
                show_shoes.cart[ma_sp] += 1
            else:
                show_shoes.cart[ma_sp] = 1

            # Update cart button
            btn_cart.config(text=update_cart_button())
            messagebox.showinfo("Thành công", f"Đã thêm {ten_sp} vào giỏ hàng!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm vào giỏ hàng: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_product(ma_sp, ten_sp):
        if role != "seller":
            return

        result = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sản phẩm '{ten_sp}' không?")
        if not result:
            return

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Delete product images first
            cursor.execute("DELETE FROM url_sp WHERE MaSP = %s", (ma_sp,))

            # Delete product
            cursor.execute("DELETE FROM sanpham WHERE MaSP = %s", (ma_sp,))

            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa sản phẩm '{ten_sp}' thành công!")

            # Refresh the product list
            show_shoes(role, username)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_add_product_form():
        # Create add product window
        add_window = tk.Toplevel(root)
        add_window.title("Thêm sản phẩm mới")
        add_window.geometry("500x600")
        add_window.resizable(False, False)
        add_window.grab_set()  # Make window modal

        # Center the window
        add_window.transient(root)
        add_window.focus()

        # Form fields
        tk.Label(add_window, text="THÊM SẢN PHẨM MỚI", font=('Arial', 16, 'bold'), fg='#2c3e50').pack(pady=20)

        # Product name
        tk.Label(add_window, text="Tên sản phẩm:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        entry_name = tk.Entry(add_window, font=('Arial', 12), width=40)
        entry_name.pack(padx=20, pady=(0, 10))

        # Price
        tk.Label(add_window, text="Giá (VNĐ):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        entry_price = tk.Entry(add_window, font=('Arial', 12), width=40)
        entry_price.pack(padx=20, pady=(0, 10))

        # Brand
        tk.Label(add_window, text="Thương hiệu:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        brand_var_add = tk.StringVar()
        brand_combo_add = ttk.Combobox(add_window, textvariable=brand_var_add, font=('Arial', 12), width=37, state='readonly')

        # Load brands
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH")
            brands_data = cursor.fetchall()
            brand_combo_add['values'] = [f"{th[1]} ({th[0]})" for th in brands_data]
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách thương hiệu: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        brand_combo_add.pack(padx=20, pady=(0, 10))

        # Quantity
        tk.Label(add_window, text="Số lượng:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        entry_quantity = tk.Entry(add_window, font=('Arial', 12), width=40)
        entry_quantity.pack(padx=20, pady=(0, 10))

        # Description
        tk.Label(add_window, text="Mô tả:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        text_description = tk.Text(add_window, font=('Arial', 11), width=42, height=6, wrap='word')
        text_description.pack(padx=20, pady=(0, 10))

        # Image URLs
        tk.Label(add_window, text="URL hình ảnh (mỗi URL một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=(10, 5))
        text_images = tk.Text(add_window, font=('Arial', 11), width=42, height=4, wrap='word')
        text_images.pack(padx=20, pady=(0, 20))

        # Buttons
        button_frame = tk.Frame(add_window)
        button_frame.pack(pady=10)

        def save_product():
            # Get form data
            name = entry_name.get().strip()
            price_str = entry_price.get().strip()
            brand_selection = brand_var_add.get()
            quantity_str = entry_quantity.get().strip()
            description = text_description.get(1.0, tk.END).strip()
            image_urls = text_images.get(1.0, tk.END).strip()

            # Validation
            if not all([name, price_str, brand_selection, quantity_str]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
                return

            try:
                price = float(price_str)
                if price <= 0:
                    raise ValueError("Giá phải lớn hơn 0")
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Số lượng phải >= 0")
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {str(e)}")
                return

            # Extract brand ID
            try:
                brand_id = brand_selection.split('(')[1].replace(')', '')
            except:
                messagebox.showerror("Lỗi", "Vui lòng chọn thương hiệu!")
                return

            # Generate product ID
            conn = None
            cursor = None
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Generate new product ID
                cursor.execute("SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'")
                result = cursor.fetchone()
                next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
                product_id = f"SP{next_number:03d}"

                # Insert product
                cursor.execute("""
                    INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (product_id, name, price, description if description else None, brand_id, quantity))

                # Insert image URLs if provided
                if image_urls:
                    urls = [url.strip() for url in image_urls.split('\n') if url.strip()]
                    for url in urls:
                        cursor.execute("INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)", (product_id, url))

                conn.commit()
                messagebox.showinfo("Thành công", f"Đã thêm sản phẩm '{name}' thành công!")
                add_window.destroy()

                # Refresh the product list
                show_shoes(role, username)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        tk.Button(button_frame, text="Lưu", command=save_product,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), padx=20).pack(side='left', padx=10)
        tk.Button(button_frame, text="Hủy", command=add_window.destroy,
                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'), padx=20).pack(side='left', padx=10)

    # Filter products function
    def filter_products():
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)

        search_text = search_var.get().lower().strip()
        selected_brand = brand_var.get()
        selected_price = price_var.get()

        filtered_products = []

        for ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong in all_products:
            # Filter by search text
            if search_text and search_text not in ten_sp.lower():
                continue

            # Filter by brand
            if selected_brand != "Tất cả" and ten_th != selected_brand:
                continue

            # Filter by price
            if selected_price != "Tất cả" and gia:
                price_val = float(gia)
                if selected_price == "Dưới 500k" and price_val >= 500000:
                    continue
                elif selected_price == "500k - 1tr" and (price_val < 500000 or price_val >= 1000000):
                    continue
                elif selected_price == "1tr - 2tr" and (price_val < 1000000 or price_val >= 2000000):
                    continue
                elif selected_price == "Trên 2tr" and price_val < 2000000:
                    continue

            filtered_products.append((ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong))

        # Populate treeview
        product_data.clear()
        for ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong in filtered_products:
            price_display = f"{float(gia):,.0f} VNĐ" if gia is not None else "N/A"
            if role == "seller":
                tree.insert("", "end", iid=ma_sp, values=(ten_sp, price_display, so_luong))
            else:
                tree.insert("", "end", iid=ma_sp, values=(ten_sp, price_display))
            product_data[ma_sp] = {
                "name": ten_sp,
                "price": price_display,
                "description": (mo_ta or "Chưa có mô tả cho sản phẩm này.").strip(),
                "images": product_images.get(ma_sp, []),
                "quantity": so_luong
            }

    # Bind filter events
    btn_search.config(command=filter_products)
    btn_filter.config(command=filter_products)
    search_entry.bind('<Return>', lambda e: filter_products())

    # Populate initial data
    product_data = {}
    filter_products()  # This will populate the tree

    # Handle product selection and enable action button
    selected_product_id = None

    def on_product_select_combined(event):
        nonlocal selected_product_id
        selection = tree.selection()

        if selection:
            selected_product_id = selection[0]

            if selected_product_id in product_data:
                if role == "buyer":
                    # Enable add to cart button
                    btn_add_to_cart.config(state='normal', bg='#27ae60')
                    status_label.config(text="Nút đã được kích hoạt - Click để thêm vào giỏ!", fg='green')
                    btn_add_to_cart.config(command=lambda: add_to_cart(selected_product_id, product_data[selected_product_id]["name"]))
                else:
                    # Enable delete product button
                    btn_delete_product.config(state='normal', bg='#e74c3c')
                    status_label.config(text="Click để xóa sản phẩm đã chọn", fg='red')
                    btn_delete_product.config(command=lambda: delete_product(selected_product_id, product_data[selected_product_id]["name"]))

                # Update product details on the right panel
                product = product_data[selected_product_id]

                # Update product name
                if role == "seller":
                    product_name_label.config(text=f"{product['name']} (SL: {product['quantity']})")
                else:
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
        else:
            selected_product_id = None
            if role == "buyer":
                btn_add_to_cart.config(state='disabled', bg='#95a5a6')
                status_label.config(text="Click sản phẩm để thêm vào giỏ hàng", fg='#7f8c8d')
            else:
                btn_delete_product.config(state='disabled', bg='#95a5a6')
                status_label.config(text="Chọn sản phẩm để xóa", fg='#7f8c8d')

    # ONLY bind this event - remove any other bindings
    tree.bind("<<TreeviewSelect>>", on_product_select_combined)

    # Right panel: Product details và image gallery
    detail_frame = tk.Frame(main_frame, bg='#f8f9fa')
    detail_frame.pack(side='right', fill='both', expand=True)

    # Product name
    product_name_label = tk.Label(detail_frame, text="Chọn sản phẩm để xem chi tiết",
                                  font=('Arial', 18, 'bold'), bg='#f8f9fa', fg='#2c3e50')
    product_name_label.pack(pady=(15, 10))

    # Main image display area
    main_image_frame = tk.Frame(detail_frame, bg='white', relief='solid', bd=1, height=300)
    main_image_frame.pack(fill='x', padx=15, pady=(0, 10))
    main_image_frame.pack_propagate(False)

    main_image_label = tk.Label(main_image_frame, text="Hình ảnh sản phẩm",
                               font=('Arial', 14), bg='white', fg='#6c757d')
    main_image_label.pack(expand=True)

    # Thumbnail gallery section
    gallery_section = tk.Frame(detail_frame, bg='#f8f9fa')
    gallery_section.pack(fill='x', padx=15, pady=(0, 10))

    tk.Label(gallery_section, text="Các ảnh khác:", font=('Arial', 12, 'bold'),
             bg='#f9f9fa').pack(anchor='w', pady=(0, 5))

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
             bg='#f9f9fa').pack(anchor='w', pady=(0, 5))

    desc_text = tk.Text(desc_section, height=5, wrap='word', font=('Arial', 11),
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
                    main_image_label_new = tk.Label(main_image_frame, image=img, bg='white')
                    main_image_label_new.image = img  # Keep reference
                    main_image_label_new.pack(expand=True)
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
                thumb_img = load_thumbnail_image(image_url)
                if thumb_img:
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

# FUNCTION HIỂN THỊ GIỎ HÀNG
def show_cart(username, role="buyer"):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shop Shoes - Giỏ hàng")
    root.geometry("1000x700")

    header_frame = tk.Frame(root, bg='#2c3e50', height=60)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)

    header_container = tk.Frame(header_frame, bg='#2c3e50')
    header_container.pack(fill='both', expand=True, padx=10)

    tk.Label(header_container, text="GIỎ HÀNG", font=('Arial', 20, 'bold'),
             fg='white', bg='#2c3e50').pack(side='left', pady=15)

    btn_back = tk.Button(header_container, text="← Quay lại",
                        command=lambda: show_shoes(role=role, username=username),
                        bg='#f39c12', fg='white', relief='flat',
                        font=('Arial', 12, 'bold'), padx=15, pady=5)
    btn_back.pack(side='right', pady=15, padx=(0, 10))

    btn_logout = tk.Button(header_container, text="Đăng xuất", command=show_login,
                          bg='#e74c3c', fg='white', relief='flat',
                          font=('Arial', 15), padx=15, pady=5)
    btn_logout.pack(side='right', pady=15)

    if username:
        tk.Label(header_container, text=f"Khách hàng: {username}",
                 font=('Arial', 14), fg='white', bg='#2c3e50').pack(side='right', pady=15, padx=(0, 15))

    main_frame = tk.Frame(root, bg='#f8f9fa')
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

        # Cập nhật memory cart để đồng bộ với UI
        if hasattr(show_shoes, 'cart'):
            show_shoes.cart.clear()
            for ma_sp, _, _, _, _, so_luong, _ in cart_items:
                if ma_sp in show_shoes.cart:
                    show_shoes.cart[ma_sp] += so_luong
                else:
                    show_shoes.cart[ma_sp] = so_luong

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
            show_cart(username, role)

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
                         command=lambda: clear_cart_db(username, role),
                         bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                         padx=20, pady=10, relief='flat', cursor='hand2')
    btn_clear.pack(side='left')

    btn_view_invoice = tk.Button(button_frame, text="📄 Xem hóa đơn",
                           command=lambda: view_invoice_from_cart_db(username, role, cart_products, total_amount),
                           bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                           padx=20, pady=10, relief='flat', cursor='hand2')
    btn_view_invoice.pack(side='right')

def clear_cart_db(username, role="buyer"):
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

        # Clear memory cart
        if hasattr(show_shoes, 'cart'):
            show_shoes.cart.clear()

        messagebox.showinfo("Thành công", "Đã xóa tất cả sản phẩm!")
        show_cart(username, role)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa giỏ hàng: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def view_invoice_from_cart_db(username, role, cart_products, total_amount):
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

    # Hiển thị trang hóa đơn
    show_invoice_page(username, role, converted_products, total_amount)

def clear_cart(username, role="buyer"):
    result = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả sản phẩm trong giỏ hàng?")
    if result:
        show_shoes.cart.clear()
        show_cart(username, role)
        messagebox.showinfo("Thành công", "Đã xóa tất cả sản phẩm!")

def view_invoice_from_cart(username, role, total_amount):
    """Xem hóa đơn từ giỏ hàng trong main.py"""
    if not hasattr(show_shoes, 'cart') or not show_shoes.cart:
        messagebox.showwarning("Cảnh báo", "Giỏ hàng trống!")
        return

    # Load product details from database
    conn = None
    cursor = None
    cart_products = {}

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for ma_sp, quantity in show_shoes.cart.items():
            cursor.execute("""
                SELECT TenSP, Gia FROM sanpham WHERE MaSP = %s
            """, (ma_sp,))
            result = cursor.fetchone()
            if result:
                ten_sp, gia = result
                price = float(gia) if gia else 0
                cart_products[ma_sp] = {
                    'name': ten_sp,
                    'price': price,
                    'quantity': quantity,
                    'total': price * quantity
                }

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu giỏ hàng: {str(e)}")
        return
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Hiển thị trang hóa đơn
    show_invoice_page(username, role, cart_products, total_amount)

def show_invoice_page(username, role, cart_products, total_amount):
    """Hiển thị trang hóa đơn chi tiết"""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shop Shoes - Hóa đơn chi tiết")
    root.geometry("1000x800")

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
    header_frame = tk.Frame(root, bg='#2c3e50', height=60)
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
                        command=lambda: show_cart(username, role),
                        bg='#95a5a6', fg='white', relief='flat',
                        font=('Arial', 12), padx=15, pady=8, cursor='hand2')
    btn_back.pack(side='right', pady=15)

    # Main content frame
    main_frame = tk.Frame(root, bg='white')
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
    from datetime import datetime
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

    # Create table for products
    table_frame = tk.Frame(products_frame, bg='white')
    table_frame.pack(fill='both', expand=True)

    # Table header
    header_table = tk.Frame(table_frame, bg='#34495e', height=40)
    header_table.pack(fill='x', pady=(0, 2))
    header_table.pack_propagate(False)

    tk.Label(header_table, text="STT", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=5).pack(side='left', padx=5, pady=5)
    tk.Label(header_table, text="Mã SP", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=8).pack(side='left', padx=5, pady=5)
    tk.Label(header_table, text="Tên sản phẩm", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=30).pack(side='left', padx=5, pady=5)
    tk.Label(header_table, text="Số lượng", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=10).pack(side='left', padx=5, pady=5)
    tk.Label(header_table, text="Đơn giá", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=15).pack(side='left', padx=5, pady=5)
    tk.Label(header_table, text="Thành tiền", font=('Arial', 12, 'bold'),
             bg='#34495e', fg='white', width=15).pack(side='left', padx=5, pady=5)

    # Product rows
    stt = 1
    for ma_sp, product in cart_products.items():
        row_frame = tk.Frame(table_frame, bg='white', relief='solid', bd=1, height=35)
        row_frame.pack(fill='x', pady=1)
        row_frame.pack_propagate(False)

        tk.Label(row_frame, text=str(stt), font=('Arial', 11),
                 bg='white', width=5).pack(side='left', padx=5, pady=5)
        tk.Label(row_frame, text=ma_sp, font=('Arial', 11),
                 bg='white', width=8).pack(side='left', padx=5, pady=5)
        tk.Label(row_frame, text=product['name'], font=('Arial', 11),
                 bg='white', width=30, anchor='w').pack(side='left', padx=5, pady=5)
        tk.Label(row_frame, text=str(product['quantity']), font=('Arial', 11),
                 bg='white', width=10).pack(side='left', padx=5, pady=5)
        tk.Label(row_frame, text=f"{product['price']:,.0f}", font=('Arial', 11),
                 bg='white', width=15).pack(side='left', padx=5, pady=5)
        tk.Label(row_frame, text=f"{product['total']:,.0f}", font=('Arial', 11),
                 bg='white', width=15).pack(side='left', padx=5, pady=5)
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
                           command=lambda: process_payment_main(username, role, cart_products, total_amount),
                           bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                           relief='flat', padx=40, pady=12, cursor='hand2')
    btn_payment.pack(side='right')

    # Print button
    btn_print = tk.Button(action_frame, text="🖨️ In hóa đơn", 
                         command=lambda: messagebox.showinfo("Thông báo", "Chức năng in hóa đơn sẽ được cập nhật!"),
                         bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                         relief='flat', padx=20, pady=10, cursor='hand2')
    btn_print.pack(side='left')

def process_payment_main(username, role, cart_products, total_amount):
    """Xử lý thanh toán từ trang hóa đơn trong main.py"""
    if not cart_products:
        messagebox.showwarning("Cảnh báo", "Không có sản phẩm để thanh toán!")
        return

    result = messagebox.askyesno("Xác nhận thanh toán",
                               f"Tổng tiền: {total_amount:,.0f} VNĐ\n\n"
                               f"Bạn có muốn tiến hành thanh toán?")
    if not result:
        return

    try:
        from datetime import datetime
        
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

        conn.commit()

        # Xóa giỏ hàng sau khi thanh toán
        show_shoes.cart.clear()

        messagebox.showinfo("Thành công", 
                          f"Thanh toán thành công!\n"
                          f"Mã hóa đơn: {ma_hd}\n"
                          f"Cảm ơn bạn đã mua hàng!")

        # Quay lại trang sản phẩm
        show_shoes(role=role, username=username)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xử lý thanh toán: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

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

