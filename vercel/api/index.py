import hmac
import hashlib
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================================
# 🔴 核心配置：请在这里填入你的真实 Token
# ==========================================
XIAOHONGSHU_TOKEN = "db3cbf951380f6f4cca6be54427ebfdf" 

@app.route('/api/index', methods=['POST'])
def handle_xiaohongshu_webhook():
    # -------------------------------------------------------------------
    # 要求 1: 解析POST消息header中的X-Red-Signature参数
    # -------------------------------------------------------------------
    signature_header = request.headers.get('X-Red-Signature')
    
    # 检查是否包含签名以及格式是否正确
    if not signature_header or '=' not in signature_header:
        return jsonify({"code": 400, "msg": "缺少签名或格式不正确"}), 400
    
    # 提取 "sha1=" 后面的真正签名值 (格式为 sha1=bf0a...)
    expected_sign = signature_header.split('=')[1]

    # -------------------------------------------------------------------
    # 要求 2: 解析POST消息的request body（未经反序列化的原始body数据）
    # -------------------------------------------------------------------
    # 使用 request.get_data() 获取原始的 Bytes 数据，绝对不能用 request.json
    raw_body = request.get_data()

    # -------------------------------------------------------------------
    # 要求 3: 以 token 为 secretKey，和 body 数据生成签名，进行校验
    # -------------------------------------------------------------------
    token_bytes = XIAOHONGSHU_TOKEN.encode('utf-8')
    
    # 使用 hmac_sha1 算法计算签名
    hmac_obj = hmac.new(token_bytes, raw_body, hashlib.sha1)
    calculated_sign = hmac_obj.hexdigest()

    # 将计算出的签名与 Header 中传来的签名进行比对
    if calculated_sign != expected_sign:
        # 如果不一致，说明数据被篡改或 Token 不对，拒绝请求
        print(f"安全拦截：签名不一致！预期:{expected_sign} 实际:{calculated_sign}")
        return jsonify({"code": 401, "msg": "签名校验失败"}), 401

    # ==========================================
    # 校验通过！处理真正的业务逻辑
    # ==========================================
    try:
        # 此时确认数据安全，可以安全地反序列化（转为字典）来读取内容了
        data = json.loads(raw_body)
        print("✅ 成功接收到安全的小红书线索数据：", data)
        
        # 💡 你可以在这里提取具体的字段，例如：
        # phone = data.get("data", {}).get("phone_num")
        # print("客户电话：", phone)
        
    except json.JSONDecodeError:
        return jsonify({"code": 400, "msg": "JSON解析异常"}), 400

    # 务必向小红书返回成功状态，否则小红书会判定推送失败并重试
    return jsonify({
        "code": 0,
        "msg": "success"
    }), 200

# 新增一个 GET 路由，专供你在浏览器里测试网站是否存活
@app.route('/api/index', methods=['GET'])
def test_alive():
    return "恭喜你！Vercel 网站存活，并且成功连通了！"
