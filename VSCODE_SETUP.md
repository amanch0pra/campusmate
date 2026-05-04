# 🚀 Running Campus Mate in VS Code

## Quick Start Commands

### 1. Open Project in VS Code
```bash
cd /Users/amanchopra/.gemini/antigravity/scratch/campus-mate
code .
```

### 2. Open Integrated Terminal
- **Mac**: `` Ctrl + ` `` or `View → Terminal`
- **Windows**: `` Ctrl + ` ``

### 3. Install Dependencies (First Time Only)
```bash
pip install -r requirements.txt
```

### 4. Train Model (First Time or After Dataset Changes)
```bash
python3 train_model.py
```

### 5. Run the Application
```bash
python3 app.py
```

### 6. Open in Browser
```
http://localhost:5000
```

---

## ⚡ Quick Commands Reference

### Start Server
```bash
python3 app.py
```

### Stop Server
- Press `Ctrl + C` in terminal

### Restart Server
```bash
# Stop with Ctrl+C, then:
python3 app.py
```

### Retrain Model
```bash
python3 train_model.py
```

---

## 📁 VS Code Recommended Extensions

Install these for better development:

1. **Python** (Microsoft) - Python language support
2. **Pylance** - Python IntelliSense
3. **HTML CSS Support** - HTML/CSS editing
4. **JavaScript (ES6)** - JS code snippets

Install via: `Cmd+Shift+X` → Search → Install

---

## 🔧 VS Code Settings (Optional)

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "python3",
    "python.terminal.activateEnvironment": true,
    "files.autoSave": "afterDelay"
}
```

---

## 🎯 Development Workflow

### Method 1: Using Terminal
1. Open VS Code integrated terminal
2. Run `python3 app.py`
3. Edit files in VS Code editor
4. Server auto-reloads on file changes (debug mode enabled)
5. Refresh browser to see changes

### Method 2: Using Run Configuration
Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask: Run App",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--port=5000",
                "--host=0.0.0.0"
            ],
            "jinja": true
        }
    ]
}
```

Then press `F5` to run with debugger.

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process on port 5000
lsof -ti:5000

# Kill process
kill $(lsof -ti:5000)

# Then restart
python3 app.py
```

### Module Not Found Error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Models Not Found Error
```bash
# Train model first
python3 train_model.py
```

---

## 📊 Check Server Status

**Terminal Output Should Show:**
```
✅ All models loaded successfully!
📊 Dataset size: 118 Q&A pairs
🎯 Modes available: Academic, Admissions...
🚀 Starting Campus Mate Chatbot Server
📍 Server running at: http://localhost:5000
```

**Browser Should Show:**
- Clean chatbot interface
- Mode selection buttons
- Input field with send button
- All features working

---

## ⌨️ Useful VS Code Shortcuts

- **Toggle Terminal**: `` Ctrl + ` ``
- **Command Palette**: `Cmd+Shift+P`
- **Quick Open**: `Cmd+P`
- **Find in Files**: `Cmd+Shift+F`
- **Split Editor**: `Cmd+\`
- **Multi-cursor**: `Cmd+D` (select word)

---

## 🎉 You're All Set!

Your chatbot should now be running on http://localhost:5000

**Test it:**
1. Ask: "What is the fee structure?"
2. Toggle dark mode 🌙
3. Try quick action buttons ⚡
4. Give feedback 👍👎

Happy coding! 🚀
