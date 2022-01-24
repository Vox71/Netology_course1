import requests
import json
from datetime import datetime


class VkGetPhoto:

    def __init__(self, id: str, token: str):
        self.token = token
        self.id = id
        self.photo_list = []
        self.dicts = []

    def get_photo_profile_list(self, id, vk_token):
        URL = "https://api.vk.com/method/photos.get"
        params = {
            "count": 3,
            "owner_id": id,
            "access_token": vk_token,
            "album_id": 'profile',
            "extended": '1',
            "photo_sizes": '1',
            "v": '5.131'
        }
        res = requests.get(URL, params=params)
        return res

    def get_photo(self):

        self.dicts.append(self.get_photo_profile_list(self.id, self.token).json())

        for dict in self.dicts:
            items = (dict.get('response')).get('items')
            for item in items:
                photo_dict = {}
                name = str((item.get('likes')).get('count'))
                if name in [file.get('filename') for file in self.photo_list]:
                    date = str(datetime.utcfromtimestamp(item.get('date')).strftime('%Y-%m-%d'))
                    name = (item.get('likes')).get('count')
                    photo_dict['filename'] = f"{name} {date}"
                else:
                    photo_dict['filename'] = f"{name}"
                photo_dict['photo'] = ((item.get('sizes'))[-1]).get('url')
                photo_dict['size_h'] = ((item.get('sizes'))[-1]).get('height')
                photo_dict['size_w'] = ((item.get('sizes'))[-1]).get('width')
                self.photo_list.append(photo_dict)
        print('Фото переименованы')
        return self.photo_list

    def json(self):
        json_file = []
        file_path = 'photo_list.json'
        for i in self.photo_list:
            json_info = {}
            json_info['filename'] = i['filename']
            json_info['size_h'] = i['size_h']
            json_info['size_w'] = i['size_w']
            json_file.append(json_info)
        with open(file_path, 'w') as f:
            json.dump(json_file, f)
