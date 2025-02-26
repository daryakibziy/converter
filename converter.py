import requests
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox, Style
from tkinter import StringVar

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
root.geometry("350x300")
root.configure(bg="#FFC0CB")  # Светло-розовый фон

# Стили
style = Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12), background="#FFC0CB")

# Поля выбора валют (Combobox)
tk.Label(root, text="Начальная валюта: ",font=("Arial", 11), bg="#FFC0CB").grid(row=0, column=0, padx=10, pady=5)
base_currency_var = StringVar(value="EUR")
base_currency_box = Combobox(root, textvariable=base_currency_var, values=CURRENCIES, state="readonly")
base_currency_box.grid(row=0, column=1, pady=5)

tk.Label(root, text="Промежуточная валюта: ", font=("Arial", 11), bg="#FFC0CB").grid(row=1, column=0, padx=10, pady=5)
target_currency_1_var = StringVar(value="RSD")
target_currency_1_box = Combobox(root, textvariable=target_currency_1_var, values=CURRENCIES, state="readonly")
target_currency_1_box.grid(row=1, column=1, pady=5)

tk.Label(root, text="Итоговая валюта:", font=("Arial", 11), bg="#FFC0CB").grid(row=2, column=0, padx=10, pady=5)
target_currency_2_var = StringVar(value="KZT")
target_currency_2_box = Combobox(root, textvariable=target_currency_2_var, values=CURRENCIES, state="readonly")
target_currency_2_box.grid(row=2, column=1, pady=5)

# Поле ввода суммы
tk.Label(root, text="Сумма:", font=("Arial", 11), bg="#FFC0CB").grid(row=3, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=3, column=1, pady=5)

# Кнопка для запуска конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_currency, bg="#FF69B4", fg="white", font=("Arial", 12, "bold"), relief="flat")
convert_button.grid(row=4, column=0, columnspan=2, pady=10)

# Поле для результата
result_label = tk.Label(root, text="", font=("Arial", 13), fg="black", bg="#FFC0CB")
result_label.grid(row=5, column=0, columnspan=2)

# Запуск главного цикла
root.mainloop()