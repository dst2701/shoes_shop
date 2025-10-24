"""
Image loading utilities
"""
from PIL import Image, ImageTk
import urllib.request
import io
import os
import shutil
import uuid
from config.database import BASE_DIR, LOCAL_IMAGE_DIR

def load_image_safely(path_or_url):
    """Load ảnh an toàn với fallback"""
    source = (path_or_url or "").strip()
    if not source:
        return None

    image = None
    try:
        if source.lower().startswith(("http://", "https://")):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(source, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() != 200:
                    return None
                raw_data = response.read()
            with Image.open(io.BytesIO(raw_data)) as img:
                image = img.copy()
        else:
            candidate_paths = []
            if os.path.isabs(source):
                candidate_paths.append(source)
            else:
                candidate_paths.append(os.path.join(LOCAL_IMAGE_DIR, source))
                candidate_paths.append(os.path.join(BASE_DIR, source))

            for file_path in candidate_paths:
                if os.path.isfile(file_path):
                    with Image.open(file_path) as img:
                        image = img.copy()
                    break

            if image is None:
                return None

        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')

        image = image.resize((600, 600), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    except Exception as e:
        print(f"Lỗi tải ảnh từ {source}: {e}")
        return None

def load_thumbnail_image(path_or_url):
    """Load ảnh thumbnail kích thước 70x70"""
    source = (path_or_url or "").strip()
    if not source:
        return None

    image = None
    try:
        if source.lower().startswith(("http://", "https://")):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(source, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() != 200:
                    return None
                raw_data = response.read()
            with Image.open(io.BytesIO(raw_data)) as img:
                image = img.copy()
        else:
            candidate_paths = []
            if os.path.isabs(source):
                candidate_paths.append(source)
            else:
                candidate_paths.append(os.path.join(LOCAL_IMAGE_DIR, source))
                candidate_paths.append(os.path.join(BASE_DIR, source))

            for file_path in candidate_paths:
                if os.path.isfile(file_path):
                    with Image.open(file_path) as img:
                        image = img.copy()
                    break

            if image is None:
                return None

        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')

        # Resize to thumbnail size
        image = image.resize((70, 70), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    except Exception as e:
        print(f"Lỗi tải thumbnail từ {source}: {e}")
        return None

def ensure_local_image_dir():
    """Ensure the local image directory exists"""
    os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)

def generate_unique_filename(original_path):
    """Generate a unique filename with the same extension as the original"""
    ext = os.path.splitext(original_path)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"

def save_uploaded_image(source_path):
    """
    Copy the selected file to LOCAL_IMAGE_DIR with a unique filename.
    Returns the stored filename (relative). Raises exception on error.
    """
    ensure_local_image_dir()
    filename = generate_unique_filename(source_path)
    dest = os.path.join(LOCAL_IMAGE_DIR, filename)
    shutil.copy2(source_path, dest)
    return filename  # This will be stored in url_sp.URLAnh

def insert_uploaded_image_to_db(db_conn, ma_sp, stored_filename):
    """
    Insert a new row into url_sp table.
    db_conn is a database connection with cursor() and commit().
    """
    sql = "INSERT INTO `url_sp` (`MaSP`, `URLAnh`) VALUES (%s, %s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(sql, (ma_sp, stored_filename))
        db_conn.commit()
        return True
    except Exception as e:
        print(f"Error inserting image record: {e}")
        return False
    finally:
        cursor.close()

