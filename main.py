from VKGET import *
from YALOAD import *

if __name__ == '__main__':
    vk_token = input("Введите ваш VK токен:")
    id = input("Введите ID пользователя ВК:")
    downloader = VkGetPhoto(id, vk_token)
    res1 = downloader.get_photo_profile_list(id, vk_token)
    exception_vk = res1.json().get('error')
    if exception_vk is not None:
        print('Неверный токен или ID пользователя')
    else:
        print('Данные от VK API получены')
        list = downloader.get_photo()
        downloader.json()
        print('Json файл создан')
        yandex_token = input("Введите ваш Яндекс токен:")
        uploader = YandexLoadPhotos(yandex_token)
        res2 = uploader.test_exceptions()
        exception_ya = res2.json().get('error')
        if exception_ya is not None:
            print('Неверный токен')
        elif res2.json().get('error') == '504':
            print('Сервис Yandex временно недоступен')
        else:
            print('Токен действителен')
            folder_name_to_create = input("Введите название создаваемой папки:")
            uploader.create_folder(folder_name_to_create)
            print('Папка создана')
            for photo in list:
                path_to_file = f"{folder_name_to_create}/{photo.get('filename')}"
                uploader.upload_file_to_disk(path_to_file, photo)
            print(f"Фотографии загружены в папку {folder_name_to_create}")
