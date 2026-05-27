import hmac
from hashlib import sha1

# 你的固定 token
TOKEN = "db3cbf951380f6f4cca6be54427ebfdf"

def hash_hmac(token, body, sha1):
    hmac_code = hmac.new(token.encode(), body.encode(), sha1)
    return hmac_code.hexdigest()

# 调用示例（你接收小红书推送时直接用）
def generate_sign(body):
    return hash_hmac(TOKEN, body, sha1)
