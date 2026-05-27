from flask import Flask, request, jsonify

app = Flask(__name__)


# 定义一个接收 POST 请求的路由
@app.route('/api/index', methods=['POST'])
def handle_post():
    # 获取客户端发送的 JSON 数据
    data = request.get_json(silent=True)

    # 这里可以添加你处理数据的逻辑
    # 比如打印出来，或者提取特定字段

    # 返回成功的响应给客户端
    return jsonify({
        "status": "success",
        "message": "Vercel 成功接收到你的 POST 请求！",
        "received_data": data
    }), 200

# Vercel 需要暴露 app 实例，所以不需要写 app.run()