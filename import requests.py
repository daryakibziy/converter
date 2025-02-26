import requests
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox

API_URL = "https://api.exchangerate-api.com/v4/latest/"

# Список популярных валют (можно расширять)
CURRENCIES = ["EUR", "USD", "RUB", "GBP", "KZT", "RSD", "CNY", "JPY"]

def get_exchange_rate(base_currency):
    """ Получает курсы валют относительно базовой валюты """
    try:
        response = requests.get(API_URL + base_currency)
        data = response.json()
        return data.get("rates", None)
    except Exception:
        return None

def convert_currency():
    """ Выполняет конвертацию и обновляет интерфейс """
    base = base_currency_var.get()
    target_1 = target_currency_1_var.get()
    target_2 = target_currency_2_var.get()

    try:
        amount = float(amount_entry.get())  # Получаем сумму
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число!")
        return

    rates = get_exchange_rate(base)
    if not rates or target_1 not in rates:
        messagebox.showerror("Ошибка", f"Не удалось получить курс {base} → {target_1}")
        return

    amount_in_target_1 = amount * rates[target_1]  # Конвертация в target_1
    rates_target_1 = get_exchange_rate(target_1)

    if not rates_target_1 or target_2 not in rates_target_1:
        messagebox.showerror("Ошибка", f"Не удалось получить курс {target_1} → {target_2}")
        return

    amount_in_target_2 = amount_in_target_1 * rates_target_1[target_2]  # Конвертация в target_2

    result_label.config(text=f"{amount} {base} = {amount_in_target_1:.2f} {target_1}\n"
                             f"{amount_in_target_1:.2f} {target_1} = {amount_in_target_2:.2f} {target_2}")

# Создаём графическое окно
root = tk.Tk()
root.title("Конвертер валют")

# Поля выбора валют (Combobox)
tk.Label(root, text="Начальная валюта:").grid(row=0, column=0)
base_currency_var = tk.StringVar(value="EUR")  # Валюта по умолчанию
base_currency_box = Combobox(root, textvariable=base_currency_var, values=CURRENCIES, state="readonly")
base_currency_box.grid(row=0, column=1)

tk.Label(root, text="Промежуточная валюта:").grid(row=1, column=0)
target_currency_1_var = tk.StringVar(value="RSD")
target_currency_1_box = Combobox(root, textvariable=target_currency_1_var, values=CURRENCIES, state="readonly")
target_currency_1_box.grid(row=1, column=1)

tk.Label(root, text="Итоговая валюта:").grid(row=2, column=0)
target_currency_2_var = tk.StringVar(value="KZT")
target_currency_2_box = Combobox(root, textvariable=target_currency_2_var, values=CURRENCIES, state="readonly")
target_currency_2_box.grid(row=2, column=1)

# Поле ввода суммы
tk.Label(root, text="Сумма:").grid(row=3, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1)

# Кнопка для запуска конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_currency)
convert_button.grid(row=4, column=0, columnspan=2)

# Поле для результата
result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
result_label.grid(row=5, column=0, columnspan=2)

# Запуск главного цикла
root.mainloop()
