import requests
from datetime import datetime
import pandas as pd
from src.utils import convert_utc_to_paris_time


def write_new_row(new_row: str, notion_token: str):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    data = {
        "parent": {"database_id": "a59dde16b30d468984c60596fe1c895a"},
        "icon": {"emoji": "⏰"},
        "properties": {"Name": {"title": [{"text": {"content": f"{new_row.capitalize()}"}}]}},
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())


def get_table_content(table_id: str, notion_token: str):
    now = datetime.now()
    today_midnight = datetime(now.year, now.month, now.day)
    url = f"https://api.notion.com/v1/databases/{table_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = {
        "filter": {
            "property": "Created time",
            "date": {
                "on_or_after": today_midnight.isoformat(),
            }
        }
    }
    response = requests.post(url, headers=headers, json=data)
    json_response = response.json()
    titles = [result["properties"]["Name"]["title"][0]["plain_text"] for result in json_response["results"]]
    start_dates = [convert_utc_to_paris_time(result["created_time"]) for result in json_response["results"]]
    return pd.DataFrame({"Task": titles, "Start date": start_dates})
