import hmac
import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔴 重要：请将下面的字符串替换为你在小红书后台获取的真实 Token！
XIAOHONGSHU_TOKEN = "db3cbf951380f6f4cca6be54427ebfdf" 

@app.route('/api/index', methods=['POST'])
def handle_xiaohongshu_webhook():
    # 1. 尝试获取小红书放在 Header 里的签名数据
    signature_header = request.headers.get('X-Red-Signature')
    
    # 如果没有签名，直接拒绝
    if not signature_header:
        return jsonify({"code": 400, "msg": "Missing Signature"}), 400
    
    # 2. 提取 'sha1=' 后面的真实签名值
    try:
        # signature_header 的格式是 "sha1=bf0a961d..."，我们需要等号后面的部分
        expected_sign = signature_header.split('=')[1]
    except IndexError:
        return jsonify({"code": 400, "msg": "Invalid Signature Format"}), 400

    # 3. 获取请求的原始二进制数据 (必须用 get_data()，千万不能先转成 JSON)
    raw_body = request.get_data()

    # 4. 使用你的 Token 和原始数据，按照小红书的规则计算 HMAC-SHA1 签名
    token_bytes = XIAOHONGSHU_TOKEN.encode('utf-8')
    hmac_obj = hmac.new(token_bytes, raw_body, hashlib.sha1)
    calculated_sign = hmac_obj.hexdigest()

    # 5. 比对我们算出的签名和小红书发来的签名是否一致
    if calculated_sign != expected_sign:
        # 签名不一致，说明不是小红书官方发来的，或者是 Token 填错了
        print(f"签名校验失败! 小红书发来的: {expected_sign}, 我们计算的: {calculated_sign}")
        return jsonify({"code": 401, "msg": "Sign Error"}), 401

    # 6. 签名校验通过！现在可以安全地解析小红书发来的 JSON 数据了
    try:
        data = json.loads(raw_body)
        print("✅ 成功接收并校验小红书数据：", data)
        
        # --- 在这里，你可以写将 data 存入数据库或处理业务的逻辑 ---
        
    except json.JSONDecodeError:
        return jsonify({"code": 400, "msg": "Invalid JSON Body"}), 400

    # 7. 给小红书返回成功的响应，告诉它我们收到了（必须返回 200 状态码）
    return jsonify({
        "code": 0,
        "msg": "success"
    }), 200
