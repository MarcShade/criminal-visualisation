from curl_cffi import requests
import json
import os

BASE_URL = "https://ws-public.interpol.int/notices/v1/red"
TOTAL_FILE = "data/total_cache.json"

class Data:
    data = {}

def get_total():
    response = requests.get(
        BASE_URL,
        params={"page": 1, "resultPerPage": 1},
        impersonate="chrome120"
    )
    if response.status_code != 200:
        return None
    return response.json().get("total")

def load_cached_total():
    if not os.path.exists(TOTAL_FILE):
        return None
    with open(TOTAL_FILE, "r") as file:
        return json.load(file).get("total")

def save_cached_total(total):
    with open(TOTAL_FILE, "w") as file:
        json.dump({"total": total}, file)

def needs_refresh():
    latest_total = get_total()
    cached_total = load_cached_total()
    if latest_total is None:
        return False
    if cached_total != latest_total:
        save_cached_total(latest_total)
        return True
    return False

def fetch_all(per_page=160):
    response = requests.get(
        BASE_URL,
        params={"page": 1, "resultPerPage": per_page},
        impersonate="chrome120"
    )
    if response.status_code != 200:
        return

    json_data = response.json()
    notices = json_data.get("_embedded", {}).get("notices", [])
    total = json_data.get("total", 0)

    for notice in notices:
        entity_id = notice.get("entity_id")
        if entity_id:
            Data.data[entity_id] = notice

    total_pages = (total + per_page - 1) // per_page

    for page in range(2, total_pages + 1):
        response = requests.get(
            BASE_URL,
            params={"page": page, "resultPerPage": per_page},
            impersonate="chrome120"
        )
        if response.status_code != 200:
            break

        json_data = response.json()
        notices = json_data.get("_embedded", {}).get("notices", [])

        for notice in notices:
            entity_id = notice.get("entity_id")
            if entity_id:
                Data.data[entity_id] = notice

print("Running Interpol update check.")
if needs_refresh():
    fetch_all()
