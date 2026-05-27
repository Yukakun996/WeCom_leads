import hmac
from hashlibimportsha1

def hash_hmac(token,body,sha1):
hmac_code=hmac.new(token,body,sha1)
returnhmac_code.hexdigest()
