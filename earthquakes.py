# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    # minmagnitude: Minimum seismic magnitude 最小震级
    # maxlatitude, minlatitude, maxlongitude, minlongitude: Define a rectangular area 定义一个矩形区域
    # orderby: time-asc: sort by time in ascending order 按时间升序排序
    # starttime, endtime: Define the time range 定义时间范围

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    with open('earthquake_data.json', 'w') as f:
        json.dump(json.loads(text), f, indent=4)
    data = json.loads(text)
    # See the README file for more information.
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?

    # print("Detailed Earthquake Data Analysis:\n")
    # # 1. Top-level structure
    # print("1. Top-level structure:")
    # for key in data.keys():
    #     value_type = type(data[key]).__name__
    #     print(f"   {key}: {value_type}")

    # # 2. Metadata information
    # print(f"\n2. Metadata (metadata):")
    # if 'metadata' in data:
    #     for key, value in data['metadata'].items():
    #         print(f"   {key}: {value}")

    # # 3. Earthquake features
    # print(f"\n3. Earthquake features (features):")
    # print(f"   Total: {len(data['features'])}")

    # if data['features']:
    #     first_quake = data['features'][0]

    #     print(f"\n   First earthquake structure:")
    #     print(f"   Feature keys: {list(first_quake.keys())}")

    #     print(f"\n   Properties (properties):")
    #     props = first_quake['properties']
    #     for key in list(props.keys())[:8]:  # first 8 properties
    #         print(f"     - {key}: {props[key]}")

    #     print(f"\n   Geometry (geometry):")
    #     geom = first_quake['geometry']
    #     print(f"     type: {geom['type']}")
    #     print(f"     coordinates: {geom['coordinates']}")
    #     print(f"        [Longitude, Latitude, Depth] = {geom['coordinates']}")


    return data


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][1], earthquake['geometry']['coordinates'][0]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    # max_magnitude = 0
    # max_location = []
    
    # for earthquake in data['features']:
    #     mag = get_magnitude(earthquake)
    #     if mag > max_magnitude:
    #         max_magnitude = mag
    #         max_location = [get_location(earthquake)]
    #     elif mag == max_magnitude:
    #         max_location.append(get_location(earthquake))

    max_magnitude = max(get_magnitude(earthquake) for earthquake in data['features'])
    
    max_location = []
    for earthquake in data['features']:
        if get_magnitude(earthquake) == max_magnitude:
            max_location.append(get_location(earthquake))

    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()
# print(data)
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")