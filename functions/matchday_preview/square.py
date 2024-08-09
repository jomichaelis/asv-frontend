from PIL import Image, ImageFont, ImageDraw
import os
import io
import requests
from datetime import datetime as dt, timedelta
from firebase_admin import storage

# script_dir = os.path.dirname(os.path.abspath(__file__))

def resize_square(image, max_size):
    rs_width, rs_height = image.size
    ratio = min(max_size/rs_width, max_size/rs_height)
    return image.resize((round(rs_width*ratio), round(rs_height*ratio)), Image.LANCZOS)


def create_square_image(data):
    bucket = storage.bucket()

    width  = 1080
    height = 1080

    # Create empty image
    img = Image.new('RGB', size=(width, height))

    # Background
    image_string = bucket.get_blob(f"matchday-preview-backgrounds/{data['asvID']}/square.png").download_as_string()
    # with open(os.path.join(script_dir, "square.png"), "rb") as f:
    #     image_string = f.read()
    background = Image.open(io.BytesIO(image_string))
    img.paste(background)

    # Logos
    home_logo_string = bucket.get_blob(data['homeWappenPath']).download_as_string()
    # home_logo_string = open(os.path.join(script_dir, "asv_moehrendorf.png"), "rb").read()
    home_logo = Image.open(io.BytesIO(home_logo_string))
    guest_logo_string = bucket.get_blob(data['guestWappenPath']).download_as_string()
    # guest_logo_string = open(os.path.join(script_dir, "tsv_frauenaurach.png"), "rb").read()
    guest_logo = Image.open(io.BytesIO(guest_logo_string))

    max_size = 240
    home_logo_to_draw = resize_square(home_logo, max_size)
    home_x  = int(540 - 60 - home_logo_to_draw.size[0])
    home_y  = int(610)

    max_size = 240
    guest_logo_to_draw = resize_square(guest_logo, max_size)
    guest_x = int(540 + 60)
    guest_y = int(610)

    img.paste(home_logo_to_draw, (home_x, home_y), home_logo_to_draw)
    img.paste(guest_logo_to_draw, (guest_x, guest_y), guest_logo_to_draw)

    # Setup Fonts
    font_anton = bucket.get_blob("fonts/Anton-Regular.ttf").download_as_string()
    # font_date = ImageFont.truetype(os.path.join(os.path.dirname(script_dir), "fonts/Anton-Regular.ttf"), 61)
    font_date = ImageFont.truetype(io.BytesIO(font_anton), 61)

    # Team Names
    draw = ImageDraw.Draw(img)

    # Date
    date_str = data['day'].upper() + ", " + data['date'] + " | " + data['time'] + " UHR"
    date_width = draw.textlength(date_str, font=font_date)
    draw.text((540-(date_width/2), 856), date_str, (0,0,0), font=font_date)
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)

    img_thumb = img.copy()
    img_thumb.thumbnail((160, 160))
    img_thumb_io = io.BytesIO()
    img_thumb.save(img_thumb_io, 'PNG', quality=100)
    img_thumb_io.seek(0)

    return img_io, img_thumb_io


def create_and_upload_square(data):
    img_io, img_thumb_io = create_square_image(data)
    bucket = storage.bucket()
    path = f"matchday-preview-images/{data['matchID']}_square.png"
    blob = bucket.blob(path)
    blob.upload_from_file(img_io, content_type="application/octet-stream")

    path_thumb = f"matchday-preview-images/{data['matchID']}_square_thumb.png"
    blob_thumb = bucket.blob(path_thumb)
    blob_thumb.upload_from_file(img_thumb_io, content_type="application/octet-stream")

    return {
        "downloadURL": blob.generate_signed_url(
            expiration=dt.now() + timedelta(days=365*100),
            method='GET'
        ),
        "path": path,
        "thumbDownloadURL": blob_thumb.generate_signed_url(
            expiration=dt.now() + timedelta(days=365*100),
            method='GET'
        ),
        "thumbPath": path_thumb
    }


# data = {
#     "asvID": "asv-moehrendorf-d7fc",
#     "homeWappenPath": "http://127.0.0.1:9199/v0/b/asv-webservices.appspot.com/o/wappen%2F2024-04-11-23-30-26_asv-logo.png?alt=media&token=e1e6b36c-718e-4f42-9573-8c60a9653c7d",
#     "guestWappenPath": "http://127.0.0.1:9199/v0/b/asv-webservices.appspot.com/o/wappen%2F2024-04-12-00-38-35_frauenaurach.png?alt=media&token=164b51c4-e60a-4e79-9761-f5199557fddf",
#     "day": "Sonntag",
#     "date": "11.04.2024",
#     "time": "23:30",
# }

# img_io, img_thumb_io = create_square_image(data)
# img_io.seek(0)
# img_thumb_io.seek(0)
# with open(os.path.join(script_dir, "square_image.png"), "wb") as f:
#     f.write(img_io.read())
# with open(os.path.join(script_dir, "square_thumb.png"), "wb") as f:
#     f.write(img_thumb_io.read())
