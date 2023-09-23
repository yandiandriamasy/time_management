import streamlit as st
import datetime
from src.connect_to_notion import write_new_row, get_table_content
import pytz
from src.utils import create_timeline_plot, adapt_data_for_plotting
from src.constants import REFERENCE_RUEIL_RER_A
from src.connect_to_prim import get_next_departures, format_prim_response
import asyncio

tz = pytz.timezone("Europe/Berlin")

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
    st.markdown(
        """
    <style>
    .time {
        font-size: 20px;
        font-weight: 300;
        color: #6f737d;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    async def watch(test):
        while True:
            # show_current_activity()
            if st.session_state.activity_name != "":
                total_seconds = (
                    datetime.datetime.now(tz) - st.session_state.activity_start
                ).total_seconds()
                # Calculate hours, minutes, and seconds
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                # Format the result as a string
                formatted_time = f"{int(hours)}H:{int(minutes)}M:{int(seconds)}S"

                test.markdown(
                    f"""
                    🚀 Current task : {st.session_state.activity_name}
                    <p class="time">
                        Time spent : {formatted_time}
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                test.markdown("🚀 Ready to start the day ?")
            await asyncio.sleep(1)

    test = st.empty()
    st.text_input("Activity name 📝:", key="widget", on_change=start_activity)
    asyncio.run(watch(test))


def page2():
    st.title("👀 Visualize your timeline")
    filter_date = st.date_input("😎 What day do you want to visualize ? ")
    df = get_table_content(TABLE_ID, NOTION_TOKEN, filter_date)
    df = adapt_data_for_plotting(df)
    fig = create_timeline_plot(df)
    # Show plot in Streamlit
    st.plotly_chart(fig)
    st.dataframe(df)


def page3():
    st.title("Go home 🚆")
    st.header("You can go home now, see you tomorrow!")
    st.header("Next departures from Rueil-Malmaison RER A station:")
    st.dataframe(
        format_prim_response(get_next_departures(REFERENCE_RUEIL_RER_A, PRIM_TOKEN))
    )
    st.balloons()


if __name__ == "__main__":
    main()
