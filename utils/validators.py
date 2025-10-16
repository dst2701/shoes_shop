"""
Functions để validate dữ liệu đầu vào
"""

def validate_registration_data(username, password, confirm_password, role, phone, full_name):
    """Validate dữ liệu đăng ký"""
    errors = []

    # Kiểm tra thông tin bắt buộc
    if not all([username, password, confirm_password, role, phone, full_name]):
        errors.append("Vui lòng nhập đầy đủ thông tin bắt buộc!")
        return errors

    # Kiểm tra vai trò
    if role not in ("buyer", "seller"):
        errors.append("Vui lòng chọn vai trò hợp lệ!")

    # Kiểm tra mật khẩu
    if password != confirm_password:
        errors.append("Mật khẩu xác nhận không khớp!")

    if len(password) < 6:
        errors.append("Mật khẩu phải có ít nhất 6 ký tự!")

    # Kiểm tra số điện thoại
    if not phone.isdigit() or len(phone) not in (10, 11):
        errors.append("Số điện thoại phải gồm 10 hoặc 11 chữ số!")

    return errors

def validate_login_data(username, password):
    """Validate dữ liệu đăng nhập"""
    if not username or not password:
        return "Vui lòng nhập đầy đủ thông tin!"
    return None
