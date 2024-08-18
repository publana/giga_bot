import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
import uuid
import json
from utils import get_file_id

CLIENT_ID = st.secrets['CLIENT_ID']
SECRET = st.secrets['SECRET']

def get_access_token(): # получаем токен от GigaChat для формирования последующих запросов
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
    }
    payload = {'scope': 'GIGACHAT_API_PERS'}
    res = requests.post(
        url=url,
        headers=headers,
        auth=HTTPBasicAuth(CLIENT_ID, SECRET),
        data=payload,
        verify=False,
    )
    access_token = res.json()['access_token']
    return access_token

def get_image(file_id: str,access_token: str):
    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{file_id}/content"
    payload = {}
    headers = {
        'Accept': 'image/jpg',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers, data=payload, verify=False)
    return response.content

def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            # {
            #     "role": "system",
            #     "content": "Ты — Василий Кандинский"
            # },
            {
                "role": "user",
                "content": msg,
            }
        ],
        "function_call": "auto",
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload, verify=False)
    try:
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        st.toast(f'Произошла оштбка: {e}. \n\nТребуется перезагрузка чатбота!')


def send_prompt_and_get_response(msg: str, access_token: str):
    res = send_prompt(msg, access_token)
    data, is_image = get_file_id(res)
    if is_image:
        data = get_image(file_id=data, access_token=access_token)
    return data, is_image