"""domain = 'https://api.vk.com/method/'
v = '5.53'
vk_token = 'Tокен доступа для ВК'
plotly_username = 'dimova17',#Имя пользователя Plot.ly
plotly_api_key = 'JUdIJJK1taivPxuS7aNL'#Ключ доступа Plot.ly"""
import requests

domain = "https://api.vk.com/method"
access_token = 'f3fd754ff3fd754ff3fd754f6df3a28432ff3fdf3fd754fa99d2c7d1e100c335b8dcbe3'
user_id = '162546124'  # PUT USER ID HERE

query_params = {
    'domain' : domain,
    'access_token': access_token,
    'user_id': user_id,
    'fields': 'sex'
}

query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.69".format(**query_params)
response = requests.get(query)