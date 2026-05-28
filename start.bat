@echo off
echo 🛡 Запуск PsychGuard...

echo 🌐 Запускаем веб-приложение...
start "WebApp" python main.py

timeout /t 3 /nobreak > nul

echo 🤖 Запускаем Telegram бота...
start "TelegramBot" python telegram_bot.py

timeout /t 2 /nobreak > nul

echo 🌍 Открываем браузер...
start http://localhost:8000
start presentation.html

echo.
echo ✅ PsychGuard запущен!
echo    Веб-приложение: http://localhost:8000
echo    Telegram бот:   @PsychGuard_Bot
echo    Презентация:    открыта в браузере
echo.
pause
