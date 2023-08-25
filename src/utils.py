from datetime import datetime
import pytz
import pandas as pd
import plotly.express as px


def convert_utc_to_paris_time(utc_time: str) -> str:
    """
    Convert UTC time to Paris time
    :param utc_time: UTC time
    :return: Paris time
    """
    utc_time = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%f%z")
    tz = pytz.timezone("Europe/Paris")
    return utc_time.astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S")


def adapt_data_for_plotting(df):
    # Convert 'Start Date' to datetime format
    df['Start date'] = pd.to_datetime(df['Start date'])
    # Create 'End Date' column
    df['End date'] = df['Start date'].shift(1)  # Use the start date of the next task as the end date
    tz = pytz.timezone("Europe/Paris")
    df.loc[df.index[0], 'End date'] = datetime.now().astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S")  # For the last task, set the end date as "now"
    return df


def create_timeline_plot(df):
    # Create a plot using Plotly
    fig = px.timeline(df, x_start='Start date', x_end='End date', title='Task Timeline', labels={'Task': 'Tasks'},
                      color='Task')
    fig.update_yaxes(categoryorder='total ascending')
    return fig
