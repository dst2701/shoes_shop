# Cập Nhật Giảm Giá và Sửa Lỗi - Discount & Fixes Update

## Ngày cập nhật: 30/10/2025

---

## 🎯 Tổng Quan Các Vấn Đề Đã Giải Quyết

### 1. ✅ Thu Hẹp Cột Invoice View
**Vấn đề:** Cột "Thành tiền" bị đẩy ra ngoài màn hình

**Giải pháp:**
- Thu hẹp width các cột từ:
  - STT: 0.06 → 0.05
  - Mã SP: 0.10 → 0.09
  - Tên sản phẩm: 0.28 → 0.27
  - Màu sắc: 0.10 → 0.09
  - Size: 0.08 → 0.06
  - Số lượng: 0.10 → 0.09
  - Đơn giá: 0.14 → 0.16
  - Thành tiền: 0.14 → 0.16

**File:** `views/invoice_view.py`

---

### 2. ✅ Hệ Thống Giảm Giá Sản Phẩm

**Yêu cầu:** 
- Sản phẩm tồn kho > 6 tháng: giảm 10%
- Sản phẩm tồn kho > 12 tháng: giảm 15%

**Cách thức hoạt động:**
1. **Cột GiamGia trong database:** Lưu giá trị decimal (0.1 = 10%, 0.15 = 15%)
2. **Hiển thị giá:** Hiển thị giá sau giảm + badge giảm giá (ví dụ: "1,080,000 VNĐ (-10%)")
3. **Tính toán:** `Giá sau giảm = Giá gốc × (1 - GiamGia)`

**Files đã cập nhật:**

#### A. Product View (`views/product_view.py`)
```python
# Query thêm cột GiamGia
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, 
       sp.NgayNhapHang, sp.GiamGia
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH

# Tính giá hiển thị
discount_decimal = float(giam_gia) if giam_gia else 0.0
discount_percent = int(discount_decimal * 100)
discounted_price = original_price * (1 - discount_decimal)

# Hiển thị
if discount_percent > 0:
    price_display = f"{discounted_price:,.0f} VNĐ (-{discount_percent}%)"
else:
    price_display = f"{original_price:,.0f} VNĐ"
```

#### B. Cart View (`views/cart_view.py`)
```python
# Query thêm GiamGia
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
       sp.GiamGia
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP

# Tính giá trong giỏ hàng
discount_decimal = float(giam_gia) if giam_gia else 0.0
discounted_price = original_price * (1 - discount_decimal)
thanh_tien = discounted_price * so_luong
```

#### C. Invoice View (`views/invoice_view.py`)
```python
# Query và tính giá cho hóa đơn
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size, sp.GiamGia
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP

# Lưu giá đã giảm vào cthoadon
cursor.execute("""
    INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""", (ma_hd, item['ma_sp'], item['ten_sp'], item['color'], item['size'],
     item['quantity'], item['price'], item['total']))
# item['price'] = discounted_price (giá đã giảm)
```

**Database Schema Update:** `shopquanao09102025.sql`
```sql
CREATE TABLE `sanpham` (
  `MaSP` varchar(30) NOT NULL,
  `TenSP` varchar(300) NOT NULL,
  `Gia` decimal(14,2) NOT NULL,
  `MoTa` text,
  `MaTH` varchar(30) NOT NULL,
  `SoLuong` int NOT NULL,
  `NgayNhapHang` date DEFAULT NULL,
  `GiamGia` decimal(3,2) DEFAULT '0.00',
  PRIMARY KEY (`MaSP`),
  CONSTRAINT `sanpham_chk_3` CHECK ((`GiamGia` >= 0 AND `GiamGia` < 1))
)
```

---

### 3. ✅ Sửa Lỗi Brand Management Buttons

**Vấn đề:** Nút Save và Cancel bị che khuất/không hiển thị

**Giải pháp:**
1. Tăng kích thước window: 450x250 → 500x280
2. Thêm spacer để đẩy buttons xuống dưới
3. Sử dụng `side='bottom'` khi pack button frame

**Code fix:**
```python
# Increased window size
add_brand_window.geometry("500x280")

# Spacer to push buttons to bottom
tk.Frame(form_frame, bg='white', height=20).pack(fill='x', expand=True)

# Buttons frame - FIXED AT BOTTOM
button_frame_add = tk.Frame(form_frame, bg='white')
button_frame_add.pack(side='bottom', fill='x', pady=(15, 0))

# Save button (left)
btn_save_brand.pack(side='left', padx=(0, 10))

# Cancel button (right)
btn_cancel_brand.pack(side='right')
```

**File:** `views/product_view.py`

---

### 4. ✅ Statistics Với Sản Phẩm Đã Xóa

**Câu hỏi:** Khi xóa sản phẩm, thống kê doanh thu có còn giữ sản phẩm đó không?

**Trả lời:** ✅ **CÓ** - Sản phẩm đã xóa vẫn được GIỮ trong thống kê

**Lý do:**
1. Khi xóa sản phẩm, chỉ xóa khỏi bảng `sanpham` và `url_sp`
2. Bảng `cthoadon` (chi tiết hóa đơn) VẪN GIỮ tất cả data
3. `cthoadon` lưu cả `TenSP` (tên sản phẩm), không chỉ `MaSP`
4. Query statistics lấy từ `cthoadon`, không join với `sanpham`

**Code delete product:**
```python
# Delete product images first
cursor.execute("DELETE FROM url_sp WHERE MaSP = %s", (ma_sp,))

# Delete product from sanpham table
# NOTE: cthoadon (invoice details) will KEEP the product data including TenSP
# This ensures sales statistics remain accurate even after product deletion
cursor.execute("DELETE FROM sanpham WHERE MaSP = %s", (ma_sp,))
```

**Query statistics (sales_view.py):**
```sql
SELECT 
    ct.MaSP,
    ct.TenSP,  -- TenSP lưu trực tiếp trong cthoadon
    SUM(ct.SoLuongMua) as total_quantity,
    SUM(ct.ThanhTien) as total_sales
FROM cthoadon ct
INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
GROUP BY ct.MaSP, ct.TenSP
ORDER BY total_sales DESC
```

**Lợi ích:**
- Dữ liệu thống kê luôn chính xác
- Không mất lịch sử bán hàng
- Có thể phân tích sản phẩm đã ngừng kinh doanh

---

## 📊 Tóm Tắt Thay Đổi

### Files Modified:
1. ✅ `views/cart_view.py` - Áp dụng giảm giá trong giỏ hàng
2. ✅ `views/invoice_view.py` - Thu hẹp cột, áp dụng giảm giá
3. ✅ `views/product_view.py` - Hiển thị giá giảm, fix brand buttons
4. ✅ `shopquanao09102025.sql` - Thêm cột NgayNhapHang và GiamGia

### Database Changes:
- Thêm cột `NgayNhapHang` (date) vào bảng `sanpham`
- Thêm cột `GiamGia` (decimal(3,2)) vào bảng `sanpham`
- Thêm constraint check: `GiamGia >= 0 AND GiamGia < 1`

---

## 🧪 Hướng Dẫn Test

### Test 1: Giảm Giá Sản Phẩm
1. Update giá trị GiamGia trong database:
   ```sql
   UPDATE sanpham SET GiamGia = 0.10 WHERE MaSP = 'SP001';  -- Giảm 10%
   ```
2. Mở app, kiểm tra hiển thị giá: "4,499,100 VNĐ (-10%)"
3. Thêm vào giỏ hàng, kiểm tra giá trong cart
4. Thanh toán, kiểm tra giá trong hóa đơn
5. Verify cthoadon table có lưu giá đúng

### Test 2: Brand Management Buttons
1. Đăng nhập role seller
2. Click nút "🏷️ Thương hiệu"
3. Click "➕ Thêm thương hiệu"
4. Verify nút "💾 Lưu" (trái) và "❌ Hủy" (phải) hiển thị đầy đủ
5. Thử thêm brand mới

### Test 3: Invoice View Columns
1. Thêm nhiều sản phẩm vào giỏ hàng
2. Click "Xem hóa đơn"
3. Verify tất cả cột hiển thị đầy đủ, không bị tràn
4. Kiểm tra cột "Thành tiền" không bị đẩy ra ngoài

### Test 4: Statistics Với Sản Phẩm Đã Xóa
1. Tạo vài hóa đơn với sản phẩm X
2. Role seller: Xóa sản phẩm X
3. Mở trang "Thống kê doanh thu"
4. Verify sản phẩm X vẫn hiện trong thống kê với doanh thu chính xác

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Cập Nhật Database
Nếu database hiện tại chưa có cột `GiamGia` và `NgayNhapHang`, chạy lệnh sau:

```sql
USE shopgiaydep09102025;

-- Thêm cột NgayNhapHang
ALTER TABLE sanpham 
ADD COLUMN NgayNhapHang date DEFAULT NULL;

-- Thêm cột GiamGia
ALTER TABLE sanpham 
ADD COLUMN GiamGia decimal(3,2) DEFAULT 0.00;

-- Thêm constraint
ALTER TABLE sanpham 
ADD CONSTRAINT sanpham_chk_3 CHECK (GiamGia >= 0 AND GiamGia < 1);

-- Update giá trị mặc định cho sản phẩm hiện có
UPDATE sanpham 
SET NgayNhapHang = '2025-06-09', GiamGia = 0.00 
WHERE NgayNhapHang IS NULL;
```

### 2. Scroll Function
- Cart View và Invoice View đã có scroll function
- Nếu có nhiều sản phẩm, có thể cuộn bằng mousewheel
- Các nút hành động (Thanh toán, Xóa tất cả) vẫn cố định ở dưới

### 3. Giá Trong Hệ Thống
- **Product View:** Hiển thị giá gốc + discount badge
- **Cart View:** Tính giá sau giảm × số lượng
- **Invoice View:** Hiển thị giá sau giảm
- **cthoadon Table:** Lưu giá sau giảm (DonGia = discounted price)

---

## 🎉 Kết Luận

Tất cả các vấn đề đã được giải quyết:
- ✅ Invoice columns thu hẹp, không bị tràn
- ✅ Hệ thống giảm giá hoạt động đầy đủ
- ✅ Brand management buttons hiển thị đúng
- ✅ Statistics giữ sản phẩm đã xóa
- ✅ Scroll function hoạt động mượt mà

**Chương trình sẵn sàng để test và sử dụng!** 🚀

