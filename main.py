import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env (override=True переопределяет системные переменные)
load_dotenv(override=True)

# Достаем данные из окружения
LAYER_NAME: str = os.getenv("LAYER_NAME")
USERNAME: str = os.getenv("USERNAME")
PASSWORD: str = os.getenv("PASSWORD")

BASE_URL = f"https://{LAYER_NAME}.quickresto.ru/platform/online/api"
auth = HTTPBasicAuth(USERNAME, PASSWORD)
HEADERS = {"Content-Type": "application/json"}


def get_all_clients():
    all_clients = []
    limit = 500  # Максимально рекомендуемый размер порции для Quick Resto
    offset = 0

    print("🚀 Начинаю загрузку всех клиентов...")

    while True:
        url = f"{BASE_URL}/list"
        query_params = {
            "moduleName": "crm.customer",
            "className": "ru.edgex.quickresto.modules.crm.customer.CrmCustomer"
        }
        payload = {
            "limit": limit,
            "offset": offset
        }

        try:
            response = requests.get(
                url,
                params=query_params,
                json=payload,
                auth=auth,
                headers=HEADERS,
                timeout=30
            )
            response.raise_for_status()

            batch = response.json()

            if not batch:
                # Если сервер вернул пустой список, значит мы дошли до конца
                break

            all_clients.extend(batch)
            print(f"📥 Загружено: {len(all_clients)}...")

            # Увеличиваем offset для следующей "страницы"
            offset += limit

            # Если вернулось меньше, чем мы просили, значит это была последняя страница
            if len(batch) < limit:
                break

        except Exception as e:
            print(f"❌ Ошибка на смещении {offset}: {e}")
            break

    return all_clients


if __name__ == "__main__":
    all_data = get_all_clients()

    print("\n" + "=" * 50)
    print(f"✅ Итого получено клиентов: {len(all_data)}")
    print("=" * 50)

    # Выведем первые 10 для проверки
    if all_data:
        print(f"{'ID':<7} | {'Имя':<25} | {'Телефон':<15}")
        print("-" * 50)
        for c in all_data[:10]:
            name = f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() or "---"
            phone = c.get('phoneNumber', '---')
            print(f"{c.get('id', 0):<7} | {name:<25} | {phone:<15}")

        if len(all_data) > 10:
            print(f"... и еще {len(all_data) - 10} клиентов")
