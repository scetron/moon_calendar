# moon.py

import json
import time
import requests
import datetime
import pandas as pd


# Nasa 'dial-a-moon' API

#  https://svs.gsfc.nasa.gov/api/dialamoon/2024-01-11T06:00

base = "https://svs.gsfc.nasa.gov/api/dialamoon/"


# get all of 2024's moon data
# start by creating a nice date range with pandas
days = pd.date_range(start="2025-01-01", end="2025-12-31").to_pydatetime().tolist()

# create a time delta of 18 hours to get the moon phase at 6pm
hours = datetime.timedelta(hours=18)
# add the time delta to each day
days = [day + hours for day in days]

# create a list to hold the moon phase data for each day
phase = []

# loop through each day and get the moon phase
for day in days:
    # create the url and filename
    url = base + f"{day:%Y-%m-%dT%H:%M}"
    filename = f"images/{day:%Y-%m-%dT%H:%M}.jpg"
    # get the moon phase data from the nasa api
    response = requests.get(url)
    # if the response is good, add the moon phase data to the list
    if response.status_code == 200:
        phase.append(
            {"time": f"{day:%Y-%m-%dT%H:%M}", "phase": response.json()["phase"]}
        )

        # get the moon image (there are several, we're interested in the low res one)
        image = requests.get(response.json()["su_image"]["url"])
        if response.status_code == 200:
            # save the image to the images folder
            with open(filename, mode="wb") as image_file:
                image_file.write(image.content)
            print(f"Got {filename}")
        else:
            print(f"Error w/ {filename}: {response.status_code} {response.text}")
    else:
        print(f"Error w/ {filename}: {response.status_code} {response.text}")
    time.sleep(0.5)


# save the moon phase data to a json file
with open("mooninfo_2025.json", "w") as moonfile:
    json.dump(phase, moonfile, indent=4)
