# index.py
from flask import Flask, jsonify, request
# ... rest of your code

app = Flask(__name__)
# CORS, routes...

# ✅ This line must be present for Vercel to detect `app`
# (Usually not required but useful if deployment fails)
app = app
