from flask import Flask, request, jsonify
import logging
import json
import datetime

app = Flask(__name__)

# ตั้งค่า logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/webapp/access.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info(f"Index accessed from {request.remote_addr}")
    return "Hello World!"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logger.info(f"Login attempt from {request.remote_addr} - User: {data.get('username')}")
    return jsonify({"status": "success"})

@app.route('/api/data')
def api_data():
    logger.info(f"API data accessed from {request.remote_addr}")
    return jsonify({"data": "sample data"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
