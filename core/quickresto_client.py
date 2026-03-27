# -*- coding: utf-8 -*-
import requests
from loguru import logger
from requests.auth import HTTPBasicAuth


class QuickRestoClient:
    def __init__(self, layer_name_quickresto=None, username_quickresto=None, password_quickresto=None):
        self.layer_name_quickresto = layer_name_quickresto
        self.username_quickresto = username_quickresto
        self.password_quickresto = password_quickresto

        self.base_url = f"https://{self.layer_name_quickresto}.quickresto.ru/platform/online/api"
        self.auth = HTTPBasicAuth(self.username_quickresto, self.password_quickresto)
        self.headers = {"Content-Type": "application/json"}

    def get_all_clients(self):
        """Получить всех клиентов"""
        all_clients = []
        limit = 500
        offset = 0

        logger.info("Загрузка всех клиентов...")

        while True:
            url = f"{self.base_url}/list"
            params = {
                "moduleName": "crm.customer",
                "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
            }
            payload = {"limit": limit, "offset": offset}

            try:
                response = requests.get(url, params=params, json=payload, auth=self.auth, headers=self.headers,
                                        timeout=30)
                response.raise_for_status()
                batch = response.json()

                if not batch:
                    break

                all_clients.extend(batch)
                logger.info(f"Загружено: {len(all_clients)}")

                offset += limit
                if len(batch) < limit:
                    break

            except Exception as e:
                logger.exception(f"Ошибка на смещении {offset}: {e}")
                break

        return all_clients

    def get_client(self, client_id):
        """Получить информацию о клиенте по ID"""
        url = f"{self.base_url}/read"
        params = {
            "moduleName": "crm.customer",
            "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer",
            "objectId": client_id,
        }

        try:
            response = requests.get(url, params=params, auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"Ошибка при чтении клиента {client_id}: {e}")
            return None

    def create_client(self, name, phone):
        """Создать нового клиента"""
        url = f"{self.base_url}/create"
        params = {
            "moduleName": "crm.customer",
            "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
        }
        body = {
            "firstName": name,
            "contactMethods": [{"type": "phoneNumber", "value": phone}]
        }

        try:
            response = requests.post(url, params=params, json=body, auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(e)
            return None

    def delete_client(self, client_id):
        """Удалить клиента по ID"""
        url = f"{self.base_url}/remove"
        params = {
            "moduleName": "crm.customer",
            "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
        }
        body = {"id": client_id}

        try:
            response = requests.post(url, params=params, json=body, auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(e)
            return None

    def get_client_by_phone(self, phone):
        """Найти клиента по номеру телефона"""
        url = f"https://{self.layer_name_quickresto}.quickresto.ru/platform/online/bonuses/filterCustomers"
        payload = {'search': phone, 'typeList': ['customer'], 'limit': 10, 'offset': 0}

        try:
            response = requests.post(url, json=payload, auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(e)
            return None

    def update_bonus(self, customer_id, amount, phone):
        """Обновить бонусы клиента"""
        url = f"https://{self.layer_name_quickresto}.quickresto.ru/platform/online/bonuses/creditHold"
        body = {
            "customerToken": {"type": "phone", "entry": "manual", "key": phone},
            "accountType": {"accountGuid": "bonus_account_type-1"},
            "amount": amount
        }

        try:
            response = requests.post(url, json=body, auth=self.auth, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(e)
            return None


if __name__ == "__main__":
    client = QuickRestoClient()
    print(client.get_all_clients())
