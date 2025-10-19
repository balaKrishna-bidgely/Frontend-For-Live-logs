# 🚀 START HERE - Live Log Viewer

## ⚡ 30-Second Quick Start

### 1. Make sure backend is running
```bash
cd /Users/dipteshdutta/Desktop/DashBoardForLogs
python3 backend.py
```

### 2. Open dashboard
```
http://localhost:5000
```

### 3. Fill the form
- **Jumphost Username**: Select from dropdown (jhnonprodqa, jhuat, jhproductqa, jhmeuat)
- **Service IP Address**: Enter IP (e.g., 10.0.0.1)
- **Log File Path**: Enter full path (e.g., /var/log/bidgely/ingesterJobs/gbUserDataIngester/gbUserDataIngester.log)

### 4. Click "Start Streaming"

Done! 🎉

---

## 📋 Form Fields Explained

### Jumphost Username (Dropdown)
Choose which jumphost to connect to:
- **jhnonprodqa** - Non-production QA environment
- **jhuat** - UAT environment
- **jhproductqa** - Product QA environment
- **jhmeuat** - ME UAT environment

### Service IP Address
The IP address of the service you want to view logs from.
Example: `10.0.0.1`

### Log File Path
Full path to the log file on the service.
Example: `/var/log/bidgely/ingesterJobs/gbUserDataIngester/gbUserDataIngester.log`

---

## 🎯 Common Log Paths

```
# Ingester Jobs
/var/log/bidgely/ingesterJobs/gbUserDataIngester/gbUserDataIngester.log

# Aggregation Services
/var/log/bidgely/aggregationServices/aggregationMessageProcessor/aggregationMessageProcessor.log

# PDF Generation Service
/var/log/bidgely/pdfGenerationService/pdfGeneration/pdfGeneration.log

# Email Services
/var/log/bidgely/emailServices/emailer/emailer.log
```

---

## 🔧 Prerequisites

✅ Backend running: `python3 backend.py`  
✅ .env file with passwords  
✅ Network access to jumphost  
✅ Valid service IP  

---

## ✅ Checklist

- [ ] Backend is running
- [ ] Dashboard loads at http://localhost:5000
- [ ] Form has 3 fields visible
- [ ] Username dropdown shows 4 options
- [ ] Can enter Service IP
- [ ] Can enter Log Path
- [ ] "Start Streaming" button is clickable

---

## 🆘 Quick Troubleshooting

### Backend won't start
```bash
# Kill old process
lsof -ti:5000 | xargs kill -9

# Start new backend
python3 backend.py
```

### Dashboard won't load
- Check backend is running
- Try refreshing browser
- Check http://localhost:5000

### "SSH Connection failed"
- Verify Service IP is correct
- Check .env has passwords
- Verify network access to jumphost

### "SSH_PASSWORD not found"
```bash
# Check .env file
cat .env

# Should show:
# SSH_PASSWORD=1234
# SERVICE_PASSWORD=#Lozer@02
```

---

## 📞 Need Help?

- **Setup Guide**: See `FINAL_SETUP_COMPLETE.md`
- **Quick Reference**: See `QUICK_REFERENCE.md`
- **Troubleshooting**: See `SSH_TIMEOUT_SOLUTIONS.md`

---

## 🎉 You're Ready!

1. Open: **http://localhost:5000**
2. Select username
3. Enter IP and log path
4. Click "Start Streaming"
5. Watch logs in real-time!

---

**Status**: ✅ Ready to Use

**Backend**: Running on http://localhost:5000

**Let's go!** 🚀

