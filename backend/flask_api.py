from flask import Flask, jsonify
from flask_cors import CORS
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Web3 connection
rpc_url = os.getenv("SEPOLIA_RPC_URL", 
    "https://ethereum-sepolia-rpc.publicnode.com")
w3 = Web3(Web3.HTTPProvider(rpc_url))

@app.route('/api/status', methods=['GET'])
def status():
    connected = w3.is_connected()
    block = w3.eth.block_number if connected else 0
    return jsonify({
        'status': 'operational',
        'blockchain': 'connected' if connected else 'disconnected',
        'network': 'sepolia',
        'block_number': block,
        'message': 'GFLO Backend Running'
    })

@app.route('/api/paths', methods=['GET'])
def paths():
    return jsonify({
        'paths': [
            {
                'id': 1,
                'name': 'Sovereign',
                'xp_required': 50000,
                'eth_fee': 0.001,
                'tier': 1,
                'emoji': '🌊'
            },
            {
                'id': 2,
                'name': 'Reformer', 
                'xp_required': 100000,
                'eth_fee': 0.01,
                'tier': 2,
                'emoji': '🎨'
            },
            {
                'id': 3,
                'name': 'Praxis',
                'xp_required': 200000,
                'eth_fee': 0.1,
                'tier': 3,
                'emoji': '🔧'
            }
        ]
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    connected = w3.is_connected()
    return jsonify({
        'total_users': 0,
        'active_paths': 0,
        'block_number': w3.eth.block_number if connected else 0,
        'network': 'sepolia',
        'treasury_balance': '0 ETH',
        'total_xp_awarded': 0
    })

@app.route('/api/ai/status', methods=['GET'])
def ai_status():
    return jsonify({
        'ai_oracle': 'initializing',
        'axioms_loaded': 3,
        'last_check': 'never',
        'fraud_detections': 0
    })

if __name__ == '__main__':
    print("🚀 GFLO Flask API Starting...")
    print(f"✅ Blockchain: {'Connected' if w3.is_connected() else 'Disconnected'}")
    print(f"📦 Block: {w3.eth.block_number if w3.is_connected() else 'N/A'}")
    print("🌐 API running on http://localhost:5000")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
