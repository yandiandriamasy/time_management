import streamlit as st
import datetime
from src.connect_to_notion import write_new_row, get_table_content
import pytz
from src.utils import create_timeline_plot

tz = pytz.timezone('Europe/Berlin')

# Your Notion API credentials
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
TABLE_ID = st.secrets["TABLE_ID"]


def get_current_hour() -> str:
    current_time = datetime.datetime.now(tz)
    return f"{current_time.hour}:{current_time.minute}"


def start_activity():
    st.session_state.activity_in_progress = True
    st.session_state.activity_name = st.session_state.widget
    st.session_state.activity_start = datetime.datetime.now(tz)
    with open(
            f"{st.session_state.activity_start.date()}.txt", "a", encoding="utf-8"
    ) as f:
        f.write(
            f'{st.session_state.activity_start.strftime("%H:%M:%S")}, "Start", {st.session_state.activity_name} \n'
        )
    write_new_row(st.session_state.activity_name, NOTION_TOKEN)


def show_current_activity():
    if st.session_state.activity_name != "":
        st.write(
            f"🚀 {st.session_state.activity_name} started at "
            f"{st.session_state.activity_start.strftime('%d/%m/%Y, %H:%M:%S')} ! "
        )
        time_elapsed = datetime.datetime.now(tz) - st.session_state.activity_start
        st.write(f"You have been working on this task for: {time_elapsed}")


def end_activity():
    with open(
            f"{st.session_state.activity_start.date()}.txt", "a", encoding="utf-8"
    ) as f:
        f.write(
            f'{datetime.datetime.now(tz).strftime("%H:%M:%S")}, "End", {st.session_state.activity_name} \n'
        )
    st.session_state.activity_in_progress = False
    st.write(
        f"✨ {st.session_state.activity_name} ended at {datetime.datetime.now(tz).strftime('%d/%m/%Y, %H:%M:%S')} ! "
    )
    st.session_state.activity_name = ""
    st.balloons()


# Streamlit app
def main():
    st.sidebar.title("🗄 Menu")
    pages = ["👻Ghost mode", "👀 Visualize your timeline"]
    page = st.sidebar.radio("Go to", pages)

    if page == "👻Ghost mode":
        page1()
    elif page == "👀 Visualize your timeline":
        page2()


def page1():
    if "activity_in_progress" not in st.session_state:
        st.session_state.activity_in_progress = False

    if "activity_name" not in st.session_state:
        st.session_state.activity_name = ""

    st.title("Ghost mode 👻")
    show_current_activity()
    st.text_input("Activity name 📝:", key="widget", on_change=start_activity)

    if st.session_state.activity_in_progress:
        print(5)
        # if st.button("Stop activity !"):
        #   end_activity()


def page2():
    try:
        df = get_table_content(TABLE_ID, NOTION_TOKEN)
        fig = create_timeline_plot(df)
        # Show plot in Streamlit
        st.plotly_chart(fig)
    except Exception as e:
        print(e)
        st.header(
            f"🤭 OMG, no data available as for {datetime.datetime.now(tz).date()}!"
        )


if __name__ == "__main__":
    main()
