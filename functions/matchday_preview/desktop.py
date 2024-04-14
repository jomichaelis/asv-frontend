from PIL import Image, ImageFont, ImageDraw
import os
import io
import requests
from datetime import datetime as dt, timedelta
from firebase_admin import storage


def resize_desktop(image, max_size):
    rs_width, rs_height = image.size
    ratio = min(max_size/rs_width, max_size/rs_height)
    return image.resize((round(rs_width*ratio), round(rs_height*ratio)), Image.LANCZOS)


def create_desktop_image(data):
    bucket = storage.bucket()

    width = 1200
    height = 620

    # Create empty image
    img = Image.new('RGB', size=(width, height))

 	# Background
    image_string = bucket.get_blob(f"matchday-preview-backgrounds/{data['asvID']}/desktop.png").download_as_string()
    background = Image.open(io.BytesIO(image_string))
    img.paste(background)

    # Logos
    home_logo_string = bucket.get_blob(data['homeWappenPath']).download_as_string()
    ĥome_logo = Image.open(io.BytesIO(home_logo_string))
    guest_logo_string = bucket.get_blob(data['guestWappenPath']).download_as_string()
    guest_logo = Image.open(io.BytesIO(guest_logo_string))
    
    home_asv = data['homeIsASV']

    max_size = 310 if home_asv else 230
    home_logo_to_draw = resize_desktop(ĥome_logo, max_size)
    home_x_offset = 60 if home_asv else 0
    home_x = int(310 - home_logo_to_draw.size[0]/2)
    home_y_offset = -30 if home_asv else 0
    home_y = int(215 - home_logo_to_draw.size[1]/2 + home_y_offset)

    max_size = 310 if not home_asv else 230
    guest_logo_to_draw = resize_desktop(guest_logo, max_size)
    guest_x_offset = -30 if not home_asv else 0
    guest_x = int(1200 - 310 - guest_logo_to_draw.size[0]/2)
    guest_y_offset = -30 if not home_asv else 0
    guest_y = int(215 - guest_logo_to_draw.size[1]/2 + guest_y_offset)

    img.paste(home_logo_to_draw, (home_x, home_y), home_logo_to_draw)
    img.paste(guest_logo_to_draw, (guest_x, guest_y), guest_logo_to_draw)

    # Setup Fonts
    font_bebas_neue = bucket.get_blob("fonts/BebasNeue.ttf").download_as_string()
    font_teams = ImageFont.truetype(io.BytesIO(font_bebas_neue), 65)
    font_liga = ImageFont.truetype(io.BytesIO(font_bebas_neue), 42)

    font_readex_pro_semibold = bucket.get_blob("fonts/ReadexPro-SemiBold.ttf").download_as_string()
    font_date = ImageFont.truetype(io.BytesIO(font_readex_pro_semibold), 32)
    
    # Team Names
    draw = ImageDraw.Draw(img)
    text = f"{data['homeName']}  -  {data['guestName']}"
    text_width1 = draw.textlength(text, font=font_teams)
    while text_width1 > (width * 0.92):
        font_teams = ImageFont.truetype(io.BytesIO(font_bebas_neue), font_teams.size - 1)
        text_width1 = draw.textlength(text, font=font_teams)
    draw.text((600-text_width1/2, 380), text, (255, 251, 0), font=font_teams)

    # Date
    date_a_width = draw.textlength(data['date'], font=font_date)
    date_b_width = draw.textlength(data['time'], font=font_date)
    draw.text(((1200-date_a_width)/2, 493), data['date'], (255, 255, 255), font=font_date)
    draw.text(((1200-date_b_width)/2, 540), data['time'], (255, 255, 255), font=font_date)
    
    # Liga
    liga_width = draw.textlength(data['liga'], font=font_liga)
    draw.text(((1200-liga_width)/2+2, 35), data['liga'], (0, 0, 0), font=font_liga)
    draw.text(((1200-liga_width)/2, 34), data['liga'], (255, 251, 0), font=font_liga)

    img_io = io.BytesIO()
    img.save(img_io, format='PNG', quality=100)
    img_io.seek(0)

    img_thumb = img.copy()
    img_thumb.thumbnail((160, 160))
    img_thumb_io = io.BytesIO()
    img_thumb.save(img_thumb_io, 'PNG', quality=100)
    img_thumb_io.seek(0)

    return img_io, img_thumb_io


def create_and_upload_desktop(data):
    img_io, img_thumb_io = create_desktop_image(data)
    bucket = storage.bucket()
    path = f"matchday-preview-images/{data['matchID']}_desktop.png"
    blob = bucket.blob(path)
    blob.upload_from_file(img_io, content_type="image/png")

    path_thumb = f"matchday-preview-images/{data['matchID']}_desktop_thumb.png"
    blob_thumb = bucket.blob(path_thumb)
    blob_thumb.upload_from_file(img_thumb_io, content_type="image/png")

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