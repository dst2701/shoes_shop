-- ============================================================================
-- SQL QUERIES FOR MYSQL WORKBENCH - SHOES SHOP PROJECT
-- Database: shopgiaydep09102025
-- Date: October 28, 2025
--
-- NOTE: Replace the example values with your actual data
-- Placeholders like %s in the documentation are Python syntax - replaced here with actual MySQL syntax
-- ============================================================================

USE shopgiaydep09102025;

-- ============================================================================
-- PRODUCT VIEW QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Load Cart from Database
-- Purpose: Load user's cart items when they log in
-- Replace 'username_here' with actual username
-- ----------------------------------------------------------------------------

-- Get customer ID from username
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Get cart ID from customer ID (replace 'KH001' with actual MaKH from above)
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Get all products in cart (replace 'GH001' with actual MaGH)
SELECT MaSP, SoLuong FROM giohangchuasanpham WHERE MaGH = 'GH001';


-- ----------------------------------------------------------------------------
-- 2. Refresh Brand Filter
-- Purpose: Get list of all brands for the filter dropdown
-- ----------------------------------------------------------------------------

SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH;


-- ----------------------------------------------------------------------------
-- 3. Update Cart Count
-- Purpose: Display total number of items in cart
-- ----------------------------------------------------------------------------

-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Get cart ID
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Calculate total items in cart
SELECT SUM(SoLuong) as TotalItems FROM giohangchuasanpham WHERE MaGH = 'GH001';


-- ----------------------------------------------------------------------------
-- 4. Load Products with Brands and Images
-- Purpose: Load all products with their details, brands, and images
-- ----------------------------------------------------------------------------

-- Get all products with brand info
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
ORDER BY sp.MaSP;

-- Get all brands for filter
SELECT DISTINCT TenTH FROM thuonghieu ORDER BY TenTH;

-- Get all product images
SELECT MaSP, URLAnh FROM url_sp ORDER BY MaSP;


-- ----------------------------------------------------------------------------
-- 5. Check Product Stock
-- Purpose: Check available stock before adding to cart
-- ----------------------------------------------------------------------------

SELECT SoLuong FROM sanpham WHERE MaSP = 'SP001';


-- ----------------------------------------------------------------------------
-- 6. Add Product to Cart (with Stock Validation)
-- Purpose: Add product to cart with comprehensive stock validation
-- ----------------------------------------------------------------------------

-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Check if cart exists
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- If cart doesn't exist, generate new cart ID
SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) as MaxID FROM giohang;

-- Create new cart (if needed) - replace GH002 with next ID
INSERT INTO giohang (MaGH, MaKH) VALUES ('GH002', 'KH001');

-- Get current stock for validation
SELECT SoLuong FROM sanpham WHERE MaSP = 'SP001';

-- Calculate total quantity in all carts (to prevent overselling)
SELECT SUM(ghsp.SoLuong) as TotalInCarts
FROM giohangchuasanpham ghsp
WHERE ghsp.MaSP = 'SP001';

-- Check if user already has this item (specific color/size)
SELECT SoLuong FROM giohangchuasanpham
WHERE MaGH = 'GH001' AND MaSP = 'SP001' AND MauSac = 'Đen' AND Size = '42';

-- Update existing cart item (if already exists)
UPDATE giohangchuasanpham
SET SoLuong = 3
WHERE MaGH = 'GH001' AND MaSP = 'SP001' AND MauSac = 'Đen' AND Size = '42';

-- OR Insert new cart item (if doesn't exist)
INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
VALUES ('GH001', 'SP001', 'Đen', '42', 2);


-- ----------------------------------------------------------------------------
-- 7. Delete Product (Seller)
-- Purpose: Remove product and its images from database
-- ----------------------------------------------------------------------------

-- Delete product images first (to maintain referential integrity)
DELETE FROM url_sp WHERE MaSP = 'SP001';

-- Delete product colors
DELETE FROM mausac_sp WHERE MaSP = 'SP001';

-- Delete product
DELETE FROM sanpham WHERE MaSP = 'SP001';


-- ----------------------------------------------------------------------------
-- 8. Load Product Colors Dynamically
-- Purpose: Load available colors for selected product
-- ----------------------------------------------------------------------------

SELECT MauSac FROM mausac_sp WHERE MaSP = 'SP001';


-- ----------------------------------------------------------------------------
-- 9. Add New Product
-- Purpose: Add new product with colors and images
-- ----------------------------------------------------------------------------

-- Create color table if not exists
CREATE TABLE IF NOT EXISTS mausac_sp (
    MaSP VARCHAR(30) NOT NULL,
    MauSac VARCHAR(100) NOT NULL,
    PRIMARY KEY (MaSP, MauSac),
    FOREIGN KEY (MaSP) REFERENCES sanpham(MaSP) ON DELETE CASCADE
);

-- Generate new product ID
SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) as MaxID FROM sanpham WHERE MaSP LIKE 'SP%';

-- Insert product (replace with actual values)
INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, NgayNhapHang)
VALUES ('SP010', 'Nike Air Max 270', 3500000, 'Giày thể thao cao cấp', 'TH001', 50, '2025-10-28');

-- Insert colors (multiple inserts for each color)
INSERT INTO mausac_sp (MaSP, MauSac) VALUES ('SP010', 'Trắng');
INSERT INTO mausac_sp (MaSP, MauSac) VALUES ('SP010', 'Đen');
INSERT INTO mausac_sp (MaSP, MauSac) VALUES ('SP010', 'Xanh Dương');

-- Insert image URLs (multiple inserts for each image)
INSERT INTO url_sp (MaSP, URLAnh) VALUES ('SP010', 'https://example.com/image1.jpg');
INSERT INTO url_sp (MaSP, URLAnh) VALUES ('SP010', 'https://example.com/image2.jpg');


-- ----------------------------------------------------------------------------
-- 10. Update Product
-- Purpose: Update product information, colors, and images
-- ----------------------------------------------------------------------------

-- Get product details
SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, sp.MaTH, sp.SoLuong, th.TenTH, sp.NgayNhapHang
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
WHERE sp.MaSP = 'SP001';

-- Get product images
SELECT URLAnh FROM url_sp WHERE MaSP = 'SP001';

-- Get product colors
SELECT MauSac FROM mausac_sp WHERE MaSP = 'SP001';

-- Load all brands for dropdown
SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH;

-- Update product information
UPDATE sanpham
SET TenSP = 'Nike Air Max 270 Updated',
    Gia = 3800000,
    MoTa = 'Updated description',
    MaTH = 'TH001',
    SoLuong = 60,
    NgayNhapHang = '2025-10-28'
WHERE MaSP = 'SP001';

-- Delete old colors
DELETE FROM mausac_sp WHERE MaSP = 'SP001';

-- Insert new colors
INSERT INTO mausac_sp (MaSP, MauSac) VALUES ('SP001', 'Trắng');
INSERT INTO mausac_sp (MaSP, MauSac) VALUES ('SP001', 'Nâu');

-- Delete old images
DELETE FROM url_sp WHERE MaSP = 'SP001';

-- Insert new images
INSERT INTO url_sp (MaSP, URLAnh) VALUES ('SP001', 'https://example.com/new1.jpg');


-- ----------------------------------------------------------------------------
-- 11. Brand Management
-- Purpose: Manage brands (view, add, delete)
-- ----------------------------------------------------------------------------

-- Load all brands
SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH;

-- Delete brand (cascade delete products and images)
-- WARNING: This will delete ALL products of this brand!
DELETE FROM url_sp WHERE MaSP IN (SELECT MaSP FROM sanpham WHERE MaTH = 'TH001');
DELETE FROM mausac_sp WHERE MaSP IN (SELECT MaSP FROM sanpham WHERE MaTH = 'TH001');
DELETE FROM sanpham WHERE MaTH = 'TH001';
DELETE FROM thuonghieu WHERE MaTH = 'TH001';

-- Check if brand exists
SELECT MaTH FROM thuonghieu WHERE TenTH = 'Nike';

-- Generate new brand ID
SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) as MaxID FROM thuonghieu WHERE MaTH LIKE 'TH%';

-- Insert new brand
INSERT INTO thuonghieu (MaTH, TenTH) VALUES ('TH003', 'Puma');


-- ============================================================================
-- CART VIEW QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 12. Load Cart Details
-- Purpose: Display all items in user's cart with calculated totals
-- ----------------------------------------------------------------------------

-- Get customer ID from username
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Get cart ID from customer ID
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Get cart items with product details and calculated totals
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
       (sp.Gia * ghsp.SoLuong) as ThanhTien
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = 'GH001'
ORDER BY sp.TenSP;


-- ----------------------------------------------------------------------------
-- 13. Remove Item from Cart
-- Purpose: Remove single item from cart
-- ----------------------------------------------------------------------------

-- Get customer and cart IDs
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Delete specific item from cart (must match product, color, and size)
DELETE FROM giohangchuasanpham
WHERE MaGH = 'GH001' AND MaSP = 'SP001' AND MauSac = 'Đen' AND Size = '42';


-- ----------------------------------------------------------------------------
-- 14. Clear Entire Cart
-- Purpose: Remove all items from cart
-- NOTE: Does NOT return quantities to inventory
-- ----------------------------------------------------------------------------

-- Get customer and cart IDs
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Delete all items from cart
DELETE FROM giohangchuasanpham WHERE MaGH = 'GH001';


-- ============================================================================
-- INVOICE VIEW QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 15. Generate Invoice Preview
-- Purpose: Display invoice preview before payment
-- ----------------------------------------------------------------------------

-- Get customer info (address and phone)
SELECT DiaChi, SDT, MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Generate next invoice ID (for preview only)
SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) as MaxID FROM hoadon WHERE MaHD LIKE 'HD%';

-- Get customer's cart
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Get cart items with details for invoice preview
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = 'GH001';


-- ----------------------------------------------------------------------------
-- 16. Process Payment (CRITICAL TRANSACTION)
-- Purpose: Complete payment - creates invoice, updates inventory, clears cart
-- IMPORTANT: In production, this should be wrapped in a TRANSACTION
-- ----------------------------------------------------------------------------

-- Start transaction
START TRANSACTION;

-- Get customer ID
SELECT MaKH FROM khachhang WHERE TenDN = 'username_here';

-- Generate actual invoice ID
SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) as MaxID FROM hoadon WHERE MaHD LIKE 'HD%';

-- Create invoice header record
INSERT INTO hoadon (MaHD, MaKH, NgayLap)
VALUES ('HD010', 'KH001', '2025-10-28');

-- Get customer's cart
SELECT MaGH FROM giohang WHERE MaKH = 'KH001';

-- Get all cart items with full details
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = 'GH001';

-- For each item, check stock availability
SELECT SoLuong FROM sanpham WHERE MaSP = 'SP001';

-- Insert invoice line item (repeat for each product)
INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
VALUES ('HD010', 'SP001', 'Nike Air Max', 'Đen', '42', 2, 3500000, 7000000);

-- Decrease product quantity with safety check
UPDATE sanpham
SET SoLuong = GREATEST(0, SoLuong - 2)
WHERE MaSP = 'SP001';

-- Verify quantity is not negative (safety check)
SELECT SoLuong FROM sanpham WHERE MaSP = 'SP001';

-- Clear cart after successful payment
DELETE FROM giohangchuasanpham WHERE MaGH = 'GH001';

-- Commit transaction (if all steps succeeded)
COMMIT;

-- If any error occurred, rollback:
-- ROLLBACK;


-- ============================================================================
-- SALES VIEW QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 17. Load Monthly Sales Statistics
-- Purpose: Get sales statistics for a specific month/year
-- Replace month (10) and year (2025) with desired values
-- ----------------------------------------------------------------------------

SELECT
    ct.MaSP,
    sp.TenSP,
    SUM(ct.SoLuongMua) as total_quantity,
    sp.Gia as unit_price,
    SUM(ct.SoLuongMua * sp.Gia) as total_sales
FROM cthoadon ct
INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
INNER JOIN sanpham sp ON ct.MaSP = sp.MaSP
WHERE MONTH(hd.NgayLap) = 10 AND YEAR(hd.NgayLap) = 2025
GROUP BY ct.MaSP, sp.TenSP, sp.Gia
ORDER BY total_sales DESC;


-- ============================================================================
-- PRODUCT MODEL QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 18. Generate Product ID
-- Purpose: Auto-generate next product ID
-- ----------------------------------------------------------------------------

SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) as MaxID FROM sanpham WHERE MaSP LIKE 'SP%';

-- To use: Add 1 to MaxID and format as SP{number:03d}
-- Example: If MaxID = 5, next ID = SP006


-- ----------------------------------------------------------------------------
-- 19. Generate Brand ID
-- Purpose: Auto-generate next brand ID
-- ----------------------------------------------------------------------------

SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) as MaxID FROM thuonghieu WHERE MaTH LIKE 'TH%';


-- ----------------------------------------------------------------------------
-- 20. Get or Create Brand
-- Purpose: Ensure brand exists, create if needed
-- ----------------------------------------------------------------------------

-- Check if brand exists
SELECT MaTH FROM thuonghieu WHERE TenTH = 'Nike';

-- If not exists, create new brand
INSERT INTO thuonghieu (MaTH, TenTH, MoTa)
VALUES ('TH001', 'Nike', 'Thương hiệu thể thao quốc tế');


-- ----------------------------------------------------------------------------
-- 21. Get All Products
-- Purpose: Retrieve all products sorted by name
-- ----------------------------------------------------------------------------

SELECT MaSP, TenSP, Gia, MoTa
FROM sanpham
ORDER BY TenSP;


-- ----------------------------------------------------------------------------
-- 22. Get Product Images
-- Purpose: Get all image URLs for a specific product
-- ----------------------------------------------------------------------------

SELECT URLAnh
FROM url_sp
WHERE MaSP = 'SP001'
ORDER BY URLAnh;


-- ----------------------------------------------------------------------------
-- 23. Get Product by ID
-- Purpose: Retrieve single product details
-- ----------------------------------------------------------------------------

SELECT MaSP, TenSP, Gia, MoTa
FROM sanpham
WHERE MaSP = 'SP001';


-- ----------------------------------------------------------------------------
-- 24. Search and Filter Products
-- Purpose: Advanced product search with multiple filters
-- ----------------------------------------------------------------------------

-- Search by product name (contains 'Nike')
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
WHERE s.TenSP LIKE '%Nike%'
ORDER BY s.TenSP;

-- Filter by brand
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
WHERE t.TenTH = 'Nike'
ORDER BY s.TenSP;

-- Sort by price (low to high)
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
ORDER BY s.Gia ASC;

-- Sort by price (high to low)
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
ORDER BY s.Gia DESC;

-- Combined: Search + Brand Filter + Price Sort
SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
FROM sanpham s
JOIN thuonghieu t ON s.MaTH = t.MaTH
WHERE s.TenSP LIKE '%Air%' AND t.TenTH = 'Nike'
ORDER BY s.Gia DESC;


-- ============================================================================
-- LOGIN/REGISTRATION QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 25. User Authentication (Buyer)
-- Purpose: Verify buyer login credentials
-- WARNING: Passwords should be hashed in production!
-- ----------------------------------------------------------------------------

-- Check buyer credentials
SELECT MaKH, TenKH FROM khachhang
WHERE TenDN = 'john_doe' AND MatKhau = 'password123';


-- ----------------------------------------------------------------------------
-- 26. User Authentication (Seller)
-- Purpose: Verify seller/employee login credentials
-- ----------------------------------------------------------------------------

-- Check seller credentials
SELECT MaNV, TenNV FROM nhanvien
WHERE TenDN = 'seller01' AND MatKhau = 'password123';


-- ----------------------------------------------------------------------------
-- 27. User Registration (Buyer)
-- Purpose: Register new customer and create their shopping cart
-- ----------------------------------------------------------------------------

-- Check if username exists
SELECT MaKH FROM khachhang WHERE TenDN = 'new_user';

-- Check if phone number exists
SELECT MaKH FROM khachhang WHERE SDT = '0123456789';

-- Generate new customer ID
SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) as MaxID FROM khachhang WHERE MaKH LIKE 'KH%';

-- Register new buyer (replace values)
INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
VALUES ('KH005', 'Nguyen Van A', '0123456789', '123 Nguyen Trai, HN', 'new_user', 'password123');

-- Generate new cart ID
SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) as MaxID FROM giohang;

-- Create cart for new user
INSERT INTO giohang (MaGH, MaKH) VALUES ('GH005', 'KH005');


-- ----------------------------------------------------------------------------
-- 28. User Registration (Seller)
-- Purpose: Register new employee/seller
-- ----------------------------------------------------------------------------

-- Check if username exists (in employee table)
SELECT MaNV FROM nhanvien WHERE TenDN = 'new_seller';

-- Generate new employee ID
SELECT MAX(CAST(SUBSTRING(MaNV, 11) AS UNSIGNED)) as MaxID FROM nhanvien WHERE MaNV LIKE 'B23DCCN%';

-- Register new seller (replace values)
INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
VALUES ('B23DCCN005', 'Tran Thi B', 'new_seller', 'password123');


-- ============================================================================
-- USEFUL QUERIES FOR TESTING & DEBUGGING
-- ============================================================================

-- View all customers
SELECT * FROM khachhang;

-- View all products with brands
SELECT sp.*, th.TenTH
FROM sanpham sp
LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH;

-- View all carts with customer info
SELECT gh.MaGH, kh.TenKH, kh.TenDN
FROM giohang gh
JOIN khachhang kh ON gh.MaKH = kh.MaKH;

-- View cart contents for all users
SELECT gh.MaGH, kh.TenKH, ghsp.MaSP, sp.TenSP, ghsp.MauSac, ghsp.Size, ghsp.SoLuong
FROM giohang gh
JOIN khachhang kh ON gh.MaKH = kh.MaKH
JOIN giohangchuasanpham ghsp ON gh.MaGH = ghsp.MaGH
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
ORDER BY kh.TenKH, sp.TenSP;

-- View all invoices with customer info
SELECT hd.MaHD, hd.NgayLap, kh.TenKH, kh.TenDN
FROM hoadon hd
JOIN khachhang kh ON hd.MaKH = kh.MaKH
ORDER BY hd.NgayLap DESC;

-- View invoice details
SELECT hd.MaHD, hd.NgayLap, ct.MaSP, ct.TenSP, ct.MauSac, ct.Size, ct.SoLuongMua, ct.DonGia, ct.ThanhTien
FROM hoadon hd
JOIN cthoadon ct ON hd.MaHD = ct.MaHD
WHERE hd.MaHD = 'HD001';

-- Total sales by product
SELECT sp.MaSP, sp.TenSP,
       SUM(ct.SoLuongMua) as TotalSold,
       SUM(ct.ThanhTien) as TotalRevenue
FROM sanpham sp
LEFT JOIN cthoadon ct ON sp.MaSP = ct.MaSP
GROUP BY sp.MaSP, sp.TenSP
ORDER BY TotalRevenue DESC;

-- Products with low stock (less than 10)
SELECT MaSP, TenSP, SoLuong
FROM sanpham
WHERE SoLuong < 10
ORDER BY SoLuong ASC;

-- Products with no images
SELECT sp.MaSP, sp.TenSP
FROM sanpham sp
LEFT JOIN url_sp u ON sp.MaSP = u.MaSP
WHERE u.MaSP IS NULL;

-- Count products per brand
SELECT th.TenTH, COUNT(sp.MaSP) as ProductCount
FROM thuonghieu th
LEFT JOIN sanpham sp ON th.MaTH = sp.MaTH
GROUP BY th.TenTH
ORDER BY ProductCount DESC;


-- ============================================================================
-- DATA CLEANUP QUERIES (USE WITH CAUTION!)
-- ============================================================================

-- Clear all cart items (but keep cart structure)
-- DELETE FROM giohangchuasanpham;

-- Reset auto-increment counters (if needed)
-- ALTER TABLE sanpham AUTO_INCREMENT = 1;

-- Delete test data
-- DELETE FROM khachhang WHERE TenDN LIKE 'test%';


-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================

