import requests
import streamlit as st

def write_new_row(new_row):
    url = "https://api.notion.com/v1/pages"

    # Your Notion API credentials
    NOTION_TOKEN = st.secrets["NOTION_TOKEN"]

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
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