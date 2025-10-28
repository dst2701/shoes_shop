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
        btn_view.pack(side='left')
        # Add hover effect
        add_button_hover_effect(btn_view, '#3498db', get_hover_color('#3498db'))

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
        tree.heading("Mã SP", text="Mã SP")
        tree.heading("Tên sản phẩm", text="Tên sản phẩm")
        tree.heading("SL bán", text="SL bán")
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
