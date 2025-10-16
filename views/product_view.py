"""
Giao diện hiển thị sản phẩm - thiết kế giống hệt file gốc
"""
import tkinter as tk
from tkinter import ttk, messagebox
from views.base_view import BaseView
from models.product import get_all_products, get_product_images
from utils.image_utils import load_image_safely, load_thumbnail_image

class ProductView(BaseView):
    def __init__(self, role=None, username=None):
        super().__init__("Shop Shoes - Danh sách sản phẩm", "1400x800")  # Tăng kích thước cửa sổ
        self.role = role
        self.username = username
        self.product_data = {}
        self.product_images = {}
        # Add image reference storage to prevent garbage collection
        self.current_main_image = None
        self.thumbnail_images = []
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập giao diện sản phẩm với thanh tìm kiếm rõ ràng và giỏ hàng"""
        # Header frame giống file gốc
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=70)  # Tăng height cho cart
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        header_container = tk.Frame(header_frame, bg='#2c3e50')
        header_container.pack(fill='both', expand=True, padx=10)

        tk.Label(header_container, text="SHOP GIÀY", font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(side='left', pady=15)

        # Right side: Cart, User info, Logout
        right_header = tk.Frame(header_container, bg='#2c3e50')
        right_header.pack(side='right', pady=15)

        # Cart button với số lượng
        self.cart_count = 0
        cart_frame = tk.Frame(right_header, bg='#2c3e50')
        cart_frame.pack(side='right', padx=(0, 15))

        self.cart_btn = tk.Button(cart_frame, text=f"🛒 Giỏ hàng ({self.cart_count})",
                                 command=self.open_cart,
                                 bg='#f39c12', fg='white', relief='flat',
                                 font=('Arial', 12, 'bold'), padx=12, pady=8,
                                 cursor='hand2')
        self.cart_btn.pack()

        btn_logout = tk.Button(right_header, text="Đăng xuất", command=self.handle_logout,
                              bg='#e74c3c', fg='white', relief='flat',
                              font=('Arial', 12), padx=12, pady=8)
        btn_logout.pack(side='right', padx=(0, 10))

        if self.username:
            role_label = "Người bán" if self.role == "seller" else "Khách hàng"
            tk.Label(right_header, text=f"{role_label}: {self.username}",
                     font=('Arial', 11), fg='white', bg='#2c3e50').pack(side='right', padx=(0, 15))

        # Load product data và cart
        self.load_product_data()
        self.load_cart_count()

        # THANH TÌM KIẾM - Layout cải thiện với màu sắc rõ ràng
        search_outer = tk.Frame(self.root, bg='#34495e', relief='raised', bd=3)
        search_outer.pack(fill='x', padx=8, pady=(8, 0))

        search_frame = tk.Frame(search_outer, bg='#ecf0f1', relief='ridge', bd=2)
        search_frame.pack(fill='x', padx=3, pady=3)

        search_container = tk.Frame(search_frame, bg='#ecf0f1')
        search_container.pack(fill='x', padx=12, pady=10)

        # Search label với icon lớn hơn
        tk.Label(search_container, text="🔍 TÌM KIẾM SẢN PHẨM:",
                 font=('Arial', 13, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(side='left')

        # Search controls
        search_controls = tk.Frame(search_container, bg='#ecf0f1')
        search_controls.pack(side='right')

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_controls, textvariable=self.search_var,
                                    font=('Arial', 11), width=25, relief='solid', bd=2)
        self.search_entry.pack(side='left', padx=(0, 8))

        tk.Button(search_controls, text="Tìm kiếm", command=self.apply_filters,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', padx=12, pady=6, cursor='hand2').pack(side='left', padx=2)

        tk.Button(search_controls, text="Xóa", command=self.clear_search,
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                 relief='flat', padx=12, pady=6, cursor='hand2').pack(side='left', padx=2)

        # BỘ LỌC - Layout cải thiện
        filter_outer = tk.Frame(self.root, bg='#34495e', relief='raised', bd=3)
        filter_outer.pack(fill='x', padx=8, pady=(0, 8))

        filter_frame = tk.Frame(filter_outer, bg='#d5dbdb', relief='ridge', bd=2)
        filter_frame.pack(fill='x', padx=3, pady=3)

        filter_container = tk.Frame(filter_frame, bg='#d5dbdb')
        filter_container.pack(fill='x', padx=12, pady=8)

        # Brand filter
        brand_section = tk.Frame(filter_container, bg='#d5dbdb')
        brand_section.pack(side='left')

        tk.Label(brand_section, text="THƯƠNG HIỆU:", font=('Arial', 11, 'bold'),
                 bg='#d5dbdb', fg='#2c3e50').pack(side='left')

        self.brand_var = tk.StringVar(value="Tất cả")
        brand_options = tk.Frame(brand_section, bg='#d5dbdb')
        brand_options.pack(side='left', padx=(10, 20))

        for option in ["Tất cả", "Nike", "Adidas"]:
            tk.Radiobutton(brand_options, text=option, variable=self.brand_var, value=option,
                          bg='#d5dbdb', fg='#2c3e50', font=('Arial', 10),
                          selectcolor='#3498db', activebackground='#d5dbdb',
                          command=self.apply_filters, cursor='hand2').pack(side='left', padx=5)

        # Price sort
        price_section = tk.Frame(filter_container, bg='#d5dbdb')
        price_section.pack(side='left')

        tk.Label(price_section, text="SẮP XẾP GIÁ:", font=('Arial', 11, 'bold'),
                 bg='#d5dbdb', fg='#2c3e50').pack(side='left')

        self.price_sort_var = tk.StringVar(value="Mặc định")
        price_options = tk.Frame(price_section, bg='#d5dbdb')
        price_options.pack(side='left', padx=10)

        for option in ["Mặc định", "Giá thấp → cao", "Giá cao → thấp"]:
            tk.Radiobutton(price_options, text=option, variable=self.price_sort_var, value=option,
                          bg='#d5dbdb', fg='#2c3e50', font=('Arial', 10),
                          selectcolor='#e74c3c', activebackground='#d5dbdb',
                          command=self.apply_filters, cursor='hand2').pack(side='left', padx=5)

        # Main content frame - Giảm padding top để chừa chỗ cho search/filter
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=8, pady=(0, 8))

        # Left panel: Product list - Giảm kích thước hơn nữa
        left_panel = tk.Frame(main_frame, width=380)  # Giảm từ 420 xuống 380
        left_panel.pack(side='left', fill='y', padx=(0, 8))
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="Danh sách giày", font=('Arial', 15, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(0, 5))

        # Result count label
        self.result_label = tk.Label(left_panel, text="", font=('Arial', 9), fg='#7f8c8d')
        self.result_label.pack(anchor='w', pady=(0, 5))

        tree_frame = tk.Frame(left_panel)
        tree_frame.pack(fill='both', expand=True)

        # TreeView với nút Add to Cart
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # Tăng height để chứa button

        self.tree = ttk.Treeview(tree_frame, columns=("Tên", "Giá", "Thương hiệu", "Action"),
                                show="headings", height=10)  # Giảm height
        self.tree.heading("Tên", text="Tên giày")
        self.tree.heading("Giá", text="Giá")
        self.tree.heading("Thương hiệu", text="Thương hiệu")
        self.tree.heading("Action", text="")

        self.tree.column("Tên", width=160)  # Giảm width
        self.tree.column("Giá", width=90, anchor='e')
        self.tree.column("Thương hiệu", width=80, anchor='center')
        self.tree.column("Action", width=40, anchor='center')

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right panel: Product details - Giảm kích thước
        detail_frame = tk.Frame(main_frame, bg='#f8f9fa')
        detail_frame.pack(side='right', fill='both', expand=True)

        # Product name
        self.product_name_label = tk.Label(detail_frame, text="Chọn sản phẩm để xem chi tiết",
                                      font=('Arial', 16, 'bold'), bg='#f8f9fa', fg='#2c3e50')
        self.product_name_label.pack(pady=(10, 8))

        # Main image - Giảm height
        self.main_image_frame = tk.Frame(detail_frame, bg='white', relief='solid', bd=1, height=280)
        self.main_image_frame.pack(fill='x', padx=12, pady=(0, 8))
        self.main_image_frame.pack_propagate(False)

        self.main_image_label = tk.Label(self.main_image_frame, text="Hình ảnh sản phẩm",
                                   font=('Arial', 12), bg='white', fg='#6c757d')
        self.main_image_label.pack(expand=True)

        # Thumbnail gallery - Giảm height
        gallery_section = tk.Frame(detail_frame, bg='#f8f9fa')
        gallery_section.pack(fill='x', padx=12, pady=(0, 8))

        tk.Label(gallery_section, text="Các ảnh khác:", font=('Arial', 11, 'bold'),
                 bg='#f9f9fa').pack(anchor='w', pady=(0, 3))

        thumbnail_frame = tk.Frame(gallery_section, bg='white', height=60, relief='solid', bd=1)
        thumbnail_frame.pack(fill='x')
        thumbnail_frame.pack_propagate(False)

        self.thumbnail_canvas = tk.Canvas(thumbnail_frame, bg='white', height=58)
        self.thumbnail_scrollbar = ttk.Scrollbar(thumbnail_frame, orient='horizontal', command=self.thumbnail_canvas.xview)
        self.thumbnail_scrollable = tk.Frame(self.thumbnail_canvas, bg='white')

        self.thumbnail_scrollable.bind("<Configure>",
                                 lambda e: self.thumbnail_canvas.configure(scrollregion=self.thumbnail_canvas.bbox("all")))
        self.thumbnail_canvas.create_window((0, 0), window=self.thumbnail_scrollable, anchor="nw")
        self.thumbnail_canvas.configure(xscrollcommand=self.thumbnail_scrollbar.set)

        self.thumbnail_canvas.pack(side='top', fill='both', expand=True)
        self.thumbnail_scrollbar.pack(side='bottom', fill='x')

        # Description - Giảm height
        desc_section = tk.Frame(detail_frame, bg='#f8f9fa')
        desc_section.pack(fill='both', expand=True, padx=12, pady=(0, 10))

        tk.Label(desc_section, text="Mô tả sản phẩm:", font=('Arial', 11, 'bold'),
                 bg='#f9f9fa').pack(anchor='w', pady=(0, 3))

        self.desc_text = tk.Text(desc_section, height=4, wrap='word', font=('Arial', 10),  # Giảm height
                           state='disabled', bg='white', relief='solid', bd=1)
        self.desc_text.pack(fill='both', expand=True)

        # Add to cart section cho sản phẩm được chọn
        cart_section = tk.Frame(detail_frame, bg='#f8f9fa')
        cart_section.pack(fill='x', padx=12, pady=(0, 10))

        self.add_to_cart_btn = tk.Button(cart_section, text="🛒 THÊM VÀO GIỎ HÀNG",
                                        command=self.add_selected_to_cart,
                                        bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                        relief='flat', padx=20, pady=8, cursor='hand2',
                                        state='disabled')
        self.add_to_cart_btn.pack(pady=5)

        self.selected_product_id = None

        # Populate treeview
        self.populate_product_list()

        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)
        self.tree.bind("<Button-1>", self.on_tree_click)  # Handle add to cart clicks
        self.search_entry.bind('<Return>', lambda e: self.apply_filters())

        # Mouse wheel scroll
        def on_mousewheel(event):
            self.thumbnail_canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        self.thumbnail_canvas.bind("<MouseWheel>", on_mousewheel)

    def load_product_data(self):
        """Load dữ liệu sản phẩm và ảnh với thông tin thương hiệu"""
        try:
            # Load product data và images với thông tin thương hiệu
            product_rows = []
            product_images = {}  # Dictionary để lưu tất cả ảnh của mỗi sản phẩm
            conn = None
            cursor = None

            # Import mysql connector để kết nối database trực tiếp như file gốc
            import mysql.connector

            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep"
            )
            cursor = conn.cursor()

            # Sửa lại tên cột từ MaThuongHieu thành MaTH
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH
                FROM sanpham sp 
                LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
                ORDER BY sp.TenSP
            """)
            product_rows = cursor.fetchall()

            # Lấy tất cả ảnh của từng sản phẩm - giống file gốc
            cursor.execute("""
                SELECT MaSP, URLAnh
                FROM url_sp
                ORDER BY MaSP
            """)
            image_rows = cursor.fetchall()

            # Tổ chức ảnh theo sản phẩm - giống file gốc
            for ma_sp, url_anh in image_rows:
                if ma_sp not in product_images:
                    product_images[ma_sp] = []
                product_images[ma_sp].append(url_anh)

            # Tạo product_data với thông tin thương hiệu
            for ma_sp, ten_sp, gia, mo_ta, ten_thuong_hieu in product_rows:
                price_display = f"{float(gia):,.0f} VNĐ" if gia is not None else "N/A"
                brand_display = ten_thuong_hieu or "Khác"

                self.product_data[ma_sp] = {
                    "name": ten_sp,
                    "price": price_display,
                    "price_value": float(gia) if gia is not None else 0,  # Để sort
                    "brand": brand_display,
                    "description": (mo_ta or "Chưa có mô tả cho sản phẩm này.").strip(),
                    "images": product_images.get(ma_sp, [])
                }

            # Store original data for filtering
            self.original_product_data = self.product_data.copy()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            print(f"Chi tiết lỗi: {e}")  # Debug log
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def populate_product_list(self):
        """Điền dữ liệu vào treeview với thông tin thương hiệu và nút thêm giỏ hàng"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add filtered/sorted products với nút "+"
        for ma_sp, data in self.product_data.items():
            self.tree.insert("", "end", iid=ma_sp, values=(data["name"], data["price"], data["brand"], "➕"))

        # Update result count
        total_products = len(self.product_data)
        if hasattr(self, 'result_label'):
            if total_products == len(self.original_product_data):
                self.result_label.config(text=f"Hiển thị tất cả {total_products} sản phẩm")
            else:
                self.result_label.config(text=f"Tìm thấy {total_products} sản phẩm")

    def on_product_select(self, event):
        """Handle khi chọn sản phẩm - giống file gốc"""
        selection = self.tree.selection()
        if not selection:
            return

        ma_sp = selection[0]
        if ma_sp not in self.product_data:
            return

        product = self.product_data[ma_sp]

        # Update product name
        self.product_name_label.config(text=product["name"])

        # Update description
        self.desc_text.config(state='normal')
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(1.0, product["description"])
        self.desc_text.config(state='disabled')

        # Update images
        images = product["images"]
        if images:
            self.show_main_image(images[0])  # Show first image as main
            self.update_thumbnail_gallery(images)
        else:
            self.show_main_image(None)
            self.update_thumbnail_gallery([])

        # Enable "Add to Cart" button
        self.add_to_cart_btn.config(state='normal')
        self.selected_product_id = ma_sp  # Save selected product ID

    def show_main_image(self, image_url):
        """Hiển thị ảnh chính - giống file gốc"""
        try:
            # Clear current image
            for widget in self.main_image_frame.winfo_children():
                widget.destroy()

            if image_url:
                img = load_image_safely(image_url)
                if img:
                    # Resize để fit main display area
                    main_image_label = tk.Label(self.main_image_frame, image=img, bg='white')
                    main_image_label.image = img  # Keep reference
                    main_image_label.pack(expand=True)
                    # Store reference in the class to prevent garbage collection
                    self.current_main_image = img
                else:
                    tk.Label(self.main_image_frame, text="❌ Không thể tải hình ảnh",
                           font=('Arial', 14), bg='white', fg='#e74c3c').pack(expand=True)
                    print(f"Không thể tải ảnh từ: {image_url}")  # Debug log
            else:
                tk.Label(self.main_image_frame, text="Không có hình ảnh",
                       font=('Arial', 14), bg='white', fg='#6c757d').pack(expand=True)
        except Exception as e:
            print(f"Lỗi show_main_image: {e}")  # Debug log
            tk.Label(self.main_image_frame, text="Lỗi tải hình ảnh",
                   font=('Arial', 14), bg='white', fg='#e74c3c').pack(expand=True)

    def update_thumbnail_gallery(self, images):
        """Cập nhật gallery thumbnails - giống file gốc"""
        # Clear current thumbnails
        for widget in self.thumbnail_scrollable.winfo_children():
            widget.destroy()

        # Clear previous thumbnail references
        self.thumbnail_images = []

        if not images:
            tk.Label(self.thumbnail_scrollable, text="Không có ảnh khác",
                   font=('Arial', 10), bg='white', fg='#6c757d').pack(side='left', padx=10, pady=20)
            return

        for i, image_url in enumerate(images):
            try:
                # Load thumbnail image - giống file gốc
                img = load_image_safely(image_url)
                if img:
                    # Resize to thumbnail size (70x70) - giống file gốc
                    thumb_img = load_thumbnail_image(image_url)

                    if thumb_img:
                        # Store reference to prevent garbage collection
                        self.thumbnail_images.append(thumb_img)

                        # Create thumbnail button - giống file gốc
                        thumb_btn = tk.Button(self.thumbnail_scrollable, image=thumb_img,
                                             command=lambda url=image_url: self.show_main_image(url),
                                             relief='solid', bd=2, cursor='hand2',
                                             bg='white', activebackground='#e9ecef')
                        thumb_btn.image = thumb_img  # Keep reference
                        thumb_btn.pack(side='left', padx=3, pady=3)

                        # Hover effects - giống file gốc
                        def on_enter(e, btn=thumb_btn):
                            btn.config(bd=3, bg='#dee2e6')
                        def on_leave(e, btn=thumb_btn):
                            btn.config(bd=2, bg='white')

                        thumb_btn.bind("<Enter>", on_enter)
                        thumb_btn.bind("<Leave>", on_leave)
                    else:
                        # Fallback button nếu không load được thumbnail - giống file gốc
                        thumb_btn = tk.Button(self.thumbnail_scrollable, text=f"Ảnh {i+1}",
                                             command=lambda url=image_url: self.show_main_image(url),
                                             width=8, height=4, cursor='hand2',
                                             relief='solid', bd=2, bg='white')
                        thumb_btn.pack(side='left', padx=3, pady=3)
                else:
                    # Fallback button nếu không load được ảnh - giống file gốc
                    thumb_btn = tk.Button(self.thumbnail_scrollable, text=f"Ảnh {i+1}",
                                         command=lambda url=image_url: self.show_main_image(url),
                                         width=8, height=4, cursor='hand2',
                                         relief='solid', bd=2, bg='white')
                    thumb_btn.pack(side='left', padx=3, pady=3)

            except Exception as e:
                print(f"Lỗi tạo thumbnail {i+1}: {e}")
                # Tạo placeholder button - giống file gốc
                thumb_btn = tk.Button(self.thumbnail_scrollable, text=f"Ảnh {i+1}",
                                     command=lambda url=image_url: self.show_main_image(url),
                                     width=8, height=4, cursor='hand2',
                                     relief='solid', bd=2, bg='white')
                thumb_btn.pack(side='left', padx=3, pady=3)

    def apply_filters(self):
        """Áp dụng tìm kiếm và bộ lọc"""
        # Get filter criteria
        search_text = self.search_var.get().strip().lower()
        selected_brand = self.brand_var.get()
        price_sort = self.price_sort_var.get()

        # Start with original data
        filtered_data = {}

        for ma_sp, product in self.original_product_data.items():
            # Apply search filter
            if search_text:
                if (search_text not in product["name"].lower() and
                    search_text not in product["description"].lower() and
                    search_text not in product["brand"].lower()):
                    continue

            # Apply brand filter
            if selected_brand != "Tất cả":
                if product["brand"] != selected_brand:
                    continue

            # Product passes all filters
            filtered_data[ma_sp] = product

        # Apply sorting
        if price_sort == "Giá thấp → cao":
            # Sort by price ascending
            sorted_items = sorted(filtered_data.items(), key=lambda x: x[1]["price_value"])
            filtered_data = dict(sorted_items)
        elif price_sort == "Giá cao → thấp":
            # Sort by price descending
            sorted_items = sorted(filtered_data.items(), key=lambda x: x[1]["price_value"], reverse=True)
            filtered_data = dict(sorted_items)
        # "Mặc định" keeps original order

        # Update displayed data
        self.product_data = filtered_data
        self.populate_product_list()

        # Update status
        total_products = len(filtered_data)
        print(f"Hiển thị {total_products} sản phẩm sau khi lọc")

    def clear_search(self):
        """Xóa tìm kiếm và reset filters"""
        self.search_var.set("")
        self.brand_var.set("Tất cả")
        self.price_sort_var.set("Mặc định")

        # Reset to original data
        self.product_data = self.original_product_data.copy()
        self.populate_product_list()

        # Clear product detail panel
        self.product_name_label.config(text="Chọn sản phẩm để xem chi tiết")
        for widget in self.main_image_frame.winfo_children():
            widget.destroy()
        tk.Label(self.main_image_frame, text="Hình ảnh sản phẩm",
                 font=('Arial', 14), bg='white', fg='#6c757d').pack(expand=True)

        for widget in self.thumbnail_scrollable.winfo_children():
            widget.destroy()

        self.desc_text.config(state='normal')
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.config(state='disabled')

    def load_cart_count(self):
        """Load số lượng sản phẩm trong giỏ hàng"""
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep"
            )
            cursor = conn.cursor()

            # Sửa lại tên cột từ TenDangNhap thành TenDN
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()

            if result:
                ma_kh = result[0]
                # Lấy MaGH từ MaKH
                cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
                gh_result = cursor.fetchone()

                if gh_result:
                    ma_gh = gh_result[0]
                    # Đếm số sản phẩm trong giỏ hàng
                    cursor.execute("SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaGH = %s", (ma_gh,))
                    count_result = cursor.fetchone()
                    self.cart_count = count_result[0] if count_result[0] else 0
                else:
                    self.cart_count = 0
            else:
                self.cart_count = 0

            # Update cart button text
            if hasattr(self, 'cart_btn'):
                self.cart_btn.config(text=f"🛒 Giỏ hàng ({self.cart_count})")

        except Exception as e:
            print(f"Lỗi load cart count: {e}")
            self.cart_count = 0
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def on_tree_click(self, event):
        """Handle click trên treeview - bao gồm add to cart"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x, event.y)
            if column == "#4":  # Action column
                item = self.tree.identify_row(event.y)
                if item:
                    self.add_to_cart(item)

    def add_to_cart(self, product_id):
        """Thêm sản phẩm vào giỏ hàng từ danh sách"""
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="tungds270105",
                database="shopgiaydep"
            )
            cursor = conn.cursor()

            # Lấy MaKH từ username
            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (self.username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin khách hàng!")
                return

            ma_kh = result[0]

            # Lấy hoặc tạo giỏ hàng
            cursor.execute("SELECT MaGH FROM giohang WHERE MaKH = %s", (ma_kh,))
            gh_result = cursor.fetchone()

            if not gh_result:
                # Tạo giỏ hàng mới
                cursor.execute("SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang")
                max_id = cursor.fetchone()[0]
                new_id = 1 if not max_id else max_id + 1
                ma_gh = f"GH{new_id:03d}"

                cursor.execute("INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)", (ma_gh, ma_kh))
            else:
                ma_gh = gh_result[0]

            # Kiểm tra sản phẩm đã có trong giỏ hàng chưa (với size và màu mặc định)
            cursor.execute("""
                SELECT SoLuong FROM giohangchuasanpham 
                WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
            """, (ma_gh, product_id))

            existing = cursor.fetchone()

            if existing:
                # Tăng số lượng
                new_quantity = existing[0] + 1
                cursor.execute("""
                    UPDATE giohangchuasanpham 
                    SET SoLuong = %s 
                    WHERE MaGH = %s AND MaSP = %s AND MauSac = 'Đen' AND Size = '42'
                """, (new_quantity, ma_gh, product_id))
            else:
                # Thêm sản phẩm mới
                cursor.execute("""
                    INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
                    VALUES (%s, %s, 'Đen', '42', 1)
                """, (ma_gh, product_id))

            conn.commit()

            # Update cart count
            self.load_cart_count()

            # Show success message
            product_name = self.product_data[product_id]["name"]
            messagebox.showinfo("Thành công", f"Đã thêm '{product_name}' vào giỏ hàng!")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm vào giỏ hàng: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def add_selected_to_cart(self):
        """Thêm sản phẩm được chọn vào giỏ hàng"""
        if self.selected_product_id:
            self.add_to_cart(self.selected_product_id)

    def open_cart(self):
        """Mở view giỏ hàng"""
        from views.cart_view import CartView
        cart_view = CartView(username=self.username, parent_view=self)
        cart_view.show()

    def handle_logout(self):
        """Xử lý đăng xuất"""
        self.close()
        # Import here to avoid circular import
        from views.login_view import LoginView
        login_view = LoginView(on_login_success=self.handle_login_success)
        login_view.show()

    def handle_login_success(self, role, username):
        """Xử lý khi đăng nhập thành công"""
        # Close current view
        self.close()
        # Create new product view
        new_view = ProductView(role=role, username=username)
        new_view.show()

    def close(self):
        """Đóng view với proper cleanup"""
        try:
            if self.root:
                self.root.quit()
                self.root.destroy()
        except:
            pass
