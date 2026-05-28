#!/bin/bash

echo "🛡 Запуск PsychGuard..."

# Start web app in background
echo "🌐 Запускаем веб-приложение..."
python main.py &
WEB_PID=$!

# Wait for web app to start
sleep 3

# Start Telegram bot in background
echo "🤖 Запускаем Telegram бота..."
python telegram_bot.py &
BOT_PID=$!

sleep 2

# Open browser
echo "🌍 Открываем браузер..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
    open presentation.html
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start http://localhost:8000
    start presentation.html
else
    xdg-open http://localhost:8000
    xdg-open presentation.html
fi

echo ""
echo "✅ PsychGuard запущен!"
echo "   Веб-приложение: http://localhost:8000"
echo "   Telegram бот:   @PsychGuard_Bot"
echo "   Презентация:    открыта в браузере"
echo ""
echo "Нажми Ctrl+C чтобы остановить всё"

# Wait and handle stop
trap "echo '🛑 Останавливаем...'; kill $WEB_PID $BOT_PID 2>/dev/null; exit" INT
wait
