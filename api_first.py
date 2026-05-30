import json
import requests
import uuid
from settings import EMAIL, PASSWORD, BASE_URL


class Pets:
    """ API library for interacting with the Swagger service http://34.141.58 """

    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None

    def get_registered(self) -> int:
        auto_email = uuid.uuid4().hex
        auto_pass = uuid.uuid4().hex
        data = {
            "email": f'{auto_email}.il',
            "password": auto_pass,
            "confirm_password": auto_pass
        }
        res = requests.post(self.base_url + 'register', json=data)

        response_json = res.json()
        my_id = response_json.get('id')
        my_token = response_json.get('token')
        print(f"Registered ID: {my_id}")
        print(f"Registered Token: {my_token}")

        headers = {'Authorization': f'Bearer {my_token}'}
        params = {'id': my_id}
        res_del = requests.delete(self.base_url + f'users/{my_id}', headers=headers, params=params)
        status = res_del.status_code
        print(f"Delete status: {status}")
        return status

    def get_token(self):
        """Get authentication token by registering or logging in dynamically"""
        data = {
            "email": EMAIL,
            "password": PASSWORD
        }
        # 1. Сначала пробуем авторизоваться
        res = requests.post(self.base_url + 'login', json=data)
        status = res.status_code
        response_json = res.json()

        # 2. Если сервер вернул ошибку или нет токена — регистрируем этот email на лету
        if status != 200 or 'token' not in response_json:
            print(f"Вход не удался. Регистрируем динамического пользователя: {EMAIL}")
            reg_data = {
                "email": EMAIL,
                "password": PASSWORD,
                "confirm_password": PASSWORD
            }
            res = requests.post(self.base_url + 'register', json=reg_data)
            status = res.status_code
            response_json = res.json()

        # 3. Финальная проверка на наличие токена в ответе
        if 'token' not in response_json:
            print(f"Критическая ошибка API! Сервер вернул: {response_json}")
            return None, status, None

        self.token = response_json['token']
        self.user_id = response_json['id']
        print(f"Токен успешно получен! Token: {self.token}")
        return self.token, 200, self.user_id

    def get_list_users(self):
        """Get list of all users"""
        if not self.token:
            self.get_token()

        headers = {'Authorization': f'Bearer {self.token}'}
        res = requests.get(self.base_url + 'users', headers=headers)
        status = res.status_code
        my_id = res.text

        print(res.json())
        return status, my_id

    def get_pet(self):
        """Create a new pet for the authorized user"""
        if not self.token:
            self.get_token()

        headers = {'Authorization': f'Bearer {self.token}'}
        data = {
            "id": self.user_id,
            "name": 'Garfild',
            "type": 'cat',
            "age": 2,
            "owner_id": self.user_id
        }
        res = requests.post(self.base_url + 'pet', json=data, headers=headers)
        status = res.status_code

        response_json = res.json()
        pet_id = response_json.get('id')
        print(f"Pet ID: {pet_id}")
        print(response_json)
        return pet_id, status

    def get_pet_photo(self):
        """Upload a photo for a specific pet"""
        if not self.token:
            self.get_token()

        pet_id, _ = self.get_pet()
        headers = {'Authorization': f'Bearer {self.token}'}

        # Безопасное открытие файла. Убедитесь, что папка tests/photo/ и файл cat.jpg существуют
        files = {'pic': ('cat.jpg', open('tests/photo/cat.jpg', 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
        status = res.status_code
        link = res.json().get('link')
        print(res.json())
        return status, link

    def get_pet_like(self, pet_id=557):
        """Like a pet by its ID"""
        if not self.token:
            self.get_token()

        headers = {'Authorization': f'Bearer {self.token}'}
        data = {"id": pet_id}
        res = requests.put(self.base_url + f'pet/{pet_id}/like', json=data, headers=headers)
        status = res.status_code
        print(res.json())
        print(status)
        return status


# Данный блок защищает от автоматического выполнения при импорте в PyTest
if __name__ == '__main__':
    p = Pets()
    p.get_registered()
    p.get_token()
    p.get_list_users()
    p.get_pet()
    p.get_pet_photo()
    p.get_pet_like()