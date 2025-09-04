@echo off
setlocal enabledelayedexpansion

:: папка с тестами (поднимаемся на уровень вверх)
set TEST_FOLDER=..\tests\signup_page

:: корневая папка для отчетов
set REPORT_ROOT=..\reports

:: получаем текущую дату в формате ГГГГ-ММ-ДД
for /f "tokens=1-3 delims=." %%a in ("%date%") do (
    set YYYY=%%c
    set MM=%%b
    set DD=%%a
)
set DATE_STR=%YYYY%-%MM%-%DD%

:: папка для отчетов за текущую дату
set REPORT_FOLDER=%REPORT_ROOT%\%DATE_STR%

:: считаем, сколько html-файлов уже есть в папке
set COUNT=0
if exist %REPORT_FOLDER% (
    for %%f in (%REPORT_FOLDER%\*.html) do (
        set /a COUNT+=1
    )
)

:: увеличиваем номер прогона
set /a COUNT+=1

:: имя файла отчета
set REPORT_FILE=%COUNT%.html

:: создаём папку для отчетов, если её нет
if not exist %REPORT_FOLDER% mkdir %REPORT_FOLDER%

:: запускаем pytest с формированием html-отчета
pytest %TEST_FOLDER% --html=%REPORT_FOLDER%\%REPORT_FILE% --self-contained-html -v

echo.
echo Отчет сформирован: %REPORT_FOLDER%\%REPORT_FILE%
pause
