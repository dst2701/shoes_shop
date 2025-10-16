# Shoes Shop GUI Application

Ứng dụng quản lý cửa hàng giày với giao diện đồ họa được xây dựng bằng Python Tkinter.

## Cấu trúc dự án

```
D:\shop_giay\
├── main.py                 # File chính để chạy ứng dụng
├── config/
│   ├── __init__.py
│   └── database.py         # Cấu hình kết nối database
├── models/
│   ├── __init__.py
│   ├── user.py            # Model quản lý người dùng
│   └── product.py         # Model quản lý sản phẩm
├── views/
│   ├── __init__.py
│   ├── base_view.py       # Base class cho views
│   ├── login_view.py      # Giao diện đăng nhập/đăng ký
│   └── product_view.py    # Giao diện hiển thị sản phẩm
├── utils/
│   ├── __init__.py
│   ├── image_utils.py     # Xử lý ảnh
│   └── validators.py      # Validation functions
├── images/                # Thư mục chứa ảnh (tùy chọn)
├── shop.sql              # Database schema
└── README.md             # File hướng dẫn này
```

## Yêu cầu hệ thống

- Python 3.6+
- MySQL Server
- Các thư viện Python:
  - tkinter (thường có sẵn với Python)
  - mysql-connector-python
  - Pillow (PIL)

## Cài đặt

1. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install mysql-connector-python Pillow
   ```

2. **Thiết lập database:**
   - Khởi động MySQL Server
   - Import file `shop.sql` vào MySQL:
     ```sql
     mysql -u root -p < shop.sql
     ```

3. **Cấu hình kết nối database:**
   - Mở file `config/database.py`
   - Cập nhật thông tin kết nối MySQL của bạn:
     ```python
     DB_CONFIG = {
         'host': '127.0.0.1',
         'user': 'root',        # Thay đổi username
         'password': 'your_password',  # Thay đổi password
         'database': 'shopgiaydep'
     }
     ```

## Chạy ứng dụng

```bash
python main.py
```

## Tính năng

### Cho khách hàng (buyer):
- Xem danh sách sản phẩm
- Tìm kiếm sản phẩm
- Xem chi tiết sản phẩm và hình ảnh
- Đăng ký tài khoản mới

### Cho nhân viên (seller):
- Tất cả tính năng của khách hàng
- Quản lý sản phẩm (sẽ được thêm trong tương lai)

## Tài khoản mẫu

### Khách hàng:
- Username: `nguyenvanbao` / Password: `abc123`
- Username: `vuminhduong` / Password: `87654321`

### Nhân viên:
- Username: `tandat` / Password: `D23CNTT`
- Username: `ngoduchieu` / Password: `D23CNTT`

## Lợi ích của việc refactor

1. **Tách biệt trách nhiệm:** Mỗi file có một chức năng rõ ràng
2. **Dễ bảo trì:** Code được tổ chức theo module, dễ tìm và sửa lỗi
3. **Tái sử dụng:** Các function có thể được sử dụng lại ở nhiều nơi
4. **Mở rộng:** Dễ dàng thêm tính năng mới mà không ảnh hưởng code cũ
5. **Kiểm thử:** Có thể test từng module riêng biệt

## Hướng phát triển

- Thêm tính năng giỏ hàng
- Quản lý đơn hàng
- Báo cáo thống kê
- API REST
- Giao diện web
