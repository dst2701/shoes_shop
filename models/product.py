"""
Model xử lý dữ liệu sản phẩm
"""
from config.database import get_db_connection

def generate_product_id(cursor):
    """Tạo mã sản phẩm tự động - kiểm tra cả bảng sanpham và cthoadon để tránh trùng lặp"""
    # Lấy mã lớn nhất từ bảng sanpham
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM sanpham WHERE MaSP LIKE 'SP%'"
    )
    result_sanpham = cursor.fetchone()
    max_sanpham = (result_sanpham[0] or 0) if result_sanpham and result_sanpham[0] is not None else 0

    # Lấy mã lớn nhất từ bảng cthoadon (để tránh tái sử dụng mã đã bị xoá)
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaSP, 3) AS UNSIGNED)) FROM cthoadon WHERE MaSP LIKE 'SP%'"
    )
    result_cthoadon = cursor.fetchone()
    max_cthoadon = (result_cthoadon[0] or 0) if result_cthoadon and result_cthoadon[0] is not None else 0

    # Lấy số lớn nhất trong cả 2 bảng và tăng thêm 1
    next_number = max(max_sanpham, max_cthoadon) + 1
    return f"SP{next_number:03d}"

def generate_brand_id(cursor):
    """Tạo mã thương hiệu tự động"""
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaTH, 3) AS UNSIGNED)) FROM thuonghieu WHERE MaTH LIKE 'TH%'"
    )
    result = cursor.fetchone()
    next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
    return f"TH{next_number:03d}"

def get_or_create_brand(cursor, brand_name):
    """Lấy mã thương hiệu hoặc tạo mới nếu chưa tồn tại"""
    # Kiểm tra thương hiệu đã tồn tại
    cursor.execute("SELECT MaTH FROM thuonghieu WHERE TenTH = %s", (brand_name,))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        # Tạo thương hiệu mới
        brand_id = generate_brand_id(cursor)
        cursor.execute(
            "INSERT INTO thuonghieu (MaTH, TenTH, MoTa) VALUES (%s, %s, %s)",
            (brand_id, brand_name, f"Thương hiệu {brand_name}")
        )
        return brand_id

def get_all_products():
    """Lấy tất cả sản phẩm từ database"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MaSP, TenSP, Gia, MoTa
            FROM sanpham
            ORDER BY TenSP
        """)
        
        return cursor.fetchall()

    except Exception as e:
        print(f"Lỗi lấy dữ liệu sản phẩm: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_product_images(ma_sp):
    """Lấy tất cả ảnh của một sản phẩm"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT URLAnh
            FROM url_sp
            WHERE MaSP = %s
            ORDER BY URLAnh
        """, (ma_sp,))

        result = cursor.fetchall()
        return [row[0] for row in result] if result else []

    except Exception as e:
        print(f"Lỗi lấy ảnh sản phẩm {ma_sp}: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_product_by_id(ma_sp):
    """Lấy thông tin chi tiết một sản phẩm"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MaSP, TenSP, Gia, MoTa
            FROM sanpham
            WHERE MaSP = %s
        """, (ma_sp,))

        return cursor.fetchone()

    except Exception as e:
        print(f"Lỗi lấy sản phẩm {ma_sp}: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_product(name, price, description, brand_name, quantity, image_urls):
    """Thêm sản phẩm mới vào database"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tạo hoặc lấy mã thương hiệu
        brand_id = get_or_create_brand(cursor, brand_name)

        # Tạo mã sản phẩm tự động
        product_id = generate_product_id(cursor)

        # Thêm sản phẩm
        cursor.execute("""
            INSERT INTO sanpham (MaSP, TenSP, Gia, MoTa, MaTH, SoLuong)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (product_id, name, price, description, brand_id, quantity))

        # Thêm URL ảnh nếu có
        if image_urls:
            for url in image_urls:
                if url.strip():  # Chỉ thêm URL không rỗng
                    cursor.execute("""
                        INSERT INTO url_sp (MaSP, URLAnh) VALUES (%s, %s)
                    """, (product_id, url.strip()))

        conn.commit()
        return product_id

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Lỗi thêm sản phẩm: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def delete_product(ma_sp):
    """Xóa sản phẩm khỏi database"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Xóa URL ảnh trước
        cursor.execute("DELETE FROM url_sp WHERE MaSP = %s", (ma_sp,))

        # Xóa sản phẩm
        cursor.execute("DELETE FROM sanpham WHERE MaSP = %s", (ma_sp,))

        conn.commit()
        return cursor.rowcount > 0  # True nếu có sản phẩm bị xóa

    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Lỗi xóa sản phẩm: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_all_brands():
    """Lấy tất cả thương hiệu"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MaTH, TenTH FROM thuonghieu ORDER BY TenTH")
        return cursor.fetchall()

    except Exception as e:
        print(f"Lỗi lấy danh sách thương hiệu: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def search_products(search_term="", brand_filter="", price_filter=""):
    """Tìm kiếm và lọc sản phẩm"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT s.MaSP, s.TenSP, s.Gia, s.MoTa, t.TenTH
            FROM sanpham s
            JOIN thuonghieu t ON s.MaTH = t.MaTH
            WHERE 1=1
        """
        params = []

        # Tìm kiếm theo tên
        if search_term:
            query += " AND s.TenSP LIKE %s"
            params.append(f"%{search_term}%")

        # Lọc theo thương hiệu
        if brand_filter:
            query += " AND t.TenTH = %s"
            params.append(brand_filter)

        # Sắp xếp theo giá
        if price_filter == "low_to_high":
            query += " ORDER BY s.Gia ASC"
        elif price_filter == "high_to_low":
            query += " ORDER BY s.Gia DESC"
        else:
            query += " ORDER BY s.TenSP"

        cursor.execute(query, params)
        return cursor.fetchall()

    except Exception as e:
        print(f"Lỗi tìm kiếm sản phẩm: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
