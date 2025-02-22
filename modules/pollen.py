import logging, requests, datetime
from modules.pollen_dataclasses import *
from dacite import from_dict, Config

logger = logging.getLogger(__name__)

class Pollen:

    def __init__(self, apiKey:str):
        self.url = "https://pollen.googleapis.com/v1"
        self.base_params = {
            "key": apiKey
        }
        self.cast_config = Config({
            datetime.datetime: datetime.datetime.fromisoformat,
            datetime.date: datetime.date.fromisoformat,
        })

    def get(self, path:str, params:dict) -> dict | None:
        try:
            response = requests.get(
                url=f"{self.url}/{path}",
                params=dict(**self.base_params, **params)
            )
            if response.status_code != 200:
                logging.error(f"{response.url} return {response.status_code}: {response.text}")
                return None
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Request failed: {e}")
            return None

    def get_forecast(self,
        locationLatitude:str,
        locationLongitude:str,
        days:int=1,
        languageCode:str='en',
        plantsDescription:bool=False,
    ) -> PollenData:
        res_dict = self.get("forecast:lookup", {
            "location.latitude": locationLatitude,
            "location.longitude": locationLongitude,
            "days": days,
            "languageCode": languageCode,
            "plantsDescription": plantsDescription
        })
        if res_dict != None:
            return from_dict(data_class=PollenData, data=res_dict, config=self.cast_config)
        return None
