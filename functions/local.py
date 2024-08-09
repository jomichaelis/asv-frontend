import hashlib
import io
import os
import pathlib
import requests
import typing

from PIL import Image
from bs4 import BeautifulSoup

from datetime import datetime as dt, timedelta

from firebase_admin import credentials, initialize_app, firestore

# LOCAL ONLY
def create_teams(bfv_liga_url):
    page = requests.get(bfv_liga_url)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("li", {"data-nav-item": "Tabelle"})
    rows = table.find("table").find_all("tr", class_="bfv-table-entry--data")
    for row in rows:
        team = row.find("td", class_="bfv-table-entry__cell--team").find("a")
        team_name = team.text.strip()
        team_link = team['href']
        teams_ref = db.collection("teams3")
        r = team_link.split("/")
        id = r[-2] + "-" + hashlib.shake_256(r[-1].encode()).hexdigest(2)
        print(team_name, id)
        _ = teams_ref.document(id).set({
            'name': team_name,
            'isASV': False,
            'long1': "",
            'long2': "",
            'wappen_square': None,
            'wappen_x160': None,
            'teamURL': team_link,
            'teamID': "-".join(r[-2:]),
        })


script_path = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(script_path, "asv-webservices-service-account.json")

cred = credentials.Certificate(cred_path)
initialize_app(cred)
db = firestore.client()

bfv_liga_url = "https://www.bfv.de/wettbewerbe/meisterschaften/a-klasse-1/02Q4F0604O000006VS5489B4VTH92TNV-G"

create_teams(bfv_liga_url=bfv_liga_url)
