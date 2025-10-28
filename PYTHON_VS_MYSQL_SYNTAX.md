# 🔄 Python vs MySQL Syntax - Side by Side Comparison

## Quick Answer to Your Question

**Q: Why does `SELECT MaKH FROM khachhang WHERE TenDN = %s` give a syntax error in MySQL?**

**A: Because `%s` is Python syntax, not MySQL!**

---

## 📊 Visual Comparison

### Example 1: Simple SELECT

| Context | Code | Works In |
|---------|------|----------|
| **Python (GUI)** | `cursor.execute("SELECT MaKH FROM khachhang WHERE TenDN = %s", (username,))` | ✅ Python/GUI |
| **MySQL Workbench** | `SELECT MaKH FROM khachhang WHERE TenDN = 'john_doe';` | ✅ MySQL |

---

### Example 2: INSERT Statement

#### In Python Code:
```python
cursor.execute("""
    INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong)
    VALUES (%s, %s, %s, %s, %s, %s)
""", ('SP010', 'Nike Air Max', 3500000, 'Great shoes', 'TH001', 50))
```

#### In MySQL Workbench:
```sql
INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong)
VALUES ('SP010', 'Nike Air Max', 3500000, 'Great shoes', 'TH001', 50);
```

---

### Example 3: UPDATE Statement

#### In Python Code:
```python
cursor.execute("""
    UPDATE sanpham 
    SET TenSP = %s, Gia = %s, SoLuong = %s
    WHERE MaSP = %s
""", (new_name, new_price, new_quantity, product_id))
```

#### In MySQL Workbench:
```sql
UPDATE sanpham 
SET TenSP = 'Nike Air Max 2024', Gia = 3800000, SoLuong = 60
WHERE MaSP = 'SP001';
```

---

### Example 4: DELETE Statement

#### In Python Code:
```python
cursor.execute("DELETE FROM giohangchuasanpham WHERE MaGH = %s AND MaSP = %s", 
               (cart_id, product_id))
```

#### In MySQL Workbench:
```sql
DELETE FROM giohangchuasanpham WHERE MaGH = 'GH001' AND MaSP = 'SP001';
```

---

## 🎯 The Pattern

### Python Pattern:
```python
cursor.execute("SQL with %s placeholders", (value1, value2, value3))
                        ↑                         ↑
                   Placeholders              Actual values (tuple)
```

### MySQL Pattern:
```sql
SQL with 'actual' and 1000 and 'values';
              ↑        ↑         ↑
          String    Number    String
```

---

## 📋 Data Type Rules

### In Python Code:
```python
# Python automatically handles the quoting
cursor.execute("WHERE TenDN = %s", (username,))      # String
cursor.execute("WHERE Gia = %s", (price,))           # Number  
cursor.execute("WHERE NgayLap = %s", (date,))        # Date
```

### In MySQL Workbench:
```sql
-- You must quote correctly
WHERE TenDN = 'john_doe'          -- String needs quotes
WHERE Gia = 3500000               -- Number NO quotes
WHERE NgayLap = '2025-10-28'      -- Date needs quotes
```

---

## 🔍 Real Examples from Your Project

### 1. Login Check

**In your GUI (login_view.py):**
```python
cursor.execute("SELECT MaKH, TenKH FROM khachhang WHERE TenDN = %s AND MatKhau = %s",
               (username, password))
```

**To test in MySQL Workbench:**
```sql
SELECT MaKH, TenKH FROM khachhang WHERE TenDN = 'testuser' AND MatKhau = 'password123';
```

---

### 2. Add to Cart

**In your GUI (product_view.py):**
```python
cursor.execute("""
    INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
    VALUES (%s, %s, %s, %s, %s)
""", (ma_gh, ma_sp, selected_color, selected_size, quantity))
```

**To test in MySQL Workbench:**
```sql
INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
VALUES ('GH001', 'SP001', 'Đen', '42', 2);
```

---

### 3. Get Cart Items

**In your GUI (cart_view.py):**
```python
cursor.execute("""
    SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
           (sp.Gia * ghsp.SoLuong) as ThanhTien
    FROM giohangchuasanpham ghsp
    JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
    WHERE ghsp.MaGH = %s
    ORDER BY sp.TenSP
""", (ma_gh,))
```

**To test in MySQL Workbench:**
```sql
SELECT ghsp.MaSP, sp.TenSP, sp.Gia, ghsp.MauSac, ghsp.Size, ghsp.SoLuong,
       (sp.Gia * ghsp.SoLuong) as ThanhTien
FROM giohangchuasanpham ghsp
JOIN sanpham sp ON ghsp.MaSP = sp.MaSP
WHERE ghsp.MaGH = 'GH001'
ORDER BY sp.TenSP;
```

---

### 4. Sales Statistics

**In your GUI (sales_view.py):**
```python
cursor.execute("""
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
""", (month, year))
```

**To test in MySQL Workbench:**
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
WHERE MONTH(hd.NgayLap) = 10 AND YEAR(hd.NgayLap) = 2025
GROUP BY ct.MaSP, sp.TenSP, sp.Gia
ORDER BY total_sales DESC;
```

---

## 🛠️ Conversion Cheat Sheet

| Python | MySQL | Notes |
|--------|-------|-------|
| `%s` | `'text'` | String value |
| `%s` | `123` | Numeric value |
| `%s` | `'2025-10-28'` | Date value |
| `%s, %s` | `'text', 123` | Multiple values |
| `VALUES (%s, %s, %s)` | `VALUES ('A', 'B', 'C')` | INSERT |
| `WHERE col = %s` | `WHERE col = 'value'` | WHERE clause |
| `LIKE %s` | `LIKE '%search%'` | LIKE pattern |

---

## ✅ Your Action Items

1. **For Understanding Code**: Read `SQL_QUERIES_DOCUMENTATION.md`
   - Shows how queries work in Python
   - Explains the `%s` placeholders
   - Documents all 31 query patterns

2. **For Testing in MySQL**: Use `SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql`
   - All queries converted to MySQL syntax
   - No placeholders, ready to run
   - Just update the example values

3. **For Quick Reference**: Check `QUICK_START_GUIDE.md`
   - Common patterns
   - Quick examples
   - Troubleshooting tips

---

## 🎓 Why Use Placeholders in Python?

### ❌ BAD (Vulnerable to SQL Injection):
```python
query = f"SELECT * FROM khachhang WHERE TenDN = '{username}'"
cursor.execute(query)
```

### ✅ GOOD (Safe from SQL Injection):
```python
cursor.execute("SELECT * FROM khachhang WHERE TenDN = %s", (username,))
```

**Why?**
- The connector library **escapes special characters**
- Prevents SQL injection attacks
- Handles data types correctly
- Example: If username = `"admin' OR '1'='1"`, the placeholder method treats it as a literal string, not SQL code!

---

## 📌 Summary

| Aspect | Python/GUI Code | MySQL Workbench |
|--------|-----------------|-----------------|
| **Placeholder** | `%s` | Actual value |
| **Quoting** | Automatic | Manual |
| **Safety** | Prevents SQL injection | You must be careful |
| **Testing** | Run the app | Run SQL file |
| **Purpose** | Production code | Testing/debugging |

---

**Bottom Line:**
- `%s` = Python placeholder (for code)
- Replace with actual values for MySQL testing
- Use the provided SQL file for easy testing!

🎉 **Problem Solved!**

