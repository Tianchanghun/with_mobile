import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests

# apiKey, apiSecret 입력 필수
apiKey = 'NCSAVCBCDEFG9LQP'
apiSecret = 'XSPJQ0B9GHI3EVERY17R34Q5IS2BODYHI'

# 아래 값은 필요시 수정
protocol = 'https'
domain = 'api.solapi.com'
prefix = ''

def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def get_headers(apiKey, apiSecret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    return {
      'Authorization': 'HMAC-SHA256 ApiKey=' + apiKey + ', Date=' + date + ', salt=' + salt + ', signature=' +
                             get_signature(apiSecret, data),
      'Content-Type': 'application/json; charset=utf-8'
    }

def getUrl(path):
  url = '%s://%s' % (protocol, domain)
  if prefix != '':
    url = url + prefix
  url = url + path
  return url

def sendMany(data):
  return requests.post(getUrl('/messages/v4/send-many'), headers=get_headers(apiKey, apiSecret), json=data)

# 한번 요청으로 1만건의 메시지 발송이 가능합니다.
if __name__ == '__main__':
  data = {
    'messages': [

      # 알림톡 발송
      {
        'to': '01085213713',
        'from': '01073395062',
        'text': '#{이름}님 #{년월일} 입찰 정보를 전달 합니다.#{입찰정보}',
        'kakaoOptions': {
          'pfId': 'KA01PF200323182344986oTFz9CIabcx',
          'templateId': 'KA01TP210324044418025IKNOZCxWiy3',
          'buttons': [
            {
              'buttonType': 'MD', # 상담요청하기 (상담요청하기 버튼을 누르면 메시지 내용이 상담원에게 그대로 전달됩니다.)
              'buttonName': '상담요청하기'
            }
          ]
        }
      }
      # ...
      # 1만건까지 추가 가능
    ]
  }
  res = sendMany(data)
  print(json.dumps(res.json(), indent=2, ensure_ascii=False))