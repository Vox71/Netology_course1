import requests
import json
from datetime import datetime


class VkGetPhoto:

    def __init__(self, token: str):
        self.token = token
        self.photo_list = []
        self.dicts = []

    def get_photo_profile_list(self, id):
        URL = "https://api.vk.com/method/photos.get"
        params = {
            "count": 3,
            "owner_id": id.strip(),
            "access_token": vk_token,
            "album_id": 'profile',
            "extended": '1',
            "photo_sizes": '1',
            "v": '5.131'
        }
        res = requests.get(URL, params=params)
        return res

    def get_photo(self):
        self.dicts.append(self.get_photo_profile_list(id).json())

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
        file_path = 'photo_list.json'
        with open(file_path, 'w') as f:
            json.dump(self.photo_list, f)
        return self.photo_list


class YandexLoadPhotos:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            "Contens-Type": 'application/json',
            "Authorization": f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href_dict = self._get_upload_link(disk_file_path=disk_file_path)
        href = href_dict.get("href", "")
        photo_href = requests.get(filename.get('photo'))
        response = requests.put(href, data=photo_href)
        response.raise_for_status()
        if response.status_code == 201:
            print(f"Фотография {filename.get('filename')} загруженна.")

    def create_folder(self, folder_name):
        dir_name = folder_name
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {yandex_token}'
        }
        params = {'path': dir_name}

        requests.put(url, headers=headers, params=params, timeout=5)


if __name__ == '__main__':
    vk_token = input("Введите ваш VK токен:")
    id = input("Введите ID пользователя ВК:")
    yandex_token = input("Введите ваш Яндекс токен:")
    folder_name_to_create = input("Введите название создаваемой папки:")
    downloader = VkGetPhoto(vk_token)
    uploader = YandexLoadPhotos(yandex_token)
    list = downloader.get_photo()
    uploader.create_folder(folder_name_to_create)
    for photo in list:
        path_to_file = f"{folder_name_to_create}/{photo.get('filename')}"
        uploader.upload_file_to_disk(path_to_file, photo)
