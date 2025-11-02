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
        tree.heading("SL sản phẩm", text="Số lượng Sản Phẩm")

        # Column widths
        tree.column("STT", width=50, anchor='center')
        tree.column("Mã HĐ", width=120, anchor='center')
        tree.column("Ngày lập", width=200, anchor='center')
        tree.column("Tổng tiền", width=180, anchor='e')
        tree.column("SL sản phẩm", width=120, anchor='center')

        # Configure treeview style
        style = ttk.Style()
        style.configure("History.Treeview", font=('Arial', 13), rowheight=35)
        style.configure("History.Treeview.Heading", font=('Arial', 15, 'bold'))
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
            """Show detailed view of selected invoice - A4 format"""
            selection = tree.selection()
            if not selection:
                return

            ma_hd = selection[0]

            # Create details window - Optimized for 16:9 screens with resizing capability
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Hóa đơn #{ma_hd}")

            # Get screen dimensions
            screen_width = details_window.winfo_screenwidth()
            screen_height = details_window.winfo_screenheight()

            # Set window size to fit full invoice width (increased to 1050 to show right side completely)
            window_width = 1050
            window_height = int(screen_height * 0.85)  # 85% of screen height

            details_window.geometry(f"{window_width}x{window_height}")
            details_window.resizable(True, True)  # Allow resizing
            details_window.minsize(950, 600)  # Minimum size (increased to fit invoice)
            details_window.configure(bg='#f5f5f5')

            # Center window
            details_window.update_idletasks()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            details_window.transient(self.root)
            details_window.grab_set()
            details_window.lift()
            details_window.focus_force()

            # Main container with button at bottom (not scrollable)
            main_container = tk.Frame(details_window, bg='#f5f5f5')
            main_container.pack(fill='both', expand=True)

            # Scrollable canvas for invoice content
            canvas_frame = tk.Frame(main_container, bg='#f5f5f5')
            canvas_frame.pack(fill='both', expand=True, padx=0, pady=0)

            main_canvas = tk.Canvas(canvas_frame, bg='#f5f5f5', highlightthickness=0)
            main_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=main_canvas.yview)

            scrollable_frame = tk.Frame(main_canvas, bg='#f5f5f5')
            scrollable_frame.bind(
                "<Configure>",
                lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            )

            main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            main_canvas.configure(yscrollcommand=main_scrollbar.set)

            # Enable mousewheel scrolling
            def _on_mousewheel(event):
                main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

            # Unbind mousewheel when window is closed
            def _on_close():
                main_canvas.unbind_all("<MouseWheel>")
                details_window.destroy()

            main_scrollbar.pack(side="right", fill="y")
            main_canvas.pack(side="left", fill="both", expand=True)

            # Fixed close button at bottom (outside scroll area)
            button_container = tk.Frame(main_container, bg='#f5f5f5', height=70)
            button_container.pack(fill='x', side='bottom', padx=20, pady=10)
            button_container.pack_propagate(False)

            btn_close = tk.Button(button_container, text="✖ Đóng", command=_on_close,
                                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                 padx=40, pady=12, cursor='hand2', relief='raised', bd=2)
            btn_close.pack(anchor='center')
            add_button_hover_effect(btn_close, '#e74c3c', get_hover_color('#e74c3c'))

            # A4 paper container with border (like the template) - adjusted to minimize right margin
            paper = tk.Frame(scrollable_frame, bg='white', relief='solid', bd=2, padx=30, pady=30)
            paper.pack(padx=2, pady=15, fill='both', expand=True)

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Get invoice info (only columns that exist in khachhang table)
                cursor.execute("""
                    SELECT hd.NgayLap, kh.TenKH, kh.SDT, kh.DiaChi
                    FROM hoadon hd
                    INNER JOIN khachhang kh ON hd.MaKH = kh.MaKH
                    WHERE hd.MaHD = %s
                """, (ma_hd,))

                invoice_info = cursor.fetchone()
                if not invoice_info:
                    messagebox.showerror("Lỗi", "Không tìm thấy thông tin hóa đơn!")
                    details_window.destroy()
                    return

                ngay_lap, ten_kh, sdt, dia_chi = invoice_info

                # === TOP RED BORDER ===
                top_border = tk.Frame(paper, bg='#8B0000', height=4)
                top_border.pack(fill='x', pady=(0, 20))

                # === HEADER SECTION: INVOICE title + LOGO ===
                header_frame = tk.Frame(paper, bg='white')
                header_frame.pack(fill='x', pady=(0, 20))

                # Left: INVOICE title
                tk.Label(header_frame, text="HÓA ĐƠN BÁN HÀNG", font=('Arial', 24, 'bold'),
                        bg='white', fg='#666666').pack(side='left', anchor='nw')

                # Right: LOGO (image.png from root folder)
                try:
                    from PIL import Image, ImageTk
                    import os
                    # Try multiple paths
                    possible_paths = [
                        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'image.png'),  # Root folder
                        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'images', 'image.png'),  # images folder
                        'D:\\shop_giay\\shoes_shop\\image.png'  # Absolute path
                    ]

                    logo_loaded = False
                    for logo_path in possible_paths:
                        if os.path.exists(logo_path):
                            logo_img = Image.open(logo_path)
                            # Resize to circular-looking size
                            logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
                            logo_photo = ImageTk.PhotoImage(logo_img)
                            logo_label = tk.Label(header_frame, image=logo_photo, bg='white', bd=0, relief='flat')
                            logo_label.image = logo_photo  # Keep reference
                            logo_label.pack(side='right', anchor='ne', padx=(10, 0))
                            logo_loaded = True
                            break

                    if not logo_loaded:
                        # Fallback: Show "LOGO" text
                        tk.Label(header_frame, text="LOGO", font=('Arial', 14, 'bold'),
                                bg='#cccccc', fg='#666666', width=8, height=4, relief='solid', bd=1).pack(side='right', anchor='ne')
                except Exception as e:
                    print(f"Cannot load logo: {e}")
                    # Fallback: Show "LOGO" text
                    tk.Label(header_frame, text="LOGO", font=('Arial', 14, 'bold'),
                            bg='#cccccc', fg='#666666', width=8, height=4, relief='solid', bd=1).pack(side='right', anchor='ne')

                # === SHOP INFO (left) + INVOICE INFO (right) ===
                info_section = tk.Frame(paper, bg='white')
                info_section.pack(fill='x', pady=(0, 25))

                # Left column: Shop info
                shop_frame = tk.Frame(info_section, bg='white')
                shop_frame.pack(side='left', anchor='nw')

                tk.Label(shop_frame, text="Cửa Hàng Giày Nhóm 10", font=('Arial', 15, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w')
                tk.Label(shop_frame, text="Km10 Đ. Nguyễn Trãi, P. Mộ Lao, Hà Đông, Hà Nội", font=('Arial', 13),
                        bg='white', fg='#555555').pack(anchor='w')
                tk.Label(shop_frame, text="Số điện thoại: (028) 1234 5678", font=('Arial', 13),
                        bg='white', fg='#555555').pack(anchor='w')
                tk.Label(shop_frame, text="Email: nhom10@stu.ptit.edu.vn", font=('Arial', 13),
                        bg='white', fg='#555555').pack(anchor='w')

                # Right column: Invoice metadata
                invoice_meta_frame = tk.Frame(info_section, bg='white')
                invoice_meta_frame.pack(side='right', anchor='ne')

                tk.Label(invoice_meta_frame, text="NGÀY LẬP", font=('Arial', 10, 'bold'),
                        bg='white', fg='#888888').pack(anchor='e')
                tk.Label(invoice_meta_frame, text=ngay_lap.strftime('%d/%m/%Y'), font=('Arial', 11),
                        bg='white', fg='#2c3e50').pack(anchor='e', pady=(0, 8))

                tk.Label(invoice_meta_frame, text="MÃ HÓA ĐƠN", font=('Arial', 10, 'bold'),
                        bg='white', fg='#888888').pack(anchor='e')
                tk.Label(invoice_meta_frame, text=ma_hd, font=('Arial', 11, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='e')

                # === BILL TO + SHIP TO ===
                billing_section = tk.Frame(paper, bg='white')
                billing_section.pack(fill='x', pady=(0, 25))

                # Left: BILL TO
                bill_frame = tk.Frame(billing_section, bg='white')
                bill_frame.pack(side='left', anchor='nw', fill='both', expand=True)

                tk.Label(bill_frame, text="THÔNG TIN KHÁCH HÀNG", font=('Arial', 13, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w')
                tk.Label(bill_frame, text=ten_kh, font=('Arial', 12),
                        bg='white', fg='#333333').pack(anchor='w', pady=(5, 0))
                tk.Label(bill_frame, text=dia_chi if dia_chi else "Chưa cập nhật", font=('Arial', 12),
                        bg='white', fg='#555555').pack(anchor='w')
                tk.Label(bill_frame, text=f"Số điện thoại: {sdt}", font=('Arial', 12),
                        bg='white', fg='#555555').pack(anchor='w')

                # Right: SHIP TO (same as BILL TO for now)
                ship_frame = tk.Frame(billing_section, bg='white')
                ship_frame.pack(side='right', anchor='ne', fill='both', expand=True)

                tk.Label(ship_frame, text="ĐỊA CHỈ GIAO HÀNG", font=('Arial', 13, 'bold'),
                        bg='white', fg='#2c3e50').pack(anchor='w')
                tk.Label(ship_frame, text=ten_kh, font=('Arial', 12),
                        bg='white', fg='#333333').pack(anchor='w', pady=(5, 0))
                tk.Label(ship_frame, text=dia_chi if dia_chi else "Chưa cập nhật", font=('Arial', 12),
                        bg='white', fg='#555555').pack(anchor='w')
                tk.Label(ship_frame, text=f"Số điện thoại: {sdt}", font=('Arial', 12),
                        bg='white', fg='#555555').pack(anchor='w')

                # === PRODUCTS TABLE ===
                # Get invoice details (products)
                cursor.execute("""
                    SELECT MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien
                    FROM cthoadon
                    WHERE MaHD = %s
                    ORDER BY TenSP
                """, (ma_hd,))

                products = cursor.fetchall()

                # Table header (RED background like template) - Using place() for perfect alignment
                table_header = tk.Frame(paper, bg='#8B0000', height=40)
                table_header.pack(fill='x', pady=(0, 0))
                table_header.pack_propagate(False)

                # Define column widths (relative positions)
                header_cols = [
                    ("MÔ TẢ SẢN PHẨM", 0.00, 0.45, 'w'),
                    ("SỐ LƯỢNG", 0.45, 0.15, 'center'),
                    ("ĐƠN GIÁ", 0.60, 0.20, 'e'),
                    ("THÀNH TIỀN", 0.80, 0.20, 'e')
                ]

                for text, relx, relwidth, anchor in header_cols:
                    header_label = tk.Label(table_header, text=text, font=('Arial', 13, 'bold'),
                                          bg='#8B0000', fg='white', anchor=anchor)
                    header_label.place(relx=relx, rely=0, relwidth=relwidth, relheight=1)

                # Table rows with place() layout
                subtotal = 0
                for idx, (ma_sp, ten_sp, mau_sac, size, so_luong, don_gia, thanh_tien) in enumerate(products):
                    subtotal += thanh_tien

                    row_bg = '#f9f9f9' if idx % 2 == 0 else 'white'
                    row_frame = tk.Frame(paper, bg=row_bg, height=32)
                    row_frame.pack(fill='x')
                    row_frame.pack_propagate(False)

                    # Description column
                    desc_text = f"{ten_sp} ({ma_sp}) - {mau_sac}/{size}"
                    desc_label = tk.Label(row_frame, text=desc_text, font=('Arial', 9),
                                         bg=row_bg, fg='#333333', anchor='w')
                    desc_label.place(relx=0.00, rely=0, relwidth=0.45, relheight=1)

                    # Quantity column
                    qty_label = tk.Label(row_frame, text=str(so_luong), font=('Arial', 9),
                                        bg=row_bg, fg='#333333', anchor='center')
                    qty_label.place(relx=0.45, rely=0, relwidth=0.15, relheight=1)

                    # Unit price column
                    price_label = tk.Label(row_frame, text=f"{don_gia:,.0f} VNĐ", font=('Arial', 9),
                                          bg=row_bg, fg='#333333', anchor='e')
                    price_label.place(relx=0.60, rely=0, relwidth=0.20, relheight=1)

                    # Total column
                    total_label = tk.Label(row_frame, text=f"{thanh_tien:,.0f} VNĐ", font=('Arial', 9),
                                          bg=row_bg, fg='#333333', anchor='e')
                    total_label.place(relx=0.80, rely=0, relwidth=0.20, relheight=1)

                # Add empty rows if needed (for design consistency)
                for i in range(max(0, 5 - len(products))):
                    empty_row = tk.Frame(paper, bg='white', height=30)
                    empty_row.pack(fill='x')
                    empty_row.pack_propagate(False)

                # === TOTALS SECTION (Right aligned like template) ===
                totals_container = tk.Frame(paper, bg='white')
                totals_container.pack(fill='x', pady=(20, 0))

                # Spacer to push totals to the right
                tk.Frame(totals_container, bg='white', width=400).pack(side='left')

                totals_frame = tk.Frame(totals_container, bg='white')
                totals_frame.pack(side='right')

                # Subtotal
                subtotal_row = tk.Frame(totals_frame, bg='white')
                subtotal_row.pack(fill='x', pady=3)
                tk.Label(subtotal_row, text="Tạm tính:", font=('Arial', 13),
                        bg='white', fg='#555555', width=25, anchor='e').pack(side='left', padx=(0, 20))
                tk.Label(subtotal_row, text=f"{subtotal:,.0f} VNĐ", font=('Arial', 13),
                        bg='white', fg='#333333', width=18, anchor='e').pack(side='left')

                # Discount (0 for now)
                discount_row = tk.Frame(totals_frame, bg='white')
                discount_row.pack(fill='x', pady=3)
                tk.Label(discount_row, text="Giảm giá:", font=('Arial', 13),
                        bg='white', fg='#555555', width=25, anchor='e').pack(side='left', padx=(0, 20))
                tk.Label(discount_row, text="0 VNĐ", font=('Arial', 13),
                        bg='white', fg='#333333', width=18, anchor='e').pack(side='left')

                # Tax (VAT)
                tax_row = tk.Frame(totals_frame, bg='white')
                tax_row.pack(fill='x', pady=3)
                tk.Label(tax_row, text="Thuế VAT (0%):", font=('Arial', 13),
                        bg='white', fg='#555555', width=25, anchor='e').pack(side='left', padx=(0, 20))
                tk.Label(tax_row, text="0 VNĐ", font=('Arial', 13),
                        bg='white', fg='#333333', width=18, anchor='e').pack(side='left')

                # Shipping/Handling
                shipping_row = tk.Frame(totals_frame, bg='white')
                shipping_row.pack(fill='x', pady=3)
                tk.Label(shipping_row, text="Phí vận chuyển:", font=('Arial', 13),
                        bg='white', fg='#555555', width=25, anchor='e').pack(side='left', padx=(0, 20))
                tk.Label(shipping_row, text="0 VNĐ", font=('Arial', 13),
                        bg='white', fg='#333333', width=18, anchor='e').pack(side='left')

                # Balance Due (Final total)
                balance_row = tk.Frame(totals_frame, bg='white')
                balance_row.pack(fill='x', pady=(10, 0))
                tk.Label(balance_row, text="TỔNG CỘNG:", font=('Arial', 15, 'bold'),
                        bg='white', fg='#2c3e50', width=25, anchor='e').pack(side='left', padx=(0, 20))
                tk.Label(balance_row, text=f"{subtotal:,.0f} VNĐ", font=('Arial', 15, 'bold'),
                        bg='white', fg='#27ae60', width=18, anchor='e').pack(side='left')

                # === SIGNATURE SECTION (bottom right) ===
                signature_section = tk.Frame(paper, bg='white')
                signature_section.pack(fill='x', pady=(40, 20))

                # Spacer
                tk.Frame(signature_section, bg='white', width=450).pack(side='left')

                signature_frame = tk.Frame(signature_section, bg='white')
                signature_frame.pack(side='right')

                # Signature line
                tk.Frame(signature_frame, bg='#cccccc', height=1, width=200).pack(fill='x', pady=(30, 5))
                tk.Label(signature_frame, text="Chữ ký Shop", font=('Arial', 13, 'italic'),
                        bg='white', fg='#888888').pack()

                # === BOTTOM RED BORDER ===
                bottom_border = tk.Frame(paper, bg='#8B0000', height=4)
                bottom_border.pack(fill='x', pady=(30, 0))

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải chi tiết: {str(e)}")
                _on_close()
                return
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()


        # Bind events
        tree.bind("<<TreeviewSelect>>", on_invoice_select)
        btn_view_details.config(command=view_invoice_details)

        # Load data on show
        load_invoice_history()

