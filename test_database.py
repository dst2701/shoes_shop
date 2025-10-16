"""
Test kết nối database và kiểm tra dữ liệu
"""
import mysql.connector

def test_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="tungds270105",
            database="shopgiaydep"
        )
        cursor = conn.cursor()

        print("=== TEST KẾT NỐI DATABASE ===")
        print("✅ Kết nối thành công!")

        # Test bảng sanpham
        print("\n=== TEST BẢNG SANPHAM ===")
        cursor.execute("SELECT COUNT(*) FROM sanpham")
        count = cursor.fetchone()[0]
        print(f"Số sản phẩm: {count}")

        cursor.execute("SELECT MaSP, TenSP, Gia FROM sanpham LIMIT 3")
        products = cursor.fetchall()
        for ma_sp, ten_sp, gia in products:
            print(f"- {ma_sp}: {ten_sp} - {gia:,.0f} VNĐ")

        # Test bảng thuonghieu
        print("\n=== TEST BẢNG THUONGHIEU ===")
        cursor.execute("SELECT COUNT(*) FROM thuonghieu")
        count = cursor.fetchone()[0]
        print(f"Số thương hiệu: {count}")

        cursor.execute("SELECT MaTH, TenTH FROM thuonghieu")
        brands = cursor.fetchall()
        for ma_th, ten_th in brands:
            print(f"- {ma_th}: {ten_th}")

        # Test JOIN sanpham với thuonghieu
        print("\n=== TEST JOIN SANPHAM-THUONGHIEU ===")
        cursor.execute("""
            SELECT sp.MaSP, sp.TenSP, sp.Gia, th.TenTH
            FROM sanpham sp 
            LEFT JOIN thuonghieu th ON sp.MaTH = th.MaTH
            ORDER BY sp.TenSP
        """)
        products_with_brands = cursor.fetchall()
        for ma_sp, ten_sp, gia, ten_th in products_with_brands:
            print(f"- {ma_sp}: {ten_sp} ({ten_th}) - {gia:,.0f} VNĐ")

        # Test bảng url_sp
        print("\n=== TEST BẢNG URL_SP ===")
        cursor.execute("SELECT COUNT(*) FROM url_sp")
        count = cursor.fetchone()[0]
        print(f"Số URL ảnh: {count}")

        cursor.execute("SELECT MaSP, URLAnh FROM url_sp LIMIT 5")
        images = cursor.fetchall()
        for ma_sp, url in images:
            print(f"- {ma_sp}: {url[:50]}...")

        print("\n✅ TẤT CẢ BẢNG HOẠT ĐỘNG BÌNH THƯỜNG!")

    except Exception as e:
        print(f"❌ LỖI: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_database()
