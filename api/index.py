# index.py
from flask import Flask, jsonify, request
import os
# ... rest of your code

app = Flask(__name__)
# CORS, routes...
API_KEY = os.getenv("OPENWEATHER_API_KEY")
# ✅ This line must be present for Vercel to detect `app`
# (Usually not required but useful if deployment fails)
app = app
