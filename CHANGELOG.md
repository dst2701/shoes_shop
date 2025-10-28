# 📋 CHANGELOG - Shoes Shop Management System

All notable changes to this project will be documented in this file.

---

## [2.0.0] - 2025-10-29

### ✨ Added
- **Invoice History View** (`views/invoice_history_view.py`)
  - Khách hàng có thể xem lịch sử tất cả đơn hàng đã mua
  - Chi tiết hóa đơn với thông tin sản phẩm đầy đủ
  - Hiển thị giá lúc mua (không phải giá hiện tại)

- **Multi-Product Cart Dialog**
  - Chọn nhiều sản phẩm cùng lúc (Ctrl+Click hoặc Shift+Click)
  - Dialog scrollable cấu hình màu/size/số lượng cho từng sản phẩm
  - Validation tồn kho real-time

- **Dynamic Sales Sorting**
  - Sắp xếp doanh thu theo: Tiền (cao→thấp), SL (cao→thấp), Mã (A→Z), Tên (A→Z)
  - Auto-refresh khi thay đổi tiêu chí
  - Mặc định: Doanh thu cao nhất

- **Discount System**
  - Tự động giảm 10% cho sản phẩm > 6 tháng
  - Tự động giảm 15% cho sản phẩm > 12 tháng
  - Hiển thị: `Giá (-X%)` trên UI

- **Color & Size Management**
  - Bảng `mausac_sp` động cho từng sản phẩm
  - Seller có thể thêm màu khi add/update product
  - Buyer chọn màu/size trước khi add to cart

### 🔧 Changed
- **Sales View**: Bỏ cột "Đơn giá" (giá thay đổi liên tục)
  - Chỉ hiển thị: STT, Mã SP, Tên, SL bán, Doanh thu
  - Query dùng `SUM(ThanhTien)` thay vì tính lại
  - Không join với bảng `sanpham` (không cần thiết)

- **Invoice Date**: Chỉ lưu ngày (DATE), không có giờ
  - `hoadon.NgayLap` = DATE type
  - Hiển thị: `dd/mm/yyyy` thay vì `dd/mm/yyyy HH:MM:SS`

- **Database Name**: `shopgiaydep09102025` → `shopquanao`

- **UI Enhancements**
  - Hover effects trên tất cả buttons
  - Dialog windows: centered, lift(), focus_force()
  - Fixed button layouts (scrollable areas)
  - Professional color scheme

### 🐛 Fixed
- **Brand Management Dialog**: Nút Save/Cancel bị đè
  - Tăng kích thước dialog: 400x200 → 450x250
  - Fixed button frame at bottom
  - Proper centering

- **Sales View**: Treeview không hiển thị
  - Removed duplicate treeview declaration
  - Added missing scrollbar pack()
  - Fixed column count (6 → 5)

- **Cart Persistence**: Giỏ hàng lưu vào database
  - `giohangchuasanpham` table
  - Không mất khi đăng xuất/shutdown app

- **Product View**: Color/Size selection
  - Moved to add-to-cart dialog
  - Better UX flow

### 🗑️ Removed
- Hardcoded color/size dropdowns from main product view
- Old `add_to_cart()` function (replaced by dialog system)
- Unit price column from sales statistics

---

## [1.0.0] - 2025-10-01

### Initial Release

#### Features
- **Login/Register System**
  - Role-based: Buyer (khachhang) vs Seller (nhanvien)
  - Password validation
  - Unique username/phone check

- **Product Management (Seller)**
  - Add/Edit/Delete products
  - Upload images (URL or local)
  - Brand management
  - Stock management

- **Shopping (Buyer)**
  - Browse products with images
  - Search products
  - Filter by brand, price
  - Add to cart
  - View cart
  - Generate invoice
  - Payment process

- **Invoice System**
  - Preview before payment
  - Auto-generate invoice ID
  - Save to `hoadon` and `cthoadon` tables
  - Stock decrease on payment
  - Clear cart after payment

- **Sales Statistics (Seller)**
  - Monthly sales report
  - Sort by revenue (descending)
  - Total revenue & quantity

- **Database Integration**
  - MySQL 8.0+
  - 10 main tables
  - Foreign key constraints
  - Data validation

---

## Database Schema Changes

### [2.0.0]
```sql
-- Added column
ALTER TABLE sanpham ADD COLUMN NgayNhapHang DATE DEFAULT NULL;

-- Created table
CREATE TABLE IF NOT EXISTS mausac_sp (
    MaSP VARCHAR(30) NOT NULL,
    MauSac VARCHAR(100) NOT NULL,
    PRIMARY KEY (MaSP, MauSac),
    FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
);
```

### [1.0.0]
- Initial database structure
- All 10 tables created

---

## Dependencies Changes

### [2.0.0]
No changes

### [1.0.0]
```
Pillow==10.0.0
mysql-connector-python==8.1.0
```

---

## Breaking Changes

### [2.0.0]
- ⚠️ **Sales View Query**: Changed from JOIN sanpham to direct cthoadon query
  - Old code relying on `sp.Gia` will break
  - Migration: Use `ct.DonGia` or `ct.ThanhTien`

- ⚠️ **Add to Cart**: Removed direct add, now uses dialog
  - Old `add_to_cart(ma_sp, ten_sp)` → Commented out
  - New: `show_multi_product_cart_dialog(selected_products)`

### [1.0.0]
N/A

---

## Upgrade Guide

### From 1.0.0 to 2.0.0

1. **Update Database Schema**
   ```sql
   ALTER TABLE sanpham ADD COLUMN NgayNhapHang DATE DEFAULT NULL;
   
   CREATE TABLE IF NOT EXISTS mausac_sp (
       MaSP VARCHAR(30) NOT NULL,
       MauSac VARCHAR(100) NOT NULL,
       PRIMARY KEY (MaSP, MauSac),
       FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
   );
   ```

2. **Update Config**
   - Change database name in `config/database.py`
   - From: `shopgiaydep09102025`
   - To: `shopquanao`

3. **Test New Features**
   - Test invoice history view
   - Test multi-product cart dialog
   - Test sales sorting options

4. **No Code Changes Required** (if using main.py)

---

## Known Issues

### [2.0.0]
- None reported

### [1.0.0]
- ✅ FIXED: Brand dialog buttons hidden (v2.0.0)
- ✅ FIXED: Sales view not showing (v2.0.0)
- ✅ FIXED: Cart not persisting (v2.0.0)

---

## Planned Features

### [3.0.0] - Future
- [ ] User profile management
- [ ] Export invoice to PDF
- [ ] Email notifications
- [ ] Product reviews/ratings
- [ ] Advanced inventory alerts
- [ ] Multi-currency support
- [ ] Dark mode UI

---

**Maintained by**: Project Team  
**Repository**: [Your Repo URL]  
**Documentation**: See `SQL_QUERIES_DOCUMENTATION.md`

