"""
Invoice History View - Lịch sử mua hàng của khách hàng
"""
import tkinter as tk
from tkinter import ttk, messagebox
from config.database import get_db_connection
from datetime import datetime
from utils.ui_effects import add_button_hover_effect, get_hover_color


class InvoiceHistoryView:
    def __init__(self, root):
        self.root = root

    def show(self, role, username, return_callback):
        """Show invoice history for buyer"""
        if role != "buyer":
            messagebox.showerror("Lỗi", "Chức năng này chỉ dành cho khách hàng!")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Shop Shoes - Lịch sử mua hàng")

        # Main container
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Back button
        btn_back = tk.Button(header_frame, text="← Quay lại",
                            command=lambda: return_callback(role, username),
                            bg='#34495e', fg='white', font=('Arial', 12, 'bold'),
                            padx=15, pady=8, relief='raised', cursor='hand2', bd=2)
        btn_back.pack(side='left', padx=20, pady=20)
        add_button_hover_effect(btn_back, '#34495e', get_hover_color('#34495e'))

        # Title
        tk.Label(header_frame, text="📜 LỊCH SỬ MUA HÀNG",
                font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white').pack(side='left', padx=20)

        # User info
        tk.Label(header_frame, text=f"Khách hàng: {username}",
                font=('Arial', 14), bg='#2c3e50', fg='white').pack(side='right', padx=20)

        # Content frame
        content_frame = tk.Frame(main_frame, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Summary frame
        summary_frame = tk.Frame(content_frame, bg='#ecf0f1', relief='solid', bd=1)
        summary_frame.pack(fill='x', pady=(0, 20))

        summary_inner = tk.Frame(summary_frame, bg='#ecf0f1', padx=20, pady=15)
        summary_inner.pack(fill='x')

        # Total invoices label
        total_invoices_label = tk.Label(summary_inner, text="Tổng đơn hàng: 0",
                                       font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#3498db')
        total_invoices_label.pack(side='left', padx=(0, 40))

        # Total amount label
        total_amount_label = tk.Label(summary_inner, text="Tổng chi tiêu: 0 VNĐ",
                                     font=('Arial', 14, 'bold'), bg='#ecf0f1', fg='#27ae60')
        total_amount_label.pack(side='left')

        # Treeview frame
        tree_frame = tk.Frame(content_frame, bg='white')
        tree_frame.pack(fill='both', expand=True)

        # Scrollbars
        vsb = tk.Scrollbar(tree_frame, orient="vertical")
        hsb = tk.Scrollbar(tree_frame, orient="horizontal")

        # Treeview for invoices
        columns = ("STT", "Mã HĐ", "Ngày lập", "Tổng tiền", "SL sản phẩm")
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
        tree.heading("Mã HĐ", text="Mã hóa đơn")
        tree.heading("Ngày lập", text="Ngày lập")
        tree.heading("Tổng tiền", text="Tổng tiền")
        tree.heading("SL sản phẩm", text="Số lượng SP")

        # Column widths
        tree.column("STT", width=50, anchor='center')
        tree.column("Mã HĐ", width=120, anchor='center')
        tree.column("Ngày lập", width=200, anchor='center')
        tree.column("Tổng tiền", width=180, anchor='e')
        tree.column("SL sản phẩm", width=120, anchor='center')

        # Configure treeview style
        style = ttk.Style()
        style.configure("History.Treeview", font=('Arial', 11), rowheight=35)
        style.configure("History.Treeview.Heading", font=('Arial', 12, 'bold'))
        tree.configure(style="History.Treeview")

        # Action buttons frame
        action_frame = tk.Frame(content_frame, bg='white')
        action_frame.pack(fill='x', pady=(20, 0))

        # View details button
        btn_view_details = tk.Button(action_frame, text="📋 Xem chi tiết",
                                     bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                     padx=20, pady=10, cursor='hand2', relief='raised',
                                     bd=2, state='disabled')
        btn_view_details.pack(side='left')
        add_button_hover_effect(btn_view_details, '#3498db', get_hover_color('#3498db'))

        # Status label
        status_label = tk.Label(action_frame, text="Chọn hóa đơn để xem chi tiết",
                               font=('Arial', 10), fg='#7f8c8d', bg='white')
        status_label.pack(side='left', padx=(20, 0))

        def load_invoice_history():
            """Load invoice history for current user"""
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

                # Get all invoices for this customer with total amount and product count
                cursor.execute("""
                    SELECT 
                        hd.MaHD,
                        hd.NgayLap,
                        SUM(ct.ThanhTien) as TongTien,
                        SUM(ct.SoLuongMua) as TongSL
                    FROM hoadon hd
                    INNER JOIN cthoadon ct ON hd.MaHD = ct.MaHD
                    WHERE hd.MaKH = %s
                    GROUP BY hd.MaHD, hd.NgayLap
                    ORDER BY hd.MaHD DESC
                """, (ma_kh,))

                invoices = cursor.fetchall()

                # Clear existing data
                for item in tree.get_children():
                    tree.delete(item)

                # Calculate totals
                total_invoices = len(invoices)
                total_amount = 0

                # Populate treeview
                for idx, (ma_hd, ngay_lap, tong_tien, tong_sl) in enumerate(invoices, 1):
                    total_amount += tong_tien

                    # Format date (only date, no time)
                    ngay_lap_str = ngay_lap.strftime("%d/%m/%Y") if ngay_lap else "N/A"

                    tree.insert("", "end", iid=ma_hd, values=(
                        idx,
                        ma_hd,
                        ngay_lap_str,
                        f"{tong_tien:,.0f} VNĐ",
                        f"{int(tong_sl):,}"
                    ))

                # Update summary labels
                total_invoices_label.config(text=f"Tổng đơn hàng: {total_invoices:,}")
                total_amount_label.config(text=f"Tổng chi tiêu: {total_amount:,.0f} VNĐ")

                # Show message if no data
                if not invoices:
                    messagebox.showinfo("Thông báo", "Bạn chưa có đơn hàng nào!")
                    status_label.config(text="Chưa có đơn hàng", fg='#e74c3c')
                else:
                    status_label.config(text=f"Tìm thấy {total_invoices} đơn hàng", fg='#27ae60')

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải lịch sử: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

        def on_invoice_select(event):
            """Handle invoice selection"""
            selection = tree.selection()

            if selection:
                btn_view_details.config(state='normal')
                status_label.config(text="Click 'Xem chi tiết' để xem thông tin đơn hàng", fg='#3498db')
            else:
                btn_view_details.config(state='disabled')
                status_label.config(text="Chọn hóa đơn để xem chi tiết", fg='#7f8c8d')

        def view_invoice_details():
            """Show detailed view of selected invoice"""
            selection = tree.selection()
            if not selection:
                return

            ma_hd = selection[0]

            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Chi tiết hóa đơn {ma_hd}")
            details_window.geometry("900x700")
            details_window.resizable(False, False)

            # Center window
            details_window.update_idletasks()
            x = (details_window.winfo_screenwidth() // 2) - (900 // 2)
            y = (details_window.winfo_screenheight() // 2) - (700 // 2)
            details_window.geometry(f"+{x}+{y}")

            details_window.transient(self.root)
            details_window.grab_set()
            details_window.lift()
            details_window.focus_force()

            # Header
            header = tk.Frame(details_window, bg='#3498db', height=80)
            header.pack(fill='x')
            header.pack_propagate(False)

            tk.Label(header, text=f"CHI TIẾT HÓA ĐƠN: {ma_hd}",
                    font=('Arial', 18, 'bold'), bg='#3498db', fg='white').pack(pady=25)

            # Content
            content = tk.Frame(details_window, bg='white', padx=30, pady=20)
            content.pack(fill='both', expand=True)

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Get invoice info
                cursor.execute("""
                    SELECT hd.NgayLap, kh.TenKH, kh.SDT, kh.DiaChi
                    FROM hoadon hd
                    INNER JOIN khachhang kh ON hd.MaKH = kh.MaKH
                    WHERE hd.MaHD = %s
                """, (ma_hd,))

                invoice_info = cursor.fetchone()
                if invoice_info:
                    ngay_lap, ten_kh, sdt, dia_chi = invoice_info

                    # Invoice info section
                    info_frame = tk.Frame(content, bg='#ecf0f1', relief='solid', bd=1)
                    info_frame.pack(fill='x', pady=(0, 20))

                    info_inner = tk.Frame(info_frame, bg='#ecf0f1', padx=20, pady=15)
                    info_inner.pack(fill='x')

                    tk.Label(info_inner, text=f"Ngày lập: {ngay_lap.strftime('%d/%m/%Y')}",
                            font=('Arial', 12), bg='#ecf0f1').pack(anchor='w', pady=2)
                    tk.Label(info_inner, text=f"Khách hàng: {ten_kh}",
                            font=('Arial', 12), bg='#ecf0f1').pack(anchor='w', pady=2)
                    tk.Label(info_inner, text=f"SĐT: {sdt}",
                            font=('Arial', 12), bg='#ecf0f1').pack(anchor='w', pady=2)
                    tk.Label(info_inner, text=f"Địa chỉ: {dia_chi}",
                            font=('Arial', 12), bg='#ecf0f1').pack(anchor='w', pady=2)

                # Get invoice details (products)
                cursor.execute("""
                    SELECT MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien
                    FROM cthoadon
                    WHERE MaHD = %s
                    ORDER BY TenSP
                """, (ma_hd,))

                products = cursor.fetchall()

                # Products label
                tk.Label(content, text="Danh sách sản phẩm:",
                        font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))

                # Products treeview
                detail_tree_frame = tk.Frame(content, bg='white')
                detail_tree_frame.pack(fill='both', expand=True)

                detail_vsb = tk.Scrollbar(detail_tree_frame, orient="vertical")

                detail_cols = ("STT", "Mã SP", "Tên sản phẩm", "Màu", "Size", "SL", "Đơn giá", "Thành tiền")
                detail_tree = ttk.Treeview(detail_tree_frame, columns=detail_cols, show='headings',
                                          yscrollcommand=detail_vsb.set, height=12)

                detail_vsb.config(command=detail_tree.yview)
                detail_vsb.pack(side='right', fill='y')
                detail_tree.pack(fill='both', expand=True)

                # Configure columns
                detail_tree.heading("STT", text="STT")
                detail_tree.heading("Mã SP", text="Mã SP")
                detail_tree.heading("Tên sản phẩm", text="Tên sản phẩm")
                detail_tree.heading("Màu", text="Màu sắc")
                detail_tree.heading("Size", text="Size")
                detail_tree.heading("SL", text="SL")
                detail_tree.heading("Đơn giá", text="Đơn giá")
                detail_tree.heading("Thành tiền", text="Thành tiền")

                detail_tree.column("STT", width=40, anchor='center')
                detail_tree.column("Mã SP", width=80, anchor='center')
                detail_tree.column("Tên sản phẩm", width=200, anchor='w')
                detail_tree.column("Màu", width=90, anchor='center')
                detail_tree.column("Size", width=60, anchor='center')
                detail_tree.column("SL", width=50, anchor='center')
                detail_tree.column("Đơn giá", width=120, anchor='e')
                detail_tree.column("Thành tiền", width=120, anchor='e')

                # Populate products
                total = 0
                for idx, (ma_sp, ten_sp, mau_sac, size, so_luong, don_gia, thanh_tien) in enumerate(products, 1):
                    total += thanh_tien
                    detail_tree.insert("", "end", values=(
                        idx,
                        ma_sp,
                        ten_sp,
                        mau_sac,
                        size,
                        so_luong,
                        f"{don_gia:,.0f} VNĐ",
                        f"{thanh_tien:,.0f} VNĐ"
                    ))

                # Total frame
                total_frame = tk.Frame(content, bg='white')
                total_frame.pack(fill='x', pady=(20, 10))

                tk.Label(total_frame, text="TỔNG CỘNG:",
                        font=('Arial', 16, 'bold'), bg='white', fg='#2c3e50').pack(side='left')
                tk.Label(total_frame, text=f"{total:,.0f} VNĐ",
                        font=('Arial', 16, 'bold'), bg='white', fg='#27ae60').pack(side='right')

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

            # Close button
            btn_close = tk.Button(content, text="Đóng", command=details_window.destroy,
                                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                                 padx=30, pady=10, cursor='hand2', relief='raised', bd=2)
            btn_close.pack(pady=(10, 0))
            add_button_hover_effect(btn_close, '#95a5a6', get_hover_color('#95a5a6'))

        # Bind events
        tree.bind("<<TreeviewSelect>>", on_invoice_select)
        btn_view_details.config(command=view_invoice_details)

        # Load data on show
        load_invoice_history()

