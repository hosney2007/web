from functools import wraps
from flask import abort
from flask_login import current_user
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app
import uuid
import os

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
        



ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def save_image(file, folder):

    if not file or file.filename == "":
        return None

    # الامتداد
    extension = file.filename.rsplit(".", 1)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file extension.")

    # نوع الملف
    if file.mimetype not in [
        "image/png",
        "image/jpeg",
        "image/webp"
    ]:
        raise ValueError("Invalid image type.")

    # التأكد إنها صورة
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)
    except Exception:
        raise ValueError("Invalid image.")

    # اسم عشوائي
    filename = f"{uuid.uuid4()}.{extension}"

    save_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        folder,
        filename
    )

    file.save(save_path)

    return f"{folder}/{filename}"