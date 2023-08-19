import http.client, urllib
import streamlit as st


def notification_andon():
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json", urllib.parse.urlencode({
        "token": st.secrets["PUSHOVER_TOKEN"],
        "title": "You should ask for help!",
        "user": st.secrets["PUSHOVER_USER"],
        "message": "You have been working on your task for more than 30 minutes!",
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
