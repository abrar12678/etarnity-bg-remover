import os
import uuid
import io
import requests
from PIL import Image
from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "etarnity-background-remover-secret-key"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "static", "processed")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

REMOVE_BG_API_KEY = os.getenv("zgMjaVPfysuLJSjrDzZnTnhW")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def remove_selected_color_background(image: Image.Image, bg_color: str, tolerance: int = 40) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    target_r, target_g, target_b = hex_to_rgb(bg_color)

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]

            if (
                abs(r - target_r) <= tolerance and
                abs(g - target_g) <= tolerance and
                abs(b - target_b) <= tolerance
            ):
                pixels[x, y] = (r, g, b, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    return image


def crop_transparent_whitespace(image: Image.Image) -> Image.Image:
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    bbox = image.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


def save_png(image: Image.Image, output_path: str):
    image = image.convert("RGBA")
    image.save(output_path, "PNG", optimize=True)


def remove_photo_background_with_api(input_path: str, output_path: str):
    with open(input_path, "rb") as image_file:
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": image_file},
            data={"size": "auto"},
            headers={"X-Api-Key": REMOVE_BG_API_KEY},
            timeout=120,
        )

    if response.status_code == requests.codes.ok:
        with open(output_path, "wb") as out:
            out.write(response.content)
    else:
        raise Exception(f"remove.bg API error: {response.status_code} - {response.text}")


@app.route("/", methods=["GET"])
def index():
    result_data = session.pop("result_data", None)
    form_data = session.pop("form_data", {})

    return render_template(
        "index.html",
        **(result_data or {}),
        selected_mode=form_data.get("mode", ""),
        selected_bg_color=form_data.get("bg_color", "#ffffff"),
    )


@app.route("/process-image", methods=["POST"])
def process_image():
    if "image" not in request.files:
        flash("No file uploaded.")
        return redirect(url_for("index"))

    file = request.files["image"]

    if file.filename == "":
        flash("Please choose an image file.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Unsupported file type. Please upload PNG, JPG, JPEG, or WebP.")
        return redirect(url_for("index"))

    mode = request.form.get("mode", "logo").strip()
    bg_color = request.form.get("bg_color", "#ffffff").strip()

    filename = secure_filename(file.filename)
    unique_id = uuid.uuid4().hex
    upload_filename = f"{unique_id}_{filename}"
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], upload_filename)
    file.save(input_path)

    try:
        image = Image.open(input_path)
        original_size = image.size

        output_filename = f"{unique_id}_background_removed.png"
        output_path = os.path.join(app.config["PROCESSED_FOLDER"], output_filename)

        if mode == "logo":
            processed = remove_selected_color_background(image, bg_color=bg_color, tolerance=40)
            processed = crop_transparent_whitespace(processed)
            save_png(processed, output_path)

        elif mode == "photo":
            remove_photo_background_with_api(input_path, output_path)
            processed = Image.open(output_path).convert("RGBA")
            processed = crop_transparent_whitespace(processed)
            save_png(processed, output_path)

        else:
            flash("Invalid mode selected.")
            return redirect(url_for("index"))

        final_image = Image.open(output_path)
        processed_size = final_image.size
        processed_file_size_kb = round(os.path.getsize(output_path) / 1024, 2)

        session["result_data"] = {
            "original_image": url_for("static", filename=f"uploads/{upload_filename}"),
            "processed_image": url_for("static", filename=f"processed/{output_filename}"),
            "download_file": output_filename,
            "original_width": original_size[0],
            "original_height": original_size[1],
            "processed_width": processed_size[0],
            "processed_height": processed_size[1],
            "processed_file_size_kb": processed_file_size_kb,
        }

        session["form_data"] = {
            "mode": mode,
            "bg_color": bg_color,
        }

        return redirect(url_for("index"))

    except Exception as e:
        print("Processing error:", e)
        flash("Something went wrong while processing the image.")
        return redirect(url_for("index"))


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename, as_attachment=True)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)