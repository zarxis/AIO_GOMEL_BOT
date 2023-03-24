from sys import getsizeof
import time

from aiogram import types
from pygismeteo import Gismeteo


async def GetWeather(message: types.Message): #, c_name
    CityName = message.text
    gismeteo = Gismeteo()
    if isinstance(CityName, str):
        search_results = gismeteo.search.by_query(CityName)
        # print(search_results)
        #print(len(search_results))
        #print(search_results, 'до цикла!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        while len(search_results) <= 0:
            search_results = gismeteo.search.by_query(CityName)
            #print("я зашел!")
            time.sleep(0.5)
        #print(len(search_results))
        #print(search_results, 'ПОСЛЕ цикла!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        #print('\n -------')
        city_id = search_results[0].id
        # print('\n------------------------------', city_id)
        current = gismeteo.current.by_id(city_id)
        # print(f'\n -------------------------------', current)

        temp = current.temperature.air.c
        d_weather = current.description.full
        hum = current.humidity.percent
        cloud = current.cloudiness.percent
        await message.answer(f"Название города: {search_results[0].name}")
        await message.answer(f'Текущая температура 🌍:{temp}'
                             '\n'f'Тип погоды 🌍:{d_weather}'
                             '\n'f'Влажность  🌍:{hum}%'
                             '\n'f'Облачность 🌍:{cloud}%')