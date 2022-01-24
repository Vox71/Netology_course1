import requests


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

    def test_exceptions(self):
        test_url = "https://cloud-api.yandex.net/v1/disk"
        headers = self.get_headers()
        params = {"fields": "error"}
        res = requests.get(test_url, headers=headers, params=params)
        return res

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
            'Authorization': f'OAuth {self.token}'
        }
        params = {'path': dir_name}

        requests.put(url, headers=headers, params=params, timeout=5)