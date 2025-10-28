# 🚀 QUICK START GUIDE - Running SQL Queries

## Understanding `%s` vs MySQL Syntax

### The Problem You Encountered:
```sql
❌ SELECT MaKH FROM khachhang WHERE TenDN = %s
```
**Error**: Syntax error in MySQL Workbench

### Why?
- `%s` is a **Python placeholder**, not MySQL syntax
- It's used in programming to safely insert values
- MySQL Workbench doesn't understand `%s`

---

## ✅ How to Fix It

### Option 1: Replace with Actual Values
```sql
✅ SELECT MaKH FROM khachhang WHERE TenDN = 'john_doe'
```

### Option 2: Use MySQL Variables
```sql
SET @username = 'john_doe';
SELECT MaKH FROM khachhang WHERE TenDN = @username;
```

### Option 3: Use the Ready-Made SQL File
Just open **`SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql`** in MySQL Workbench!

---

## 📖 Quick Examples

### Example 1: Get Customer Info
**Python Version (in code):**
```python
cursor.execute("SELECT * FROM khachhang WHERE TenDN = %s", (username,))
```

**MySQL Version (in Workbench):**
```sql
SELECT * FROM khachhang WHERE TenDN = 'username_here';
```

---

### Example 2: Add to Cart
**Python Version:**
```python
cursor.execute("""
    INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
    VALUES (%s, %s, %s, %s, %s)
""", (cart_id, product_id, color, size, quantity))
```

**MySQL Version:**
```sql
INSERT INTO giohangchuasanpham (MaGH, MaSP, MauSac, Size, SoLuong)
VALUES ('GH001', 'SP001', 'Đen', '42', 2);
```

---

### Example 3: Multiple Placeholders
**Python Version:**
```python
cursor.execute("""
    SELECT * FROM sanpham 
    WHERE Gia BETWEEN %s AND %s 
    AND MaTH = %s
""", (min_price, max_price, brand_id))
```

**MySQL Version:**
```sql
SELECT * FROM sanpham 
WHERE Gia BETWEEN 1000000 AND 5000000 
AND MaTH = 'TH001';
```

---

## 🔧 Using MySQL Variables (Advanced)

If you want to reuse values, use variables:

```sql
-- Set variables
SET @username = 'john_doe';
SET @product_id = 'SP001';
SET @min_price = 1000000;
SET @max_price = 5000000;

-- Use in queries
SELECT * FROM khachhang WHERE TenDN = @username;
SELECT * FROM sanpham WHERE MaSP = @product_id;
SELECT * FROM sanpham WHERE Gia BETWEEN @min_price AND @max_price;
```

---

## 📁 Your Files:

1. **`SQL_QUERIES_DOCUMENTATION.md`** 
   - Complete documentation with explanations
   - Shows Python syntax (with `%s`)
   - Use for understanding the code

2. **`SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql`** ⭐
   - Ready-to-run SQL queries
   - No placeholders, actual MySQL syntax
   - **Use this for testing in MySQL Workbench!**

3. **`QUICK_START_GUIDE.md`** (this file)
   - Quick reference
   - Examples and comparisons

---

## 🎯 Common Patterns

### Pattern 1: String Values
```sql
-- Python:  WHERE column = %s
-- MySQL:   WHERE column = 'value'

WHERE TenDN = 'john_doe'
WHERE MaSP = 'SP001'
WHERE TenTH = 'Nike'
```

### Pattern 2: Numeric Values
```sql
-- Python:  WHERE column = %s
-- MySQL:   WHERE column = number (no quotes!)

WHERE Gia = 3500000
WHERE SoLuong = 50
WHERE MaKH = 'KH001'  -- Note: IDs are strings, so use quotes!
```

### Pattern 3: Date Values
```sql
-- Python:  WHERE column = %s
-- MySQL:   WHERE column = 'YYYY-MM-DD'

WHERE NgayLap = '2025-10-28'
WHERE NgayNhapHang >= '2025-01-01'
```

### Pattern 4: LIKE Searches
```sql
-- Python:  WHERE column LIKE %s  (value = '%search%')
-- MySQL:   WHERE column LIKE '%search%'

WHERE TenSP LIKE '%Nike%'
WHERE SDT LIKE '012%'
```

---

## ⚠️ Important Notes

1. **String values** need **single quotes**: `'value'`
2. **Numeric values** need **no quotes**: `1000000`
3. **IDs** are stored as **strings**, so use quotes: `'SP001'`
4. **Dates** use format `'YYYY-MM-DD'`: `'2025-10-28'`
5. **NULL values** don't use quotes: `WHERE column IS NULL`

---

## 🧪 Testing Your Queries

### Step 1: Open MySQL Workbench
```sql
USE shopgiaydep09102025;
```

### Step 2: Try a Simple Query
```sql
SELECT * FROM khachhang LIMIT 5;
```

### Step 3: Test with WHERE Clause
```sql
SELECT * FROM khachhang WHERE TenDN = 'your_username';
```

### Step 4: Run Complex Queries
Open **`SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql`** and execute!

---

## 🆘 Still Getting Errors?

### Error: Unknown column
- Check column names match your database
- Use backticks for reserved words: `` `Size` ``

### Error: Syntax error near '%s'
- Replace `%s` with actual value
- Use quotes for strings

### Error: No database selected
- Run: `USE shopgiaydep09102025;`

### Error: Foreign key constraint
- Delete child records first
- Or use `ON DELETE CASCADE`

---

## 📞 Quick Help

**Want to see actual data?**
```sql
SELECT * FROM khachhang LIMIT 10;
SELECT * FROM sanpham LIMIT 10;
SELECT * FROM giohang LIMIT 10;
```

**Want to test a specific user?**
```sql
-- Find a real username first
SELECT TenDN FROM khachhang LIMIT 5;

-- Then use it
SELECT * FROM khachhang WHERE TenDN = 'actual_username_from_above';
```

---

**Happy Querying! 🎉**

*Remember: Use `SQL_QUERIES_FOR_MYSQL_WORKBENCH.sql` for ready-to-run queries!*

