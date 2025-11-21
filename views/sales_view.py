"""
Sales View - Monthly sales statistics for sellers
"""
import tkinter as tk
from tkinter import ttk, messagebox
from config.database import get_db_connection
from datetime import datetime
from utils.ui_effects import add_button_hover_effect, get_hover_color


class SalesView:
    def __init__(self, root):
        self.root = root

    def show(self, role, username, return_callback):
        """Show monthly sales statistics"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Thống kê doanh thu")

        # Main container
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Back button
        btn_back = tk.Button(header_frame, text="← Quay lại", command=lambda: return_callback(),
                            bg='#34495e', fg='white', font=('Arial', 12, 'bold'),
                            padx=15, pady=8, relief='raised', cursor='hand2', bd=2)
        btn_back.pack(side='left', padx=20, pady=20)
        # Add hover effect
        add_button_hover_effect(btn_back, '#34495e', get_hover_color('#34495e'))

        # Title
        tk.Label(header_frame, text="📊 THỐNG KÊ DOANH THU THÁNG",
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Month/Year selection frame
        selection_frame = tk.Frame(content_frame, bg='white')
        selection_frame.pack(fill='x', pady=(0, 20))

        tk.Label(selection_frame, text="Chọn tháng:", font=('Arial', 12, 'bold'),
                bg='white').pack(side='left', padx=(0, 10))

        # Month dropdown
        current_month = datetime.now().month
        current_year = datetime.now().year

        month_var = tk.StringVar(value=str(current_month))
        month_combo = ttk.Combobox(selection_frame, textvariable=month_var,
                                   values=[str(i) for i in range(1, 13)],
                                   state='readonly', width=5, font=('Arial', 12))
        month_combo.pack(side='left', padx=(0, 20))

        tk.Label(selection_frame, text="Năm:", font=('Arial', 12, 'bold'),
                bg='white').pack(side='left', padx=(0, 10))

        # Year dropdown
        year_var = tk.StringVar(value=str(current_year))
        year_combo = ttk.Combobox(selection_frame, textvariable=year_var,
                                  values=[str(i) for i in range(2020, 2030)],
                                  state='readonly', width=8, font=('Arial', 12))
        year_combo.pack(side='left', padx=(0, 20))

        # View button
        btn_view = tk.Button(selection_frame, text="🔍 Xem thống kê",
                            bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                            padx=15, pady=8, relief='raised', cursor='hand2', bd=2)
        btn_view.pack(side='left', padx=(0, 10))
        # Add hover effect
        add_button_hover_effect(btn_view, '#3498db', get_hover_color('#3498db'))

        # Report button
        btn_report = tk.Button(selection_frame, text="📄 Báo cáo",
                              bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                              padx=15, pady=8, relief='raised', cursor='hand2', bd=2,
                              command=lambda: self.show_sales_report(month_var.get(), year_var.get()))
        btn_report.pack(side='left')
        # Add hover effect
        add_button_hover_effect(btn_report, '#27ae60', get_hover_color('#27ae60'))

        # Sort filter frame
        sort_frame = tk.Frame(content_frame, bg='white')
        sort_frame.pack(fill='x', pady=(0, 20))

        tk.Label(sort_frame, text="Sắp xếp theo:", font=('Arial', 12, 'bold'),
                bg='white').pack(side='left', padx=(0, 10))

        # Sort dropdown
        sort_var = tk.StringVar(value="Doanh thu (Cao → Thấp)")
        sort_combo = ttk.Combobox(sort_frame, textvariable=sort_var,
                                  values=[
                                      "Doanh thu (Cao → Thấp)",
                                      "Số lượng bán (Cao → Thấp)",
                                      "Mã sản phẩm (A → Z)",
                                      "Tên sản phẩm (A → Z)"
                                  ],
                                  state='readonly', width=30, font=('Arial', 11))
        sort_combo.pack(side='left')

        # Summary frame
        summary_frame = tk.Frame(content_frame, bg='#ecf0f1', relief='solid', bd=1)
        summary_frame.pack(fill='x', pady=(0, 20))

        summary_inner = tk.Frame(summary_frame, bg='#ecf0f1', padx=20, pady=15)
        summary_inner.pack(fill='x')

        # Total revenue label
        total_revenue_label = tk.Label(summary_inner, text="Tổng doanh thu: 0 VNĐ",
                                      font=('Arial', 16, 'bold'), bg='#ecf0f1', fg='#27ae60')
        total_revenue_label.pack(side='left', padx=(0, 40))

        # Total products sold label
        total_products_label = tk.Label(summary_inner, text="Tổng sản phẩm bán: 0",
                                       font=('Arial', 16, 'bold'), bg='#ecf0f1', fg='#3498db')
        total_products_label.pack(side='left')

        # Treeview frame
        tree_frame = tk.Frame(content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True)

        # Scrollbars
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        hsb = tk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview - 5 columns (removed "Đơn giá")
        columns = ("STT", "Mã SP", "Tên sản phẩm", "SL bán", "Doanh thu")
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set, height=15)

        # Configure scrollbars
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill='both', expand=True)

        # Column headings
        tree.heading("STT", text="STT")
        tree.heading("Mã SP", text="Mã sản phẩm")
        tree.heading("Tên sản phẩm", text="Tên sản phẩm")
        tree.heading("SL bán", text="Số lượng bán")
        tree.heading("Doanh thu", text="Doanh thu")

        # Column widths
        tree.column("STT", width=60, anchor='center')
        tree.column("Mã SP", width=120, anchor='center')
        tree.column("Tên sản phẩm", width=350, anchor='w')
        tree.column("SL bán", width=120, anchor='center')
        tree.column("Doanh thu", width=200, anchor='e')

        # Configure treeview style for larger font
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 11), rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        def load_sales_data():
            """Load sales data for selected month/year with sorting"""
            try:
                month = int(month_var.get())
                year = int(year_var.get())
                sort_option = sort_var.get()

                conn = get_db_connection()
                cursor = conn.cursor()

                # Determine ORDER BY clause based on sort option
                if sort_option == "Doanh thu (Cao → Thấp)":
                    order_by = "total_sales DESC"
                elif sort_option == "Số lượng bán (Cao → Thấp)":
                    order_by = "total_quantity DESC"
                elif sort_option == "Mã sản phẩm (A → Z)":
                    order_by = "ct.MaSP ASC"
                elif sort_option == "Tên sản phẩm (A → Z)":
                    order_by = "ct.TenSP ASC"
                else:
                    order_by = "total_sales DESC"  # Default

                # Get sales data from cthoadon joined with hoadon
                # Group by product (MaSP, TenSP) - combining all colors and sizes
                # Use ThanhTien from cthoadon (actual sold price)
                query = f"""
                    SELECT 
                        ct.MaSP,
                        ct.TenSP,
                        SUM(ct.SoLuongMua) as total_quantity,
                        SUM(ct.ThanhTien) as total_sales
                    FROM cthoadon ct
                    INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
                    WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
                    GROUP BY ct.MaSP, ct.TenSP
                    ORDER BY {order_by}
                """

                cursor.execute(query, (month, year))

                sales_data = cursor.fetchall()

                # Clear existing data
                for item in tree.get_children():
                    tree.delete(item)

                # Calculate totals
                total_revenue = 0
                total_quantity = 0

                # Populate treeview
                for idx, (ma_sp, ten_sp, quantity, sales) in enumerate(sales_data, 1):
                    total_revenue += sales
                    total_quantity += quantity

                    tree.insert("", "end", values=(
                        idx,
                        ma_sp,
                        ten_sp,
                        f"{quantity:,}",
                        f"{sales:,.0f} VNĐ"
                    ))

                # Update summary labels
                total_revenue_label.config(text=f"Tổng doanh thu: {total_revenue:,.0f} VNĐ")
                total_products_label.config(text=f"Tổng sản phẩm bán: {total_quantity:,}")

                # Show message if no data
                if not sales_data:
                    messagebox.showinfo("Thông báo", 
                                      f"Không có dữ liệu bán hàng cho tháng {month}/{year}")

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        # Bind view button
        btn_view.config(command=load_sales_data)

        # Bind sort combo to reload data when changed
        sort_combo.bind('<<ComboboxSelected>>', lambda e: load_sales_data())

        # Load data for current month by default
        load_sales_data()

    def show_sales_report(self, month, year):
        """Show professional sales report in a popup window with charts"""
        # Create popup window
        report_window = tk.Toplevel(self.root)
        report_window.title(f"📊 Báo cáo doanh thu tháng {month}/{year}")
        report_window.geometry("1200x900")
        report_window.resizable(True, True)

        # Main container with close button frame
        button_container = tk.Frame(report_window, bg='#f5f5f5', height=50)
        button_container.pack(fill='x', side='bottom')
        button_container.pack_propagate(False)

        # Close button
        btn_close = tk.Button(button_container, text="✖ Đóng",
                            bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                            padx=20, pady=8, relief='raised', cursor='hand2', bd=2,
                            command=report_window.destroy)
        btn_close.pack(pady=10)
        add_button_hover_effect(btn_close, '#e74c3c', get_hover_color('#e74c3c'))

        # Scrollable canvas for report content
        canvas_frame = tk.Frame(report_window, bg='#f5f5f5')
        canvas_frame.pack(fill='both', expand=True, padx=0, pady=0)

        main_canvas = tk.Canvas(canvas_frame, bg='#f5f5f5', highlightthickness=0)
        main_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg='#f5f5f5')

        main_scrollbar.pack(side='right', fill='y')
        main_canvas.pack(side='left', fill='both', expand=True)

        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        def update_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox('all'))

        scrollable_frame.bind('<Configure>', update_scroll_region)

        def configure_canvas_width(event):
            canvas_width = event.width
            main_canvas.itemconfig(canvas_window, width=canvas_width)

        main_canvas.bind('<Configure>', configure_canvas_width)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        main_canvas.bind("<Enter>", lambda e: main_canvas.bind_all("<MouseWheel>", on_mousewheel))
        main_canvas.bind("<Leave>", lambda e: main_canvas.unbind_all("<MouseWheel>"))

        # Report paper container
        paper = tk.Frame(scrollable_frame, bg='white', relief='solid', bd=2, padx=40, pady=40)
        paper.pack(padx=2, pady=15, fill='both', expand=True)

        # Header with logo and shop info
        header_container = tk.Frame(paper, bg='white')
        header_container.pack(fill='x', pady=(0, 10))

        # Left: Shop info
        shop_info = tk.Frame(header_container, bg='white')
        shop_info.pack(side='left', anchor='nw')

        tk.Label(shop_info, text="Cửa hàng giày nhóm 10", font=('Arial', 16, 'bold'),
                bg='white', fg='#2c3e50').pack(anchor='w')
        tk.Label(shop_info, text="Km10 Đ. Nguyễn Trãi, P. Mộ Lao, Hà Đông, Hà Nội", font=('Arial', 10),
                bg='white', fg='#7f8c8d').pack(anchor='w')
        tk.Label(shop_info, text="Số điện thoại: (028) 1234 5678", font=('Arial', 10),
                bg='white', fg='#7f8c8d').pack(anchor='w')
        tk.Label(shop_info, text="Email: nhom10@stu.ptit.edu.vn", font=('Arial', 10),
                bg='white', fg='#7f8c8d').pack(anchor='w')

        # Right: Logo
        try:
            from PIL import Image, ImageTk
            from utils.image_utils import load_image_from_path
            logo_img = load_image_from_path("D:/shop_giay/shoes_shop/image.png", (100, 100))
            if logo_img:
                logo_label = tk.Label(header_container, image=logo_img, bg='white')
                logo_label.image = logo_img
                logo_label.pack(side='right', padx=(10, 0))
        except:
            pass

        # Red separator line
        tk.Frame(paper, bg='#8B0000', height=3).pack(fill='x', pady=(10, 20))

        # Report title
        tk.Label(paper, text="BÁO CÁO DOANH THU", font=('Arial', 22, 'bold'),
                bg='white', fg='#8B0000').pack(pady=(10, 5))

        # Report period and date
        report_info_frame = tk.Frame(paper, bg='white')
        report_info_frame.pack(pady=(0, 20))

        tk.Label(report_info_frame, text=f"Tháng {month}/{year}", font=('Arial', 14, 'bold'),
                bg='white', fg='#2c3e50').pack()
        tk.Label(report_info_frame, text=f"Ngày lập: {datetime.now().strftime('%d/%m/%Y')}",
                font=('Arial', 11), bg='white', fg='#7f8c8d').pack()

        # Get sales data from database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get total sales data
            cursor.execute("""
                SELECT 
                    ct.MaSP,
                    ct.TenSP,
                    SUM(ct.SoLuongMua) as total_quantity,
                    SUM(ct.ThanhTien) as total_sales
                FROM cthoadon ct
                INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
                WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
                GROUP BY ct.MaSP, ct.TenSP
                ORDER BY total_sales DESC
            """, (month, year))

            sales_data = cursor.fetchall()

            # Calculate summary statistics
            total_revenue = sum(row[3] for row in sales_data)
            total_quantity = sum(row[2] for row in sales_data)
            total_products = len(sales_data)

            # Summary statistics section
            stats_frame = tk.Frame(paper, bg='#ecf0f1', relief='solid', bd=1)
            stats_frame.pack(fill='x', pady=(0, 20))

            stats_inner = tk.Frame(stats_frame, bg='#ecf0f1', padx=20, pady=15)
            stats_inner.pack(fill='x')

            # Three columns for statistics
            stat1 = tk.Frame(stats_inner, bg='#ecf0f1')
            stat1.pack(side='left', expand=True, fill='x')
            tk.Label(stat1, text="Tổng doanh thu", font=('Arial', 11),
                    bg='#ecf0f1', fg='#7f8c8d').pack()
            tk.Label(stat1, text=f"{total_revenue:,.0f} VNĐ", font=('Arial', 16, 'bold'),
                    bg='#ecf0f1', fg='#27ae60').pack()

            stat2 = tk.Frame(stats_inner, bg='#ecf0f1')
            stat2.pack(side='left', expand=True, fill='x')
            tk.Label(stat2, text="Sản phẩm bán ra", font=('Arial', 11),
                    bg='#ecf0f1', fg='#7f8c8d').pack()
            tk.Label(stat2, text=f"{total_quantity:,}", font=('Arial', 16, 'bold'),
                    bg='#ecf0f1', fg='#3498db').pack()

            stat3 = tk.Frame(stats_inner, bg='#ecf0f1')
            stat3.pack(side='left', expand=True, fill='x')
            tk.Label(stat3, text="Loại sản phẩm", font=('Arial', 11),
                    bg='#ecf0f1', fg='#7f8c8d').pack()
            tk.Label(stat3, text=f"{total_products}", font=('Arial', 16, 'bold'),
                    bg='#ecf0f1', fg='#e67e22').pack()

            # Chart section - Top 5 products
            if sales_data:
                tk.Label(paper, text="TOP 5 SẢN PHẨM BÁN CHẠY", font=('Arial', 14, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w', pady=(10, 10))

                # Simple bar chart using frames
                chart_frame = tk.Frame(paper, bg='white')
                chart_frame.pack(fill='x', pady=(0, 20))

                top5 = sales_data[:5]
                max_sales = max(row[3] for row in top5) if top5 else 1

                for idx, (ma_sp, ten_sp, quantity, sales) in enumerate(top5):
                    # Product row
                    row_frame = tk.Frame(chart_frame, bg='white')
                    row_frame.pack(fill='x', pady=3)

                    # Product name (truncate if too long)
                    name_display = ten_sp[:30] + "..." if len(ten_sp) > 30 else ten_sp
                    tk.Label(row_frame, text=f"{idx+1}. {name_display}", font=('Arial', 10),
                            bg='white', fg='#2c3e50', width=35, anchor='w').pack(side='left')

                    # Bar chart
                    bar_width = int((sales / max_sales) * 400)
                    colors = ['#e74c3c', '#3498db', '#f39c12', '#27ae60', '#9b59b6']
                    bar = tk.Frame(row_frame, bg=colors[idx % 5], width=bar_width, height=25)
                    bar.pack(side='left', padx=(10, 10))
                    bar.pack_propagate(False)

                    # Sales value
                    tk.Label(row_frame, text=f"{sales:,.0f} VNĐ", font=('Arial', 10, 'bold'),
                            bg='white', fg='#2c3e50').pack(side='left')

            # Detailed table section
            tk.Label(paper, text="CHI TIẾT DOANH THU SẢN PHẨM", font=('Arial', 14, 'bold'),
                    bg='white', fg='#2c3e50').pack(anchor='w', pady=(20, 10))

            # Table header
            table_header = tk.Frame(paper, bg='#2c3e50', height=40)
            table_header.pack(fill='x', pady=(0, 0))
            table_header.pack_propagate(False)

            header_cols = [
                ("STT", 0.00, 0.08, 'center'),
                ("MÃ SẢN PHẨM", 0.08, 0.15, 'center'),
                ("TÊN SẢN PHẨM", 0.23, 0.37, 'w'),
                ("SỐ LƯỢNG", 0.60, 0.15, 'center'),
                ("DOANH THU", 0.75, 0.25, 'e')
            ]

            for text, relx, relwidth, anchor in header_cols:
                header_label = tk.Label(table_header, text=text, font=('Arial', 11, 'bold'),
                                      bg='#2c3e50', fg='white', anchor=anchor)
                header_label.place(relx=relx, rely=0, relwidth=relwidth, relheight=1)

            # Table rows
            for idx, (ma_sp, ten_sp, quantity, sales) in enumerate(sales_data):
                row_bg = '#f9f9f9' if idx % 2 == 0 else 'white'
                row_frame = tk.Frame(paper, bg=row_bg, height=35)
                row_frame.pack(fill='x')
                row_frame.pack_propagate(False)

                # STT
                tk.Label(row_frame, text=str(idx+1), font=('Arial', 10),
                        bg=row_bg, fg='#333333', anchor='center').place(
                            relx=0.00, rely=0, relwidth=0.08, relheight=1)

                # MaSP
                tk.Label(row_frame, text=ma_sp, font=('Arial', 10),
                        bg=row_bg, fg='#333333', anchor='center').place(
                            relx=0.08, rely=0, relwidth=0.15, relheight=1)

                # TenSP
                tk.Label(row_frame, text=ten_sp, font=('Arial', 10),
                        bg=row_bg, fg='#333333', anchor='w').place(
                            relx=0.23, rely=0, relwidth=0.37, relheight=1)

                # Quantity
                tk.Label(row_frame, text=f"{quantity:,}", font=('Arial', 10),
                        bg=row_bg, fg='#333333', anchor='center').place(
                            relx=0.60, rely=0, relwidth=0.15, relheight=1)

                # Sales
                tk.Label(row_frame, text=f"{sales:,.0f} VNĐ", font=('Arial', 10),
                        bg=row_bg, fg='#333333', anchor='e').place(
                            relx=0.75, rely=0, relwidth=0.25, relheight=1)

            # Summary row
            summary_row = tk.Frame(paper, bg='#ecf0f1', height=45, relief='solid', bd=1)
            summary_row.pack(fill='x', pady=(2, 0))
            summary_row.pack_propagate(False)

            tk.Label(summary_row, text="TỔNG CỘNG", font=('Arial', 12, 'bold'),
                    bg='#ecf0f1', fg='#2c3e50', anchor='center').place(
                        relx=0.00, rely=0, relwidth=0.60, relheight=1)

            tk.Label(summary_row, text=f"{total_quantity:,}", font=('Arial', 12, 'bold'),
                    bg='#ecf0f1', fg='#3498db', anchor='center').place(
                        relx=0.60, rely=0, relwidth=0.15, relheight=1)

            tk.Label(summary_row, text=f"{total_revenue:,.0f} VNĐ", font=('Arial', 12, 'bold'),
                    bg='#ecf0f1', fg='#27ae60', anchor='e').place(
                        relx=0.75, rely=0, relwidth=0.25, relheight=1)

            # Footer with signature
            tk.Frame(paper, bg='#8B0000', height=2).pack(fill='x', pady=(30, 20))

            signature_frame = tk.Frame(paper, bg='white')
            signature_frame.pack(fill='x')

            tk.Label(signature_frame, text="Chữ ký người lập báo cáo",
                    font=('Arial', 11, 'italic'), bg='white', fg='#7f8c8d').pack(side='right', pady=(10, 0))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {str(e)}")
            report_window.destroy()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
