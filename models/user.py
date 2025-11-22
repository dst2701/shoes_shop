"""
User management utilities
"""
import mysql.connector
from config.database import get_db_connection

def generate_customer_id(cursor):
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)) FROM khachhang WHERE MaKH LIKE 'KH%'"
    )
    result = cursor.fetchone()
    next_number = ((result[0] or 0) + 1) if result else 1
    return f"KH{next_number:03d}"

def generate_staff_id(cursor):
    cursor.execute(
        "SELECT MAX(CAST(SUBSTRING(MaNV, 3) AS UNSIGNED)) FROM nhanvien WHERE MaNV LIKE 'NV%'"
    )
    result = cursor.fetchone()
    next_number = ((result[0] or 0) + 1) if result and result[0] is not None else 1
    return f"NV{next_number:03d}"

def authenticate_user(username, password):
    """
    Xác thực user và trả về role
    Returns: 'buyer', 'seller', hoặc None nếu sai thông tin
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check customer
        cursor.execute(
            "SELECT MaKH FROM khachhang WHERE TenDN=%s AND MatKhau=%s",
            (username, password)
        )
        if cursor.fetchone():
            return "buyer"

        # Check staff
        cursor.execute(
            "SELECT MaNV FROM nhanvien WHERE TenDN=%s AND MatKhau=%s",
            (username, password)
        )
        if cursor.fetchone():
            return "seller"

        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def register_user(username, password, role, phone, address, full_name):
    """
    Đăng ký user mới
    Returns: True nếu thành công, raise Exception nếu có lỗi
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check existing username
        cursor.execute("SELECT 1 FROM khachhang WHERE TenDN=%s", (username,))
        if cursor.fetchone():
            raise ValueError("Tên đăng nhập đã tồn tại trong danh sách khách hàng!")

        cursor.execute("SELECT 1 FROM nhanvien WHERE TenDN=%s", (username,))
        if cursor.fetchone():
            raise ValueError("Tên đăng nhập đã tồn tại trong danh sách nhân viên!")

        if role == "buyer":
            cursor.execute("SELECT 1 FROM khachhang WHERE SDT=%s", (phone,))
            if cursor.fetchone():
                raise ValueError("Số điện thoại đã được sử dụng!")

            customer_id = generate_customer_id(cursor)
            cursor.execute(
                """
                INSERT INTO khachhang (MaKH, TenKH, SDT, DiaChi, TenDN, MatKhau)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (customer_id, full_name, phone, address if address else None, username, password)
            )

            # Không tự động tạo đơn hàng nữa - đơn hàng sẽ được tạo khi khách hàng nhấn "Tạo đơn hàng"
        else:
            staff_id = generate_staff_id(cursor)
            cursor.execute(
                """
                INSERT INTO nhanvien (MaNV, TenNV, TenDN, MatKhau)
                VALUES (%s, %s, %s, %s)
                """,
                (staff_id, full_name, username, password)
            )

        conn.commit()
        return True

    except mysql.connector.IntegrityError as err:
        raise ValueError(f"Không thể đăng ký do trùng dữ liệu: {str(err)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
