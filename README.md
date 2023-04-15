# XKCD Comics Uploader

This is a Python script that downloads a random comic from XKCD website, uploads it to a VKontakte (VK) group, and publishes it on the group's wall.

## Dependencies
* Python 3.6 or later
* `requests` library
* `dotenv` library

## Getting started

1. Clone this repository to your local machine
```commandline
git clone https://github.com/mastakcompany/XKCD-Comics-Uploader.git
```
2. Install the required dependencies by running:
```commandline
pip install -r requirements.txt
```
3. Create a VKontakte group and a standalone app. You can follow [these instructions](https://vk.com/dev/access_token) for creating a standalone app and obtaining an access token.
4. Create a `.env` file in the root of the project and add the following variables with your VK app's credentials:
```commandline
VK_ACCESS_TOKEN=<your_access_token>
VK_CLIENT_ID=<your_client_id>
VK_GROUP_ID=<your_group_id>
```
5. Run the script by executing `python main.py`.

## How it works
The script downloads a random comic from XKCD website by calling its API, saves it to the `Files` directory, uploads it to VK using VK API, and publishes it on the group's wall.

## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

### License
This project is licensed under the [MIT License](https://opensource.org/license/mit/).
