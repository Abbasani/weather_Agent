# -*- coding: utf-8 -*-
"""weatherAI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K8vN6vHpMw8LRFtkNGh29upHvMEUw5qA
"""

!pip install -U langchain-community

from langchain.tools import tool, Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.utilities import SQLDatabase

import os
import requests
WEATHER_API = "87d43b9ae73a1b83708dbd90e39d270b"



@tool
def get_weather(city:str):
    """
    Fetches the current weather for a specified city.
    """
    url = f"https://api.weatherstack.com/current?access_key={WEATHER_API}"
    city_param = {"query":city} # Renamed variable to avoid conflict with function argument

    response = requests.get(url, params=city_param)

    data = response.json()
    # Check if the API call was successful and data is available
    if "location" in data and "current" in data:
        zone =data["location"]["timezone_id"]
        time = data['current']['observation_time']
        condition = data["current"]["weather_descriptions"][0]
        temp = data["current"]["temperature"]
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_speed"]

        # Return the formatted string instead of printing
        return f"The weather In {city_param['query']}, at {time} ({zone}), the weather is {condition} with a temperature of {temp}°C. The humidity is {humidity}% and the wind speed is {wind_speed} km/h."
    else:
        # Handle cases where the API call might not return expected data
        return f"Could not retrieve weather information for {city}."

!pip install -U langchain-groq

from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = "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"

models = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

llm = ChatGroq(
    model= models[0],
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

tools = [get_weather]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True # Add this to handle parsing errors
)

# query = "I want to know the weather in New York City"
query = "I want to know the sum of weather in kano and Lagos"

response = agent.invoke(query)
print(response)
print("\n\n")