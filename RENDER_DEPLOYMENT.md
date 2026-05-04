# Campus Mate - Render Deployment Guide

## Quick Deploy to Render

### 1. Create Render Account
- Go to https://render.com
- Sign up with GitHub account

### 2. Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository: `Campus-Mate-LPU`
- Click "Connect"

### 3. Configure Service

**Basic Settings:**
- Name: `campus-mate` (or your choice)
- Region: Choose closest to you
- Branch: `main`
- Root Directory: Leave blank
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command: 
  ```
  pip install -r requirements.txt && python3 train_model.py
  ```

- Start Command:
  ```
  gunicorn app:app
  ```

**Instance Type:**
- Free tier is sufficient for demo/academic project

### 4. Environment Variables (Optional)
None required for basic deployment

### 5. Deploy
- Click "Create Web Service"
- Wait 3-5 minutes for build
- Your app will be live at: `https://campus-mate.onrender.com`

## 🎯 What Happens During Deployment

### Build Phase:
1. Installs all Python packages from `requirements.txt`
2. Downloads NLTK data
3. Trains the ML model
4. Saves model files to `models/` directory

### Start Phase:
1. Gunicorn starts the Flask app
2. App becomes accessible via Render URL
3. Auto-restarts if crashes

## ⚠️ Important Notes

### Free Tier Limitations:
- **Spins down after 15 mins of inactivity**
- First request after sleep: 30-50 seconds to wake up
- Subsequent requests: Fast (<200ms)

### Model Files:
- Models retrain on each deploy (takes ~30 seconds)
- Alternatively, commit models to Git (faster deploy but larger repo)

### To Keep Models Persistent:
Remove `models/*.pkl` from `.gitignore`, then:
```bash
git add models/
git commit -m "Add trained models"
git push
```

Then change Build Command to just:
```
pip install -r requirements.txt
```

## 🔧 Troubleshooting

### Build Fails:
- Check `requirements.txt` has all dependencies
- Ensure Python 3.9+ specified
- Check build logs in Render dashboard

### App Crashes:
- Check "Logs" tab in Render
- Verify `app.py` has no errors
- Ensure models directory exists

### Slow First Load:
- Normal for free tier (spin up time)
- Upgrade to paid tier for always-on instance

## 📊 Monitoring

- **Logs**: Real-time in Render dashboard
- **Metrics**: CPU, Memory usage visible
- **Events**: Deploy history tracked

## 🚀 After Deployment

Test your live app:
1. Visit your Render URL
2. Try all features (dark mode, feedback, quick actions)
3. Test on mobile devices
4. Share link for demo!

---

**Your app will be live at**: `https://your-app-name.onrender.com`

Replace `your-app-name` with whatever name you chose in step 3.

Good luck with deployment! 🎉
