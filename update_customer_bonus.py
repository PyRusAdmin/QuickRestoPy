# -*- coding: utf-8 -*-
import requests
from loguru import logger

from main import layer_name_quickresto, auth, headers


def update_customer_bonus(customer_id: int, amount: float, customer_phone):
    """Редактирование бонусных балов для клиента"""
    try:
        logger.info(f"Редактирование бонусных балов для клиента {customer_id}")

        url = f"https://{layer_name_quickresto}.quickresto.ru/platform/online/bonuses/creditHold"

        body = {
            "customerToken": {
                "type": "phone",  # ← тип токена: телефон
                "entry": "manual",  # ← способ ввода: вручную
                "key": customer_phone  # ← сам номер телефона
            },
            "accountType": {
                "accountGuid": "bonus_account_type-1"  # ← из данных клиента
            },
            "amount": amount
        }

        response = requests.post(url, json=body, auth=auth, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        logger.exception(e)
