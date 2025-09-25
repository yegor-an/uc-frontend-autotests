#!/usr/bin/env python3
import subprocess
import schedule
import time

# === НАСТРОЙКИ ===
# Каждая строка: (ВРЕМЯ_В_ФОРМАТЕ_HH:MM, "имя_скрипта.sh")
TASKS = [
    ("04:30", "run_login_test.sh"),
    ("04:35", "run_signup_test.sh")
]

# === ЛОГИКА ===
def run_script(script_name):
    print(f"Запуск {script_name}")
    subprocess.run(["bash", script_name], check=False)

# Регистрируем расписание
for t, script in TASKS:
    schedule.every().day.at(t).do(run_script, script)

print("Скрипт запущен. Ожидаем времени задач...")
while True:
    schedule.run_pending()
    time.sleep(10)
