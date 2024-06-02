import json
import requests

with open("secrets.json") as f:
    secrets = json.load(f)

#creds = {
#    "grant_type": "password",
#    "username": secrets["username"],
#    "password": secrets["password"],
#    "client_id": secrets["client_id"],
#    "client_secret": secrets["client_secret"],
#}

creds = {
    "grant_type": "refresh_token",
    "refresh_token": secrets["refresh_token"],
    "client_id": secrets["client_id"],
    "client_secret": secrets["client_secret"],
}

r = requests.post(
    "https://auth.mangadex.org/realms/mangadex/protocol/openid-connect/token",
    data=creds,
)
r.raise_for_status()  # raise exception if unsuccessful

tokens = r.json()
secrets["refresh_token"] = tokens["refresh_token"]
secrets["access_token"] = tokens["access_token"]

with open("secrets.json", "w") as f:
    json.dump(secrets, f, indent=4)
