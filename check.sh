#!/bin/bash
echo "=== Перевірка файлів ==="
ls -la /home/smertnik/bot/*.py
echo "=== Перевірка БД ==="
sqlite3 /home/smertnik/bot/bot.db ".tables"
echo "=== Перевірка лога ==="
tail -20 /home/smertnik/bot/bot.log