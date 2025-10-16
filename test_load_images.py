from utils.image_utils import load_image_safely, load_thumbnail_image

# Test load ảnh từ URL thực tế
test_url = "https://static.nike.com/a/images/t_PDP_144_v1/f_auto/1d00f231-689e-4059-b5bd-5daff661b885/custom-nike-metcon-9-shoes-by-you.png"

print("=== Test load_image_safely ===")
try:
    img = load_image_safely(test_url)
    if img:
        print(f"✅ Load ảnh chính thành công: {type(img)}")
    else:
        print("❌ Load ảnh chính thất bại - trả về None")
except Exception as e:
    print(f"❌ Lỗi load ảnh chính: {e}")

print("\n=== Test load_thumbnail_image ===")
try:
    thumb = load_thumbnail_image(test_url)
    if thumb:
        print(f"✅ Load thumbnail thành công: {type(thumb)}")
    else:
        print("❌ Load thumbnail thất bại - trả về None")
except Exception as e:
    print(f"❌ Lỗi load thumbnail: {e}")

# Test với URL khác
test_url2 = "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/60fa302b89ff406fa942b8113a13554f_9366/Giay_Streettalk_trang_JP8277_03_standard.jpg"

print(f"\n=== Test với URL Adidas ===")
try:
    img2 = load_image_safely(test_url2)
    if img2:
        print(f"✅ Load ảnh Adidas thành công: {type(img2)}")
    else:
        print("❌ Load ảnh Adidas thất bại - trả về None")
except Exception as e:
    print(f"❌ Lỗi load ảnh Adidas: {e}")
