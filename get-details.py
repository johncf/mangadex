import json
import requests

with open("status.json") as f:
    statuses = json.load(f)

r = requests.get(
    "https://api.mangadex.org/manga",
    params={
        "ids[]": list(statuses.keys()),
        "limit": 100,
        "contentRating[]": ["safe", "suggestive"],
        # "includes[]": ["cover_art", "artist", "author"],
    },
)
r.raise_for_status()  # raise exception if unsuccessful
data = r.json()

print("Result:", data["result"])
print("Limit:", data["limit"])
print("Total:", data["total"])

def process_link(key, value):
    if key == "al":
        return f"https://anilist.co/manga/{value}"
    elif key == "ap":
        return f"https://www.anime-planet.com/manga/{value}"
    elif key == "bw":
        return f"https://bookwalker.jp/{value}"
    elif key == "kt":
        return f"https://kitsu.io/manga/{value}"
    elif key == "mal":
        return f"https://myanimelist.net/manga/{value}"
    elif key == "mu":
        return f"https://www.mangaupdates.com/series.html?id={value}"
    elif key == "nu":
        return f"https://www.novelupdates.com/series/{value}"
    else:
        return value

details = {value: [] for value in statuses.values()}
for item in data["data"]:
    attrs = item["attributes"]
    orig_lang = attrs["originalLanguage"]
    allowed_langs = {"en", "de"} | {orig_lang, orig_lang + "-ro"}
    for key in ["isLocked", "lastVolume", "createdAt", "updatedAt", "publicationDemographic", "chapterNumbersResetOnNewVolume", "latestUploadedChapter", "availableTranslatedLanguages"]:
        del attrs[key]
    attrs["description"] = attrs["description"]["en"]
    attrs["links"] = {key: process_link(key, value) for key, value in attrs["links"].items()}
    attrs["tags"] = [tag_details["attributes"]["name"]["en"]
                     for tag_details in attrs["tags"]]
    attrs["altTitles"] = [title for title in attrs["altTitles"]
                          if allowed_langs.intersection(title.keys())]
    details[statuses[item["id"]]].append(item)

with open("details.json", "w") as f:
    json.dump(details, f, indent=4)
