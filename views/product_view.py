"""
Product View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import urllib.request
import io
import os
from config.database import get_db_connection, BASE_DIR, LOCAL_IMAGE_DIR
from utils.image_utils import load_image_safely, load_thumbnail_image

class ProductView:
    def __init__(self, root):
        self.root = root
        self.cart = {}  # Memory cart for UI sync

    def load_cart_from_database(self, username):
        """Load cart data from database - from main.py"""
        if not username:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get MaKH from username
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return

            ma_kh = result[0]

            # Get MaGH from MaKH
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()
            if not gh_result:
                return

            ma_gh = gh_result[0]

            # Get all products in cart from database
            cursor.execute("""
                SELECT MaSP, SoLuong FROM giohangchuasanpham 
                WHERE MaGH = %s
            """, (ma_gh,))

            cart_items = cursor.fetchall()

            # Clear and reload cart from database
            self.cart.clear()
            for ma_sp, so_luong in cart_items:
                self.cart[ma_sp] = so_luong

            print(f"Debug: Loaded cart from database: {self.cart}")

        except Exception as e:
            print(f"Error loading cart from database: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_shoes(self, role=None, username=None):
        """Show product list - from main.py"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Danh sách sản phẩm")
        self.root.geometry("1200x750")

        # Load cart data from database when login
        if role == "buyer":
            self.load_cart_from_database(username)

        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
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

            btn_cart = tk.Button(header_container, text=update_cart_button(),
                                command=lambda: self.show_cart_callback(username, role) if hasattr(self, 'show_cart_callback') else None,
                                bg='#f39c12', fg='white', relief='flat',
                                font=('Arial', 12, 'bold'), padx=15, pady=5)
            btn_cart.pack(side='right', pady=15, padx=(0, 10))
        else:
            # Product management button for employees
            btn_add_product = tk.Button(header_container, text="➕ Thêm sản phẩm", command=lambda: self.show_add_product_form(role, username),
                                       bg='#27ae60', fg='white', relief='flat',
                                       font=('Arial', 12, 'bold'), padx=15, pady=5)
            btn_add_product.pack(side='right', pady=15, padx=(0, 10))

        btn_logout = tk.Button(header_container, text="Đăng xuất",
                              command=lambda: self.logout_callback() if hasattr(self, 'logout_callback') else None,
                              bg='#e74c3c', fg='white', relief='flat',
                              font=('Arial', 15), padx=15, pady=5)
        btn_logout.pack(side='right', pady=15)

        if username:
            role_label = "Người bán" if role == "seller" else "Khách hàng"
            tk.Label(header_container, text=f"{role_label}: {username}",
                     font=('Arial', 14), fg='white', bg='#2c3e50').pack(side='right', pady=15, padx=(0, 15))

        # Search and Filter Frame
        search_frame = tk.Frame(self.root, bg='#ecf0f1', height=80)
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

        # Load product data and images
        all_products = []
        product_images = {}
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get product info with brand
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong
                FROM sanpham sp
                LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
                ORDER BY sp.TenSP
            """)
            all_products = cursor.fetchall()

            # Get brand list for combobox
            cursor.execute("SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH")
            brands = ["Tất cả"] + [row[0] for row in cursor.fetchall()]
            brand_combo['values'] = brands

            # Get all images for each product
            cursor.execute("""
                SELECT MaSP, URLAnh
                FROM url_sp
                ORDER BY MaSP
            """)
            image_rows = cursor.fetchall()

            # Organize images by product
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

        main_frame = tk.Frame(self.root)
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

            # Save to database instead of just memory
            conn = None
            cursor = None
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Get MaKH from username
                cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
                    return

                ma_kh = result[0]

                # Check and create cart if not exists
                cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
                gh_result = cursor.fetchone()

                if not gh_result:
                    # Create new cart ID
                    cursor.execute("SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang")
                    max_result = cursor.fetchone()
                    next_id = (max_result[0] + 1) if max_result[0] else 1
                    ma_gh = f"GH{next_id:03d}"

                    cursor.execute("INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)", (ma_gh, ma_kh))
                else:
                    ma_gh = gh_result[0]

                # Check if product already in cart (with default color and size)
                cursor.execute("""
                    SELECT SoLuong FROM giohangchuasanpham 
                    WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
                """, (ma_gh, ma_sp))

                existing = cursor.fetchone()

                if existing:
                    # Increase quantity
                    new_quantity = existing[0] + 1
                    cursor.execute("""
                        UPDATE giohangchuasanpham 
                        SET SoLuong = %s 
                        WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
                    """, (new_quantity, ma_gh, ma_sp))
                else:
                    # Add new product with default color and size
                    cursor.execute("""
                        INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
                        VALUES (%s, %s, 'Đen', '42', 1)
                    """, (ma_gh, ma_sp))

                conn.commit()

                # Update memory cart to sync with UI (temporary)
                if ma_sp in self.cart:
                    self.cart[ma_sp] += 1
                else:
                    self.cart[ma_sp] = 1

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
                self.show_shoes(role, username)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

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

        # Right panel: Product details and image gallery
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

        # Canvas for scrolling thumbnails
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

        # Functions for handling images
        def show_main_image(image_url):
            """Display main image"""
            try:
                # Clear current image
                for widget in main_image_frame.winfo_children():
                    widget.destroy()

                if image_url:
                    img = load_image_safely(image_url)
                    if img:
                        # Resize to fit main display area
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
            """Update thumbnail gallery"""
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
                        # Fallback button if can't load image
                        thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}",
                                             command=lambda url=image_url: show_main_image(url),
                                             width=8, height=4, cursor='hand2',
                                             relief='solid', bd=2, bg='white')
                        thumb_btn.pack(side='left', padx=3, pady=3)

                except Exception as e:
                    print(f"Error creating thumbnail {i+1}: {e}")
                    # Create placeholder button
                    thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}",
                                         command=lambda url=image_url: show_main_image(url),
                                         width=8, height=4, cursor='hand2',
                                         relief='solid', bd=2, bg='white')
                    thumb_btn.pack(side='left', padx=3, pady=3)

        # Mouse wheel scroll for thumbnail canvas
        def on_mousewheel(event):
            thumbnail_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

        thumbnail_canvas.bind("<MouseWheel>", on_mousewheel)

    def show_add_product_form(self, role, username):
        """Show add product form - from main.py"""
        # Create add product window
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm sản phẩm mới")
        add_window.geometry("500x600")
        add_window.resizable(False, False)
        add_window.grab_set()  # Make window modal

        # Center the window
        add_window.transient(self.root)
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
                self.show_shoes(role, username)

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

    def set_show_cart_callback(self, callback):
        """Set callback for showing cart"""
        self.show_cart_callback = callback

    def set_logout_callback(self, callback):
        """Set logout callback"""
        self.logout_callback = callback

def load_thumbnail_image(path_or_url):
    """Load thumbnail image 70x70 - from main.py"""
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
        print(f"Error loading thumbnail from {source}: {e}")
        return None
