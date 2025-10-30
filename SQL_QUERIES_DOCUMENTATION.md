# 📊 SQL QUERIES DOCUMENTATION - SHOES SHOP PROJECT

**Database**: shopquanao (project local DB)
**Project**: Shoes Shop Management System
**Last Updated**: October 29, 2025

---

## TABLE OF CONTENTS
1. [Overview & placeholders](#overview--placeholders)
2. [Database Schema (current)](#database-schema-current)
3. [Common patterns & notes](#common-patterns--notes)
4. [Product View queries](#product-view-queries)
5. [Cart View queries](#cart-view-queries)
6. [Invoice / Payment queries](#invoice--payment-queries)
7. [Invoice History queries](#invoice-history-queries)
8. [Sales / Statistics queries](#sales--statistics-queries)
9. [Login / Registration queries](#login--registration-queries)
10. [Model / Utility queries](#model--utility-queries)
11. [Appendix: Running queries in MySQL Workbench](#appendix-running-queries-in-mysql-workbench)

---

## Overview & placeholders
- This document lists the SQL queries used across the GUI project (views and models).
- All queries in the Python code use parameterized placeholders ("%s") for safety with the MySQL connector. When running queries directly in MySQL Workbench, replace `%s` with a properly quoted literal (e.g. 'username').

Example Python usage:

    cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))

Equivalent in Workbench:

    SELECT MaKH FROM khachhang WHERE TenDN = 'john_doe';

---

## Database schema (current)
This section summarizes the relevant tables and the important columns used by the application (only columns used by the code are listed).

- khachhang
  - MaKH (PK), TenKH, SDT, DiaChi, TenDN, MatKhau

- nhanvien
  - MaNV (PK), TenNV, TenDN, MatKhau

- thuonghieu
  - MaTH (PK), TenTH, MoTa

- sanpham
  - MaSP (PK), TenSP, Gia, MoTa, MaTH (FK), SoLuong, NgayNhapHang, [optional GiamGia]

- url_sp
  - MaSP (FK), URLAnh

- mausac_sp (optional/dynamic)
  - MaSP (FK), MauSac

- giohang
  - MaGH (PK), MaKH (FK)  -- ONE cart per customer; unique constraint on MaKH

- giohangchuasanpham
  - MaGH (FK), MaSP (FK), MauSac, Size, SoLuong  -- PRIMARY KEY (MaGH, MaSP, MauSac, Size)

- hoadon
  - MaHD (PK), MaKH (FK), MaNV (FK optional), NgayLap (DATE)

- cthoadon
  - MaHD (FK), MaSP (FK), TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien
  - PRIMARY KEY (MaHD, MaSP, MauSac, Size)

Notes:
- `SoLuongMua` is the quantity in `cthoadon` (not `SoLuong`). This is the column used in invoice detail queries.
- `SoLuong` in `sanpham` is the current inventory.
- The `GiamGia` column may or may not exist in some local DB copies; code guards for its absence where possible.

---

## Common patterns & notes
- ID generation patterns in the app use SQL picks like:

    SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'

  then add 1 and format as SP###.

- For creating carts on registration, the app creates a `giohang` row with a new MaGH and the user's MaKH.
- Cart items do NOT decrement inventory when added. Inventory is decremented only when an invoice is successfully paid.
- All DB modifications use parameterized statements (`%s`) in Python code.

---

## Product view queries
Module: views/product_view.py (and related model functions)

1) Load products with brand and image URLs

    SELECT sp.MaSP, sp.TenSP, sp.Gia, sp.MoTa, th.TenTH, sp.SoLuong, sp.NgayNhapHang
    FROM sanpham sp
    LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
    ORDER BY sp.MaSP

2) Load all brands for filter dropdown

    SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH

3) Load images for product gallery

    SELECT MaSP, URLAnh FROM url_sp WHERE MaSP = %s ORDER BY URLAnh

4) Search (by name OR code) + optional brand filter + price sort

    SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH, s.SoLuong
    FROM sanpham s
    LEFT JOIN thuonghieu t ON s.MaTH = t.MaTH
    WHERE (s.TenSP LIKE %s OR s.MaSP LIKE %s)
      [AND t.TenTH = %s]
    ORDER BY [s.Gia ASC | s.Gia DESC | s.TenSP]

5) Generate brand ID (utility used when adding brand)

    SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) FROM thuonghieu WHERE MaTH LIKE 'TH%'

6) Delete product and its images

    DELETE FROM url_sp WHERE MaSP = %s
    DELETE FROM sanpham WHERE MaSP = %s

---

## Cart view queries
Module: views/cart_view.py

1) Get customer's MaKH and MaGH

    SELECT MaKH FROM khachhang WHERE TenDN = %s
    SELECT MaGH FROM giohang WHERE MaKH = %s

2) Load cart items for display (with product info)

    SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
           (sp.Gia * ghsp.SoLuong) as ThanhTien
    FROM giohangchuasanpham ghsp
    JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
    WHERE ghsp.MaGH = %s
    ORDER BY sp.TenSP

3) Remove single item from cart (by product + color + size)

    DELETE FROM giohangchuasanpham
    WHERE MaGH = %s AND MaSP = %s AND MauSac = %s AND Size = %s

4) Clear entire cart

    DELETE FROM giohangchuasanpham WHERE MaGH = %s

5) Get cart count (sum of SoLuong for this user's cart)

    SELECT SUM(SoLuong) FROM giohangchuasanpham WHERE MaGH = %s

Notes:
- Adding to cart writes into `giohangchuasanpham` so the cart persists across program restarts.
- Color and Size are stored in `MauSac` and `Size` columns.

---

## Invoice / Payment queries
Module: views/invoice_view.py

1) Prepare invoice preview (get customer address & phone)

    SELECT DiaChi, SDT, MaKH FROM khachhang WHERE TenDN = %s

2) Generate next invoice ID (preview)

    SELECT MAX(CAST(SUBSTRING(MaHD, 3) AS UNSIGNED)) FROM hoadon WHERE MaHD LIKE 'HD%'

3) Full payment transaction (high-level steps and queries)
- Begin transaction in Python

- Create invoice header

    INSERT INTO hoadon (MaHD, MaKH, NgayLap) VALUES (%s, %s, %s)

- Read customer's cart items

    SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.SoLuong, ghsp.MauSac, ghsp.Size
    FROM giohangchuasanpham ghsp
    JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
    WHERE ghsp.MaGH = %s

- For each grouped item (grouping by MaSP, MauSac, Size):

    INSERT INTO cthoadon (MaHD, MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

- Decrease inventory safely (prevent negative quantities)

    UPDATE sanpham
    SET SoLuong = GREATEST(0, SoLuong - %s)
    WHERE MaSP = %s

- After all items processed, clear customer's cart

    DELETE FROM giohangchuasanpham WHERE MaGH = %s

- Commit transaction

Notes and validations:
- Before creating invoice lines, code checks stock availability using `sanpham.SoLuong` and also considers quantities already in other carts to avoid overselling.
- `GREATEST(0, SoLuong - %s)` is used to avoid negative inventory; code also verifies post-update value.

---

## Invoice history queries
Module: views/invoice_history_view.py

1) Load invoice history for a customer (aggregated totals)

    SELECT hd.MaHD, hd.NgayLap, SUM(ct.ThanhTien) AS TongTien, SUM(ct.SoLuongMua) AS TongSL
    FROM hoadon hd
    INNER JOIN cthoadon ct ON hd.MaHD = ct.MaHD
    WHERE hd.MaKH = %s
    GROUP BY hd.MaHD, hd.NgayLap
    ORDER BY hd.MaHD DESC  -- newest invoice (highest MaHD) first

2) Load invoice detail for a selected MaHD

    SELECT MaSP, TenSP, MauSac, Size, SoLuongMua, DonGia, ThanhTien
    FROM cthoadon
    WHERE MaHD = %s
    ORDER BY TenSP

Notes:
- The UI shows only DATE in history list (NgayLap). Detailed view can show all stored detail fields.
- Sorting: newest invoice first by MaHD (as requested).

---

## Sales / Statistics queries
Module: views/sales_view.py

1) Monthly sales summary (grouped by product)

    SELECT ct.MaSP, ct.TenSP,
           SUM(ct.SoLuongMua) AS total_quantity,
           SUM(ct.ThanhTien) AS total_sales
    FROM cthoadon ct
    INNER JOIN hoadon hd ON ct.MaHD = hd.MaHD
    WHERE MONTH(hd.NgayLap) = %s AND YEAR(hd.NgayLap) = %s
    GROUP BY ct.MaSP, ct.TenSP
    ORDER BY {order_by}

- `{order_by}` is replaced by one of:
  - `total_sales DESC` (default)
  - `total_quantity DESC`
  - `ct.MaSP ASC`
  - `ct.TenSP ASC`

Notes:
- We use the actual sold amount in `ThanhTien` to compute revenue (historical price stored in `cthoadon`).
- The unit price column is not shown in seller's sales report because price history is already recorded in `cthoadon`.

---

## Login / Registration queries
Module: views/login_view.py

1) Buyer (khachhang) login

    SELECT MaKH, TenKH FROM khachhang WHERE TenDN = %s AND MatKhau = %s

2) Seller (nhanvien) login

    SELECT MaNV, TenNV FROM nhanvien WHERE TenDN = %s AND MatKhau = %s

3) Buyer registration (create khachhang + cart)

    -- check username and phone
    SELECT MaKH FROM khachhang WHERE TenDN = %s
    SELECT MaKH FROM khachhang WHERE SDT = %s

    -- generate new MaKH
    SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) FROM khachhang WHERE MaKH LIKE 'KH%'

    INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
    VALUES (%s, %s, %s, %s, %s, %s)

    -- create cart row for this new customer (one-to-one)
    SELECT MAX(CAST(SUBSTRING(MaGH, 3) AS UNSIGNED)) FROM giohang WHERE MaGH LIKE 'GH%'
    INSERT INTO giohang (MaGH, MaKH) VALUES (%s, %s)

4) Seller registration

    SELECT MaNV FROM nhanvien WHERE TenDN = %s
    SELECT MAX(CAST(SUBSTRING(MaNV, 11) AS UNSIGNED)) FROM nhanvien WHERE MaNV LIKE 'B23DCCN%'
    INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau) VALUES (%s, %s, %s, %s)

Notes:
- The app enforces unique TenDN and SDT for customers. Sellers (nhanvien) also have unique TenDN.
- The UI and registration flow generate and insert ID strings (KH001, GH001, etc.).

---

## Model / utility queries
- Generate next product ID (SP)

    SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'

- Insert new product (including images & colors)

    INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong, NgayNhapHang)
    VALUES (%s, %s, %s, %s, %s, %s, %s)

    -- then insert associated records
    INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)
    INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)

- Update product

    UPDATE sanpham
    SET TenSP = %s, Gia = %s, MoTa = %s, MaTH = %s, SoLuong = %s, NgayNhapHang = %s
    WHERE MaSP = %s

    -- replace colors and images using delete-then-insert pattern
    DELETE FROM mausac_sp WHERE MaSP = %s
    INSERT INTO mausac_sp (MaSP, MauSac) VALUES (%s, %s)
    DELETE FROM url_sp WHERE MaSP = %s
    INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)

-- Brand management

    SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH
    SELECT MaTH FROM thuonghieu WHERE TenTH = %s
    DELETE FROM url_sp WHERE MaSP IN (SELECT MaSP FROM sanpham WHERE MaTH = %s)
    DELETE FROM sanpham WHERE MaTH = %s
    DELETE FROM thuonghieu WHERE MaTH = %s

---

## Appendix: Running queries in MySQL Workbench
- Replace `%s` placeholders with literal values (quoted strings when necessary).
- Use correct column names from this doc (e.g. `SoLuongMua` in `cthoadon`).
- If you get errors like "unknown column ct.SoLuong", check that the code expects `SoLuongMua` (invoice detail) vs `SoLuong` (product inventory) and that table aliases match in your query.

Example fix for the reported error:

    -- Wrong
    SELECT ct.SoLuong FROM cthoadon ct

    -- Correct
    SELECT ct.SoLuongMua FROM cthoadon ct

---

If you'd like, I can also export this documentation to PDF or create a single SQL file with all queries converted to literal form so you can run them directly in MySQL Workbench.

---

*End of documentation (updated)*
