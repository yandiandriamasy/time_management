import pandas as pd
import json
import requests
import pytz

def format_prim_response(data: dict) -> pd.DataFrame:
    """Format the response from the prim algorithm to a dataframe.

    Args:
        data (dict): The response from the prim algorithm.

    Returns:
        pd.DataFrame: The formatted dataframe.
    """
    # Extracting data
    monitored_visits = data['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']

    # Initialize empty lists to hold data
    destinations = []
    expected_arrival_times = []
    vehicle_journey_names = []

    # Loop through each monitored visit and extract the required information
    for visit in monitored_visits:
        vehicle_journey = visit['MonitoredVehicleJourney']
        destinations.append(vehicle_journey['DestinationName'][0]['value'])
        expected_arrival_times.append(vehicle_journey['MonitoredCall']['ExpectedArrivalTime'])
        vehicle_journey_names.append(vehicle_journey['VehicleJourneyName'][0]['value'])

    # Create a DataFrame
    df = pd.DataFrame({
        'Destination': destinations,
        'ExpectedArrivalTime': expected_arrival_times,
        'VehicleJourneyName': vehicle_journey_names
    })

    df['ExpectedArrivalTime'] = pd.to_datetime(df['ExpectedArrivalTime'])
    tz = pytz.timezone("Europe/Paris")
    df['ExpectedArrivalTime'] = df['ExpectedArrivalTime'].dt.astimezone(tz).strftime('%H:%M:%S')
    return df


def get_next_departures(monitoring_ref: str, api_key: str) -> str:
    url = f"https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring?MonitoringRef={monitoring_ref}"
    payload = {}
    headers = {
        'accept': 'application/json',
        'apiKey': api_key,
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()
