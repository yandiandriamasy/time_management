import streamlit as st
import datetime
from src.connect_to_notion import write_new_row, get_table_content
import pytz
from src.utils import create_timeline_plot, adapt_data_for_plotting
from src.constants import REFERENCE_RUEIL_RER_A
from src.connect_to_prim import get_next_departures, format_prim_response

tz = pytz.timezone('Europe/Berlin')

# Different credentials
NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
TABLE_ID = st.secrets["TABLE_ID"]
PRIM_TOKEN = st.secrets["PRIM_TOKEN"]


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
            f"{st.session_state.activity_start.strftime('%H:%M:%S')} ! "
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
    pages = ["👻Ghost mode", "👀Visualize your timeline", "🚆Go home"]
    page = st.sidebar.radio("Go to", pages)

    if page == "👻Ghost mode":
        page1()
    elif page == "👀Visualize your timeline":
        page2()
    elif page == "🚆Go home":
        page3()


def page1():
    if "activity_in_progress" not in st.session_state:
        st.session_state.activity_in_progress = False

    if "activity_name" not in st.session_state:
        st.session_state.activity_name = ""

    st.title("Ghost mode 👻")
    show_current_activity()
    st.text_input("Activity name 📝:", key="widget", on_change=start_activity)
    df = get_table_content(TABLE_ID, NOTION_TOKEN)
    df = adapt_data_for_plotting(df)
    fig = create_timeline_plot(df)
    # Show plot in Streamlit
    st.plotly_chart(fig)
    st.dataframe(df)

def page2():
    try:
        df = get_table_content(TABLE_ID, NOTION_TOKEN)
        df = adapt_data_for_plotting(df)
        fig = create_timeline_plot(df)
        # Show plot in Streamlit
        st.plotly_chart(fig)
        st.dataframe(df)
    except Exception as e:
        print(e)
        st.header(f"Got error : {e}")
        st.header(
            f"🤭 OMG, no data available as for {datetime.datetime.now(tz).date()}!"
        )


def page3():
    st.title("Go home 🚆")
    st.header("You can go home now, see you tomorrow!")
    st.header("Next departures from Rueil-Malmaison RER A station:")
    st.dataframe(format_prim_response(get_next_departures(REFERENCE_RUEIL_RER_A, PRIM_TOKEN)))
    st.balloons()


if __name__ == "__main__":
    main()
