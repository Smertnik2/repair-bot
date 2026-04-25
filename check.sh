#!/bin/bash
echo "Checking bot files..."
files=("main.py" "handlers.py" "ui.py" "texts.py" "config.py" "database.py" "admin.py")
for f in "${files[@]}"; do
    if [ -f "$f" ]; then
        echo "✅ $f"
    else
        echo "❌ $f missing"
    fi
done
echo "Starting bot..."
python main.py
