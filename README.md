# 👟 Shoes Shop Management System - GUI Application

**Ứng dụng quản lý cửa hàng giày với giao diện đồ họa Tkinter**

Dự án hoàn chỉnh với đầy đủ chức năng quản lý bán hàng: đăng nhập/đăng ký phân quyền, giỏ hàng đồng bộ database, quản lý sản phẩm, hóa đơn, lịch sử mua hàng, và báo cáo doanh thu.

> **Last Updated**: October 29, 2025  
> **Database**: `shopquanao`  
> **Python Version**: 3.13+

---

## 📁 Cấu Trúc Dự Án

```
D:\shop_giay\shoes_shop\
├── main.py                           # ✅ Entry point - khởi chạy ứng dụng
├── shoes_shop_GUI.py                 # 📚 Original reference file (không dùng)
├── config/
│   ├── __init__.py
│   └── database.py                   # 🔧 Cấu hình kết nối MySQL
├── models/
│   ├── __init__.py
│   ├── user.py                       # Model: User/Login
│   ├── product.py                    # Model: Product management
│   └── cart.py                       # Model: Shopping cart
├── views/
│   ├── __init__.py
│   ├── login_view.py                 # 🔐 Login/Register UI
│   ├── product_view.py               # 🛍️ Product listing (Buyer & Seller)
│   ├── cart_view.py                  # 🛒 Shopping cart UI
│   ├── invoice_view.py               # 📄 Invoice preview & payment
│   ├── invoice_history_view.py       # 📜 Purchase history (NEW)
│   └── sales_view.py                 # 📊 Sales statistics (Seller)
├── utils/
│   ├── __init__.py
│   ├── image_utils.py                # 🖼️ Image loading (URL/local)
│   ├── validators.py                 # ✔️ Input validation
│   └── ui_effects.py                 # ✨ Hover effects, colors
├── images/                           # 📁 Local image storage
├── shopquanao09102025.sql            # 💾 Database dump
├── SQL_QUERIES_DOCUMENTATION.md      # 📖 Complete SQL documentation
└── README.md                         # 📄 This file
```

---

## ✨ Tính Năng Chính

### 👤 **Khách Hàng (Buyer)**
- ✅ Đăng ký/Đăng nhập tài khoản
- ✅ Xem danh sách sản phẩm với hình ảnh
- ✅ Tìm kiếm sản phẩm (theo tên, mã)
- ✅ Lọc theo thương hiệu, giá
- ✅ Chọn màu sắc & size cho từng sản phẩm
- ✅ Thêm nhiều sản phẩm vào giỏ hàng cùng lúc
- ✅ Xem & chỉnh sửa giỏ hàng
- ✅ Tạo hóa đơn & thanh toán
- ✅ Xem lịch sử mua hàng **[NEW]**
- ✅ Giỏ hàng lưu trữ vĩnh viễn (database)

### 👨‍💼 **Nhân Viên (Seller)**
- ✅ Đăng nhập tài khoản nhân viên
- ✅ Quản lý sản phẩm: Thêm/Sửa/Xóa
- ✅ Upload ảnh (từ URL hoặc local)
- ✅ Quản lý thương hiệu: Thêm/Xóa
- ✅ Thiết lập giảm giá tự động (theo ngày nhập hàng)
- ✅ Xem báo cáo doanh thu theo tháng **[UPDATED]**
- ✅ Sắp xếp doanh thu: Theo tiền/SL/Mã/Tên **[NEW]**
- ✅ Quản lý tồn kho

### 🎨 **UI/UX Features**
- ✅ Hover effects trên tất cả buttons
- ✅ Multi-select products (Ctrl+Click)
- ✅ Scrollable dialogs
- ✅ Responsive layouts
- ✅ Professional color scheme

---

## 🔧 Yêu Cầu Hệ Thống

### **Software Requirements:**
- **Python**: 3.13+ (hoặc 3.10+)
- **MySQL Server**: 8.0+
- **OS**: Windows 10/11 (tested)

### **Python Libraries:**
```bash
pip install Pillow mysql-connector-python
```

**Hoặc sử dụng requirements.txt:**
```bash
pip install -r requirements.txt
```

---

## ⚙️ Cấu Hình Database

### **1. Import Database**

```bash
mysql -u root -p shopquanao < shopquanao09102025.sql
```

**Hoặc trong MySQL Workbench:**
1. Server → Data Import
2. Import from Self-Contained File
3. Chọn `shopquanao09102025.sql`
4. Start Import

### **2. Cấu Hình Kết Nối**

**File:** `config/database.py`

```python
def get_db_connection():
    return mysql.connector.connect(
        host='127.0.0.1',           # MySQL host
        user='root',                # MySQL username
        password='your_password',   # MySQL password
        database='shopquanao'       # Database name
    )
```

**⚠️ BẢO MẬT:** Không commit password lên Git!

**Sử dụng biến môi trường (khuyến nghị):**
```python
import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', '127.0.0.1'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'shopquanao')
    )
```

**Set biến môi trường (Windows CMD):**
```cmd
set DB_HOST=127.0.0.1
set DB_USER=root
set DB_PASSWORD=your_password
set DB_NAME=shopquanao
```

---

## 🚀 Chạy Ứng Dụng

### **Phương Pháp 1: Trực Tiếp**
```cmd
cd D:\shop_giay\shoes_shop
python main.py
```

### **Phương Pháp 2: Virtual Environment (Khuyến nghị)**
```cmd
cd D:\shop_giay\shoes_shop
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Lưu ý**: Nếu thấy `(.venv)` ở đầu command prompt → đang trong virtual environment

---

## 💾 Database Schema

### **Bảng Chính:**

1. **khachhang** - Thông tin khách hàng
   - MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau

2. **nhanvien** - Thông tin nhân viên
   - MaNV, TenNV, TenDN, MatKhau

3. **sanpham** - Sản phẩm
   - MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, **NgayNhapHang**

4. **thuonghieu** - Thương hiệu
   - MaTH, TenTH

5. **url_sp** - Ảnh sản phẩm
   - MaSP, URLAnh (hỗ trợ URL và local path)

6. **mausac_sp** - Màu sắc sản phẩm
   - MaSP, MauSac (dynamic table)

7. **giohang** - Giỏ hàng
   - MaGH, MaKH (1-1 relationship)

8. **giohangchuasanpham** - Chi tiết giỏ hàng
   - MaGH, MaSP, MauSac, Size, SoLuong

9. **hoadon** - Hóa đơn
   - MaHD, MaKH, MaNV, NgayLap (DATE format)

10. **cthoadon** - Chi tiết hóa đơn
    - MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien

**📖 Chi tiết**: Xem `SQL_QUERIES_DOCUMENTATION.md`

---

## 🎯 Hướng Dẫn Sử Dụng

### **Đăng Nhập Lần Đầu**

**Tài khoản test (nếu database đã có data mẫu):**
- **Khách hàng**: Username/Password theo dữ liệu trong bảng `khachhang`
- **Nhân viên**: Username/Password theo dữ liệu trong bảng `nhanvien`

**Hoặc đăng ký tài khoản mới:**
1. Click "Đăng ký"
2. Chọn role (Khách hàng/Nhân viên)
3. Điền thông tin
4. Đăng nhập

### **Workflow Khách Hàng**
```
Đăng nhập → Xem sản phẩm → Chọn màu/size → Thêm vào giỏ
→ Xem giỏ hàng → Xem hóa đơn → Thanh toán → Xem lịch sử
```

### **Workflow Nhân Viên**
```
Đăng nhập → Quản lý sản phẩm → Quản lý thương hiệu
→ Xem báo cáo doanh thu → Sắp xếp theo tiêu chí
```

---

## 🐛 Troubleshooting

### **Lỗi Kết Nối Database**
```
mysql.connector.errors.InterfaceError
```
**Giải pháp:**
1. Kiểm tra MySQL Server đang chạy
2. Xác nhận thông tin trong `config/database.py`
3. Test connection: `mysql -u root -p shopquanao`

### **Lỗi Import Module**
```
ModuleNotFoundError: No module named 'PIL'
```
**Giải pháp:**
```cmd
pip install Pillow mysql-connector-python
```

### **Ảnh Không Hiển Thị**
**Nguyên nhân:** URL không hợp lệ hoặc file không tồn tại

**Giải pháp:**
1. Kiểm tra URL trong bảng `url_sp`
2. Kiểm tra thư mục `images/` có ảnh không
3. Test load ảnh: Xem `utils/image_utils.py`

### **Giỏ Hàng Trống Sau Khi Đăng Xuất**
**Lưu ý:** Giỏ hàng được lưu vào database!
- Đăng nhập lại → Giỏ hàng vẫn còn
- Chỉ mất nếu click "Thanh toán" (đã chuyển thành hóa đơn)

---

## 📚 Tài Liệu Tham Khảo

| File | Mô Tả |
|------|-------|
| `SQL_QUERIES_DOCUMENTATION.md` | Tất cả SQL queries với giải thích |
| `PYTHON_VS_MYSQL_SYNTAX.md` | Hướng dẫn chuyển đổi %s sang MySQL |
| `QUICK_START_GUIDE.md` | Hướng dẫn khởi động nhanh |
| `SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql` | Queries chạy trực tiếp trong MySQL |

---

## 🔒 Bảo Mật

**⚠️ QUAN TRỌNG:**
- ❌ **KHÔNG** commit password vào Git
- ✅ Sử dụng biến môi trường
- ✅ Tạo file `.env` (thêm vào `.gitignore`)
- ✅ Mã hóa password trong database

**File `.gitignore` nên có:**
```
.env
config/local_settings.py
*.pyc
__pycache__/
.venv/
```

---

## 📊 Tính Năng Nổi Bật

### **1. Multi-Product Cart Dialog**
- Chọn nhiều sản phẩm cùng lúc (Ctrl+Click)
- Cấu hình màu/size/số lượng cho từng sản phẩm
- Scrollable dialog
- Validation số lượng tồn kho

### **2. Dynamic Discount System**
- Tự động giảm giá sản phẩm > 6 tháng: **10%**
- Tự động giảm giá sản phẩm > 12 tháng: **15%**
- Hiển thị rõ ràng: `3,500,000 VNĐ (-10%)`

### **3. Invoice History**
- Xem tất cả đơn hàng đã mua
- Chi tiết từng hóa đơn
- Hiển thị giá lúc mua (không phải giá hiện tại)

### **4. Advanced Sales Report**
- Báo cáo theo tháng/năm
- Sắp xếp: Doanh thu/SL/Mã/Tên
- Gộp tất cả màu sắc/size
- Chính xác từ giá bán thực tế

---

## 🛠️ Development

### **Project Structure Philosophy:**
- **MVC Pattern**: Models, Views, separate logic
- **Modular**: Each view is independent
- **Database-first**: Cart, invoice stored in DB
- **Professional UI**: Hover effects, colors, layouts

### **Key Technologies:**
- **GUI**: Tkinter (Python standard library)
- **Database**: MySQL 8.0+
- **Image**: Pillow (PIL fork)
- **Security**: Password hashing, SQL injection prevention

---

## 📝 Changelog

### **Version 2.0 (Current) - October 29, 2025**
- ✅ Added Invoice History View
- ✅ Multi-product cart dialog
- ✅ Dynamic sorting in sales report
- ✅ Removed unit price column (focus on revenue)
- ✅ Hover effects on all buttons
- ✅ Brand management UI fixes
- ✅ Discount system based on import date

### **Version 1.0 - October 2025**
- ✅ Basic product management
- ✅ Cart functionality
- ✅ Invoice generation
- ✅ Sales statistics

---

## 👨‍💻 Contributors

**Project by**: [Your Name]  
**Database**: MySQL  
**Framework**: Python Tkinter  
**Last Updated**: October 29, 2025

---

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra `SQL_QUERIES_DOCUMENTATION.md`
2. Xem phần Troubleshooting
3. Check database connection
4. Verify Python libraries installed

---

**🎉 Project hoàn chỉnh và sẵn sàng sử dụng!**
- `hoadon` (MaHD, MaKH, NgayLap, TongTien, ...)
- `cthoadon` (MaHD, MaSP, SoLuong, DonGia, MauSac, Size, ...)

(Để đảm bảo đúng, kiểm tra file `.sql` mà bạn đang dùng — repo có `shopquanao09102025.sql` và có thể có file khác.)

## Chạy ứng dụng

Sau khi cài dependency và cấu hình DB, chạy:

```cmd
python main.py
```

- Nếu bạn thấy thông báo thiếu module `PIL` hoặc `mysql.connector`, cài lại bằng `pip install Pillow mysql-connector-python` trong virtualenv đang dùng.
- Nếu chương trình chạy nhưng không hiện ảnh: kiểm tra `config/database.py` `LOCAL_IMAGE_DIR` và đường dẫn ảnh lưu trữ, hoặc đảm bảo các đường dẫn URL ảnh hợp lệ.

## Lưu ý vận hành và debug nhanh

- Nếu giao diện khác so với file gốc `shoes_shop_GUI.py`, có thể bạn đang chạy `main.py`/một view đã được chỉnh sửa; `shoes_shop_GUI.py` được giữ làm tham chiếu gốc, đừng sửa nếu muốn so sánh giao diện ban đầu.
- Các vấn đề thường gặp:
  - ModuleNotFoundError: PIL — cài Pillow
  - mysql.connector.errors.InterfaceError / Access denied — kiểm tra thông tin kết nối
  - Ảnh không show: kiểm tra `Image.open` và cách load ảnh (từ URL hay file)
  - Lỗi khi thay đổi schema (ví dụ bỏ cột GiamGia): sửa code truy vấn tương ứng để phù hợp số cột mong đợi

## Ghi chú về bảo mật

- Không commit mật khẩu DB vào git. Sử dụng biến môi trường hoặc file cấu hình riêng (không theo dõi trong git).

