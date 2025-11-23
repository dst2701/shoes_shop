# TÀI LIỆU TRUY VẤN SQL - SHOP GIÀY

Tài liệu này chứa tất cả các câu lệnh truy vấn SQL được sử dụng trong ứng dụng Shop Giày, được tổ chức theo chức năng.

---

## MỤC LỤC

1. [Cấu trúc Database](#cấu-trúc-database)
2. [Xác thực người dùng](#xác-thực-người-dùng)
3. [Quản lý sản phẩm](#quản-lý-sản-phẩm)
4. [Quản lý giỏ hàng](#quản-lý-giỏ-hàng)
5. [Quản lý đơn hàng](#quản-lý-đơn-hàng)
6. [Quản lý hóa đơn](#quản-lý-hóa-đơn)
7. [Thống kê doanh thu](#thống-kê-doanh-thu)
8. [Quản lý thương hiệu](#quản-lý-thương-hiệu)
9. [Quản lý màu sắc và size](#quản-lý-màu-sắc-và-size)

---

## CẤU TRÚC DATABASE

### Thông tin kết nối Database
```python
# File: config/database.py
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'shopgiaydep22112025',
    'user': 'root',
    'password': ''
}
```

### Sơ đồ quan hệ giữa các bảng

```
┌─────────────────────┐
│   KHACHHANG         │
├─────────────────────┤
│ PK: MaKH            │◄─────────┐
│     TenKH           │          │
│     SDT (Unique)    │          │
│     DiaChi          │          │
│     TenDN (Unique)  │          │
│     MatKhau         │          │
└─────────────────────┘          │
         │                       │
         │                       │
         ├──────────────┐        │
         │              │        │
         ▼              ▼        │
┌─────────────────────┐ ┌──────────────────┐
│ GIOHANGCHUASANPHAM  │ │    DONHANG       │
├─────────────────────┤ ├──────────────────┤
│ PK: MaKH            │ │ PK: MaDH         │
│ PK: MaSP            │ │ FK: MaKH    ─────┘
│ PK: MauSac          │ │     NgayLap      │
│ PK: Size            │ └──────────────────┘
│ FK: MaKH         ───┤          │
│ FK: MaSP         ───┤          │
│     SoLuong         │          ▼
└─────────────────────┘ ┌──────────────────┐
         │              │   SPTRONGDON     │
         │              ├──────────────────┤
         │              │ PK: MaDH         │
         │              │ PK: MaSP         │
         │              │ PK: MauSac       │
         │              │ PK: Size         │
         │              │ FK: MaDH    ─────┘
         │              │ FK: MaSP    ─────┐
         │              │     SoLuong      │
         │              └──────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────────┐ ┌─────────────────────┐
│     SANPHAM         │ │      HOADON         │
├─────────────────────┤ ├─────────────────────┤
│ PK: MaSP            │ │ PK: MaHD            │
│     TenSP           │ │ FK: MaKH        ────┼─┐
│     Gia             │ │ FK: MaNV        ────┼─┼─┐
│     MoTa            │ │     NgayLap         │ │ │
│ FK: MaTH        ────┼─┐ └─────────────────────┘ │ │
│     SoLuong         │ │          │               │ │
│     NgayNhapHang    │ │          │               │ │
│     GiamGia         │ │          ▼               │ │
└─────────────────────┘ │ ┌─────────────────────┐ │ │
         │              │ │     CTHOADON        │ │ │
         │              │ ├─────────────────────┤ │ │
         ├──────────────┤ │ PK: MaHD            │ │ │
         │              │ │ PK: MaSP            │ │ │
         │              │ │ PK: MauSac          │ │ │
         ▼              │ │ PK: Size            │ │ │
┌─────────────────────┐ │ │ FK: MaHD        ────┼─┘ │
│    THUONGHIEU       │ │ │     TenSP (lưu)     │   │
├─────────────────────┤ │ │     SoLuongMua      │   │
│ PK: MaTH            │◄┘ │     DonGia          │   │
│     TenTH           │   │     MauSac          │   │
│     MoTa            │   │     Size            │   │
└─────────────────────┘   │     ThanhTien       │   │
                          └─────────────────────┘   │
         ┌────────────────────────┐                 │
         │                        │                 │
         ▼                        ▼                 │
┌─────────────────────┐  ┌─────────────────────┐   │
│     URL_SP          │  │    MAUSAC_SP        │   │
├─────────────────────┤  ├─────────────────────┤   │
│ PK: MaSP            │  │ PK: MaSP            │   │
│ PK: URLAnh          │  │ PK: MauSac          │   │
│ FK: MaSP        ────┼──┤ FK: MaSP        ────┤   │
│     URLAnh          │  │     MauSac          │   │
└─────────────────────┘  └─────────────────────┘   │
                                  │                 │
                                  ▼                 │
                         ┌─────────────────────┐   │
                         │     SIZE_SP         │   │
                         ├─────────────────────┤   │
                         │ PK: MaSP            │   │
                         │ PK: Size            │   │
                         │ FK: MaSP        ────┼───┘
                         │     Size            │
                         └─────────────────────┘

┌─────────────────────┐
│     NHANVIEN        │
├─────────────────────┤
│ PK: MaNV            │◄────── (Referenced by HOADON.MaNV)
│     TenNV           │
│     TenDN (Unique)  │
│     MatKhau         │
└─────────────────────┘
```

### Danh sách các bảng chi tiết

#### 1. Bảng khachhang (Khách hàng)
**Khóa chính:** MaKH  
**Khóa duy nhất:** SDT, TenDN

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaKH | VARCHAR(30) | Mã khách hàng (PK) |
| TenKH | VARCHAR(200) | Tên khách hàng |
| SDT | VARCHAR(11) | Số điện thoại (Unique) |
| DiaChi | VARCHAR(300) | Địa chỉ |
| TenDN | VARCHAR(100) | Tên đăng nhập (Unique) |
| MatKhau | VARCHAR(255) | Mật khẩu |

**Quan hệ:**
- Một khách hàng có nhiều đơn hàng (1:N với donhang)
- Một khách hàng có một giỏ hàng tạm (1:N với giohangchuasanpham)
- Một khách hàng có nhiều hóa đơn (1:N với hoadon)

#### 2. Bảng nhanvien (Nhân viên/Người bán)
**Khóa chính:** MaNV  
**Khóa duy nhất:** TenDN

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaNV | VARCHAR(30) | Mã nhân viên (PK) |
| TenNV | VARCHAR(200) | Tên nhân viên |
| TenDN | VARCHAR(100) | Tên đăng nhập (Unique) |
| MatKhau | VARCHAR(255) | Mật khẩu |

**Quan hệ:**
- Một nhân viên có thể xử lý nhiều hóa đơn (1:N với hoadon)

#### 3. Bảng thuonghieu (Thương hiệu)
**Khóa chính:** MaTH

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaTH | VARCHAR(30) | Mã thương hiệu (PK) |
| TenTH | VARCHAR(200) | Tên thương hiệu |
| MoTa | TEXT | Mô tả thương hiệu |

**Quan hệ:**
- Một thương hiệu có nhiều sản phẩm (1:N với sanpham)

#### 4. Bảng sanpham (Sản phẩm)
**Khóa chính:** MaSP  
**Khóa ngoại:** MaTH → thuonghieu(MaTH)

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaSP | VARCHAR(30) | Mã sản phẩm (PK) |
| TenSP | VARCHAR(300) | Tên sản phẩm |
| Gia | DECIMAL(14,2) | Giá sản phẩm |
| MoTa | TEXT | Mô tả sản phẩm |
| MaTH | VARCHAR(30) | Mã thương hiệu (FK) |
| SoLuong | INT | Số lượng tồn kho |
| NgayNhapHang | DATE | Ngày nhập hàng |
| GiamGia | INT | Phần trăm giảm giá (0-100) |

**Quan hệ:**
- Một sản phẩm thuộc một thương hiệu (N:1 với thuonghieu)
- Một sản phẩm có nhiều hình ảnh (1:N với url_sp)
- Một sản phẩm có nhiều màu sắc (1:N với mausac_sp)
- Một sản phẩm có nhiều size (1:N với size_sp)
- Một sản phẩm có thể có trong nhiều giỏ hàng (1:N với giohangchuasanpham)
- Một sản phẩm có thể có trong nhiều đơn hàng (1:N với sptrongdon)

#### 5. Bảng url_sp (Hình ảnh sản phẩm)
**Khóa chính:** (MaSP, URLAnh)  
**Khóa ngoại:** MaSP → sanpham(MaSP) ON DELETE CASCADE

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaSP | VARCHAR(30) | Mã sản phẩm (PK, FK) |
| URLAnh | VARCHAR(500) | Đường dẫn URL hình ảnh (PK) |

**Quan hệ:**
- Nhiều hình ảnh thuộc một sản phẩm (N:1 với sanpham)
- Xóa sản phẩm sẽ tự động xóa tất cả hình ảnh (CASCADE)

#### 6. Bảng mausac_sp (Màu sắc sản phẩm)
**Khóa chính:** (MaSP, MauSac)  
**Khóa ngoại:** MaSP → sanpham(MaSP) ON DELETE CASCADE

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaSP | VARCHAR(30) | Mã sản phẩm (PK, FK) |
| MauSac | VARCHAR(100) | Tên màu sắc (PK) |

**Quan hệ:**
- Nhiều màu sắc thuộc một sản phẩm (N:1 với sanpham)
- Xóa sản phẩm sẽ tự động xóa tất cả màu sắc (CASCADE)

#### 7. Bảng size_sp (Kích cỡ sản phẩm)
**Khóa chính:** (MaSP, Size)  
**Khóa ngoại:** MaSP → sanpham(MaSP) ON DELETE CASCADE

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaSP | VARCHAR(30) | Mã sản phẩm (PK, FK) |
| Size | VARCHAR(20) | Kích cỡ (PK) |

**Quan hệ:**
- Nhiều size thuộc một sản phẩm (N:1 với sanpham)
- Xóa sản phẩm sẽ tự động xóa tất cả size (CASCADE)

#### 8. Bảng giohangchuasanpham (Giỏ hàng tạm thời)
**Khóa chính:** (MaKH, MaSP, MauSac, Size)  
**Khóa ngoại:**
- MaKH → khachhang(MaKH) ON DELETE CASCADE
- MaSP → sanpham(MaSP) ON DELETE CASCADE

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaKH | VARCHAR(30) | Mã khách hàng (PK, FK) |
| MaSP | VARCHAR(30) | Mã sản phẩm (PK, FK) |
| MauSac | VARCHAR(100) | Màu sắc sản phẩm (PK) |
| Size | VARCHAR(20) | Kích cỡ sản phẩm (PK) |
| SoLuong | INT | Số lượng trong giỏ |

**Quan hệ:**
- Giỏ hàng tạm thuộc một khách hàng (N:1 với khachhang)
- Giỏ hàng tạm chứa nhiều sản phẩm khác nhau (N:1 với sanpham)
- Xóa khách hàng hoặc sản phẩm sẽ tự động xóa khỏi giỏ hàng (CASCADE)

#### 9. Bảng donhang (Đơn hàng)
**Khóa chính:** MaDH  
**Khóa ngoại:** MaKH → khachhang(MaKH)

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaDH | VARCHAR(30) | Mã đơn hàng (PK) - Format: GHxxx |
| MaKH | VARCHAR(30) | Mã khách hàng (FK) |
| NgayLap | DATETIME | Ngày tạo đơn hàng |

**Quan hệ:**
- Một đơn hàng thuộc một khách hàng (N:1 với khachhang)
- Một đơn hàng có nhiều sản phẩm (1:N với sptrongdon)

#### 10. Bảng sptrongdon (Sản phẩm trong đơn hàng)
**Khóa chính:** (MaDH, MaSP, MauSac, Size)  
**Khóa ngoại:**
- MaDH → donhang(MaDH)
- MaSP → sanpham(MaSP)

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaDH | VARCHAR(30) | Mã đơn hàng (PK, FK) |
| MaSP | VARCHAR(30) | Mã sản phẩm (PK, FK) |
| MauSac | VARCHAR(100) | Màu sắc (PK) |
| Size | VARCHAR(20) | Kích cỡ (PK) |
| SoLuong | INT | Số lượng |

**Quan hệ:**
- Sản phẩm trong đơn thuộc một đơn hàng (N:1 với donhang)
- Sản phẩm trong đơn tham chiếu đến sản phẩm (N:1 với sanpham)

#### 11. Bảng hoadon (Hóa đơn)
**Khóa chính:** MaHD  
**Khóa ngoại:**
- MaKH → khachhang(MaKH)
- MaNV → nhanvien(MaNV) (nullable)

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaHD | VARCHAR(40) | Mã hóa đơn (PK) - Format: HDxxx |
| MaKH | VARCHAR(30) | Mã khách hàng (FK) |
| MaNV | VARCHAR(30) | Mã nhân viên (FK, có thể NULL) |
| NgayLap | DATE | Ngày lập hóa đơn |

**Quan hệ:**
- Một hóa đơn thuộc một khách hàng (N:1 với khachhang)
- Một hóa đơn có thể được xử lý bởi một nhân viên (N:1 với nhanvien)
- Một hóa đơn có nhiều sản phẩm (1:N với cthoadon)

#### 12. Bảng cthoadon (Chi tiết hóa đơn)
**Khóa chính:** (MaHD, MaSP, MauSac, Size)  
**Khóa ngoại:** MaHD → hoadon(MaHD)

| Cột | Kiểu dữ liệu | Mô tả |
|-----|--------------|-------|
| MaHD | VARCHAR(40) | Mã hóa đơn (PK, FK) |
| MaSP | VARCHAR(30) | Mã sản phẩm (PK) |
| TenSP | VARCHAR(300) | Tên sản phẩm (lưu để bảo toàn dữ liệu) |
| MauSac | VARCHAR(100) | Màu sắc (PK) |
| Size | VARCHAR(50) | Kích cỡ (PK) |
| SoLuongMua | INT | Số lượng mua |
| DonGia | DECIMAL(14,2) | Đơn giá |
| ThanhTien | DECIMAL(16,2) | Thành tiền |

**Quan hệ:**
- Chi tiết hóa đơn thuộc một hóa đơn (N:1 với hoadon)
- Lưu TenSP để bảo toàn dữ liệu khi sản phẩm bị xóa

### Ràng buộc và quy tắc quan trọng

1. **Ràng buộc CHECK:**
   - sanpham.SoLuong >= 0
   - sanpham.Gia > 0
   - giohangchuasanpham.SoLuong > 0
   - sptrongdon.SoLuong > 0
   - cthoadon.SoLuongMua >= 0
   - cthoadon.DonGia > 0
   - khachhang.SDT phải match pattern ^[0-9]{10,11}$
   - khachhang.MatKhau phải có độ dài >= 6
   - nhanvien.MatKhau phải có độ dài >= 6

2. **Ràng buộc UNIQUE:**
   - khachhang.TenDN
   - khachhang.SDT
   - nhanvien.TenDN

3. **ON DELETE CASCADE:**
   - Xóa sanpham → tự động xóa url_sp, mausac_sp, size_sp
   - Xóa khachhang → tự động xóa giohangchuasanpham
   - Xóa sanpham → tự động xóa giohangchuasanpham

4. **Bảo toàn dữ liệu lịch sử:**
   - Bảng cthoadon lưu TenSP để không bị ảnh hưởng khi xóa sản phẩm
   - Bảng cthoadon KHÔNG có ON DELETE CASCADE với sanpham

---

## XÁC THỰC NGƯỜI DÙNG

### 1. Kiểm tra đăng nhập khách hàng
```sql
SELECT MaKH FROM khachhang 
WHERE TenDN = %s AND MatKhau = %s;
```
Mục đích: Xác thực thông tin đăng nhập của khách hàng

### 2. Kiểm tra đăng nhập nhân viên
```sql
SELECT MaNV FROM nhanvien 
WHERE TenDN = %s AND MatKhau = %s;
```
Mục đích: Xác thực thông tin đăng nhập của nhân viên/người bán

### 3. Kiểm tra trùng tên đăng nhập (khách hàng)
```sql
SELECT 1 FROM khachhang WHERE TenDN = %s;
```
Mục đích: Kiểm tra tên đăng nhập đã tồn tại trong bảng khách hàng

### 4. Kiểm tra trùng tên đăng nhập (nhân viên)
```sql
SELECT 1 FROM nhanvien WHERE TenDN = %s;
```
Mục đích: Kiểm tra tên đăng nhập đã tồn tại trong bảng nhân viên

### 5. Kiểm tra trùng số điện thoại
```sql
SELECT 1 FROM khachhang WHERE SDT = %s;
```
Mục đích: Kiểm tra số điện thoại đã được sử dụng

### 6. Tạo mã khách hàng tự động
```sql
SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) 
FROM khachhang 
WHERE MaKH LIKE 'KH%';
```
Mục đích: Lấy mã khách hàng lớn nhất để tạo mã mới (KH001, KH002,...)

### 7. Tạo mã nhân viên tự động
```sql
SELECT MAX(CAST(SUBSTRING(MaNV, 3) AS UNSIGNED)) 
FROM nhanvien 
WHERE MaNV LIKE 'NV%';
```
Mục đích: Lấy mã nhân viên lớn nhất để tạo mã mới (NV001, NV002,...)

### 8. Đăng ký khách hàng mới
```sql
INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
VALUES (%s, %s, %s, %s, %s, %s);
```
Mục đích: Thêm bản ghi khách hàng mới vào database

### 9. Đăng ký nhân viên mới
```sql
INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
VALUES (%s, %s, %s, %s);
```
Mục đích: Thêm bản ghi nhân viên mới vào database

### 10. Lấy mã khách hàng từ tên đăng nhập
```sql
SELECT MaKH FROM khachhang WHERE TenDN = %s;
```
Mục đích: Truy vấn mã khách hàng để sử dụng trong các thao tác khác

---

## QUẢN LÝ SẢN PHẨM

### 11. Tải danh sách sản phẩm với thông tin thương hiệu
```sql
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang, sp.GiamGia
FROM sanpham sp
JOIN thuonghieu th ON sp.MaTH = th.MaTH
ORDER BY sp.TenSP;
```
Mục đích: Lấy tất cả sản phẩm kèm tên thương hiệu, giảm giá và ngày nhập hàng

### 12. Lấy hình ảnh sản phẩm
```sql
SELECT MaSP, URLAnh
FROM url_sp
ORDER BY MaSP;
```
Mục đích: Lấy tất cả đường dẫn hình ảnh của sản phẩm

### 13. Lấy số lượng tồn kho và giảm giá
```sql
SELECT SoLuong, GiamGia FROM sanpham WHERE MaSP = %s;
```
Mục đích: Kiểm tra tồn kho và phần trăm giảm giá của sản phẩm

### 14. Cập nhật giảm giá tự động theo ngày nhập hàng
```sql
UPDATE sanpham SET GiamGia = %s WHERE MaSP = %s;
```
Mục đích: Tự động cập nhật giảm giá 10% (>6 tháng) hoặc 15% (>12 tháng) dựa vào ngày nhập hàng

### 15. Tạo mã sản phẩm mới
```sql
SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) 
FROM sanpham 
WHERE MaSP LIKE 'SP%';
```
Mục đích: Tạo mã sản phẩm tự động (SP001, SP002,...)

### 16. Thêm sản phẩm mới
```sql
INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, NgayNhapHang, GiamGia)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
```
Mục đích: Thêm sản phẩm mới vào database

### 17. Thêm hình ảnh sản phẩm
```sql
INSERT INTO url_sp (MaSP, URLAnh)
VALUES (%s, %s);
```
Mục đích: Thêm URL hình ảnh cho sản phẩm (có thể nhiều ảnh)

### 18. Cập nhật thông tin sản phẩm
```sql
UPDATE sanpham 
SET TenSP = %s, Gia = %s, MoTa = %s, MaTH = %s, SoLuong = %s, NgayNhapHang = %s
WHERE MaSP = %s;
```
Mục đích: Cập nhật thông tin sản phẩm (tên, giá, mô tả, thương hiệu, số lượng, ngày nhập)

### 19. Xóa sản phẩm
```sql
-- Xóa từ giỏ hàng tạm
DELETE FROM giohangchuasanpham WHERE MaSP = %s;

-- Xóa từ đơn hàng chưa thanh toán
DELETE FROM sptrongdon WHERE MaSP = %s;

-- Xóa hình ảnh
DELETE FROM url_sp WHERE MaSP = %s;

-- Xóa sản phẩm (cthoadon sẽ giữ dữ liệu TenSP để bảo toàn lịch sử)
DELETE FROM sanpham WHERE MaSP = %s;
```
Mục đích: Xóa sản phẩm và các dữ liệu liên quan (trừ lịch sử hóa đơn)

### 20. Cập nhật số lượng sau khi bán
```sql
UPDATE sanpham 
SET SoLuong = SoLuong - %s 
WHERE MaSP = %s;
```
Mục đích: Giảm số lượng tồn kho sau khi khách hàng thanh toán

### 21. Lấy màu sắc của sản phẩm
```sql
SELECT MauSac FROM mausac_sp WHERE MaSP = %s;
```
Mục đích: Lấy danh sách màu sắc có sẵn của một sản phẩm

### 22. Lấy size của sản phẩm
```sql
SELECT Size FROM size_sp WHERE MaSP = %s ORDER BY CAST(Size AS UNSIGNED);
```
Mục đích: Lấy danh sách size có sẵn của một sản phẩm (sắp xếp theo số)

### 23. Thêm màu sắc cho sản phẩm
```sql
INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s);
```
Mục đích: Thêm màu sắc mới cho sản phẩm

### 24. Thêm size cho sản phẩm
```sql
INSERT INTO size_sp (MaSP, Size) VALUES (%s, %s);
```
Mục đích: Thêm size mới cho sản phẩm

### 25. Xóa màu sắc của sản phẩm
```sql
DELETE FROM mausac_sp WHERE MaSP = %s;
```
Mục đích: Xóa tất cả màu sắc của sản phẩm (thường dùng khi cập nhật)

### 26. Xóa size của sản phẩm
```sql
DELETE FROM size_sp WHERE MaSP = %s;
```
Mục đích: Xóa tất cả size của sản phẩm (thường dùng khi cập nhật)

---

## QUẢN LÝ GIỎ HÀNG

### 27. Đếm tổng số sản phẩm trong giỏ hàng
```sql
SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaKH = %s;
```
Mục đích: Tính tổng số lượng sản phẩm trong giỏ hàng để hiển thị badge

### 28. Tải giỏ hàng của khách hàng
```sql
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong, sp.GiamGia
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaKH = %s
ORDER BY sp.TenSP;
```
Mục đích: Lấy tất cả sản phẩm trong giỏ hàng kèm thông tin chi tiết

### 29. Kiểm tra sản phẩm đã có trong giỏ chưa
```sql
SELECT SoLuong FROM giohangchuasanpham 
WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s;
```
Mục đích: Kiểm tra sản phẩm với màu sắc và size cụ thể đã trong giỏ chưa

### 30. Thêm sản phẩm vào giỏ hàng
```sql
INSERT INTO giohangchuasanpham (MaKH, MaSP, MauSac, Size, SoLuong)
VALUES (%s, %s, %s, %s, %s);
```
Mục đích: Thêm sản phẩm mới vào giỏ hàng tạm thời

### 31. Cập nhật số lượng sản phẩm trong giỏ
```sql
UPDATE giohangchuasanpham 
SET SoLuong = %s 
WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s;
```
Mục đích: Cập nhật số lượng khi thêm sản phẩm đã có trong giỏ

### 32. Xóa một sản phẩm khỏi giỏ hàng
```sql
DELETE FROM giohangchuasanpham 
WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s;
```
Mục đích: Xóa một sản phẩm cụ thể khỏi giỏ hàng

---

## QUẢN LÝ ĐƠN HÀNG

### 33. Tạo mã đơn hàng mới
```sql
SELECT MAX(CAST(SUBSTRING(MaDH, 3) AS UNSIGNED)) FROM donhang;
```
Mục đích: Tạo mã đơn hàng tự động (GH001, GH002,...)

### 34. Tạo đơn hàng mới
```sql
INSERT INTO donhang (MaDH, MaKH, NgayLap)
VALUES (%s, %s, %s);
```
Mục đích: Tạo đơn hàng mới khi khách hàng nhấn "Tạo đơn hàng"

### 35. Thêm sản phẩm vào đơn hàng
```sql
INSERT INTO sptrongdon (MaDH, MaSP, MauSac, Size, SoLuong)
VALUES (%s, %s, %s, %s, %s);
```
Mục đích: Thêm sản phẩm được chọn vào đơn hàng

### 36. Xóa sản phẩm khỏi giỏ hàng sau khi tạo đơn
```sql
DELETE FROM giohangchuasanpham 
WHERE MaKH = %s AND MaSP = %s AND MauSac = %s AND Size = %s;
```
Mục đích: Xóa sản phẩm khỏi giỏ hàng tạm sau khi đã chuyển vào đơn hàng

### 37. Lấy danh sách đơn hàng chưa thanh toán
```sql
SELECT dh.MaDH, dh.NgayLap, 
       SUM(sp.Gia * (1 - sp.GiamGia/100) * spd.SoLuong) as TongTien
FROM donhang dh
JOIN sptrongdon spd ON dh.MaDH = spd.MaDH
JOIN sanpham sp ON spd.MaSP = sp.MaSP
WHERE dh.MaKH = %s
GROUP BY dh.MaDH, dh.NgayLap
ORDER BY dh.MaDH DESC;
```
Mục đích: Hiển thị tất cả đơn hàng chưa thanh toán của khách hàng

### 38. Lấy chi tiết một đơn hàng
```sql
SELECT spd.MaSP, sp.TenSP, sp.Gia, spd.MauSac, spd.Size, spd.SoLuong, sp.GiamGia
FROM sptrongdon spd
JOIN sanpham sp ON spd.MaSP = sp.MaSP
WHERE spd.MaDH = %s;
```
Mục đích: Lấy thông tin chi tiết các sản phẩm trong một đơn hàng

### 39. Xóa đơn hàng chưa thanh toán
```sql
-- Xóa sản phẩm trong đơn
DELETE FROM sptrongdon WHERE MaDH = %s;

-- Xóa đơn hàng
DELETE FROM donhang WHERE MaDH = %s;
```
Mục đích: Xóa đơn hàng và các sản phẩm trong đơn khi khách hàng không muốn mua nữa

---

## QUẢN LÝ HÓA ĐƠN

### 40. Tạo mã hóa đơn mới
```sql
SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) 
FROM hoadon 
WHERE MaHD LIKE 'HD%';
```
Mục đích: Tạo mã hóa đơn tự động (HD001, HD002,...)

### 41. Tạo hóa đơn khi thanh toán
```sql
INSERT INTO hoadon (MaHD, MaKH, MaNV, NgayLap)
VALUES (%s, %s, %s, %s);
```
Mục đích: Tạo hóa đơn mới khi khách hàng thanh toán đơn hàng

### 42. Thêm chi tiết hóa đơn
```sql
INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
```
Mục đích: Lưu chi tiết từng sản phẩm trong hóa đơn

### 43. Xóa đơn hàng sau khi thanh toán
```sql
-- Xóa sản phẩm trong đơn
DELETE FROM sptrongdon WHERE MaDH = %s;

-- Xóa đơn hàng
DELETE FROM donhang WHERE MaDH = %s;
```
Mục đích: Xóa đơn hàng tạm sau khi đã chuyển thành hóa đơn

### 44. Lấy lịch sử hóa đơn của khách hàng
```sql
SELECT hd.MaHD, hd.NgayLap, SUM(ct.ThanhTien) as TongTien
FROM hoadon hd
JOIN cthoadon ct ON hd.MaHD = ct.MaHD
WHERE hd.MaKH = %s
GROUP BY hd.MaHD, hd.NgayLap
ORDER BY hd.MaHD DESC;
```
Mục đích: Hiển thị lịch sử mua hàng của khách hàng (sắp xếp mới nhất đầu tiên)

### 45. Lấy chi tiết một hóa đơn cụ thể
```sql
SELECT ct.MaSP, ct.TenSP, ct.MauSac, ct.Size, ct.SoLuongMua, ct.DonGia, ct.ThanhTien
FROM cthoadon ct
WHERE ct.MaHD = %s
ORDER BY ct.TenSP;
```
Mục đích: Xem chi tiết các sản phẩm trong một hóa đơn đã thanh toán

### 46. Lấy thông tin khách hàng từ hóa đơn
```sql
SELECT hd.MaHD, hd.NgayLap, kh.TenKH, kh.DiaChi, kh.SDT
FROM hoadon hd
JOIN khachhang kh ON hd.MaKH = kh.MaKH
WHERE hd.MaHD = %s;
```
Mục đích: Lấy thông tin khách hàng để hiển thị trên hóa đơn

---

## THỐNG KÊ DOANH THU

### 47. Thống kê doanh thu theo tháng
```sql
SELECT 
    sp.MaSP,
    sp.TenSP,
    SUM(ct.SoLuongMua) as TongSoLuong,
    SUM(ct.ThanhTien) as TongDoanhThu
FROM cthoadon ct
JOIN hoadon hd ON ct.MaHD = hd.MaHD
JOIN sanpham sp ON ct.MaSP = sp.MaSP
WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
GROUP BY sp.MaSP, sp.TenSP
ORDER BY TongDoanhThu DESC;
```
Mục đích: Thống kê doanh thu và số lượng bán được theo từng sản phẩm trong tháng

### 48. Tổng doanh thu tháng
```sql
SELECT SUM(ct.ThanhTien) as TongDoanhThu
FROM cthoadon ct
JOIN hoadon hd ON ct.MaHD = hd.MaHD
WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s;
```
Mục đích: Tính tổng doanh thu của một tháng cụ thể

### 49. Sản phẩm bán chạy nhất
```sql
SELECT 
    ct.MaSP,
    ct.TenSP,
    SUM(ct.SoLuongMua) as TongSoLuong,
    SUM(ct.ThanhTien) as TongDoanhThu
FROM cthoadon ct
GROUP BY ct.MaSP, ct.TenSP
ORDER BY TongSoLuong DESC
LIMIT 10;
```
Mục đích: Xếp hạng 10 sản phẩm bán chạy nhất theo số lượng

---

## QUẢN LÝ THƯƠNG HIỆU

### 50. Lấy danh sách thương hiệu
```sql
SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH;
```
Mục đích: Lấy tên tất cả thương hiệu để hiển thị trong dropdown filter

### 51. Tạo mã thương hiệu mới
```sql
SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) 
FROM thuonghieu 
WHERE MaTH LIKE 'TH%';
```
Mục đích: Tạo mã thương hiệu tự động (TH001, TH002,...)

### 52. Thêm thương hiệu mới
```sql
INSERT INTO thuonghieu (MaTH, TenTH, MoTa)
VALUES (%s, %s, %s);
```
Mục đích: Thêm thương hiệu mới vào database

### 53. Cập nhật thương hiệu
```sql
UPDATE thuonghieu 
SET TenTH = %s, MoTa = %s 
WHERE MaTH = %s;
```
Mục đích: Cập nhật thông tin thương hiệu

### 54. Xóa thương hiệu
```sql
DELETE FROM thuonghieu WHERE MaTH = %s;
```
Mục đích: Xóa thương hiệu (sẽ thất bại nếu có sản phẩm đang sử dụng)

### 55. Lấy thông tin thương hiệu
```sql
SELECT MaTH, TenTH, MoTa FROM thuonghieu ORDER BY TenTH;
```
Mục đích: Lấy danh sách đầy đủ thông tin thương hiệu

---

## QUẢN LÝ MÀU SẮC VÀ SIZE

### 56. Lấy tất cả màu sắc của sản phẩm
```sql
SELECT MauSac FROM mausac_sp WHERE MaSP = %s;
```
Mục đích: Hiển thị dropdown màu sắc khi khách hàng chọn sản phẩm

### 57. Lấy tất cả size của sản phẩm
```sql
SELECT Size FROM size_sp WHERE MaSP = %s ORDER BY CAST(Size AS UNSIGNED);
```
Mục đích: Hiển thị dropdown size khi khách hàng chọn sản phẩm (sắp xếp từ nhỏ đến lớn)

---

## GHI CHÚ QUAN TRỌNG

### Quản lý Transaction
- Luôn sử dụng transaction cho các thao tác sửa đổi nhiều bảng
- Chỉ commit sau khi tất cả thao tác liên quan thành công
- Rollback khi có lỗi để đảm bảo tính nhất quán của dữ liệu

### Tính toàn vẹn dữ liệu
- Foreign key constraint đảm bảo tính toàn vẹn tham chiếu
- Sử dụng ON DELETE CASCADE cẩn thận để tránh mất dữ liệu ngoài ý muốn
- Luôn validate dữ liệu đầu vào trước khi thực thi query

### Bảo mật
- Luôn sử dụng parameterized queries (%s placeholders) để ngăn SQL injection
- Không bao giờ nối trực tiếp input của người dùng vào câu lệnh SQL
- Lưu mật khẩu an toàn (nên sử dụng hashing trong môi trường production)

### Hiệu suất
- Index các cột foreign key để tăng tốc độ join
- Sử dụng kiểu dữ liệu phù hợp (DECIMAL cho giá, INT cho số lượng)
- Cân nhắc thêm index cho các cột thường xuyên tìm kiếm (TenDN, SDT)

### Workflow hệ thống
1. Khách hàng thêm sản phẩm vào giỏ hàng: lưu vào bảng giohangchuasanpham
2. Khách hàng chọn sản phẩm và tạo đơn hàng: chuyển dữ liệu sang donhang và sptrongdon
3. Khách hàng thanh toán đơn hàng: tạo hóa đơn trong bảng hoadon và cthoadon, xóa đơn hàng
4. Sau thanh toán: giảm số lượng tồn kho trong bảng sanpham

Ngày cập nhật: 23/11/2025

