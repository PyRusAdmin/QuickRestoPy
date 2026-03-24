# -*- coding: utf-8 -*-
import json

import requests
from loguru import logger

from config import console
from main import base_url, auth, headers


def create_client(name_customer, phone_customer, BASE_URL, auth, headers):
    """Создание нового клиента"""
    try:
        url = f"{BASE_URL}/create"

        query_params = {
            "moduleName": "crm.customer",
            "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
        }

        body = {
            "firstName": name_customer,
            "contactMethods": [
                {
                    "type": "phoneNumber",
                    "value": phone_customer
                }
            ]
        }

        # post - отправка запроса
        # get - получение данных

        response = requests.post(
            url,
            params=query_params,
            json=body,
            auth=auth,
            headers=headers,
            timeout=30
        )
        
        # Проверяем статус ответа
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 500:
            # Для ошибки 500 проверим, возможно это дубликат клиента
            error_text = response.text
            if "duplicate" in error_text.lower() or "exists" in error_text.lower() or "уже существует" in error_text.lower():
                logger.warning(f"Клиент с телефоном {phone_customer} уже существует")
                return {"error": "duplicate_customer", "message": f"Клиент с телефоном {phone_customer} уже существует"}
            else:
                logger.error(f"Ошибка сервера при создании клиента: {response.status_code} - {error_text}")
                return None
        else:
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.exception(e)
        return None


def demo_create_client():
    """Пример использования функции create_client"""
    result = create_client(
        name_customer='Виталий',
        phone_customer='79493531398',
        BASE_URL=base_url,
        auth=auth,
        headers=headers
    )
    
    if result:
        if "error" in result and result["error"] == "duplicate_customer":
            print(f"Клиент с телефоном 79493531398 уже существует")
            console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Не удалось создать клиента")
    print(100 * "#")


if __name__ == "__main__":
    demo_create_client()
