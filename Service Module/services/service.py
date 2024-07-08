from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/service/transaction', methods=['GET'])
def transaction():
    # Transaction logic here
    pass

@app.route('/service/wallet', methods=['POST'])
def wallet():
    # Wallet service logic here
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
