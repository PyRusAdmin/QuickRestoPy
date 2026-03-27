# -*- coding: utf-8 -*-
import json

from rich.console import Console
from rich.prompt import Prompt

from core.quickresto_client import QuickRestoClient

console = Console()


def main():
    client = QuickRestoClient()

    menu_items = [
        ("get_all_clients", "Получить всех клиентов", client.get_all_clients),
        ("get_client", "Получить информацию о клиенте", lambda: run_get_client(client)),
        ("create_client", "Создать нового клиента", lambda: run_create_client(client)),
        ("delete_client", "Удалить клиента", lambda: run_delete_client(client)),
        ("get_client_by_phone", "Найти клиента по телефону", lambda: run_get_client_by_phone(client)),
        ("update_bonus", "Обновить бонусы клиента", lambda: run_update_bonus(client)),
    ]

    while True:
        console.clear()
        console.print("[bold cyan]Меню QuickResto API[/bold cyan]\n")

        for i, (_, desc, _) in enumerate(menu_items, 1):
            console.print(f"  [yellow]{i}.[/yellow] {desc}")

        console.print(f"\n  [yellow]0.[/yellow] Выход")

        choice = Prompt.ask(
            "\n[bold]Выберите пункт меню[/bold]",
            choices=[str(i) for i in range(len(menu_items) + 1)],
            show_choices=False,
        )

        if choice == "0":
            break

        idx = int(choice) - 1
        if 0 <= idx < len(menu_items):
            console.clear()
            try:
                menu_items[idx][2]()
            except Exception as e:
                console.print(f"[red]Ошибка: {e}[/red]")

            console.input("\n[dim]Нажмите Enter для продолжения...[/dim]")


def run_get_client(client):
    client_id = int(Prompt.ask("Введите client_id"))
    result = client.get_client(client_id)
    if result:
        console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        console.print("[red]Клиент не найден[/red]")


def run_create_client(client):
    name = Prompt.ask("Введите имя клиента")
    phone = Prompt.ask("Введите номер телефона")
    result = client.create_client(name, phone)
    if result:
        console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        console.print("[red]Ошибка при создании клиента[/red]")


def run_delete_client(client):
    client_id = int(Prompt.ask("Введите client_id для удаления"))
    result = client.delete_client(client_id)
    if result:
        console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        console.print("[red]Ошибка при удалении клиента[/red]")


def run_get_client_by_phone(client):
    phone = Prompt.ask("Введите номер телефона")
    result = client.get_client_by_phone(phone)
    if result:
        console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        console.print("[red]Клиент не найден[/red]")


def run_update_bonus(client):
    customer_id = int(Prompt.ask("Введите customer_id"))
    amount = float(Prompt.ask("Введите количество бонусов"))
    phone = Prompt.ask("Введите номер телефона")
    result = client.update_bonus(customer_id, amount, phone)
    if result:
        console.print_json(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        console.print("[red]Ошибка при обновлении бонусов[/red]")


if __name__ == "__main__":
    main()
