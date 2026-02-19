@echo off
setlocal enabledelayedexpansion

:: переходим в корень проекта (на уровень выше от папки скрипта)
cd /d "%~dp0.."

:: папка с тестами
set TEST_FOLDER=tests\regdet_page

:: корневая папка для отчетов
set REPORT_ROOT=reports\regdet_page

:: получаем текущую дату в формате ГГГГ-ММ-ДД
set RAWDATE=%date%
set RAWDATE=%RAWDATE:~-10%

if "%RAWDATE:~2,1%"=="/" (
    :: формат США MM/DD/YYYY
    set MM=%RAWDATE:~0,2%
    set DD=%RAWDATE:~3,2%
    set YYYY=%RAWDATE:~6,4%
) else (
    :: формат DD.MM.YYYY
    set DD=%RAWDATE:~0,2%
    set MM=%RAWDATE:~3,2%
    set YYYY=%RAWDATE:~6,4%
)

set DATE_STR=%YYYY%-%MM%-%DD%

:: папка для отчетов за текущую дату (внутри regdet_page)
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
