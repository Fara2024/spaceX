# -*- coding: utf-8 -*-
"""Data_collection.API_week1_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1snfzFIM7RqCXn_-vL7peISF5qUTU6jS7

'''Data Collection API.week1_1.py

# Predicting SpaceX Falcon 9 First Stage Landing: A Journey into Machine Learning and Artificial Intelligence



Collecting the data

In this project, you will embark on an exciting journey into the world of machine learning and artificial intelligence as a data scientist, tasked with a crucial mission: predicting the landing success of the SpaceX Falcon 9 first stage. SpaceX has revolutionized the aerospace industry with its ability to reuse the first stage of the Falcon 9 rocket. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is because SpaceX can reuse the first stage. Therefore if we can determine if the first stage will land, we can determine the cost of a launch. This information can be used if an alternate company wants to bid against SpaceX for a rocket launch. In this lab, you will collect and make sure the data is in the correct format from an API. The following is an example of a successful and launch.

objectives

In this lab, you will make a get request to the SpaceX API. You will also do some basic data wrangling and formating.

Request to the SpaceX API(Imagine the SpaceX API as a treasure trove of information about their rocket launches. As a data scientist, you need specific data to fuel your research) .Clean the requested data(The data you receive from the SpaceX API might not be in a perfect, organized format. This is where your data wrangling skills come into play. This process is like tidying up a messy warehouse)
"""

!pip install requests

!pip install numpy

!pip install pandas

"""# Requests allows us to make HTTP requests which we will use to get data from an API
# import requests        # Used for making HTTP requests to websites and APIs.
"""

import requests

"""# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
#import numpy as np  # Used for numerical computations and working with arrays and matrices.Importing the pandas library for data analysis.

"""

import numpy as np

"""# Pandas is a software library written for the Python programming language for data manipulation and analysis.
#import pandas as pd    # Used for data analysis and working with DataFrames.
"""

import pandas as pd

"""# Datetime is a library that allows us to represent dates
#import datetime  # In Python, datetime refers to a built-in module that provides functionality for working with dates and times. It offers various classes and functions to represent, manipulate, and format dates, times, and timedeltas.
"""

import datetime

"""# Setting this option will print all collumns of a dataframe. This option specifies the maximum number of columns to display when printing a DataFrame. By default, pandas only shows the first 20 columns. Setting this option to None disables this restriction and displays all columns."""

pd.set_option('display.max_columns', None)

"""# Setting this option will print all of the data in a feature. This option determines the maximum width of each column when printing a DataFrame. The default value is usually 50 characters, meaning that wider columns are truncated with an ellipsis (...). Setting this option to None removes this limitation and displays the full content of each column."""

pd.set_option('display.max_colwidth', None)

"""#"The spacex_url variable name can be freely chosen and replaced with any other appropriate name."
"""

spacex_url="https://api.spacexdata.com/v4/launches/past"

response = requests.get(spacex_url)

print(response.content)

"""'''You should see the response contains massive information about SpaceX launches. Next, let's try to discover some more relevant information for this project.

#Task 1: Request and parse the SpaceX launch data using the GET request
To make the requested JSON results more consistent, we will use the following static response object for this project:
'''

#"static" means that the content of the URL stored in the static_json_url variable does not change. In other words, this URL always points to a specific JSON file with content that remains constant and doesn't update over time.
"""

static_json_url = 'https:\\cf-courses-data.s3.us.cloud-object-storage.apddomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'

response.status_code    #In the context of data collection, a status code of 200 typically indicates a successful operation, meaning the data collection process has completed without any errors.

"""#Python comes with a built-in library called json that facilitates working with JSON data. This library provides functions for decoding JSON from strings and Python objects, as well as encoding Python objects into JSON strings.
#JSON is often utilized for exchanging data with APIs.
"""

data = response.json()

"""#Once normalized, data becomes easier to access and manipulate using Pandas' data manipulation functions. You can easily select, filter, sort, and aggregate data based on specific criteria, facilitating further analysis and insights."""

data = pd.json_normalize(data)

"""'''Get the head of the dataframe'''"""

data.head()

"""#After gathering information from our data and understanding the columns and their contents, we may encounter columns named "links" that seem irrelevant to our analysis. As a data scientist, it's crucial to go beyond existing knowledge and acquire project-specific insights. This involves thorough research, consultations with clients or stakeholders, and a deep understanding of the problem at hand. This additional knowledge plays a significant role in shaping the problem-solving approach and formulating effective solutions."""

data.info()

data.columns

"""'''We will now use the API again to get information about the launches using the IDs given for each launch. Specifically we will be using columns rocket, payloads, launchpad, and cores.'''

#Identify and segregate the crucial data
# Lets take a subset of our dataframe keeping only the features we want and the flight number, and date_utc.
"""

dada = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

"""#"The SpaceX project requires us to focus on testing single-core rockets. We won't be examining rockets that employ two-core boosters."
# ==1: This comparison operator checks whether the length of each element in the cores column is equal to 1.
# ==1: This comparison operator checks whether the length of each element in the payloads column is equal to 1.
#It calculates the length of each individual element in the payloads column. This length represents the number of items within each element, which are assumed to be lists or arrays in this context.
#To extract rows where the length is equal to one and add them to the original DataFrame, you can use the following code:
#We will remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
"""

data = data[data['cores'].map(len)==1]

data = data[data['payloads'].map(len)==1]

"""#To apply a lambda function that extracts the first element (index 0) using the map method on each column in Python, you can follow these steps:
# Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
"""

data['cores'] = data['cores'].map(lambda x:x[0])

data['payloads'] = data['payloads'].map(lambda x:x[0])

"""#Extracting Date Without Time from a Column
# We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
"""

data['date'] = pd.to_datetime(data['date_utc']).dt.date

"""#We only want to test launches that were before this date.
#We don't want this column to be based on hour or minute; we want it to be based on date.
# Using the date we will restrict the dates of the launches
"""

data = data[data['date'] <= datetime.date(2020, 11, 13)]

"""#From the rocket we would like to learn the booster name.
#From the payload we would like to learn the mass of the payload and the orbit that it is going to
#From the launchpad we would like to know the name of the launch site being used, the longitude, and the latitude.
#From cores we would like to learn the outcome of the landing, the type of the landing, number of flights with that core, whether gridfins were used, whether the core is reused, whether legs were used, the landing pad used, the block of the core which is a number used to seperate version of cores, the number of times this specific core has been reused, and the serial of the core.

'''# "We are preparing a list of things we want."
'''

#The data from these requests will be stored in lists and will be used to create a new dataframe.
"""

BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

#Explanation:1.Fetches data ( an IP address or URL as input) 2.Processes rocket column 3.Converts to string 4.Converts to JSON
#To extract rocket names from JSON responses, we can define a function that iterates through the rocket column and retrieves the relevant information from the corresponding JSON URLs
def getBoosterVersion(data):
    for x in data['rocket']:
        response= requests.get("https://api.spacexdata.com/v4/rockets/"+ str(x)).json()
         #The extracted booster version information is then appended to the BoosterVersion array.
        BoosterVersion.append(response['name'])
        #In essence, the name variable serves as a placeholder for the current rocket being processed in the loop. It enables the function to access the relevant API data and extract the corresponding booster version name.

# Now, let's apply getBoosterVersion function method to get the booster version
# Call getBoosterVersion
# getBoosterVersion is the name of our function.
# the list has now been update
getBoosterVersion(data)

print(BoosterVersion) #As you can see, it is the name of our rockets, but we are currently working with the Falcon 9.

# Call getPayloadData
#From the payload we would like to learn the mass of the payload and the orbit that it is going to.
#Takes the dataset and uses the payloads column to call the API and append the data to the lists
#It extracts the mass_kg (mass in kilograms) value.
#It extracts the orbit value (the orbit around which the payload is traveling).
#It appends the mass_kg to a pre-existing list named payloads_mass.
#It appends the orbit to a pre-existing list named orbits.
def getPayloadData(data):
    for load in data['payloads']:
        response= requests.get("https://api.spacexdata.com/v4/payloads/"+ load).json()  #This function takes a URL (where payload data resides) as input.
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

# Call getPayloadData
getPayloadData(data)

print(getPayloadData)

PayloadMass[0:4]

Orbit[0:4]

#From the launchpad we would like to know the name of the launch site being used, the logitude, and the latitude.
# Takes the dataset and uses the launchpad column to call the API and append the data to the list
def getLaunchSite(data):
    for x in data['launchpad']:
        response= requests.get("https://api.spacexdata.com/v4/launchpads/"+str(data['launchpad'][0])).json()
        LaunchSite.append(response['name'])
        Longitude.append(response['longitude'])
        Latitude.append(response['latitude'])

# Call getLaunchSite
getLaunchSite(data)

LaunchSite[0:4]

# Takes the dataset and uses the cores column to call the API and append the data to the lists
def getCoreData(data):
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])

# Call getCoreData
getCoreData(data)

Outcome[0:6]

"""# "Now, let's create our final dataset by organizing the collected data into a dictionary structure."
"""

#Finally lets construct our dataset using the data we have obtained. We we combine the columns into a dictionary
launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

len(GridFins)

#Now, let's convert our constructed dictionary into a DataFrame.
data2 = pd.DataFrame(launch_dict)

data2.head(5)

data2.info()

"""# Task 2: Filter the dataframe to only include `Falcon 9` launches"""

#Then, we need to create a Pandas data frame from the dictionary launch_dict.
# Hint data['BoosterVersion']!='Falcon 1'
data_falcon9 = data2[data2['BoosterVersion'] == 'Falcon9']

data_falcon9   #These are the columns we've created so far, but we haven't added any content to them yet.

len('data_falcone9')

data2.info()

data_falcon9.to_csv('data_falcon9_week01.csv' , index=False)