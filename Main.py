""" Приложение для отслеживания курсов криптовалют к USD """
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import requests
import json

# Словарь криптовалют: ключ - ID для API CoinGecko, значение - отображаемое имя
CRYPTO_LIST = {
    "bitcoin": "Биткоин (BTC)",
    "ethereum": "Эфириум (ETH)",
    "solana": "Солана (SOL)",
    "toncoin": "TON (TON)",
    "dogecoin": "Догикоин (DOGE)",
    "cardano": "Кардано (ADA)",
    "ripple": "Риппл (XRP)"
}

def update_crypto_label(event):
    """Обновляет метку с полным названием при выборе из списка"""
    crypto_id = crypto_combobox.get()
    full_name = CRYPTO_LIST.get(crypto_id, "Неизвестно")
    name_label.config(text=f"Полное название: {full_name}")

def get_exchange_rate():
    """Запрашивает курс выбранной криптовалюты к USD через CoinGecko API"""
    crypto_id = crypto_combobox.get()
    
    if not crypto_id:
        mb.showwarning("Внимание", "Пожалуйста, выберите криптовалюту из списка.")
        return

    try:
        # Формируем URL запроса к API CoinGecko
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
        
        # Отправляем GET-запрос с таймаутом 10 секунд
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Вызовет ошибку, если статус ответа не 200 OK
        
        data = response.json()
        
        # Проверяем, есть ли нужная криптовалюта в ответе
        if crypto_id in data and "usd" in data[crypto_id]:
            rate = data[crypto_id]["usd"]
            full_name = CRYPTO_LIST[crypto_id]
            
            # Форматируем результат и выводим в метку
            result_text = f"Текущий курс: 1 {crypto_id.upper()} = {rate:,.2f} USD"
            result_label.config(text=result_text, fg="green")
        else:
            result_label.config(text="Данные о курсе не найдены", fg="red")
            
    except requests.exceptions.ConnectionError:
        mb.showerror("Ошибка сети", "Не удалось подключиться к интернету. Проверьте соединение.")
        result_label.config(text="Ошибка сети", fg="red")
    except requests.exceptions.Timeout:
        mb.showerror("Ошибка", "Превышено время ожидания ответа от сервера.")
        result_label.config(text="Таймаут запроса", fg="red")
    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка API", f"Произошла ошибка при получении данных: {e}")
        result_label.config(text="Ошибка API", fg="red")
    except Exception as e:
        mb.showerror("Неизвестная ошибка", f"Произошла непредвиденная ошибка: {e}")

# === Создание графического интерфейса ===
window = tk.Tk()
window.title("Курсы криптовалют")
window.geometry("400x300")
window.resizable(False, False)

# Отступы для всех элементов
pad_opts = {"padx": 20, "pady": 10}

# 1. Надпись "Криптовалюта:"
tk.Label(window, text="Криптовалюта:", font=("Arial", 11)).pack(**pad_opts)

# 2. Выпадающий список
crypto_combobox = ttk.Combobox(window, values=list(CRYPTO_LIST.keys()), state="readonly", width=25)
crypto_combobox.pack(**pad_opts)
crypto_combobox.bind("<<ComboboxSelected>>", update_crypto_label)
crypto_combobox.current(0) # Выбираем Bitcoin по умолчанию

# 3. Метка с полным названием
name_label = ttk.Label(window, text=f"Полное название: {CRYPTO_LIST['bitcoin']}", font=("Arial", 10, "italic"))
name_label.pack(**pad_opts)

# 4. Кнопка получения курса
btn_get_rate = tk.Button(window, text="Получить курс к USD", command=get_exchange_rate, 
                         bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=20)
btn_get_rate.pack(**pad_opts)

# 5. Метка для вывода результата
result_label = tk.Label(window, text="Нажмите кнопку для получения курса", font=("Arial", 12, "bold"), fg="gray")
result_label.pack(**pad_opts)

# Запуск главного цикла
window.mainloop()