import mysql.connector

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='tungds270105',
        database='shopgiaydep'
    )
    cursor = conn.cursor()
    
    # Kiểm tra dữ liệu ảnh
    cursor.execute('SELECT MaSP, URLAnh FROM url_sp LIMIT 5')
    images = cursor.fetchall()
    print('=== Dữ liệu ảnh trong database ===')
    for ma_sp, url in images:
        print(f'SP: {ma_sp}, URL: {url}')
    
    # Kiểm tra một sản phẩm cụ thể
    cursor.execute('SELECT MaSP FROM sanpham LIMIT 1')
    first_product = cursor.fetchone()
    if first_product:
        ma_sp = first_product[0]
        cursor.execute('SELECT URLAnh FROM url_sp WHERE MaSP = %s', (ma_sp,))
        product_images = cursor.fetchall()
        print(f'\n=== Ảnh của sản phẩm {ma_sp} ===')
        for img in product_images:
            print(f'URL: {img[0]}')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'Lỗi: {e}')
