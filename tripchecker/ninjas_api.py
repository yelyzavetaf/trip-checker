import requests
from dotenv import load_dotenv
import os
load_dotenv()


class set_coordinates():
    def __init__(self, name):
        self.name = name
        api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)
        self.rresponse = requests.get(api_url, headers={'X-Api-Key': os.getenv('NINJAS_API')})

    def longitude(self):
        if self.rresponse.status_code == requests.codes.ok:
            result = self.rresponse.json()
            if result:
                return result[0]['longitude']
        else:
            return None

    def latitude(self):
        if self.rresponse.status_code == requests.codes.ok:
            result = self.rresponse.json()
            if result:
                return result[0]['latitude']
        else:
            return None


