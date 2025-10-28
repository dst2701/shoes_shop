# 📊 SQL QUERIES DOCUMENTATION - SHOES SHOP PROJECT

**Database**: `shopgiaydep09102025`  
**Project**: Shoes Shop Management System  
**Date**: October 28, 2025

---

## TABLE OF CONTENTS
1. [Database Overview](#database-overview)
2. [Product View Queries](#product-view)
3. [Cart View Queries](#cart-view)
4. [Invoice View Queries](#invoice-view)
5. [Sales View Queries](#sales-view)
6. [Product Model Queries](#product-model)
7. [Login/Registration Queries](#login-registration)
8. [Database Schema](#database-schema)

---

## DATABASE OVERVIEW

### Tables in the System:
1. **khachhang** - Customer information
2. **nhanvien** - Employee/Seller information
3. **sanpham** - Product information
4. **thuonghieu** - Brand information
5. **url_sp** - Product images (URLs)
6. **mausac_sp** - Product available colors (dynamic table)
7. **giohang** - Shopping cart (one per customer)
8. **giohangchuasanpham** - Cart items (with color, size, quantity)
9. **hoadon** - Invoice/Order headers
10. **cthoadon** - Invoice/Order details (items purchased)

---

## ⚠️ IMPORTANT: About the `%s` Placeholders

### Understanding the Syntax

In this documentation, you'll see queries like:
```sql
SELECT MaKH FROM khachhang WHERE TenDN = %s
```

**The `%s` is NOT MySQL syntax** - it's a **placeholder** used by Python's MySQL connector library (like `mysql-connector-python` or `pymysql`).

### Two Different Contexts:

#### 1️⃣ **In Python/GUI Code** (How it's used in the project):
```python
cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))
#                                                        ↑         ↑
#                                                   Placeholder   Actual value
```
The `%s` gets **automatically replaced** with the actual value (safely escaped to prevent SQL injection).

#### 2️⃣ **In MySQL Workbench** (How YOU should run it):
```sql
SELECT MaKH FROM khachhang WHERE TenDN = 'john_doe';
--                                        ↑
--                                   Actual value in quotes
```

### Quick Reference:

| Python Code | MySQL Workbench |
|-------------|-----------------|
| `WHERE MaSP = %s` | `WHERE MaSP = 'SP001'` |
| `WHERE Gia > %s` | `WHERE Gia > 1000000` |
| `WHERE TenDN = %s` | `WHERE TenDN = 'username'` |
| `VALUES (%s, %s, %s)` | `VALUES ('SP001', 'Nike', 3500000)` |

### 📁 Ready-to-Run SQL File

I've created a separate file **`SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql`** with all queries converted to actual MySQL syntax that you can run directly in MySQL Workbench!

---

## PRODUCT VIEW

### 1. Load Cart from Database
**Module**: `views/product_view.py`  
**Function**: `load_cart_from_database()`

```sql
-- Get customer ID from username
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Get cart ID from customer ID
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Get all products in cart
SELECT MaSP, SoLuong FROM giohangchuasanpham WHERE MaGH = %s
```

**Purpose**: Load user's cart items when they log in

**Returns**: List of (MaSP, SoLuong) tuples

---

### 2. Refresh Brand Filter
**Module**: `views/product_view.py`  
**Function**: `refresh_brand_filter()`

```sql
SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH
```

**Purpose**: Get list of all brands for the filter dropdown

**Returns**: List of brand names

---

### 3. Update Cart Count
**Module**: `views/product_view.py`  
**Function**: `update_cart_button()`

```sql
-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Get cart ID
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Calculate total items in cart
SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaGH = %s
```

**Purpose**: Display total number of items in cart on button

**Returns**: Total quantity of items in cart

---

### 4. Load Products with Brands and Images
**Module**: `views/product_view.py`  
**Function**: `show_shoes()`

```sql
-- Get all products with brand info
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
ORDER BY sp.MaSP

-- Get all brands for filter
SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH

-- Get all product images
SELECT MaSP, URLAnh FROM url_sp ORDER BY MaSP
```

**Purpose**: Load all products with their details, brands, and images for display

**Returns**: Complete product catalog with images

---

### 5. Check Product Stock
**Module**: `views/product_view.py`  
**Function**: `add_to_cart()`

```sql
SELECT SoLuong FROM sanpham WHERE MaSP = %s
```

**Purpose**: Check available stock before adding to cart

**Returns**: Current stock quantity

---

### 6. Add Product to Cart (with Stock Validation)
**Module**: `views/product_view.py`  
**Function**: `add_to_cart_with_quantity()`

```sql
-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Get or check cart exists
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Create new cart if doesn't exist
SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang
INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)

-- Get current stock
SELECT SoLuong FROM sanpham WHERE MaSP = %s

-- Calculate total quantity in all carts (across all users)
SELECT SUM(ghsp.SoLuong) 
FROM giohangchuasanpham ghsp
WHERE ghsp.MaSP = %s

-- Check if user already has this item (with specific color/size)
SELECT SoLuong FROM giohangchuasanpham 
WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s

-- Update existing cart item
UPDATE giohangchuasanpham 
SET SoLuong = %s 
WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s

-- OR Insert new cart item
INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
VALUES (%s, %s, %s, %s, %s)
```

**Purpose**: Add product to cart with comprehensive stock validation across all users

**Validation Logic**:
- Checks total stock available
- Calculates total quantity already in all carts
- Prevents overselling by validating remaining stock
- Supports color and size variants

---

### 7. Delete Product (Seller)
**Module**: `views/product_view.py`  
**Function**: `delete_product()`

```sql
-- Delete product images first (cascade)
DELETE FROM url_sp WHERE MaSP = %s

-- Delete product
DELETE FROM sanpham WHERE MaSP = %s
```

**Purpose**: Remove product and its images from database

**Note**: Deletes in correct order to maintain referential integrity

---

### 8. Load Product Colors Dynamically
**Module**: `views/product_view.py`  
**Function**: `on_product_select_combined()`

```sql
SELECT MauSac FROM mausac_sp WHERE MaSP = %s
```

**Purpose**: Load available colors for selected product

**Returns**: List of available colors for the product

**Fallback**: Returns default colors (Trắng, Xanh Dương, Đen, Nâu) if no colors found

---

### 9. Add New Product
**Module**: `views/product_view.py`  
**Function**: `save_product()`

```sql
-- Create color table if not exists
CREATE TABLE IF NOT EXISTS mausac_sp (
    MaSP VARCHAR(30) NOT NULL,
    MauSac VARCHAR(100) NOT NULL,
    PRIMARY KEY (MaSP, MauSac),
    FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
)

-- Generate new product ID
SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'

-- Insert product
INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, NgayNhapHang)
VALUES (%s, %s, %s, %s, %s, %s, %s)

-- Insert colors (multiple inserts)
INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)

-- Insert image URLs (multiple inserts)
INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)
```

**Purpose**: Add new product with colors and images

**ID Generation Pattern**: SP001, SP002, SP003, etc.

---

### 10. Update Product
**Module**: `views/product_view.py`  
**Function**: `show_edit_product_form()` and `update_product()`

```sql
-- Get product details
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, sp.MaTH, sp.SoLuong, th.TenTH, sp.NgayNhapHang
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
WHERE sp.MaSP = %s

-- Get product images
SELECT URLAnh FROM url_sp WHERE MaSP = %s

-- Get product colors
SELECT MauSac FROM mausac_sp WHERE MaSP = %s

-- Load all brands for dropdown
SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH

-- Update product information
UPDATE sanpham 
SET TenSP = %s, Gia = %s, MoTa = %s, MaTH = %s, SoLuong = %s, NgayNhapHang = %s
WHERE MaSP = %s

-- Delete old colors
DELETE FROM mausac_sp WHERE MaSP = %s

-- Insert new colors
INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)

-- Delete old images
DELETE FROM url_sp WHERE MaSP = %s

-- Insert new images
INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)
```

**Purpose**: Update product information, colors, and images

**Note**: Uses delete-then-insert pattern for colors and images

---

### 11. Brand Management
**Module**: `views/product_view.py`  
**Function**: `show_brand_management()`

```sql
-- Load all brands
SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH

-- Delete brand (with cascade delete of related data)
DELETE FROM url_sp WHERE MaSP IN (SELECT MaSP FROM sanpham WHERE MaTH = %s)
DELETE FROM sanpham WHERE MaTH = %s
DELETE FROM thuonghieu WHERE MaTH = %s

-- Check if brand exists
SELECT MaTH FROM thuonghieu WHERE TenTH = %s

-- Generate new brand ID
SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) FROM thuonghieu WHERE MaTH LIKE 'TH%'

-- Insert new brand
INSERT INTO thuonghieu (MaTH, TenTH) VALUES (%s, %s)
```

**Purpose**: Manage brands (view, add, delete)

**ID Generation Pattern**: TH001, TH002, TH003, etc.

**Warning**: Deleting a brand also deletes all associated products

---

## CART VIEW

### 12. Load Cart Details
**Module**: `views/cart_view.py`  
**Function**: `show_cart()`

```sql
-- Get customer ID from username
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Get cart ID from customer ID
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Get cart items with product details and calculated totals
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
       (sp.Gia * ghsp.SoLuong) as ThanhTien
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = %s
ORDER BY sp.TenSP
```

**Purpose**: Display all items in user's cart with calculated totals

**Returns**: Complete cart with product details, prices, and subtotals

---

### 13. Remove Item from Cart
**Module**: `views/cart_view.py`  
**Function**: `remove_from_cart_db()`

```sql
-- Get customer and cart IDs
SELECT MaKH FROM khachhang WHERE TenDN = %s
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Delete specific item from cart (by product, color, and size)
DELETE FROM giohangchuasanpham 
WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s
```

**Purpose**: Remove single item from cart

**Note**: Requires exact match on product code, color, and size

---

### 14. Clear Entire Cart
**Module**: `views/cart_view.py`  
**Function**: `clear_cart_db()`

```sql
-- Get customer and cart IDs
SELECT MaKH FROM khachhang WHERE TenDN = %s
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Delete all items from cart
DELETE FROM giohangchuasanpham WHERE MaGH = %s
```

**Purpose**: Remove all items from cart

**Important Note**: Does NOT return quantities to inventory (items were never deducted)

---

## INVOICE VIEW

### 15. Generate Invoice Preview
**Module**: `views/invoice_view.py`  
**Function**: `show_invoice_page()`

```sql
-- Get customer info (address and phone)
SELECT DiaChi, SDT, MaKH FROM khachhang WHERE TenDN = %s

-- Generate next invoice ID (for preview only)
SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'

-- Get customer's cart
SELECT MaKH FROM khachhang WHERE TenDN = %s
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Get cart items with details for invoice preview
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = %s
```

**Purpose**: Display invoice preview before payment

**ID Pattern**: HD001, HD002, HD003, etc.

**Note**: Invoice ID is generated but not saved until payment

---

### 16. Process Payment (CRITICAL TRANSACTION)
**Module**: `views/invoice_view.py`  
**Function**: `process_payment_main()`

```sql
-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Generate actual invoice ID
SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'

-- Create invoice header record
INSERT INTO hoadon (MaHD, MaKH, NgayLap)
VALUES (%s, %s, %s)

-- Get customer's cart
SELECT MaGH FROM giohang WHERE MaKH = %s

-- Get all cart items with full details
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = %s

-- For each grouped item:

-- Check current stock availability
SELECT SoLuong FROM sanpham WHERE MaSP = %s

-- Insert invoice line item
INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

-- Decrease product quantity with safety check
UPDATE sanpham 
SET SoLuong = GREATEST(0, SoLuong - %s)
WHERE MaSP = %s

-- Verify quantity is not negative (safety check)
SELECT SoLuong FROM sanpham WHERE MaSP = %s

-- Clear cart after successful payment
DELETE FROM giohangchuasanpham WHERE MaGH = %s
```

**Purpose**: Complete payment transaction - creates invoice, updates inventory, clears cart

**Transaction Flow**:
1. Validate stock for each item
2. Create invoice header
3. Insert invoice details (grouped by product/color/size)
4. Decrease inventory (with GREATEST to prevent negatives)
5. Verify no negative quantities
6. Clear customer's cart
7. Commit all or rollback if any step fails

**Safety Features**:
- Stock validation before processing
- GREATEST(0, value) prevents negative inventory
- Double-check after update
- Atomic transaction (all or nothing)

---

## SALES VIEW

### 17. Load Monthly Sales Statistics
**Module**: `views/sales_view.py`  
**Function**: `load_sales_data()`

```sql
SELECT 
    ct.MaSP,
    sp.TenSP,
    SUM(ct.SoLuongMua) as total_quantity,
    sp.Gia as unit_price,
    SUM(ct.SoLuongMua * sp.Gia) as total_sales
FROM cthoadon ct
INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
INNER JOIN sanpham sp ON ct.MaSP = sp.MaSP
WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
GROUP BY ct.MaSP, sp.TenSP, sp.Gia
ORDER BY total_sales DESC
```

**Purpose**: Get sales statistics for a specific month/year, sorted by revenue

**Returns**: 
- Product code
- Product name
- Total quantity sold
- Unit price
- Total revenue per product

**Sorting**: Descending by total revenue (best sellers first)

---

## PRODUCT MODEL

### 18. Generate Product ID
**Module**: `models/product.py`  
**Function**: `generate_product_id()`

```sql
SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'
```

**Purpose**: Auto-generate next product ID

**Pattern**: SP001, SP002, SP003...

---

### 19. Generate Brand ID
**Module**: `models/product.py`  
**Function**: `generate_brand_id()`

```sql
SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) FROM thuonghieu WHERE MaTH LIKE 'TH%'
```

**Purpose**: Auto-generate next brand ID

**Pattern**: TH001, TH002, TH003...

---

### 20. Get or Create Brand
**Module**: `models/product.py`  
**Function**: `get_or_create_brand()`

```sql
-- Check if brand exists
SELECT MaTH FROM thuonghieu WHERE TenTH = %s

-- If not exists, create new brand
INSERT INTO thuonghieu (MaTH, TenTH, MoTa) VALUES (%s, %s, %s)
```

**Purpose**: Ensure brand exists, create if needed

**Returns**: Brand ID (existing or newly created)

---

### 21. Get All Products
**Module**: `models/product.py`  
**Function**: `get_all_products()`

```sql
SELECT MaSP, TenSP, Gia, MoTa
FROM sanpham
ORDER BY TenSP
```

**Purpose**: Retrieve all products sorted by name

---

### 22. Get Product Images
**Module**: `models/product.py`  
**Function**: `get_product_images()`

```sql
SELECT URLAnh
FROM url_sp
WHERE MaSP = %s
ORDER BY URLAnh
```

**Purpose**: Get all image URLs for a specific product

---

### 23. Get Product by ID
**Module**: `models/product.py`  
**Function**: `get_product_by_id()`

```sql
SELECT MaSP, TenSP, Gia, MoTa
FROM sanpham
WHERE MaSP = %s
```

**Purpose**: Retrieve single product details

---

### 24. Add Product (Model Version)
**Module**: `models/product.py`  
**Function**: `add_product()`

```sql
-- Get or create brand first
SELECT MaTH FROM thuonghieu WHERE TenTH = %s

-- Generate product ID
SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'

-- Insert product
INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong)
VALUES (%s, %s, %s, %s, %s, %s)

-- Insert image URLs (loop for each URL)
INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)
```

**Purpose**: Add new product with automatic brand creation

**Note**: Model version with simpler interface

---

### 25. Delete Product (Model Version)
**Module**: `models/product.py`  
**Function**: `delete_product()`

```sql
-- Delete images first
DELETE FROM url_sp WHERE MaSP = %s

-- Delete product
DELETE FROM sanpham WHERE MaSP = %s
```

**Purpose**: Remove product and related images

**Returns**: True if product was deleted, False otherwise

---

### 26. Get All Brands
**Module**: `models/product.py`  
**Function**: `get_all_brands()`

```sql
SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH
```

**Purpose**: Retrieve all brands sorted by name

---

### 27. Search and Filter Products
**Module**: `models/product.py`  
**Function**: `search_products()`

```sql
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
WHERE 1=1
  [AND s.TenSP LIKE %s]           -- If search_term provided
  [AND t.TenTH = %s]               -- If brand_filter provided
ORDER BY [s.Gia ASC | s.Gia DESC | s.TenSP]  -- Based on price_filter
```

**Purpose**: Advanced product search with multiple filters

**Filters**:
- Search term (LIKE match on product name)
- Brand filter (exact match)
- Price sorting (low to high, high to low, or by name)

---

## LOGIN REGISTRATION

### 28. User Authentication (Buyer)
**Module**: `views/login_view.py`  
**Function**: `login()` / `authenticate_user()`

```sql
-- Check buyer credentials
SELECT MaKH, TenKH FROM khachhang 
WHERE TenDN = %s AND MatKhau = %s
```

**Purpose**: Verify buyer login credentials

**Returns**: Customer ID and name if valid

---

### 29. User Authentication (Seller)
**Module**: `views/login_view.py`  
**Function**: `login()` / `authenticate_user()`

```sql
-- Check seller credentials
SELECT MaNV, TenNV FROM nhanvien 
WHERE TenDN = %s AND MatKhau = %s
```

**Purpose**: Verify seller/employee login credentials

**Returns**: Employee ID and name if valid

---

### 30. User Registration (Buyer)
**Module**: `views/login_view.py`  
**Function**: `register_buyer()`

```sql
-- Check if username exists
SELECT MaKH FROM khachhang WHERE TenDN = %s

-- Check if phone number exists
SELECT MaKH FROM khachhang WHERE SDT = %s

-- Generate new customer ID
SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) FROM khachhang WHERE MaKH LIKE 'KH%'

-- Register new buyer
INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
VALUES (%s, %s, %s, %s, %s, %s)

-- Create cart for new user
SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang
INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)
```

**Purpose**: Register new customer and create their shopping cart

**ID Patterns**:
- Customer: KH001, KH002, KH003...
- Cart: GH001, GH002, GH003...

**Validations**:
- Username must be unique
- Phone number must be unique
- Password must be >= 6 characters (constraint in DB)
- Phone must be 10-11 digits (constraint in DB)

---

### 31. User Registration (Seller)
**Module**: `views/login_view.py`  
**Function**: `register_seller()`

```sql
-- Check if username exists (in employee table)
SELECT MaNV FROM nhanvien WHERE TenDN = %s

-- Generate new employee ID
SELECT MAX(CAST(SUBSTRING(MaNV, 11) AS UNSIGNED)) FROM nhanvien WHERE MaNV LIKE 'B23DCCN%'

-- Register new seller
INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
VALUES (%s, %s, %s, %s)
```

**Purpose**: Register new employee/seller

**ID Pattern**: B23DCCN001, B23DCCN002, etc.

**Note**: Sellers do not have shopping carts

---

## DATABASE SCHEMA

### Primary Tables Structure

#### khachhang (Customers)
```sql
CREATE TABLE `khachhang` (
  `MaKH` varchar(30) NOT NULL,
  `TenKH` varchar(200) NOT NULL,
  `SDT` varchar(11) NOT NULL,
  `DiaChi` varchar(300) DEFAULT NULL,
  `TenDN` varchar(100) NOT NULL,
  `MatKhau` varchar(255) NOT NULL,
  PRIMARY KEY (`MaKH`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `TenDN` (`TenDN`),
  CONSTRAINT `khachhang_chk_1` CHECK (regexp_like(`SDT`,'^[0-9]{10,11}$')),
  CONSTRAINT `khachhang_chk_2` CHECK ((char_length(`MatKhau`) >= 6))
)
```

#### nhanvien (Employees/Sellers)
```sql
CREATE TABLE `nhanvien` (
  `MaNV` varchar(30) NOT NULL,
  `TenNV` varchar(200) NOT NULL,
  `TenDN` varchar(100) NOT NULL,
  `MatKhau` varchar(255) NOT NULL,
  PRIMARY KEY (`MaNV`),
  UNIQUE KEY `TenDN` (`TenDN`),
  CONSTRAINT `nhanvien_chk_1` CHECK ((char_length(`MatKhau`) >= 6))
)
```

#### sanpham (Products)
```sql
CREATE TABLE `sanpham` (
  `MaSP` varchar(30) NOT NULL,
  `TenSP` varchar(300) NOT NULL,
  `Gia` decimal(14,2) NOT NULL,
  `MoTa` text,
  `MaTH` varchar(30) NOT NULL,
  `SoLuong` int NOT NULL,
  PRIMARY KEY (`MaSP`),
  KEY `MaTH` (`MaTH`),
  CONSTRAINT `sanpham_ibfk_1` FOREIGN KEY (`MaTH`) REFERENCES `thuonghieu` (`MaTH`),
  CONSTRAINT `sanpham_chk_1` CHECK ((`Gia` > 0)),
  CONSTRAINT `sanpham_chk_2` CHECK ((`SoLuong` >= 0))
)
```

#### thuonghieu (Brands)
```sql
CREATE TABLE `thuonghieu` (
  `MaTH` varchar(30) NOT NULL,
  `TenTH` varchar(200) NOT NULL,
  `MoTa` text,
  PRIMARY KEY (`MaTH`)
)
```

#### giohang (Shopping Carts)
```sql
CREATE TABLE `giohang` (
  `MaGH` varchar(30) NOT NULL,
  `MaKH` varchar(30) NOT NULL,
  PRIMARY KEY (`MaGH`),
  UNIQUE KEY `MaKH` (`MaKH`),
  CONSTRAINT `giohang_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`)
)
```

#### giohangchuasanpham (Cart Items)
```sql
CREATE TABLE `giohangchuasanpham` (
  `MaGH` varchar(30) NOT NULL,
  `MaSP` varchar(30) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  `Size` varchar(20) NOT NULL,
  `SoLuong` int NOT NULL,
  PRIMARY KEY (`MaGH`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `giohangchuasanpham_ibfk_1` FOREIGN KEY (`MaGH`) REFERENCES `giohang` (`MaGH`),
  CONSTRAINT `giohangchuasanpham_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`),
  CONSTRAINT `giohangchuasanpham_chk_1` CHECK ((`SoLuong` > 0))
)
```

#### hoadon (Invoices/Orders)
```sql
CREATE TABLE `hoadon` (
  `MaHD` varchar(40) NOT NULL,
  `MaKH` varchar(30) NOT NULL,
  `MaNV` varchar(30) DEFAULT NULL,
  `NgayLap` date NOT NULL,
  PRIMARY KEY (`MaHD`),
  KEY `MaKH` (`MaKH`),
  KEY `MaNV` (`MaNV`),
  CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`),
  CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`MaNV`) REFERENCES `nhanvien` (`MaNV`)
)
```

#### cthoadon (Invoice Details)
```sql
CREATE TABLE `cthoadon` (
  `MaHD` varchar(40) NOT NULL,
  `MaSP` varchar(30) NOT NULL,
  `TenSP` varchar(300) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  `Size` varchar(50) NOT NULL,
  `SoLuongMua` int NOT NULL,
  `DonGia` decimal(14,2) NOT NULL,
  `ThanhTien` decimal(16,2) NOT NULL,
  PRIMARY KEY (`MaHD`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `cthoadon_ibfk_1` FOREIGN KEY (`MaHD`) REFERENCES `hoadon` (`MaHD`),
  CONSTRAINT `cthoadon_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`),
  CONSTRAINT `cthoadon_chk_1` CHECK ((`SoLuongMua` >= 0)),
  CONSTRAINT `cthoadon_chk_2` CHECK ((`DonGia` > 0))
)
```

#### url_sp (Product Images)
```sql
CREATE TABLE `url_sp` (
  `MaSP` varchar(30) NOT NULL,
  `URLAnh` varchar(500) NOT NULL,
  PRIMARY KEY (`MaSP`,`URLAnh`),
  CONSTRAINT `url_sp_ibfk_1` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`)
)
```

#### mausac_sp (Product Colors - Dynamic)
```sql
CREATE TABLE IF NOT EXISTS `mausac_sp` (
  `MaSP` VARCHAR(30) NOT NULL,
  `MauSac` VARCHAR(100) NOT NULL,
  PRIMARY KEY (MaSP, MauSac),
  FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
)
```

---

## KEY SQL PATTERNS & TECHNIQUES

### 1. Auto-Increment ID Generation
```sql
SELECT MAX(CAST(SUBSTRING(MaXX, 3) AS UNSIGNED)) FROM table WHERE MaXX LIKE 'XX%'
```
**Used for**: Products (SP), Customers (KH), Employees (B23DCCN), Brands (TH), Carts (GH), Invoices (HD)

### 2. Stock Validation Pattern
```sql
-- Get total in all carts
SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaSP = %s

-- Compare with available stock
SELECT SoLuong FROM sanpham WHERE MaSP = %s

-- Update with safety check
UPDATE sanpham SET SoLuong = GREATEST(0, SoLuong - %s) WHERE MaSP = %s
```

### 3. Cascade Delete Pattern
```sql
-- Delete in order of dependencies
DELETE FROM url_sp WHERE MaSP = %s
DELETE FROM sanpham WHERE MaSP = %s
```

### 4. Join Patterns
```sql
-- LEFT JOIN (include nulls)
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH

-- INNER JOIN (only matching records)
INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
```

### 5. Grouping and Aggregation
```sql
SELECT MaSP, SUM(SoLuongMua) as total, SUM(SoLuongMua * Gia) as revenue
FROM cthoadon
GROUP BY MaSP
ORDER BY revenue DESC
```

### 6. Date Filtering
```sql
WHERE MONTH(NgayLap) = %s AND YEAR(NgayLap) = %s
```

---

## IMPORTANT NOTES

### Transaction Management
- **Payment Processing**: Uses atomic transactions (all or nothing)
- **Rollback**: Triggered on any error during payment
- **Commit**: Only after all steps complete successfully

### Stock Management
- Cart items do NOT reduce inventory
- Inventory reduced ONLY on payment completion
- Validation checks total demand across ALL users
- GREATEST(0, value) prevents negative stock

### Data Integrity
- Foreign key constraints enforce referential integrity
- CHECK constraints validate data (price > 0, quantity >= 0, password length, phone format)
- UNIQUE constraints prevent duplicates (username, phone)
- Cascade deletes maintain consistency

### Security Considerations
- All queries use parameterized statements (%s) to prevent SQL injection
- Passwords stored as plain text (⚠️ **Should be hashed in production**)
- No input sanitization visible in queries (relies on application layer)

### Performance Optimizations
- Indexes on foreign keys
- Indexes on unique columns
- ORDER BY on indexed columns when possible
- Joins optimized with proper indexes

---

## QUERY STATISTICS

**Total Query Patterns**: 31  
**Total Tables**: 10  
**Total Foreign Keys**: 11  
**Total Unique Constraints**: 5  
**Total Check Constraints**: 8

### Query Distribution by Module:
- **Product View**: 11 query groups
- **Cart View**: 3 query groups
- **Invoice View**: 2 query groups
- **Sales View**: 1 query group
- **Product Model**: 10 query groups
- **Login/Registration**: 4 query groups

---

## DATABASE RELATIONSHIPS

```
khachhang (1) ----< giohang (1) ----< giohangchuasanpham (M) >---- sanpham
    |                                                                   |
    |                                                                   |
    v                                                                   v
  hoadon (1) ----< cthoadon (M) >--------------------------------- sanpham
    |                                                                   |
    v                                                                   v
nhanvien                                                          thuonghieu
                                                                        |
                                                                        v
                                                                   url_sp
                                                                   mausac_sp
```

**Legend**: (1) = One, (M) = Many, < = One-to-Many relationship

---

**End of Documentation**

*Generated on: October 28, 2025*  
*Database: shopgiaydep09102025*  
*Project: Shoes Shop Management System*

