# Tóm tắt thay đổi Database - 22/11/2025

## Database mới
- **Tên database**: `shopgiaydep22112025` (thay vì `shopgiaydep09102025`)

## Các bảng đã đổi tên

### 1. Bảng `giohang` → `donhang`
- **Cột chính**: `MaGH` → `MaDH` (Mã Đơn Hàng)
- **Cột bổ sung mới**: `NgayLap` (datetime) - Ngày lập đơn hàng
- **Ràng buộc**: 
  - Primary Key: `MaDH`
  - Foreign Key: `MaKH` references `khachhang(MaKH)`
  - Unique: `MaKH` (mỗi khách hàng có 1 đơn hàng)

### 2. Bảng `giohangchuasanpham` → `sptrongdon`
- **Cột**: `MaGH` → `MaDH`
- **Các cột khác**: `MaSP`, `MauSac`, `Size`, `SoLuong`
- **Primary Key**: (`MaDH`, `MaSP`, `MauSac`, `Size`)
- **Foreign Keys**:
  - `MaDH` references `donhang(MaDH)`
  - `MaSP` references `sanpham(MaSP)`

## Các file đã được cập nhật

### 1. Config
- ✅ `config/database.py`: Cập nhật tên database thành `shopgiaydep22112025`

### 2. Models
- ✅ `models/user.py`: 
  - Dòng 93: `INSERT INTO donhang (MaDH, MaKH)` (thay vì giohang)

### 3. Views
- ✅ `views/product_view.py`:
  - Load cart: `SELECT MaDH FROM donhang WHERE MaKH = %s`
  - Cart items: `SELECT MaSP, SoLuong FROM sptrongdon WHERE MaDH = %s`
  - Update cart button: Đếm số lượng từ `sptrongdon`
  - Add to cart: INSERT/UPDATE vào `sptrongdon`
  - Delete product: `DELETE FROM sptrongdon WHERE MaSP = %s`

- ✅ `views/cart_view.py`:
  - Get cart: `SELECT MaDH FROM donhang WHERE MaKH = %s`
  - Cart details: `FROM sptrongdon ghsp JOIN sanpham sp WHERE ghsp.MaDH = %s`
  - Remove item: `DELETE FROM sptrongdon WHERE MaDH = %s AND ...`
  - Empty cart: `DELETE FROM sptrongdon WHERE MaDH = %s`

- ✅ `views/invoice_view.py`:
  - Get cart for payment: `SELECT MaDH FROM donhang WHERE MaKH = %s`
  - Clear paid items: `DELETE FROM sptrongdon WHERE MaDH = %s AND ...`

## Lưu ý quan trọng

### Logic không thay đổi
- Mặc dù tên bảng đã đổi, logic của ứng dụng vẫn giữ nguyên
- Biến trong code vẫn sử dụng tên `ma_gh` (để tránh phá vỡ logic), nhưng truy vấn đúng cột `MaDH`

### Cột mới trong bảng `sanpham`
- `NgayNhapHang` (date): Ngày nhập hàng, default '2025-06-09'
- `GiamGia` (int): Phần trăm giảm giá, default 0

### Tương thích ngược
- Code cũ sẽ KHÔNG hoạt động với database mới
- Cần migrate dữ liệu nếu chuyển từ database cũ sang mới
- Các constraint và foreign keys đã được giữ nguyên

## Kiểm tra
Đã kiểm tra các file sau và không còn tham chiếu đến bảng cũ:
- ✅ models/user.py
- ✅ views/product_view.py
- ✅ views/cart_view.py
- ✅ views/invoice_view.py
- ✅ views/invoice_history_view.py
- ✅ views/sales_view.py

## Trạng thái: ✅ HOÀN THÀNH
Tất cả các tham chiếu đến bảng cũ đã được cập nhật thành công.

