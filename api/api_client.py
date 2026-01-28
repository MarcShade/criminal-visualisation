from curl_cffi import requests
import json
import os
import pprint

class Data:
    _data = None
    DATA_FILE = "api/data_file.json"
    BASE_URL = "https://ws-public.interpol.int/notices/v1/red"
    TOTAL_FILE = "api/total_cache.json"

    @classmethod
    def get_data(cls):
        if cls._data is None:
            try:
                with open(cls.DATA_FILE, "r", encoding="utf-8") as f:
                    cls._data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                cls._data = {}
                with open(cls.DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(cls._data, f)
        return cls._data

    @classmethod
    def get_total(cls):
        response = requests.get(
            cls.BASE_URL,
            params={"page": 1, "resultPerPage": 1},
            impersonate="chrome120"
        )
        if response.status_code != 200:
            return None
        return response.json().get("total")
    
    @classmethod
    def load_cached_total(cls):
        if not os.path.exists(cls.TOTAL_FILE):
            return None
        with open(cls.TOTAL_FILE, "r") as f:
            return json.load(f).get("total")

    @classmethod
    def save_cached_total(cls, total):
        with open(cls.TOTAL_FILE, "w") as f:
            json.dump({"total": total}, f)

    @classmethod
    def save_data(cls):
        with open(cls.DATA_FILE, "w") as f:
            json.dump(Data.data, f, indent=2)

    @classmethod
    def needs_refresh(cls):
        latest_total = cls.get_total()
        cached_total = cls.load_cached_total()

        if latest_total is None:
            return False

        if cached_total != latest_total:
            cls.save_cached_total(latest_total)
            return True

        return False

    @classmethod
    def fetch_all_notices(cls, per_page=160):
        notices = []

        response = requests.get(
            cls.BASE_URL,
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
                cls.BASE_URL,
                params={"page": page, "resultPerPage": per_page},
                impersonate="chrome120"
            )
            if response.status_code != 200:
                continue

            json_data = response.json()
            notices.extend(json_data.get("_embedded", {}).get("notices", []))

        return notices

    @classmethod
    def fetch_notice_details(cls, notices):
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
            cls._data.append(notice_details)

            pprint.pprint({
                "name": notice_details.get("forename"),
                "entity_id": notice_details.get("entity_id"),
                "link": link
            })
        print(f"Dead requests: {dead_requests}")
