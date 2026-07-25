import hashlib
import hmac
import json


def create_signature(payload: str, secret: str):
    # convert JSON payload into string
    payload_string = json.dumps(
        payload,
        separators=(",", ":"),
        sort_keys=True
    )

    #create HMAC SHA256 signature
    signature = hmac.new(
        secret.encode(),
        payload_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature

