import hashlib
import io
import pathlib
import requests

from PIL import Image
from bs4 import BeautifulSoup

from datetime import datetime as dt, timedelta

from firebase_admin import credentials, initialize_app, firestore, storage, _apps
from firebase_functions import firestore_fn, storage_fn, https_fn, options

from matchday_preview.story import create_and_upload_story
from matchday_preview.square import create_and_upload_square


if not _apps:
    cred = credentials.Certificate("./asv-webservices-service-account.json")
    default_app = initialize_app(cred)


def resize(image, resize: bool=True, dim: list=[160, 160]):
    # Resize if needed
    img = image.copy()
    # Extend to square
    width, height = img.size
    if width > height:
        result = Image.new('RGBA', (width, width), (0,0,0,0))
        result.paste(img, (0, (width - height) // 2))
        img = result
    elif height > width:
        result = Image.new('RGBA', (height, height), (0,0,0,0))
        result.paste(img, ((height - width) // 2, 0))
        img = result
    if resize:
        img = img.resize(dim, Image.LANCZOS)
    width, height = img.size
    return img, width, height


@storage_fn.on_object_finalized(region='europe-west3')
def generate_wappen_thumbnail(event: storage_fn.CloudEvent[storage_fn.StorageObjectData]):
    bucket_name = event.data.bucket
    file_path = pathlib.PurePath(event.data.name)
    content_type = event.data.content_type

    metadata = event.data.metadata

    # Exit if this is not triggered inside the "wappen" folder.
    if file_path.parts[0] != "wappen":
        print("File is not in wappen folder - do not generate thumbnail.")
        return

    # Exit if this is triggered on a file that is not an image.
    if not content_type or not content_type.startswith("image/"):
        print(f"This is not an image. ({content_type})")
        return

    # Exit if the image is already a thumbnail.
    if "_thumb_" in file_path.name:
        print("Already a thumbnail.")
        return

    bucket = storage.bucket(bucket_name)

    image_blob = bucket.blob(str(file_path))
    image_bytes = image_blob.download_as_bytes()
    image = Image.open(io.BytesIO(image_bytes))

    sizes = [
        { 'dim': [160, 160], 'name': 'x160', 'resize': True},
        { 'dim': [image.size[0], image.size[1]], 'name': 'square', 'resize': False},
    ]

    for data in sizes:
        dim = data['dim']
        name = data['name']
        should_resize = data['resize']

        img, w, h = resize(image, resize=should_resize, dim=dim)

        thumbnail_io = io.BytesIO()
        img.save(thumbnail_io, format="png")
        filename = f"{file_path.stem}_thumb_{name}.png"
        thumbnail_path = file_path.parent / pathlib.PurePath(filename)
        thumbnail_blob = bucket.blob(str(thumbnail_path))
        thumbnail_blob.upload_from_string(thumbnail_io.getvalue(), content_type="image/png")
        print(f"Thumbnail generated with dimensions {dim}: {thumbnail_path}")
        
        # Write back to database
        db = firestore.client()
        team_ref = db.collection("teams3")
        team_ref.document(metadata.get("teamID")).update(
            { 'wappen_' + name: {
                'filename': filename,
                'url': thumbnail_blob.generate_signed_url(
                    expiration=dt.now() + timedelta(days=365*100),
                    method='GET'
                ),
                'path': str(thumbnail_path),
                'content_type': "image/png",
                'dim': [w, h],
                'size': len(thumbnail_io.getvalue()),
              }
            }
        )

    team_ref.document(metadata.get("teamID")).update(
        { 'status': 'okay' }
    )


@https_fn.on_call(region="europe-west3")
def fetchUpcomingMatch(req: https_fn.CallableRequest):
    bfvURL = req.data["bfvURL"]

    page = requests.get(bfvURL)
    soup = BeautifulSoup(page.content, "html.parser")
    next_match_link = soup.find_all("div", class_="bfv-result-tile")[1].find("a", recursive=False)['href']

    page = requests.get(next_match_link)
    soup = BeautifulSoup(page.content, "html.parser")

    home = soup.find("div", class_="bfv-matchdata-result__team-name--team0").text.strip()
    guest = soup.find("div", class_="bfv-matchdata-result__team-name--team1").text.strip()

    isLive = soup.find("div", class_="bfv-matchdata-result__ticker--live") is not None

    home_team = 1
    if home[-2:] == " 2":
        home_team = 2
        home = home.replace(' 2', '')
    if home[-3:] == " II":
        home_team = 2
        home = home.replace(' II', '')
    if home[-2:] == " 3":
        home_team = 3
        home = home.replace(' 3', '')
    if home[-4:] == " III":
        home_team = 3
        home = home.replace(' III', '')
	
    guest_team = 1
    if guest[-2:] == " 2":
        guest_team = 2
        guest = guest.replace(' 2', '')
    if guest[-3:] == " II":
        guest_team = 2
        guest = guest.replace(' II', '')
    if guest[-2:] == " 3":
        guest_team = 3
        guest = guest.replace(' 3', '')
    if guest[-4:] == " III":
        guest_team = 3
        guest = guest.replace(' III', '')

    # date
    datetime = soup.find("div", class_="bfv-matchday-date-time").findAll("span", recursive=False)
    date_str = datetime[1].text.strip()[:10]
    time_str = datetime[1].text.strip()[-9:-4]
    d = dt(
        day=int(date_str[:2]),
        month=int(date_str[3:5]),
        year=int(date_str[6:]),
        hour=int(time_str[:2]),
        minute=int(time_str[3:])
    )
    d = dt.strptime(f"{date_str}T{time_str}", '%d.%m.%YT%H:%M')
    kickoff = d.isoformat()

    # liga
    liga = soup.find("a", class_="bfv-link-heading").find("h3").text

    return {
        "home": home,
        "guest": guest,
        "home_team": home_team,
        "guest_team": guest_team,
        "date": kickoff,
        "liga": liga,
        "isLive": isLive,
    }


@https_fn.on_call(region="europe-west3")
def create_matchday_preview(req: https_fn.CallableRequest):
    image_square = create_and_upload_square(req.data)
    image_story = create_and_upload_story(req.data)
    return {
        "storyDownloadURL": image_story["downloadURL"],
        "storyPath": image_story["path"],
        "storyThumbDownloadURL": image_story["thumbDownloadURL"],
        "storyThumbPath": image_story["thumbPath"],
        "squareDownloadURL": image_square["downloadURL"],
        "squarePath": image_square["path"],
        "squareThumbDownloadURL": image_square["thumbDownloadURL"],
        "squareThumbPath": image_square["thumbPath"],
    }


@https_fn.on_call(region="europe-west3")
def get_next_matches(req: https_fn.CallableRequest):
    page = requests.get(req.data['teamURL'])
    soup = BeautifulSoup(page.content, "html.parser")
    next_game = soup.find_all("div", class_="bfv-spieltag-eintrag")[0]
    link_to_match = next_game.find("a", class_="bfv-spieltag-eintrag__match-link")['href']

    page = requests.get(link_to_match)
    soup = BeautifulSoup(page.content, "html.parser")

    # date
    datetime_str = soup.find("div", class_="bfv-matchday-date-time").find_all("span")
    date_str, time_str = datetime_str[1].text.strip().split("/")
    date_str = date_str.strip()
    time_str = time_str.strip().replace("Uhr", "").strip()
    d = dt.strptime(f"{date_str}T{time_str}", '%d.%m.%YT%H:%M')
    timestamp = d.timestamp()

    # teams
    team_home = soup.find("div", class_="bfv-matchdata-result__team--team0")
    team_home = team_home.find("a", class_="bfv-matchdata-result__team-link")
    r = team_home['href'].split("/")
    team_home_id = r[-2] + "-" + hashlib.shake_256(r[-1].encode()).hexdigest(2)
    team_guest = soup.find("div", class_="bfv-matchdata-result__team--team1")
    team_guest = team_guest.find("a", class_="bfv-matchdata-result__team-link")
    r = team_guest['href'].split("/")
    team_guest_id = r[-2] + "-" + hashlib.shake_256(r[-1].encode()).hexdigest(2)
    matchday_id = f"{team_home_id}-{team_guest_id}-{round(timestamp)}"

    return {
        'team_home': team_home_id,
        'team_guest': team_guest_id,
        'timestamp': d.isoformat()
    }
