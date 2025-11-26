"""
Product View - matches main.py structure exactly
"""
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from PIL import Image, ImageTk
import urllib.request
import io
import os
from config.database import get_db_connection, BASE_DIR, LOCAL_IMAGE_DIR
from utils.image_utils import load_image_safely, load_thumbnail_image, save_uploaded_image, insert_uploaded_image_to_db
from utils.ui_effects import add_button_hover_effect, COLORS, get_hover_color

class ProductView:
    def __init__(self, root):
        self.root = root
        self.brand_combo = None  # Store reference to brand combo for refreshing

    def get_cart_count_from_db(self, username):
        """Get cart count from database - giohangchuasanpham"""
        if not username:
            return 0

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
            result = cursor.fetchone()
            if not result:
                return 0

            ma_kh = result[0]

            cursor.execute("SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaKH = %s", (ma_kh,))
            count_result = cursor.fetchone()
            return count_result[0] if count_result and count_result[0] else 0
        except Exception as e:
            print(f"❌ Error getting cart count: {e}")
            return 0
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def refresh_brand_filter(self):
        """Refresh the brand filter dropdown with updated data - moved to class level"""
        if not self.brand_combo:
            return
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH")
            brands = ["Tất cả"] + [row[0] for row in cursor.fetchall()]
            self.brand_combo['values'] = brands
            print(f"Debug: Brand filter updated with {len(brands)-1} brands")
        except Exception as e:
            print(f"Error refreshing brand filter: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def show_sales_view(self, role, username):
        """Show sales statistics view"""
        from views.sales_view import SalesView
        sales_view = SalesView(self.root)
        sales_view.show(role, username, lambda: self.show_shoes(role, username))

    def show_shoes(self, role=None, username=None):
        """Show product list - from main.py"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Danh sách sản phẩm")
        self.root.geometry("1200x750")

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
                """Calculate cart count from database giohangchuasanpham"""
                cart_count = self.get_cart_count_from_db(username)
                return f"🛒 Giỏ hàng ({cart_count})"


            btn_cart = tk.Button(header_container, text=update_cart_button(),
                                command=lambda: self.show_cart_callback(username, role) if hasattr(self, 'show_cart_callback') else None,
                                bg='#f39c12', fg='white', relief='flat',
                                font=('Arial', 12, 'bold'), padx=15, pady=5, cursor='hand2', bd=2)
            btn_cart.pack(side='right', pady=15, padx=(0, 10))
            # Add hover effect
            add_button_hover_effect(btn_cart, '#f39c12', get_hover_color('#f39c12'))

            # Invoice history button for buyers
            btn_history = tk.Button(header_container, text="📜 Lịch sử",
                                   command=lambda: self.show_invoice_history(role, username) if hasattr(self, 'show_invoice_history') else None,
                                   bg='#9b59b6', fg='white', relief='flat',
                                   font=('Arial', 12, 'bold'), padx=15, pady=5, cursor='hand2', bd=2)
            btn_history.pack(side='right', pady=15, padx=(0, 10))
            # Add hover effect
            add_button_hover_effect(btn_history, '#9b59b6', get_hover_color('#9b59b6'))
        else:
            # No product management button in header for sellers anymore
            pass

        btn_logout = tk.Button(header_container, text="Đăng xuất",
                              command=lambda: self.logout_callback() if hasattr(self, 'logout_callback') else None,
                              bg='#e74c3c', fg='white', relief='flat',
                              font=('Arial', 15), padx=15, pady=5, cursor='hand2', bd=2)
        btn_logout.pack(side='right', pady=15)
        # Add hover effect
        add_button_hover_effect(btn_logout, '#e74c3c', get_hover_color('#e74c3c'))

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
                              bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                              padx=10, cursor='hand2', relief='raised', bd=2)
        btn_search.pack(side='left', padx=5)
        # Add hover effect
        add_button_hover_effect(btn_search, '#3498db', get_hover_color('#3498db'))

        # Sales statistics button for sellers
        if role == "seller":
            btn_sales = tk.Button(search_container, text="📊 Doanh thu",
                                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                                 padx=15, pady=5, relief='raised', cursor='hand2', bd=2,
                                 command=lambda: self.show_sales_view(role, username))
            btn_sales.pack(side='left', padx=10)
            # Add hover effect
            add_button_hover_effect(btn_sales, '#9b59b6', get_hover_color('#9b59b6'))

        # Filter frame
        filter_container = tk.Frame(search_frame, bg='#ecf0f1')
        filter_container.pack(side='right', fill='y', pady=10, padx=(0, 10))

        # Brand filter
        tk.Label(filter_container, text="Thương hiệu:", font=('Arial', 12, 'bold'),
                 bg='#ecf0f1').pack(side='left', padx=(10, 5))

        brand_var = tk.StringVar(value="Tất cả")
        brand_combo = ttk.Combobox(filter_container, textvariable=brand_var, width=12, state='readonly',
                                  font=('Arial', 11))
        brand_combo.pack(side='left', padx=5)

        # Store reference to brand combo for refreshing
        self.brand_combo = brand_combo

        # Price filter
        tk.Label(filter_container, text="Giá:", font=('Arial', 12, 'bold'),
                 bg='#ecf0f1').pack(side='left', padx=(10, 5))

        price_var = tk.StringVar(value="Tất cả")
        price_combo = ttk.Combobox(filter_container, textvariable=price_var, width=12, state='readonly',
                                  font=('Arial', 11), values=["Tất cả", "Dưới 500k", "500k - 1tr", "1tr - 2tr", "Trên 2tr"])
        price_combo.pack(side='left', padx=5)

        btn_filter = tk.Button(filter_container, text="Lọc",
                              bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                              padx=10, cursor='hand2', relief='raised', bd=2)
        btn_filter.pack(side='left', padx=5)
        # Add hover effect
        add_button_hover_effect(btn_filter, '#27ae60', get_hover_color('#27ae60'))

        # Load product data and images
        all_products = []
        product_images = {}
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get product info with brand, import date and discount for price calculation
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang, sp.GiamGia
                FROM sanpham sp
                LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
                ORDER BY sp.MaSP
            """)
            all_products = cursor.fetchall()

            # AUTO-UPDATE GiamGia based on NgayNhapHang (stock age)
            from datetime import datetime
            current_date = datetime.now()

            for ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong, ngay_nhap_hang, giam_gia_current in all_products:
                if ngay_nhap_hang and so_luong > 0:  # Only for products with stock > 0 (IN STOCK)
                    try:
                        # Calculate months difference
                        import_date = ngay_nhap_hang if isinstance(ngay_nhap_hang, datetime) else datetime.strptime(str(ngay_nhap_hang), '%Y-%m-%d')
                        months_old = (current_date.year - import_date.year) * 12 + (current_date.month - import_date.month)

                        # Determine discount based on age
                        new_discount = 0
                        if months_old >= 12:
                            new_discount = 15  # 15% for 12+ months
                        elif months_old >= 6:
                            new_discount = 10  # 10% for 6+ months

                        # Update database if discount changed
                        if new_discount != giam_gia_current:
                            cursor.execute("""
                                UPDATE sanpham SET GiamGia = %s WHERE MaSP = %s
                            """, (new_discount, ma_sp))
                            print(f"Auto-updated discount for {ma_sp}: {giam_gia_current}% -> {new_discount}% (age: {months_old} months)")
                    except Exception as e:
                        print(f"Error auto-updating discount for {ma_sp}: {e}")
                        pass

            # Commit discount updates
            conn.commit()

            # Re-fetch products with updated discounts
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang, sp.GiamGia
                FROM sanpham sp
                LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
                ORDER BY sp.MaSP
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

        # Configure style for larger fonts in Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Arial', 11))
        style.configure("Custom.Treeview.Heading", font=('Arial', 12, 'bold'))

        # Add quantity column for sellers
        if role == "seller":
            tree = ttk.Treeview(tree_frame, columns=("Mã SP", "Tên", "Giá", "SL"), show="headings", height=8, style="Custom.Treeview")
            tree.heading("Mã SP", text="Mã SP")
            tree.heading("Tên", text="Tên giày")
            tree.heading("Giá", text="Giá")
            tree.heading("SL", text="SL")
            tree.column("Mã SP", width=80)
            tree.column("Tên", width=140)
            tree.column("Giá", width=120, anchor='e')
            tree.column("SL", width=50, anchor='e')
        else:
            # Enable multiple selection for buyers
            tree = ttk.Treeview(tree_frame, columns=("Mã SP", "Tên", "Giá"), show="headings", height=8,
                               style="Custom.Treeview", selectmode='extended')
            tree.heading("Mã SP", text="Mã SP")
            tree.heading("Tên", text="Tên giày")
            tree.heading("Giá", text="Giá")
            tree.column("Mã SP", width=80)
            tree.column("Tên", width=160)
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
            status_label.pack(anchor='w', pady=(10, 0))
        else:
            # Product management buttons frame for sellers - FIXED BUTTON ALIGNMENT
            # First row: Delete and Add buttons (centered and same size)
            buttons_row1_frame = tk.Frame(action_button_frame)
            buttons_row1_frame.pack(fill='x', pady=(5, 2))

            # Create a container for centering the buttons
            center_container1 = tk.Frame(buttons_row1_frame)
            center_container1.pack(anchor='center')

            # STANDARDIZED BUTTON PARAMETERS - All buttons exactly the same
            BUTTON_FONT = ('Arial', 11, 'bold')
            BUTTON_PADX = 10
            BUTTON_PADY = 8
            BUTTON_WIDTH = 16  # Fixed width for all buttons
            BUTTON_SPACING = 10  # Consistent spacing between buttons

            # Delete product button (left in center container)
            btn_delete_product = tk.Button(center_container1, text="🗑️ Xóa sản phẩm",
                                          bg='#e74c3c', fg='white', font=BUTTON_FONT,
                                          padx=BUTTON_PADX, pady=BUTTON_PADY, relief='raised', state='disabled',
                                          cursor='hand2', bd=2, width=BUTTON_WIDTH)
            btn_delete_product.pack(side='left', padx=(0, BUTTON_SPACING))

            # Add product button (right in center container)
            btn_add_product = tk.Button(center_container1, text="➕ Thêm sản phẩm",
                                       bg='#27ae60', fg='white', font=BUTTON_FONT,
                                       padx=BUTTON_PADX, pady=BUTTON_PADY, relief='raised',
                                       cursor='hand2', bd=2, width=BUTTON_WIDTH,
                                       command=lambda: self.show_add_product_form(role, username))
            btn_add_product.pack(side='right')
            # Add hover effect
            add_button_hover_effect(btn_add_product, '#27ae60', get_hover_color('#27ae60'))

            # Second row: Edit and Brand buttons (centered and same size)
            buttons_row2_frame = tk.Frame(action_button_frame)
            buttons_row2_frame.pack(fill='x', pady=(2, 5))

            # Create a container for centering the buttons
            center_container2 = tk.Frame(buttons_row2_frame)
            center_container2.pack(anchor='center')

            # Edit product button (left in center container)
            btn_edit_product = tk.Button(center_container2, text="✏️ Sửa sản phẩm",
                                        bg='#f39c12', fg='white', font=BUTTON_FONT,
                                        padx=BUTTON_PADX, pady=BUTTON_PADY, relief='raised', state='disabled',
                                        cursor='hand2', bd=2, width=BUTTON_WIDTH)
            btn_edit_product.pack(side='left', padx=(0, BUTTON_SPACING))

            # Brand management button (right in center container)
            btn_brand_management = tk.Button(center_container2, text="🏷️ Thương hiệu",
                                           bg='#9b59b6', fg='white', font=BUTTON_FONT,
                                           padx=BUTTON_PADX, pady=BUTTON_PADY, relief='raised',
                                           cursor='hand2', bd=2, width=BUTTON_WIDTH,
                                           command=lambda: self.show_brand_management(role, username))
            btn_brand_management.pack(side='right')
            # Add hover effect
            add_button_hover_effect(btn_brand_management, '#9b59b6', get_hover_color('#9b59b6'))

            status_label = tk.Label(action_button_frame, text="Chọn sản phẩm để xóa hoặc sửa",
                                   font=('Arial', 10), fg='#7f8c8d')
            status_label.pack(anchor='w')

        # Functions
        def refresh_brand_filter():
            """Refresh the brand filter dropdown with updated data"""
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH")
                brands = ["Tất cả"] + [row[0] for row in cursor.fetchall()]
                brand_combo['values'] = brands
                print(f"Debug: Brand filter updated with {len(brands)-1} brands")
            except Exception as e:
                print(f"Error refreshing brand filter: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        def show_multi_product_cart_dialog(selected_products):
            """Show dialog for adding multiple products to cart with color, size, and quantity options"""
            if not selected_products:
                return

            # Create scrollable dialog with larger size
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Thêm {len(selected_products)} sản phẩm vào giỏ hàng")
            dialog.geometry("800x650")  # Increased width from 650 to 800
            dialog.resizable(False, False)
            dialog.grab_set()
            dialog.transient(self.root)

            # Center dialog on screen
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
            y = (dialog.winfo_screenheight() // 2) - (650 // 2)
            dialog.geometry(f"+{x}+{y}")

            # Header
            header = tk.Frame(dialog, bg='#3498db', height=60)
            header.pack(fill='x')
            header.pack_propagate(False)

            tk.Label(header, text=f"🛒 Cấu hình {len(selected_products)} sản phẩm",
                    font=('Arial', 16, 'bold'), bg='#3498db', fg='white').pack(pady=15)

            # Main content frame (to contain scrollable area)
            content_frame = tk.Frame(dialog, bg='#f0f0f0')
            content_frame.pack(fill='both', expand=True)

            # Create scrollable frame for products - CENTERED
            scroll_container = tk.Frame(content_frame, bg='#f0f0f0')
            scroll_container.pack(fill='both', expand=True, padx=20, pady=10)

            canvas = tk.Canvas(scroll_container, bg='white', highlightthickness=0)
            scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='white')

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            # Center the content in canvas
            canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

            # Update canvas width to center content
            def update_canvas_width(event):
                canvas_width = event.width
                canvas.itemconfig(canvas_frame, width=canvas_width)

            canvas.bind('<Configure>', update_canvas_width)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Enable mousewheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            dialog.bind_all("<MouseWheel>", _on_mousewheel)

            # Store product configurations
            product_configs = {}

            # Create configuration for each product - CENTERED with better width
            for idx, product_id in enumerate(selected_products):
                if product_id not in product_data:
                    continue

                product = product_data[product_id]

                # Product frame - wider and centered
                product_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', bd=2, width=700)
                product_frame.pack(padx=30, pady=10, fill='x')

                # Product header
                header_frame = tk.Frame(product_frame, bg='#ecf0f1')
                header_frame.pack(fill='x')

                tk.Label(header_frame, text=f"{idx + 1}. {product['name']}",
                        font=('Arial', 13, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(anchor='w', padx=10, pady=8)

                # Price info
                price_text = product['price']
                if product.get('discount', 0) > 0:
                    discounted_price = product['original_price'] * (1 - product['discount'] / 100)
                    price_text = f"{discounted_price:,.0f} VNĐ (-{product['discount']}%)"

                tk.Label(header_frame, text=price_text,
                        font=('Arial', 11), bg='#ecf0f1', fg='#27ae60').pack(anchor='w', padx=10, pady=(0, 8))

                # Configuration frame
                config_frame = tk.Frame(product_frame, bg='white')
                config_frame.pack(fill='x', padx=15, pady=15)

                # Color selection
                color_label_frame = tk.Frame(config_frame, bg='white')
                color_label_frame.pack(fill='x', pady=(0, 8))

                tk.Label(color_label_frame, text="Màu sắc:", font=('Arial', 11, 'bold'),
                        bg='white').pack(side='left')

                # Get colors from database
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT MauSac FROM mausac_sp WHERE MaSP = %s", (product_id,))
                    colors = [row[0] for row in cursor.fetchall()]
                    if not colors:
                        colors = ["Trắng", "Xanh Dương", "Đen", "Nâu"]
                except:
                    colors = ["Trắng", "Xanh Dương", "Đen", "Nâu"]
                finally:
                    if 'cursor' in locals() and cursor:
                        cursor.close()
                    if 'conn' in locals() and conn:
                        conn.close()

                color_var = tk.StringVar(value=colors[0])
                color_combo = ttk.Combobox(config_frame, textvariable=color_var, width=25,
                                          state='readonly', font=('Arial', 11), values=colors)
                color_combo.pack(fill='x', pady=(0, 8))

                # Size selection
                size_label_frame = tk.Frame(config_frame, bg='white')
                size_label_frame.pack(fill='x', pady=(0, 8))

                tk.Label(size_label_frame, text="Kích cỡ:", font=('Arial', 11, 'bold'),
                        bg='white').pack(side='left')

                # Get sizes from database
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT Size FROM size_sp WHERE MaSP = %s ORDER BY CAST(Size AS UNSIGNED)", (product_id,))
                    sizes = [row[0] for row in cursor.fetchall()]
                    if not sizes:
                        sizes = [str(i) for i in range(36, 46)]
                except:
                    sizes = [str(i) for i in range(36, 46)]
                finally:
                    if 'cursor' in locals() and cursor:
                        cursor.close()
                    if 'conn' in locals() and conn:
                        conn.close()

                size_var = tk.StringVar(value=sizes[0] if sizes else "42")
                size_combo = ttk.Combobox(config_frame, textvariable=size_var, width=25,
                                         state='readonly', font=('Arial', 11),
                                         values=sizes)
                size_combo.pack(fill='x', pady=(0, 8))

                # Quantity selection
                qty_label_frame = tk.Frame(config_frame, bg='white')
                qty_label_frame.pack(fill='x', pady=(0, 8))

                tk.Label(qty_label_frame, text=f"Số lượng (Còn: {product['quantity']}):",
                        font=('Arial', 11, 'bold'), bg='white').pack(side='left')

                qty_var = tk.IntVar(value=1)
                qty_spin = tk.Spinbox(config_frame, from_=1, to=product['quantity'],
                                     textvariable=qty_var, width=23, font=('Arial', 11),
                                     justify='center')
                qty_spin.pack(fill='x')

                # Store configuration
                product_configs[product_id] = {
                    'name': product['name'],
                    'color_var': color_var,
                    'size_var': size_var,
                    'qty_var': qty_var,
                    'max_qty': product['quantity']
                }

            # Button frame (FIXED at bottom like seller's add product)
            button_frame = tk.Frame(dialog, bg='white', relief='ridge', bd=1, height=70)
            button_frame.pack(side='bottom', fill='x')
            button_frame.pack_propagate(False)

            def add_all_to_cart():
                """Add all configured products to cart"""
                added_count = 0
                errors = []

                for product_id, config in product_configs.items():
                    try:
                        color = config['color_var'].get()
                        size = config['size_var'].get()
                        qty = config['qty_var'].get()

                        if qty <= 0 or qty > config['max_qty']:
                            errors.append(f"{config['name']}: Số lượng không hợp lệ")
                            continue

                        # Add to cart using existing function
                        add_to_cart_with_quantity(product_id, config['name'], color, size, qty)
                        added_count += 1

                    except Exception as e:
                        errors.append(f"{config['name']}: {str(e)}")

                # Unbind mousewheel before closing
                dialog.unbind_all("<MouseWheel>")
                dialog.destroy()

                # Show result
                if added_count > 0:
                    btn_cart.config(text=update_cart_button())

                # if errors:
                #     messagebox.showwarning("Cảnh báo",
                #         f"Đã thêm {added_count}/{len(product_configs)} sản phẩm.\n\nLỗi:\n" + "\n".join(errors[:3]))
                # else:
                #     messagebox.showinfo("Thành công",
                #         f"Đã thêm {added_count} sản phẩm vào giỏ hàng!")

            def cancel_dialog():
                dialog.unbind_all("<MouseWheel>")
                dialog.destroy()

            # Add buttons - FIXED AT BOTTOM LEFT AND RIGHT
            btn_add_all = tk.Button(button_frame, text="✅ Thêm tất cả vào giỏ", command=add_all_to_cart,
                                   bg='#27ae60', fg='white', font=('Arial', 13, 'bold'),
                                   padx=30, pady=10, cursor='hand2', relief='raised', bd=2)
            btn_add_all.pack(side='left', padx=20, pady=15)
            add_button_hover_effect(btn_add_all, '#27ae60', get_hover_color('#27ae60'))

            btn_cancel = tk.Button(button_frame, text="❌ Hủy bỏ", command=cancel_dialog,
                                  bg='#e74c3c', fg='white', font=('Arial', 13, 'bold'),
                                  padx=30, pady=10, cursor='hand2', relief='raised', bd=2)
            btn_cancel.pack(side='right', padx=20, pady=15)
            add_button_hover_effect(btn_cancel, '#e74c3c', get_hover_color('#e74c3c'))

        # OLD add_to_cart function - NO LONGER USED
        # This function is replaced by show_multi_product_cart_dialog
        # Keeping it commented for reference only
        '''
        def add_to_cart(ma_sp, ten_sp):
            # This function used color_var and size_var which are removed
            # Now using dialog system instead
            pass
        '''

        def add_to_cart_with_quantity(ma_sp, ten_sp, selected_color, selected_size, quantity):
            """Add product to cart - Save to DATABASE giohangchuasanpham"""
            print(f"Debug: Adding {quantity}x {ten_sp} (Color: {selected_color}, Size: {selected_size}) to cart")

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

                # Get current available stock and discount
                cursor.execute("SELECT SoLuong, GiamGia FROM sanpham WHERE MaSP = %s", (ma_sp,))
                stock_result = cursor.fetchone()
                if not stock_result:
                    messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!")
                    return

                available_stock, giam_gia = stock_result

                # Check if cart already has this item
                cursor.execute("""
                    SELECT SoLuong FROM giohangchuasanpham 
                    WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
                """, (ma_kh, ma_sp, selected_color, selected_size))
                existing = cursor.fetchone()
                current_quantity_in_cart = existing[0] if existing else 0
                new_total_quantity = current_quantity_in_cart + quantity

                # Validation: Check stock
                if new_total_quantity > available_stock:
                    remaining = available_stock - current_quantity_in_cart
                    messagebox.showwarning("Cảnh báo tồn kho",
                                         f"Không thể thêm {quantity} sản phẩm '{ten_sp}'!\n\n"
                                         f"📦 Tồn kho: {available_stock}\n"
                                         f"🛒 Đã có trong giỏ: {current_quantity_in_cart}\n"
                                         f"✅ Có thể thêm tối đa: {remaining}\n"
                                         f"(Màu: {selected_color}, Size: {selected_size})")
                    return

                # Add or update cart in DATABASE
                if existing:
                    cursor.execute("""
                        UPDATE giohangchuasanpham 
                        SET SoLuong = %s 
                        WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
                    """, (new_total_quantity, ma_kh, ma_sp, selected_color, selected_size))
                    success_message = (f"Đã cập nhật giỏ hàng!\n"
                                     f"Sản phẩm: {ten_sp}\n"
                                     f"Màu sắc: {selected_color}, Size: {selected_size}\n"
                                     f"Số lượng mới: {new_total_quantity}")
                else:
                    cursor.execute("""
                        INSERT INTO giohangchuasanpham (MaKH, MaSP, MauSac, Size, SoLuong)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (ma_kh, ma_sp, selected_color, selected_size, quantity))
                    success_message = (f"Đã thêm vào giỏ hàng!\n"
                                     f"Sản phẩm: {ten_sp}\n"
                                     f"Màu sắc: {selected_color}, Size: {selected_size}\n"
                                     f"Số lượng: {quantity}")

                conn.commit()

                # Update cart button
                btn_cart.config(text=update_cart_button())

                # Show success message
                remaining_after = available_stock - new_total_quantity
                messagebox.showinfo("Thành công",
                                   f"{success_message}\n\n"
                                   f"📦 Còn lại trong kho: {remaining_after}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm vào giỏ hàng: {str(e)}")
                import traceback
                traceback.print_exc()
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

                # Delete all related records in correct order to avoid foreign key constraint errors

                # 1. Delete from giohangchuasanpham (temporary cart items)
                cursor.execute("DELETE FROM giohangchuasanpham WHERE MaSP = %s", (ma_sp,))

                # 2. Delete from sptrongdon (order items - unpaid orders)
                cursor.execute("DELETE FROM sptrongdon WHERE MaSP = %s", (ma_sp,))

                # 3. Delete product images
                cursor.execute("DELETE FROM url_sp WHERE MaSP = %s", (ma_sp,))

                # 4. Delete product from sanpham table
                # NOTE: cthoadon (invoice details) will KEEP the product data including TenSP
                # This ensures sales statistics remain accurate even after product deletion
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
            out_of_stock_count = 0
            low_stock_count = 0

            for ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong, ngay_nhap_hang, giam_gia in all_products:
                # Filter by search text - Updated to search both product code and name
                if search_text and search_text not in ten_sp.lower() and search_text not in ma_sp.lower():
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

                filtered_products.append((ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong, ngay_nhap_hang, giam_gia))

                # Count stock warnings for sellers
                if role == "seller":
                    if so_luong == 0:
                        out_of_stock_count += 1
                    elif so_luong <= 5:
                        low_stock_count += 1

            # Populate treeview with stock warnings for sellers
            product_data.clear()
            for ma_sp, ten_sp, gia, mo_ta, ten_th, so_luong, ngay_nhap_hang, giam_gia in filtered_products:
                # Use GiamGia from database (stored as int, e.g., 10 = 10%, 15 = 15%)
                discount_percent = int(giam_gia) if giam_gia else 0

                # Apply discount to price display with compact messaging
                if gia is not None:
                    original_price = float(gia)
                    if discount_percent > 0:
                        # Calculate discounted price: original_price * (1 - discount_percent/100)
                        discounted_price = original_price * (1 - discount_percent / 100)
                        price_display = f"{discounted_price:,.0f} VNĐ (-{discount_percent}%)"
                    else:
                        price_display = f"{original_price:,.0f} VNĐ"
                else:
                    price_display = "N/A"

                if role == "seller":
                    # Add visual indicators for stock levels
                    if so_luong == 0:
                        display_name = f"⚠️ {ten_sp} (HẾT HÀNG)"
                        item_id = tree.insert("", "end", iid=ma_sp, values=(ma_sp, display_name, price_display, so_luong))
                        tree.set(item_id, "SL", f"⚠️ {so_luong}")
                    elif so_luong <= 5:
                        display_name = f"⚡ {ten_sp} (SẮP HẾT)"
                        item_id = tree.insert("", "end", iid=ma_sp, values=(ma_sp, display_name, price_display, so_luong))
                        tree.set(item_id, "SL", f"⚡ {so_luong}")
                    else:
                        tree.insert("", "end", iid=ma_sp, values=(ma_sp, ten_sp, price_display, so_luong))
                else:
                    tree.insert("", "end", iid=ma_sp, values=(ma_sp, ten_sp, price_display))

                # Calculate actual discounted price for cart
                original_price_val = float(gia) if gia else 0
                actual_price = original_price_val * (1 - discount_percent / 100) if discount_percent > 0 else original_price_val

                product_data[ma_sp] = {
                    "name": ten_sp,
                    "price": price_display,
                    "description": (mo_ta or "Chưa có mô tả cho sản phẩm này.").strip(),
                    "images": product_images.get(ma_sp, []),
                    "quantity": so_luong,
                    "discount": discount_percent,
                    "original_price": original_price_val,
                    "discounted_price": actual_price  # Giá sau khi giảm để dùng cho cart
                }

            # Update status label with count and stock warnings
            if role == "seller":
                status_text = f"Tổng sản phẩm: {len(filtered_products)}"
                if out_of_stock_count > 0:
                    status_text += f" | ⚠️ HẾT HÀNG: {out_of_stock_count}"
                if low_stock_count > 0:
                    status_text += f" | ⚡ SẮP HẾT: {low_stock_count}"
                status_label.config(text=status_text, fg='#e74c3c' if out_of_stock_count > 0 else '#f39c12' if low_stock_count > 0 else '#7f8c8d')

                # Show warning popup for critical stock levels
                if out_of_stock_count > 0 and not hasattr(filter_products, '_warning_shown'):
                    messagebox.showwarning("Cảnh báo hàng tồn",
                                         f"Có {out_of_stock_count} sản phẩm đã hết hàng!\n"
                                         f"Vui lòng nhập thêm hàng hoặc ẩn sản phẩm.")
                    filter_products._warning_shown = True
            else:
                status_label.config(text=f"Tổng sản phẩm: {len(filtered_products)}", fg='#7f8c8d')

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

        def on_product_select_combined(event):
            nonlocal selected_product_id
            selection = tree.selection()

            if selection:
                if role == "buyer":
                    # For buyers: support multiple selection
                    selected_product_id = selection  # Store all selections
                    num_selected = len(selection)

                    # Enable add to cart button
                    btn_add_to_cart.config(state='normal', bg='#27ae60')
                    add_button_hover_effect(btn_add_to_cart, '#27ae60', get_hover_color('#27ae60'))

                    if num_selected == 1:
                        status_label.config(text="Đã chọn 1 sản phẩm - Click để thêm vào giỏ!", fg='green')
                        # Update product details for single selection
                        product = product_data[selection[0]]
                        product_name_label.config(text=product["name"])

                        if product['discount'] > 0:
                            original_price = product['original_price']
                            discounted_price = original_price * (1 - product['discount'] / 100)
                            product_price_label.config(
                                text=f"Giá: {discounted_price:,.0f} VNĐ (-{product['discount']}%)\n"
                                     f"Giá gốc: {original_price:,.0f} VNĐ",
                                fg='#e74c3c'
                            )
                        else:
                            product_price_label.config(text=product['price'], fg='#27ae60')

                        desc_text.config(state='normal')
                        desc_text.delete(1.0, tk.END)
                        desc_text.insert(1.0, product["description"])
                        desc_text.config(state='disabled')

                        images = product["images"]
                        if images:
                            show_main_image(images[0])
                            update_thumbnail_gallery(images)
                        else:
                            show_main_image(None)
                            update_thumbnail_gallery([])
                    else:
                        status_label.config(text=f"Đã chọn {num_selected} sản phẩm - Click để thêm vào giỏ!", fg='green')
                        product_name_label.config(text=f"{num_selected} sản phẩm đã chọn")
                        product_price_label.config(text="", fg='#27ae60')
                        desc_text.config(state='normal')
                        desc_text.delete(1.0, tk.END)
                        desc_text.insert(1.0, "Nhiều sản phẩm được chọn. Click thêm vào giỏ để cấu hình từng sản phẩm.")
                        desc_text.config(state='disabled')
                        show_main_image(None)
                        update_thumbnail_gallery([])

                    # Set command for add to cart with all selections
                    btn_add_to_cart.config(command=lambda: show_multi_product_cart_dialog(selection))

                else:
                    # For sellers: single selection only
                    selected_product_id = selection[0]
                    if selected_product_id in product_data:
                        # Enable delete and edit product buttons with hover effects
                        btn_delete_product.config(state='normal', bg='#e74c3c')
                        add_button_hover_effect(btn_delete_product, '#e74c3c', get_hover_color('#e74c3c'))
                        btn_edit_product.config(state='normal', bg='#f39c12')
                        add_button_hover_effect(btn_edit_product, '#f39c12', get_hover_color('#f39c12'))
                        status_label.config(text="Click để xóa hoặc sửa sản phẩm đã chọn", fg='blue')
                        btn_delete_product.config(command=lambda: delete_product(selected_product_id, product_data[selected_product_id]["name"]))
                        btn_edit_product.config(command=lambda: self.show_edit_product_form(selected_product_id, role, username))

                        # Update product details on the right panel
                        product = product_data[selected_product_id]

                        # Update product name
                        product_name_label.config(text=f"{product['name']} (SL: {product['quantity']})")

                        # Update price with discount info
                        if product['discount'] > 0:
                            original_price = product['original_price']
                            discounted_price = original_price * (1 - product['discount'] / 100)
                            product_price_label.config(
                                text=f"Giá: {discounted_price:,.0f} VNĐ (-{product['discount']}%)\n"
                                     f"Giá gốc: {original_price:,.0f} VNĐ",
                                fg='#e74c3c'
                            )
                        else:
                            product_price_label.config(text=product['price'], fg='#27ae60')

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
                    status_label.config(text="Chọn sản phẩm để thêm vào giỏ hàng", fg='#7f8c8d')
                else:
                    btn_delete_product.config(state='disabled', bg='#95a5a6')
                    btn_edit_product.config(state='disabled', bg='#95a5a6')
                    status_label.config(text="Chọn sản phẩm để xóa hoặc sửa", fg='#7f8c8d')

        # ONLY bind this event - remove any other bindings
        tree.bind("<<TreeviewSelect>>", on_product_select_combined)

        # Right panel: Product details and image gallery
        detail_frame = tk.Frame(main_frame, bg='#f8f9fa')
        detail_frame.pack(side='right', fill='both', expand=True)

        # Product name
        product_name_label = tk.Label(detail_frame, text="Chọn sản phẩm để xem chi tiết",
                                      font=('Arial', 18, 'bold'), bg='#f8f9fa', fg='#2c3e50')
        product_name_label.pack(pady=(15, 5))

        # Price label (with discount if applicable)
        product_price_label = tk.Label(detail_frame, text="",
                                       font=('Arial', 16, 'bold'), bg='#f8f9fa', fg='#27ae60')
        product_price_label.pack(pady=(0, 10))

        # Create horizontal container for image and gallery
        content_container = tk.Frame(detail_frame, bg='#f8f9fa')
        content_container.pack(fill='both', expand=True, padx=15)

        # Left side - Image and description section
        image_section = tk.Frame(content_container, bg='#f8f9fa')
        image_section.pack(side='left', fill='both', expand=True, padx=(0, 15))

        # Main image display area (reduced height to accommodate wider price column)
        main_image_frame = tk.Frame(image_section, bg='white', relief='solid', bd=1, height=450)
        main_image_frame.pack(fill='x', pady=(0, 15))
        main_image_frame.pack_propagate(False)

        main_image_label = tk.Label(main_image_frame, text="Hình ảnh sản phẩm",
                                   font=('Arial', 14), bg='white', fg='#6c757d')
        main_image_label.pack(expand=True)

        # Description area (below main image, more visible with better spacing)
        desc_section = tk.Frame(image_section, bg='#f8f9fa', relief='solid', bd=1)
        desc_section.pack(fill='x', pady=(0, 10))

        tk.Label(desc_section, text="Mô tả sản phẩm:", font=('Arial', 12, 'bold'),
                 bg='#f8f9fa').pack(anchor='w', pady=(5, 5), padx=5)

        desc_text = tk.Text(desc_section, height=4, wrap='word', font=('Arial', 11),
                           state='disabled', bg='white', relief='solid', bd=1)
        desc_text.pack(fill='both', expand=True, padx=5, pady=(0, 5))

        # Right side - Thumbnail gallery section (with better spacing)
        gallery_section = tk.Frame(content_container, bg='#f8f9fa', width=120)
        gallery_section.pack(side='right', fill='y', padx=(15, 0))
        gallery_section.pack_propagate(False)

        tk.Label(gallery_section, text="Các ảnh khác:", font=('Arial', 12, 'bold'),
                 bg='#f8f9fa').pack(anchor='w', pady=(0, 10))

        # Scrollable thumbnail container (adjusted height)
        thumbnail_frame = tk.Frame(gallery_section, bg='white', height=380, relief='solid', bd=1)
        thumbnail_frame.pack(fill='both', expand=True)

        # Canvas for scrolling thumbnails (vertical scrolling now)
        thumbnail_canvas = tk.Canvas(thumbnail_frame, bg='white')
        thumbnail_scrollbar = ttk.Scrollbar(thumbnail_frame, orient='vertical', command=thumbnail_canvas.yview)
        thumbnail_scrollable = tk.Frame(thumbnail_canvas, bg='white')

        thumbnail_scrollable.bind("<Configure>",
                                 lambda e: thumbnail_canvas.configure(scrollregion=thumbnail_canvas.bbox("all")))
        thumbnail_canvas.create_window((0, 0), window=thumbnail_scrollable, anchor="nw")
        thumbnail_canvas.configure(yscrollcommand=thumbnail_scrollbar.set)

        thumbnail_canvas.pack(side='left', fill='both', expand=True)
        thumbnail_scrollbar.pack(side='right', fill='y')

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
                       font=('Arial', 10), bg='white', fg='#6c757d').pack(pady=20)
                return

            for i, image_url in enumerate(images):
                try:
                    # Load thumbnail image
                    thumb_img = load_thumbnail_image(image_url)
                    if thumb_img:
                        # Create thumbnail button - now arranged vertically and centered
                        thumb_btn = tk.Button(thumbnail_scrollable, image=thumb_img,
                                             command=lambda url=image_url: show_main_image(url),
                                             relief='solid', bd=2, cursor='hand2',
                                             bg='white', activebackground='#e9ecef')
                        thumb_btn.image = thumb_img  # Keep reference
                        thumb_btn.pack(pady=3, padx=5, anchor='center')  # Added anchor='center'

                        # Hover effects
                        def on_enter(e, btn=thumb_btn):
                            btn.config(bd=3, bg='#dee2e6')
                        def on_leave(e, btn=thumb_btn):
                            btn.config(bd=2, bg='white')

                        thumb_btn.bind("<Enter>", on_enter)
                        thumb_btn.bind("<Leave>", on_leave)

                    else:
                        # Fallback button if can't load image - also centered
                        thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}",
                                             command=lambda url=image_url: show_main_image(url),
                                             width=8, height=4, cursor='hand2',
                                             relief='solid', bd=2, bg='white')
                        thumb_btn.pack(pady=3, padx=5, anchor='center')  # Added anchor='center'

                except Exception as e:
                    print(f"Error creating thumbnail {i+1}: {e}")
                    # Create placeholder button - also centered
                    thumb_btn = tk.Button(thumbnail_scrollable, text=f"Ảnh {i+1}",
                                         command=lambda url=image_url: show_main_image(url),
                                         width=8, height=4, cursor='hand2',
                                         relief='solid', bd=2, bg='white')
                    thumb_btn.pack(pady=3, padx=5, anchor='center')  # Added anchor='center'

        # Mouse wheel scroll for thumbnail canvas
        def on_mousewheel(event):
            thumbnail_canvas.xview_scroll(int(-1*(event.delta/120)), "units")

        thumbnail_canvas.bind("<MouseWheel>", on_mousewheel)

    def show_add_product_form(self, role, username):
        """Show add product form - from main.py"""
        # Create add product window
        add_window = tk.Toplevel(self.root)
        add_window.title("Thêm sản phẩm mới")
        add_window.geometry("600x650")  # Increased width and height for better visibility
        add_window.resizable(False, False)
        add_window.grab_set()  # Make window modal

        # Center the window
        add_window.transient(self.root)
        add_window.focus()

        # Unbind mousewheel when window closes
        def on_closing():
            add_window.unbind_all("<MouseWheel>")
            add_window.destroy()

        add_window.protocol("WM_DELETE_WINDOW", on_closing)

        # IMPORTANT: Pack button frame FIRST to reserve space at bottom
        button_frame = tk.Frame(add_window, bg='#f0f0f0', relief='ridge', bd=1)
        button_frame.pack(side='bottom', fill='x', padx=10, pady=10)

        # Create canvas with scrollbar for scrollable content
        canvas = tk.Canvas(add_window, bg='white')
        scrollbar = tk.Scrollbar(add_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar - they will fill remaining space above buttons
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Use scrollable_frame as main_container
        main_container = scrollable_frame

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        add_window.bind_all("<MouseWheel>", _on_mousewheel)

        # Form fields
        tk.Label(main_container, text="THÊM SẢN PHẨM MỚI", font=('Arial', 16, 'bold'), fg='#2c3e50').pack(pady=(10, 20))

        # Product name
        tk.Label(main_container, text="Tên sản phẩm:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_name = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_name.pack(padx=10, pady=(0, 8))

        # Price
        tk.Label(main_container, text="Giá (VNĐ):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_price = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_price.pack(padx=10, pady=(0, 8))

        # Brand
        tk.Label(main_container, text="Thương hiệu:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        brand_var_add = tk.StringVar()
        brand_combo_add = ttk.Combobox(main_container, textvariable=brand_var_add, font=('Arial', 12), width=37, state='readonly')

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

        brand_combo_add.pack(padx=10, pady=(0, 8))

        # Quantity
        tk.Label(main_container, text="Số lượng:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_quantity = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_quantity.pack(padx=10, pady=(0, 8))

        # Import Date (NgayNhapHang)
        tk.Label(main_container, text="Ngày nhập hàng (YYYY-MM-DD):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_import_date = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_import_date.pack(padx=10, pady=(0, 8))

        # Description
        tk.Label(main_container, text="Mô tả:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_description = tk.Text(main_container, font=('Arial', 11), width=42, height=5, wrap='word')  # Reduced height from 6 to 5
        text_description.pack(padx=10, pady=(0, 8))

        # Colors (Available colors for this product)
        tk.Label(main_container, text="Màu sắc có sẵn (mỗi màu một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_colors = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        text_colors.insert(1.0, "Trắng\nXanh Dương\nĐen\nNâu")  # Default colors
        text_colors.pack(padx=10, pady=(0, 8))

        # Sizes (Available sizes for this product)
        tk.Label(main_container, text="Kích cỡ có sẵn (mỗi size một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_sizes = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        text_sizes.insert(1.0, "\n".join([str(i) for i in range(36, 46)]))  # Default sizes 36-45
        text_sizes.pack(padx=10, pady=(0, 8))

        # Image URLs
        tk.Label(main_container, text="URL hình ảnh (mỗi URL một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_images = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        text_images.pack(padx=10, pady=(0, 8))

        # Image Upload Section
        upload_frame = tk.Frame(main_container)
        upload_frame.pack(fill='x', padx=10, pady=(5, 8))

        tk.Label(upload_frame, text="Hoặc tải ảnh từ thiết bị:", font=('Arial', 11, 'bold')).pack(anchor='w')

        # Store uploaded image filenames temporarily
        uploaded_images = []

        upload_btn_frame = tk.Frame(upload_frame)
        upload_btn_frame.pack(anchor='w', pady=(5, 0))

        def upload_image():
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
            file_path = filedialog.askopenfilename(parent=add_window, title="Chọn hình ảnh", filetypes=filetypes)
            if file_path:
                try:
                    # Save to local directory
                    filename = save_uploaded_image(file_path)
                    uploaded_images.append(filename)
                    # Update label to show count
                    upload_count_label.config(text=f"Đã chọn: {len(uploaded_images)} ảnh", fg='#27ae60')
                    messagebox.showinfo("Thành công", f"Đã thêm ảnh: {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")

        tk.Button(upload_btn_frame, text="📁 Chọn ảnh từ máy", command=upload_image,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=10, pady=5, cursor='hand2').pack(side='left')

        upload_count_label = tk.Label(upload_btn_frame, text="Chưa chọn ảnh nào",
                                      font=('Arial', 10), fg='#7f8c8d')
        upload_count_label.pack(side='left', padx=(10, 0))


        def save_product():
            # Get form data
            name = entry_name.get().strip()
            price_str = entry_price.get().strip()
            brand_selection = brand_var_add.get()
            quantity_str = entry_quantity.get().strip()
            import_date_str = entry_import_date.get().strip()
            description = text_description.get(1.0, tk.END).strip()
            colors = text_colors.get(1.0, tk.END).strip()
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

                # Validate import date format if provided
                if import_date_str:
                    from datetime import datetime
                    try:
                        datetime.strptime(import_date_str, '%Y-%m-%d')
                    except ValueError:
                        raise ValueError("Ngày nhập hàng phải theo định dạng YYYY-MM-DD")
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

                # Create color table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mausac_sp (
                        MaSP VARCHAR(30) NOT NULL,
                        MauSac VARCHAR(100) NOT NULL,
                        PRIMARY KEY (MaSP, MauSac),
                        FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
                    )
                """)

                # Create size table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS size_sp (
                        MaSP VARCHAR(30) NOT NULL,
                        Size VARCHAR(20) NOT NULL,
                        PRIMARY KEY (MaSP, Size),
                        FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
                    )
                """)

                # Generate new product ID - sử dụng hàm từ models/product.py
                from models.product import generate_product_id
                product_id = generate_product_id(cursor)

                # Insert product with import date
                cursor.execute("""
                    INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, NgayNhapHang)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (product_id, name, price, description if description else None, brand_id, quantity,
                      import_date_str if import_date_str else None))

                # Insert colors if provided
                if colors:
                    color_list = [color.strip() for color in colors.split('\n') if color.strip()]
                    for color in color_list:
                        cursor.execute("INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)", (product_id, color))

                # Insert sizes if provided
                sizes = text_sizes.get(1.0, tk.END).strip()
                if sizes:
                    size_list = [size.strip() for size in sizes.split('\n') if size.strip()]
                    for size in size_list:
                        cursor.execute("INSERT INTO size_sp (MaSP, Size) VALUES (%s, %s)", (product_id, size))

                # Insert image URLs if provided
                if image_urls:
                    urls = [url.strip() for url in image_urls.split('\n') if url.strip()]
                    for url in urls:
                        cursor.execute("INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)", (product_id, url))

                # Insert uploaded images
                for filename in uploaded_images:
                    cursor.execute("INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)", (product_id, filename))

                conn.commit()
                total_images = len([url.strip() for url in image_urls.split('\n') if url.strip()]) + len(uploaded_images)
                total_colors = len([color.strip() for color in colors.split('\n') if color.strip()])
                messagebox.showinfo("Thành công", f"Đã thêm sản phẩm '{name}' với {total_colors} màu và {total_images} ảnh thành công!")
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

        # Action buttons with proper colors and positions
        tk.Button(button_frame, text="💾 Lưu", command=save_product,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(side='left', padx=15, pady=10)
        tk.Button(button_frame, text="❌ Hủy", command=on_closing,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(side='right', padx=15, pady=10)

    def show_edit_product_form(self, product_id, role, username):
        """Show edit product form with current data loaded"""
        # First, get current product data from database
        conn = None
        cursor = None
        current_data = {}
        current_images = []

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get product details
            cursor.execute("""
                SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, sp.MaTH, sp.SoLuong, th.TenTH, sp.NgayNhapHang
                FROM sanpham sp
                LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
                WHERE sp.MaSP = %s
            """, (product_id,))

            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!")
                return

            current_data = {
                'id': result[0],
                'name': result[1],
                'price': result[2],
                'description': result[3] or "",
                'brand_id': result[4],
                'quantity': result[5],
                'brand_name': result[6],
                'import_date': result[7].strftime('%Y-%m-%d') if result[7] else ''
            }

            # Get product images
            cursor.execute("SELECT URLAnh FROM url_sp WHERE MaSP = %s", (product_id,))
            current_images = [row[0] for row in cursor.fetchall()]

            # Get product colors
            current_colors = []
            try:
                cursor.execute("SELECT MauSac FROM mausac_sp WHERE MaSP = %s", (product_id,))
                current_colors = [row[0] for row in cursor.fetchall()]
            except Exception as e:
                # If table doesn't exist yet, use default colors
                print(f"Note: Color table may not exist yet: {e}")
                current_colors = ["Trắng", "Xanh Dương", "Đen", "Nâu"]

            # Get product sizes
            current_sizes = []
            try:
                cursor.execute("SELECT Size FROM size_sp WHERE MaSP = %s ORDER BY CAST(Size AS UNSIGNED)", (product_id,))
                current_sizes = [row[0] for row in cursor.fetchall()]
            except Exception as e:
                # If table doesn't exist yet, use default sizes
                print(f"Note: Size table may not exist yet: {e}")
                current_sizes = [str(i) for i in range(36, 46)]

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu sản phẩm: {str(e)}")
            return
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Create edit product window
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Sửa sản phẩm: {current_data['name']}")
        edit_window.geometry("600x650")  # Increased width and height for better visibility
        edit_window.resizable(False, False)
        edit_window.grab_set()  # Make window modal

        # Center the window
        edit_window.transient(self.root)
        edit_window.focus()

        # Unbind mousewheel when window closes
        def on_closing():
            edit_window.unbind_all("<MouseWheel>")
            edit_window.destroy()

        edit_window.protocol("WM_DELETE_WINDOW", on_closing)

        # IMPORTANT: Pack button frame FIRST to reserve space at bottom
        button_frame = tk.Frame(edit_window, bg='#f0f0f0', relief='ridge', bd=1)
        button_frame.pack(side='bottom', fill='x', padx=10, pady=10)

        # Create canvas with scrollbar for scrollable content
        canvas = tk.Canvas(edit_window, bg='white')
        scrollbar = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar - they will fill remaining space above buttons
        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Use scrollable_frame as main_container
        main_container = scrollable_frame

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        edit_window.bind_all("<MouseWheel>", _on_mousewheel)

        # Form fields
        tk.Label(main_container, text=f"SỬA SẢN PHẨM: {current_data['name']}",
                font=('Arial', 16, 'bold'), fg='#f39c12').pack(pady=(10, 20))

        # Product name
        tk.Label(main_container, text="Tên sản phẩm:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_name = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_name.insert(0, current_data['name'])
        entry_name.pack(padx=10, pady=(0, 8))

        # Price
        tk.Label(main_container, text="Giá (VNĐ):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_price = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_price.insert(0, str(current_data['price']))
        entry_price.pack(padx=10, pady=(0, 8))

        # Brand
        tk.Label(main_container, text="Thương hiệu:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        brand_var_edit = tk.StringVar()
        brand_combo_edit = ttk.Combobox(main_container, textvariable=brand_var_edit, font=('Arial', 12), width=37, state='readonly')

        # Load brands and set current brand
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH")
            brands_data = cursor.fetchall()
            brand_options = [f"{th[1]} ({th[0]})" for th in brands_data]
            brand_combo_edit['values'] = brand_options

            # Set current brand as selected
            current_brand_text = f"{current_data['brand_name']} ({current_data['brand_id']})"
            brand_var_edit.set(current_brand_text)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách thương hiệu: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        brand_combo_edit.pack(padx=10, pady=(0, 8))

        # Quantity
        tk.Label(main_container, text="Số lượng:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_quantity = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_quantity.insert(0, str(current_data['quantity']))
        entry_quantity.pack(padx=10, pady=(0, 8))

        # Import Date (NgayNhapHang)
        tk.Label(main_container, text="Ngày nhập hàng (YYYY-MM-DD):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        entry_import_date = tk.Entry(main_container, font=('Arial', 12), width=40)
        entry_import_date.insert(0, current_data['import_date'])
        entry_import_date.pack(padx=10, pady=(0, 8))

        # Description
        tk.Label(main_container, text="Mô tả:", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_description = tk.Text(main_container, font=('Arial', 11), width=42, height=5, wrap='word')
        text_description.insert(1.0, current_data['description'])
        text_description.pack(padx=10, pady=(0, 8))

        # Colors (Available colors for this product)
        tk.Label(main_container, text="Màu sắc có sẵn (mỗi màu một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_colors = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        if current_colors:
            text_colors.insert(1.0, '\n'.join(current_colors))
        else:
            text_colors.insert(1.0, "Trắng\nXanh Dương\nĐen\nNâu")  # Default colors
        text_colors.pack(padx=10, pady=(0, 8))

        # Sizes (Available sizes for this product)
        tk.Label(main_container, text="Kích cỡ có sẵn (mỗi size một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_sizes_edit = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        if current_sizes:
            text_sizes_edit.insert(1.0, '\n'.join(current_sizes))
        else:
            text_sizes_edit.insert(1.0, "\n".join([str(i) for i in range(36, 46)]))  # Default sizes
        text_sizes_edit.pack(padx=10, pady=(0, 8))

        # Image URLs
        tk.Label(main_container, text="URL hình ảnh (mỗi URL một dòng):", font=('Arial', 12, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        text_images = tk.Text(main_container, font=('Arial', 11), width=42, height=3, wrap='word')
        if current_images:
            text_images.insert(1.0, '\n'.join(current_images))
        text_images.pack(padx=10, pady=(0, 8))

        # Image Upload Section
        upload_frame = tk.Frame(main_container)
        upload_frame.pack(fill='x', padx=10, pady=(5, 8))

        tk.Label(upload_frame, text="Hoặc tải ảnh từ thiết bị:", font=('Arial', 11, 'bold')).pack(anchor='w')

        # Store uploaded image filenames temporarily
        uploaded_images = []

        upload_btn_frame = tk.Frame(upload_frame)
        upload_btn_frame.pack(anchor='w', pady=(5, 0))

        def upload_image():
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
            file_path = filedialog.askopenfilename(parent=edit_window, title="Chọn hình ảnh", filetypes=filetypes)
            if file_path:
                try:
                    # Save to local directory
                    filename = save_uploaded_image(file_path)
                    uploaded_images.append(filename)
                    # Update label to show count
                    upload_count_label.config(text=f"Đã chọn: {len(uploaded_images)} ảnh mới", fg='#27ae60')
                    messagebox.showinfo("Thành công", f"Đã thêm ảnh: {os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể tải ảnh: {str(e)}")

        tk.Button(upload_btn_frame, text="📁 Chọn ảnh từ máy", command=upload_image,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=10, pady=5, cursor='hand2').pack(side='left')

        upload_count_label = tk.Label(upload_btn_frame, text="Chưa chọn ảnh mới nào",
                                      font=('Arial', 10), fg='#7f8c8d')
        upload_count_label.pack(side='left', padx=(10, 0))


        def update_product():
            # Get form data
            name = entry_name.get().strip()
            price_str = entry_price.get().strip()
            brand_selection = brand_var_edit.get()
            quantity_str = entry_quantity.get().strip()
            import_date_str = entry_import_date.get().strip()
            description = text_description.get(1.0, tk.END).strip()
            colors = text_colors.get(1.0, tk.END).strip()
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

                # Validate import date format if provided
                if import_date_str:
                    from datetime import datetime
                    try:
                        datetime.strptime(import_date_str, '%Y-%m-%d')
                    except ValueError:
                        raise ValueError("Ngày nhập hàng phải theo định dạng YYYY-MM-DD")
            except ValueError as e:
                messagebox.showerror("Lỗi", f"Dữ liệu không hợp lệ: {str(e)}")
                return

            # Extract brand ID
            try:
                brand_id = brand_selection.split('(')[1].replace(')', '')
            except:
                messagebox.showerror("Lỗi", "Vui lòng chọn thương hiệu!")
                return

            # Update database
            conn = None
            cursor = None
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Create color table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS mausac_sp (
                        MaSP VARCHAR(30) NOT NULL,
                        MauSac VARCHAR(100) NOT NULL,
                        PRIMARY KEY (MaSP, MauSac),
                        FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
                    )
                """)

                # Create size table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS size_sp (
                        MaSP VARCHAR(30) NOT NULL,
                        Size VARCHAR(20) NOT NULL,
                        PRIMARY KEY (MaSP, Size),
                        FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
                    )
                """)

                # Update product with import date
                cursor.execute("""
                    UPDATE sanpham 
                    SET TenSP = %s, Gia = %s, MoTa = %s, MaTH = %s, SoLuong = %s, NgayNhapHang = %s
                    WHERE MaSP = %s
                """, (name, price, description if description else None, brand_id, quantity,
                      import_date_str if import_date_str else None, product_id))

                # Delete old colors
                cursor.execute("DELETE FROM mausac_sp WHERE MaSP = %s", (product_id,))

                # Insert new colors if provided
                if colors:
                    color_list = [color.strip() for color in colors.split('\n') if color.strip()]
                    for color in color_list:
                        cursor.execute("INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)", (product_id, color))

                # Delete old sizes
                cursor.execute("DELETE FROM size_sp WHERE MaSP = %s", (product_id,))

                # Insert new sizes if provided
                sizes_edit = text_sizes_edit.get(1.0, tk.END).strip()
                if sizes_edit:
                    size_list = [size.strip() for size in sizes_edit.split('\n') if size.strip()]
                    for size in size_list:
                        cursor.execute("INSERT INTO size_sp (MaSP, Size) VALUES (%s, %s)", (product_id, size))

                # Delete old images
                cursor.execute("DELETE FROM url_sp WHERE MaSP = %s", (product_id,))

                # Insert new image URLs if provided
                if image_urls:
                    urls = [url.strip() for url in image_urls.split('\n') if url.strip()]
                    for url in urls:
                        cursor.execute("INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)", (product_id, url))

                # Insert uploaded images
                for filename in uploaded_images:
                    cursor.execute("INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)", (product_id, filename))

                conn.commit()
                total_images = len([url.strip() for url in image_urls.split('\n') if url.strip()]) + len(uploaded_images)
                total_colors = len([color.strip() for color in colors.split('\n') if color.strip()])
                total_sizes = len([size.strip() for size in sizes_edit.split('\n') if size.strip()])
                messagebox.showinfo("Thành công", f"Đã cập nhật sản phẩm '{name}' với {total_colors} màu, {total_sizes} size và {total_images} ảnh thành công!")
                edit_window.destroy()

                # Refresh the product list
                self.show_shoes(role, username)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật sản phẩm: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Action buttons with proper colors and positions
        tk.Button(button_frame, text="✏️ Cập nhật", command=update_product,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(side='left', padx=15, pady=10)
        tk.Button(button_frame, text="❌ Hủy", command=on_closing,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2').pack(side='right', padx=15, pady=10)

    def show_brand_management(self, role, username):
        """Show brand management interface for sellers"""
        # Create brand management window
        brand_window = tk.Toplevel(self.root)
        brand_window.title("Quản lý thương hiệu")
        brand_window.geometry("600x500")
        brand_window.resizable(False, False)

        # Center the window
        brand_window.update_idletasks()
        x = (brand_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (brand_window.winfo_screenheight() // 2) - (500 // 2)
        brand_window.geometry(f"+{x}+{y}")

        # Make sure it's on top
        brand_window.transient(self.root)
        brand_window.grab_set()  # Make window modal
        brand_window.lift()  # Raise to top
        brand_window.focus_force()  # Force focus

        # Header
        header_frame = tk.Frame(brand_window, bg='#9b59b6', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="QUẢN LÝ THƯƠNG HIỆU", font=('Arial', 18, 'bold'),
                 fg='white', bg='#9b59b6').pack(pady=15)

        # Main content frame
        main_frame = tk.Frame(brand_window)
        main_frame.pack(fill='both', expand=True, padx=15, pady=10)

        # Brand list frame
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True, pady=(0, 10))

        tk.Label(list_frame, text="Danh sách thương hiệu:", font=('Arial', 14, 'bold')).pack(anchor='w', pady=(0, 10))

        # Treeview for brands
        tree_frame = tk.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)

        # Configure style
        style = ttk.Style()
        style.configure("Brand.Treeview", font=('Arial', 12))
        style.configure("Brand.Treeview.Heading", font=('Arial', 13, 'bold'))

        brand_tree = ttk.Treeview(tree_frame, columns=("Mã TH", "Tên thương hiệu"), show="headings",
                                 height=12, style="Brand.Treeview")
        brand_tree.heading("Mã TH", text="Mã thương hiệu")
        brand_tree.heading("Tên thương hiệu", text="Tên thương hiệu")
        brand_tree.column("Mã TH", width=150, anchor='center')
        brand_tree.column("Tên thương hiệu", width=300, anchor='w')

        scrollbar_brand = ttk.Scrollbar(tree_frame, orient="vertical", command=brand_tree.yview)
        brand_tree.configure(yscrollcommand=scrollbar_brand.set)

        brand_tree.pack(side="left", fill="both", expand=True)
        scrollbar_brand.pack(side="right", fill="y")

        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))

        # First row: Delete and Add buttons
        buttons_row1 = tk.Frame(button_frame)
        buttons_row1.pack(fill='x', pady=(0, 5))

        btn_delete_brand = tk.Button(buttons_row1, text="🗑️ Xóa thương hiệu",
                                    bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                    padx=15, pady=8, relief='raised', state='disabled',
                                    cursor='hand2', bd=2)
        btn_delete_brand.pack(side='left')

        btn_add_brand = tk.Button(buttons_row1, text="➕ Thêm thương hiệu",
                                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                 padx=15, pady=8, relief='raised',
                                 cursor='hand2', bd=2)
        btn_add_brand.pack(side='right')
        # Add hover effect
        add_button_hover_effect(btn_add_brand, '#27ae60', get_hover_color('#27ae60'))

        # Status label
        status_brand_label = tk.Label(button_frame, text="Chọn thương hiệu để xóa",
                                     font=('Arial', 10), fg='#7f8c8d')
        status_brand_label.pack(pady=(5, 0))

        # Load brand data
        def load_brands():
            # Clear current items
            for item in brand_tree.get_children():
                brand_tree.delete(item)

            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH")
                brands = cursor.fetchall()

                for ma_th, ten_th in brands:
                    brand_tree.insert("", "end", iid=ma_th, values=(ma_th, ten_th))

                status_brand_label.config(text=f"Tổng số thương hiệu: {len(brands)}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải danh sách thương hiệu: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Brand selection handler
        selected_brand_id = None

        def on_brand_select(event):
            nonlocal selected_brand_id
            selection = brand_tree.selection()

            if selection:
                selected_brand_id = selection[0]
                btn_delete_brand.config(state='normal', bg='#e74c3c')
                add_button_hover_effect(btn_delete_brand, '#e74c3c', get_hover_color('#e74c3c'))
                status_brand_label.config(text="Click để xóa thương hiệu đã chọn", fg='red')
            else:
                selected_brand_id = None
                btn_delete_brand.config(state='disabled', bg='#95a5a6')
                status_brand_label.config(text="Chọn thương hiệu để xóa", fg='#7f8c8d')

        brand_tree.bind("<<TreeviewSelect>>", on_brand_select)

        # Delete brand function
        def delete_brand():
            if not selected_brand_id:
                return

            # Get brand name for confirmation
            selected_item = brand_tree.item(selected_brand_id)
            brand_name = selected_item['values'][1]

            result = messagebox.askyesno("Xác nhận",
                                       f"Bạn có chắc chắn muốn xóa thương hiệu '{brand_name}' không?\n\n"
                                       f"Lưu ý: Tất cả sản phẩm của thương hiệu này cũng sẽ bị xóa!")
            if not result:
                return

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Delete products of this brand first
                cursor.execute("DELETE FROM url_sp WHERE MaSP IN (SELECT MaSP FROM sanpham WHERE MaTH = %s)", (selected_brand_id,))
                cursor.execute("DELETE FROM sanpham WHERE MaTH = %s", (selected_brand_id,))

                # Delete brand
                cursor.execute("DELETE FROM thuonghieu WHERE MaTH = %s", (selected_brand_id,))

                conn.commit()
                messagebox.showinfo("Thành công", f"Đã xóa thương hiệu '{brand_name}' thành công!")

                # Refresh brand list in this window
                load_brands()

                # Refresh the product view's brand filter
                self.refresh_brand_filter()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa thương hiệu: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Add brand function
        def add_brand():
            # Create add brand dialog - INCREASED HEIGHT for buttons visibility
            add_brand_window = tk.Toplevel(brand_window)
            add_brand_window.title("Thêm thương hiệu mới")
            add_brand_window.geometry("520x300")  # Increased to 520x300 - MORE SPACE!
            add_brand_window.resizable(False, False)

            # Center the dialog
            add_brand_window.update_idletasks()
            x = (add_brand_window.winfo_screenwidth() // 2) - (520 // 2)
            y = (add_brand_window.winfo_screenheight() // 2) - (300 // 2)
            add_brand_window.geometry(f"+{x}+{y}")

            # Make sure it's on top
            add_brand_window.transient(brand_window)
            add_brand_window.grab_set()
            add_brand_window.lift()
            add_brand_window.focus_force()

            # MAIN CONTAINER with fixed structure
            main_container = tk.Frame(add_brand_window, bg='white')
            main_container.pack(fill='both', expand=True)

            # TOP SECTION - Form content (NOT EXPANDABLE)
            top_section = tk.Frame(main_container, bg='white')
            top_section.pack(side='top', fill='x', padx=30, pady=(20, 10))

            tk.Label(top_section, text="THÊM THƯƠNG HIỆU MỚI", font=('Arial', 14, 'bold'),
                     fg='#27ae60', bg='white').pack(pady=(0, 15))

            tk.Label(top_section, text="Tên thương hiệu:", font=('Arial', 12, 'bold'),
                    bg='white').pack(anchor='w', pady=(0, 5))
            entry_brand_name = tk.Entry(top_section, font=('Arial', 12), width=42)
            entry_brand_name.pack(pady=(0, 10), fill='x')
            entry_brand_name.focus()

            # MIDDLE SPACER - Expandable to push buttons down
            spacer = tk.Frame(main_container, bg='white')
            spacer.pack(side='top', fill='both', expand=True)

            # BOTTOM SECTION - Buttons (ALWAYS AT BOTTOM)
            # Use fixed height and pack_propagate(False) to ensure buttons always visible
            button_frame_add = tk.Frame(main_container, bg='white', height=70)
            button_frame_add.pack(side='bottom', fill='x', padx=30, pady=(10, 20))
            button_frame_add.pack_propagate(False)  # CRITICAL: Prevent shrinking!

            # Create inner container for buttons with padding
            buttons_container = tk.Frame(button_frame_add, bg='white')
            buttons_container.pack(fill='both', expand=True, pady=10)

            def save_brand():
                brand_name = entry_brand_name.get().strip()
                if not brand_name:
                    messagebox.showerror("Lỗi", "Vui lòng nhập tên thương hiệu!")
                    return

                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    # Check if brand already exists
                    cursor.execute("SELECT MaTH FROM thuonghieu WHERE TenTH = %s", (brand_name,))
                    if cursor.fetchone():
                        messagebox.showerror("Lỗi", f"Thương hiệu '{brand_name}' đã tồn tại!")
                        return

                    # Generate new brand ID
                    cursor.execute("SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) FROM thuonghieu WHERE MaTH LIKE 'TH%'")
                    result = cursor.fetchone()
                    next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
                    brand_id = f"TH{next_number:03d}"

                    # Insert brand
                    cursor.execute("INSERT INTO thuonghieu (MaTH, TenTH) VALUES (%s, %s)", (brand_id, brand_name))
                    conn.commit()

                    messagebox.showinfo("Thành công", f"Đã thêm thương hiệu '{brand_name}' thành công!")
                    add_brand_window.destroy()

                    # Refresh brand list in this window
                    load_brands()

                    # Refresh the product view's brand filter
                    self.refresh_brand_filter()

                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể thêm thương hiệu: {str(e)}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()

            # Save and Cancel buttons with hover effects
            # Pack into buttons_container (not button_frame_add directly)
            btn_save_brand = tk.Button(buttons_container, text="💾 Lưu", command=save_brand,
                                      bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                      padx=25, pady=8, cursor='hand2', relief='raised', bd=2)
            btn_save_brand.pack(side='left', padx=5)
            add_button_hover_effect(btn_save_brand, '#27ae60', get_hover_color('#27ae60'))

            btn_cancel_brand = tk.Button(buttons_container, text="❌ Hủy", command=add_brand_window.destroy,
                                        bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                        padx=25, pady=8, cursor='hand2', relief='raised', bd=2)
            btn_cancel_brand.pack(side='left', padx=5)
            add_button_hover_effect(btn_cancel_brand, '#e74c3c', get_hover_color('#e74c3c'))

            # Enter key to save
            entry_brand_name.bind('<Return>', lambda e: save_brand())

        # Bind button functions
        btn_delete_brand.config(command=delete_brand)
        btn_add_brand.config(command=add_brand)

        # Load initial data
        load_brands()

    def set_show_cart_callback(self, callback):
        """Set callback for showing cart"""
        self.show_cart_callback = callback

    def set_show_invoice_history_callback(self, callback):
        """Set callback for showing invoice history"""
        self.show_invoice_history = callback

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
