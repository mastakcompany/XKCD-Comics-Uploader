import random
import shutil
from pathlib import Path
import os

import requests
from dotenv import load_dotenv


def get_random_comic_number():
    api_endpoint = 'https://xkcd.com/info.0.json'
    response = requests.get(api_endpoint)
    response.raise_for_status()
    number_of_topics = response.json().get('num')
    return random.randint(1, number_of_topics)


def download_random_comic(name, path):
    comic_number = get_random_comic_number()
    api_endpoint = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(api_endpoint)
    response.raise_for_status()
    caption = response.json()["alt"]
    image_url = response.json()["img"]
    download_image(image_url, path, name)
    return caption


def download_image(url, path, name):
    Path(path).mkdir(parents=True, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(f'{path}/{name}.jpg', 'wb') as file:
        file.write(response.content)


def remove_images(path):
    shutil.rmtree(path)


def get_wall_upload_server(group_id, api_version, access_token):
    api_endpoint = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': access_token,
        'group_id': group_id,
        'v': api_version
    }
    response = requests.get(
        api_endpoint,
        params=params
    )
    response.raise_for_status()
    photo = response.json()["response"]
    album_id = photo["album_id"]
    upload_url = photo["upload_url"]
    user_id = photo["user_id"]

    return album_id, upload_url, user_id


def upload_photo(upload_url, image_path, image_name):
    with open(f'{image_path}/{image_name}.jpg', 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(
            url=upload_url,
            files=files
        )
        response.raise_for_status()
        server = response.json()["server"]
        photo = response.json()["photo"]
        photo_hash = response.json()["hash"]
    return server, photo, photo_hash


def save_photo_on_wall(access_token, client_id, group_id, photo, server, photo_hash):
    api_endpoint = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': access_token,
        'user_id': client_id,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'v': api_version,
    }
    response = requests.post(
        api_endpoint,
        params=params
    )
    response.raise_for_status()
    media = response.json()["response"]
    media_id = media[0]["id"]
    owner_id = media[0]["owner_id"]

    return media_id, owner_id


def publish_photo_on_wall(access_token, group_id, caption, owner_id, media_id, api_version):
    api_save_photo = f'https://api.vk.com/method/wall.post'
    from_group = 1
    params = {
        'access_token': access_token,
        'owner_id': f'-{group_id}',
        'from_group': from_group,
        'message': caption,
        'attachments': f'photo{owner_id}_{media_id}',
        'v': api_version
    }
    response = requests.post(
        api_save_photo,
        params=params
    )
    response.raise_for_status()


if __name__ == '__main__':
    api_version = '5.131'
    image_name = 'comics'
    path = './Files/'
    load_dotenv()
    access_token = os.environ['VK_ACCESS_TOKEN']
    client_id = os.environ['VK_CLIENT_ID']
    group_id = os.environ['VK_GROUP_ID']
    caption = download_random_comic(image_name, path)
    album_id, upload_url, user_id = get_wall_upload_server(group_id, api_version, access_token)
    server, photo, photo_hash = upload_photo(upload_url, path, image_name)
    media_id, owner_id = save_photo_on_wall(
        access_token,
        client_id,
        group_id,
        photo,
        server,
        photo_hash
    )
    publish_photo_on_wall(
        access_token,
        group_id,
        caption,
        owner_id,
        media_id,
        api_version
    )

    remove_images(path)
