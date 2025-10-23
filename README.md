# Shoes Shop GUI (Tkinter) — Current Status

Ứng dụng quản lý cửa hàng giày bằng giao diện đồ họa Tkinter. Dự án hiện đã hoàn thiện hầu hết các chức năng chính: đăng nhập/đăng ký, tìm kiếm và lọc sản phẩm, giỏ hàng đồng bộ với cơ sở dữ liệu, tạo hóa đơn (invoice), và các chức năng dành cho nhân viên (thêm/sửa/xóa sản phẩm, quản lý thương hiệu, báo cáo doanh thu).

> Lưu ý: README này mô tả trạng thái hiện tại của repo và cách cấu hình nhanh để chạy trên máy của bạn.

## Cấu trúc dự án (thư mục chính)

```
D:\shop_giay\shoes_shop\
├── main.py                      # Entry point: khởi chạy ứng dụng GUI
├── shoes_shop_GUI.py            # (Original/gốc) GUI reference - không chỉnh sửa nếu bạn muốn giữ bản gốc
├── config/
│   ├── __init__.py
│   └── database.py              # Hàm get_db_connection() - chỉnh cấu hình kết nối DB tại đây
├── models/                      # Model mapping cho bảng database: user, product, cart...
├── views/                       # Views/GUI modules: product_view, cart_view, invoice_view, ...
├── utils/                       # Hỗ trợ: image xử lý, validators, v.v.
├── images/                      # (Nếu có) ảnh tải về / lưu trữ cục bộ
├── shopquanao09102025.sql       # SQL dump (có thể có nhiều file .sql trong repo)
├── README.md
└── tests/ (nếu có)
```

(Thư mục ở trên là bản tóm tắt; repo chứa thêm các file hỗ trợ và test như `test_database.py`, `test_images.py`, v.v.)

## Tính năng chính hiện tại

- Đăng ký/Đăng nhập (role: Khách hàng / Nhân viên)
- Hiển thị danh sách sản phẩm kèm hình ảnh (tải ảnh online hoặc từ thư mục `images/`)
- Thanh tìm kiếm + bộ lọc theo thương hiệu và giá (tăng/giảm)
- Giỏ hàng gắn với từng tài khoản và lưu vào DB (`giohang`, `giohangchuasanpham`)
- Xem chi tiết giỏ hàng, chuyển thành hóa đơn, lưu `hoadon` và `cthoadon`
- Nhân viên: thêm / sửa / xóa sản phẩm, quản lý thương hiệu, xem báo cáo doanh thu
- Quản lý kích thước và màu sắc trên GUI (lưu vào cột `Size` và `MauSac` khi thêm vào giỏ/hoá đơn)

## Yêu cầu hệ thống

- Python 3.10+ (hoặc phiên bản tương thích với các package đang dùng)
- MySQL Server
- Thư viện Python:
  - pillow
  - mysql-connector-python

Cài đặt nhanh:

```cmd
pip install -r requirements.txt
```

Nếu bạn không có file `requirements.txt`, cài thủ công:

```cmd
pip install Pillow mysql-connector-python
```

Lưu ý: Trên Windows, chạy trong terminal `cmd.exe` hoặc PowerShell; nếu bạn đang dùng virtual environment (.venv) hãy đảm bảo đã kích hoạt nó trước khi cài.

## Cấu hình kết nối MySQL (bắt buộc)

Hiện tại hàm `get_db_connection()` nằm tại `config/database.py`. Mặc định file đang sử dụng cấu hình cục bộ ví dụ (host `127.0.0.1`, user `root`, database `shopgiaydep09102025`).

Cách chỉnh nhanh (khuyến nghị):

1. Mở `config/database.py` và sửa trực tiếp các tham số `host`, `user`, `password`, `database` theo MySQL của bạn.

2. (Tốt hơn) Sử dụng biến môi trường để tránh lưu mật khẩu trong mã nguồn. Ví dụ (thay thế nội dung `get_db_connection()`):

```python
import os
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('SHOP_DB_HOST', '127.0.0.1'),
        user=os.environ.get('SHOP_DB_USER', 'root'),
        password=os.environ.get('SHOP_DB_PASSWORD', ''),
        database=os.environ.get('SHOP_DB_NAME', 'shopgiaydep09102025'),
    )
```

Với cách này, bạn có thể trước khi chạy app set biến môi trường trong cmd.exe như:

```cmd
set SHOP_DB_HOST=127.0.0.1
set SHOP_DB_USER=root
set SHOP_DB_PASSWORD=your_password
set SHOP_DB_NAME=shopgiaydep09102025
python main.py
```


## Database: các bảng quan trọng

Tùy vào SQL dump của bạn nhưng thông thường dự án sử dụng các bảng sau (ví dụ):
- `khachhang` (MaKH, Username, Password, HoTen, DiaChi, DienThoai, ...)
- `nhanvien` (MaNV, Username, Password, HoTen, ...)
- `sanpham` (MaSP, TenSP, DonGia, SoLuong, MauSac, Size, GiamGia, NgayNhapHang, ...)
- `thuonghieu` (MaTH, TenTH)
- `giohang` (MaGH, MaKH)
- `giohangchuasanpham` (MaGH, MaSP, SoLuong, MauSac, Size, DonGia, ...)
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

