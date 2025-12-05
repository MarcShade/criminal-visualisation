from curl_cffi import requests
import json
import os
import pprint

BASE_URL = "https://ws-public.interpol.int/notices/v1/red"
TOTAL_FILE = "api_client/total_cache.json"
DATA_FILE = "api_client/data_file.json"

class Data:
    data = []

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
    with open(TOTAL_FILE, "r") as f:
        return json.load(f).get("total")

def save_cached_total(total):
    with open(TOTAL_FILE, "w") as f:
        json.dump({"total": total}, f)

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(Data.data, f, indent=2)

def needs_refresh():
    latest_total = get_total()
    cached_total = load_cached_total()

    if latest_total is None:
        return False

    if cached_total != latest_total:
        save_cached_total(latest_total)
        return True

    return False

def fetch_all_notices(per_page=160):
    notices = []

    response = requests.get(
        BASE_URL,
        params={"page": 1, "resultPerPage": per_page},
        impersonate="chrome120"
    )
    if response.status_code != 200:
        raise RuntimeError("Cannot fetch first page")

    json_data = response.json()
    notices.extend(json_data.get("_embedded", {}).get("notices", []))
    total = json_data.get("total", 0)

    total_pages = (total + per_page - 1) // per_page

    for page in range(2, total_pages + 1):
        response = requests.get(
            BASE_URL,
            params={"page": page, "resultPerPage": per_page},
            impersonate="chrome120"
        )
        if response.status_code != 200:
            continue

        json_data = response.json()
        notices.extend(json_data.get("_embedded", {}).get("notices", []))

    return notices

def fetch_notice_details(notices):
    dead_requests = 0
    for notice in notices:
        link = notice.get("_links", {}).get("self", {}).get("href")
        if not link:
            continue

        response = requests.get(link, impersonate="chrome120")
        if response.status_code != 200:
            dead_requests += 1
            continue

        notice_details = response.json()
        Data.data.append(notice_details)

        pprint.pprint({
            "name": notice_details.get("forename"),
            "entity_id": notice_details.get("entity_id"),
            "link": link
        })
    print(f"Dead requests: {dead_requests}")

if needs_refresh():
    notices = fetch_all_notices()
    fetch_notice_details(notices)
    save_data()
