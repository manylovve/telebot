import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('subscriptions.db')
cursor = conn.cursor()

# Выполнение запроса SQL для выбора всех записей из таблицы подписчиков
cursor.execute("SELECT * FROM subscribers")

# Получение результатов запроса
subscribers = cursor.fetchall()

# Вывод результатов
for subscriber in subscribers:
    print(subscriber)

# Закрытие соединения с базой данных
conn.close()
