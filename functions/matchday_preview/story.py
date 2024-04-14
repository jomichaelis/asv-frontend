from PIL import Image, ImageFont, ImageDraw
import os
import io
import requests
from datetime import datetime as dt, timedelta
from firebase_admin import storage


def resize_story(image, max_size):
    rs_width, rs_height = image.size
    ratio = min(max_size/rs_width, max_size/rs_height)
    return image.resize((round(rs_width*ratio), round(rs_height*ratio)), Image.LANCZOS)


def create_story_image(data):
    bucket = storage.bucket()

    width = 1080
    height = 1920

    # Create empty image
    img = Image.new('RGB', size=(width, height))

    # Background
    image_string = bucket.get_blob(f"matchday-preview-backgrounds/{data['asvID']}/story.png").download_as_string()
    background = Image.open(io.BytesIO(image_string))
    img.paste(background)

    # Logos
    home_logo_string = bucket.get_blob(data['homeWappenPath']).download_as_string()
    ĥome_logo = Image.open(io.BytesIO(home_logo_string))
    guest_logo_string = bucket.get_blob(data['guestWappenPath']).download_as_string()
    guest_logo = Image.open(io.BytesIO(guest_logo_string))
	
    home_asv = data['homeIsASV']

    max_size = 550 if home_asv else 400
    home_logo_to_draw = resize_story(ĥome_logo, max_size)
    home_x_offset = 60 if home_asv else 0
    home_x = int(270 - home_logo_to_draw.size[0]/2 + home_x_offset)
    home_y_offset = -100 if home_asv else 50
    home_y = int(680 - home_logo_to_draw.size[1]/2 + home_y_offset)

    max_size = 550 if not home_asv else 400
    guest_logo_to_draw = resize_story(guest_logo, max_size)
    guest_x_offset = -30 if not home_asv else 0
    guest_x = int(1080 - 270 - guest_logo_to_draw.size[0]/2 + guest_x_offset)
    guest_y_offset = -100 if not home_asv else 50
    guest_y = int(680 - guest_logo_to_draw.size[1]/2 + guest_y_offset)

    img.paste(home_logo_to_draw, (home_x, home_y), home_logo_to_draw)
    img.paste(guest_logo_to_draw, (guest_x, guest_y), guest_logo_to_draw)

    # Setup Fonts
    font_bebas_neue = bucket.get_blob("fonts/BebasNeue.ttf").download_as_string()
    font_teams = ImageFont.truetype(io.BytesIO(font_bebas_neue), 105)
    font_liga = ImageFont.truetype(io.BytesIO(font_bebas_neue), 70)

    font_readex_pro_semibold = bucket.get_blob("fonts/ReadexPro-SemiBold.ttf").download_as_string()
    font_date = ImageFont.truetype(io.BytesIO(font_readex_pro_semibold), 62)

    # Team Names
    draw = ImageDraw.Draw(img)
    minus = "-"
    home_team_width1 = draw.textlength(data["homeName"], font=font_teams)
    while home_team_width1 > (width * 0.92):
        font_teams = ImageFont.truetype(io.BytesIO(font_bebas_neue), font_teams.size - 1)
        home_team_width1 = draw.textlength(data["homeName"], font=font_teams)
    guest_team_width1 = draw.textlength(data["guestName"], font=font_teams)
    while guest_team_width1 > (width * 0.92):
        font_teams = ImageFont.truetype(io.BytesIO(font_bebas_neue), font_teams.size - 1)
        guest_team_width1 = draw.textlength(data["guestName"], font=font_teams)
    home_team_width1 = draw.textlength(data["homeName"], font=font_teams)
    minus_width1 = draw.textlength(minus, font=font_teams)
    draw.text((540-(home_team_width1/2), 1100), data["homeName"], (255, 251, 0), font=font_teams)
    draw.text((540-(minus_width1/2), 1200), minus, (255, 251, 0), font=font_teams)
    draw.text((540-(guest_team_width1/2), 1300), data["guestName"], (255, 251, 0), font=font_teams)

    # Date
    date_a_width = draw.textlength(data['date'], font=font_date)
    date_b_width = draw.textlength(data['time'], font=font_date)
    draw.text(((1080-date_a_width)/2, 1600), data['date'], (255, 255, 255), font=font_date)
    draw.text(((1080-date_b_width)/2, 1700), data['time'], (255, 255, 255), font=font_date)

    # Liga
    liga_width = draw.textlength(data['liga'], font=font_liga)
    draw.text(((1080-liga_width)/2+3, 152), data['liga'], (0, 0, 0), font=font_liga)
    draw.text(((1080-liga_width)/2, 150), data['liga'], (255, 251, 0), font=font_liga)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)

    img_thumb = img.copy()
    img_thumb.thumbnail((160, 160))
    img_thumb_io = io.BytesIO()
    img_thumb.save(img_thumb_io, 'PNG', quality=100)
    img_thumb_io.seek(0)

    return img_io, img_thumb_io


def create_and_upload_story(data):
    img_io, img_thumb_io = create_story_image(data)
    bucket = storage.bucket()
    path = f"matchday-preview-images/{data['matchID']}_story.png"
    blob = bucket.blob(path)
    blob.upload_from_file(img_io, content_type="image/png")

    path_thumb = f"matchday-preview-images/{data['matchID']}_story_thumb.png"
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