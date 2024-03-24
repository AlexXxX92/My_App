import requests
from pprint import pprint
from datetime import date
import json





class vk_photo:
    def __init__(self, token = input('введите токен vk: '), id = input('введите id vk: ')):
        self.token = token
        self.id = id



    def vk_info_photos(self):
        url = 'https://api.vk.com/method/'


        params = {'user_ids': self.id,
              'owner_id': self.id,
              'album_id': 'profile',
              'access_token': self.token,
              'v': '5.131',
              'extended': '1',
              'count': '5',
              'photo_sizes': '1'
                 }

        response = requests.get(url + 'photos.get', params=params).json()
        photos_list = []

        for photo in response['response']['items']:
            photos_dict = {}
            if not photos_list:
                photos_dict.update(file_name=f"{photo['likes']['count']}.jpg", url=photo['sizes'][-1]['url'],size=photo['sizes'][-1]['type'])
            elif photo['likes']['count'] == int(photos_list[0]['file_name'][0]):
                photos_dict.update(file_name=f"{photo['likes']['count']}_{date.fromtimestamp(photo['date']).strftime('%Y-%m-%d')}.jpg",url=photo['sizes'][-1]['url'], size=photo['sizes'][-1]['type'])
            else:
                photos_dict.update(file_name=f"{photo['likes']['count']}.jpg", url=photo['sizes'][-1]['url'],size=photo['sizes'][-1]['type'])
            photos_list.append(photos_dict)
        return photos_list

    def json_vk(self):
        info = []
        for i in vk_photo().vk_info_photos():
            info_dict = {}
            info_dict['file_name'] = i['file_name']
            info_dict['size'] = i['size']
            info.append(info_dict)
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f)



# yandex создание папки
class yandex_disk:
    def __init__(self, token = input('введите токен YA: ')):
        self.token = token

    def new_folder_ya(self, fold_name = input('введите название папки: ')):
        self.fold_name = fold_name


        url ='https://cloud-api.yandex.net/v1/disk/resources'


        headers = {'Authorization': f'OAuth {self.token}'
                   }

        params = {'path': self.fold_name,
                  }

        response = requests.put(url, headers=headers, params=params).json()

        return response




    def load_to_ya(self):
        self.new_folder_ya()
        vk_photo().json_vk()
        count = 0
        for u in vk_photo().vk_info_photos():
            count += 1
            url_load = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

            headers = {'Authorization': f'OAuth {self.token}'
                       }

            params_load = {'url': u['url'],
                       'path': f'{self.fold_name}/{u["file_name"]}',
                       'overwrite': 'true',
                       'fields': u['file_name']
                       }
            response = requests.post(url_load, headers=headers, params=params_load)



            pprint(f"Загружено: {u['file_name']}|{count} из {len(vk_photo().vk_info_photos())}")


yandex_disk().load_to_ya()
