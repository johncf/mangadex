import json
import requests

with open("secrets.json") as f:
    secrets = json.load(f)

session_token = secrets["access_token"]

r = requests.get(
    "https://api.mangadex.org/manga/status",
    headers={
        "Authorization": f"Bearer {session_token}"
    },
)
r.raise_for_status()  # raise exception if unsuccessful
data = r.json()
print("Result:", data["result"])

with open("status.json", "w") as f:
    json.dump(data["statuses"], f, indent=4)
