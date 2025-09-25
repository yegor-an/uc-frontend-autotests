#!/bin/bash

# папка с тестами (поднимаемся на уровень вверх)
TEST_FOLDER="../tests/login_page"

# корневая папка для отчетов
REPORT_ROOT="../reports/login"

# получаем текущую дату в формате ГГГГ-ММ-ДД
DATE_STR=$(date +%F)

# папка для отчетов за текущую дату
REPORT_FOLDER="$REPORT_ROOT/$DATE_STR"

# считаем, сколько html-файлов уже есть в папке
COUNT=0
if [ -d "$REPORT_FOLDER" ]; then
  COUNT=$(ls "$REPORT_FOLDER"/*.html 2>/dev/null | wc -l)
fi

# увеличиваем номер прогона
COUNT=$((COUNT+1))

# имя файла отчета
REPORT_FILE="$COUNT.html"

# создаём папку для отчетов, если её нет
mkdir -p "$REPORT_FOLDER"

# запускаем pytest с формированием html-отчета
pytest "$TEST_FOLDER" --html="$REPORT_FOLDER/${REPORT_FILE}.tmp" --self-contained-html -v
mv "$REPORT_FOLDER/${REPORT_FILE}.tmp" "$REPORT_FOLDER/$REPORT_FILE"

echo
echo "Отчет сформирован: $REPORT_FOLDER/$REPORT_FILE"
