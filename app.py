from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({'message': '你好，這是從 JavaScript 獲取的訊息！'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False)
