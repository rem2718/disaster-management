import requests
# from app.config import Config

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9UQXpNREkwT1VZNVJETkJRVEU0UlVRMFJrWkVNakEyUTBWQ09UVXhOamN5UTBRNE5EWTJOUSJ9.eyJodHRwczovL2htcWMuY2xvdWQuZW1haWwiOiIyMTk0MTAwMDJAcHN1LmVkdS5zYSIsImlzcyI6Imh0dHBzOi8vYXV0aC5oaXZlbXEuY2xvdWQvIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTczOTQ2Mzk5NzczMzIyMTQ5NjYiLCJhdWQiOlsiaGl2ZW1xLWNsb3VkLWFwaSIsImh0dHBzOi8vaGl2ZW1xLWNsb3VkLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MTM2MjIxOTksImV4cCI6MTcxMzcwODU5OSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImF6cCI6Iklham80ZTMyanh3VXM4QWRGeGd4UW4yVlAzWXdJWlRLIn0.Nb8C3t2AV2f_4RGnn9zrjYsy1sAK4fDyM47rGU9GfYRzsZ7lcoNadr0x6AFU7-cK1OBuDemy7SvBh_PnNoupdaMgga0pOQm5StRQrE9igDf0DEGdqPu514KbXOkqGofUMnFGF20Za6twAMeMKbYfWJc55h-zQb5lH5DCSbox3rXBlJ34oin9f9Wk1AdTXQ30_Wo70WA2qOZrS-JdJg2qDm46OthmIZes_iVmzqTxmbXHhug3_dgoY_v4hH0VhP3IlRyt1pNw1ZcgRw8Ww54AQ63yCDGW4_zIEkUSE0v7hx4fF2dIv_eedjeC5k3um1K2ELjmwaCgSco2uZ9ajZzqSw",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://console.hivemq.cloud",
    "pragma": "no-cache",
    "referer": "https://console.hivemq.cloud/",
    "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "traceparent": "00-bd78e25655a035271962387c88133b29-7939709a53f8ec69-01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}

json_data = {
    "credentials": {
        "username": "ReemNour",
        "password": "Qwe123s@",
        "permissions": [
            "PUBLISH_SUBSCRIBE",
        ],
    },
}
url = "https://api.console.hivemq.cloud/api/v1/clusters/df29475dfed14680a1a57a1c8e98b400/credentials/mqtt"


# response = requests.post(
#     url,
#     headers=headers,
#     json=json_data,
# )

# print(response)

def _login():
    pass

def create_user(username, password):
    pass

def delete_user(username):
    pass

import requests

cookies = {
    '_csrf': 'Ckc03VQ0oxyXHRNjc9CP_U_y',
    'did': 's%3Av0%3A40dbd5e0-c2a7-11ee-9552-97851a35eab6.g8O6bHQCEKFaxegCXkBAN4XW8zTspC%2FugQU%2FuYKOPSA',
    'did_compat': 's%3Av0%3A40dbd5e0-c2a7-11ee-9552-97851a35eab6.g8O6bHQCEKFaxegCXkBAN4XW8zTspC%2FugQU%2FuYKOPSA',
    'ajs_anonymous_id': '%228133b10f-a197-4bcf-ac8a-3fb5ac2b4ac3%22',
    '__cf_bm': '5jJR4.AByL6cr7.O.oA68bV2jxXhCJlJkF_Gu7xAFeU-1713634756-1.0.1.1-ZO5NrRvW1dt1wDJYcVWiDkwk6ysIsxt6eEjh1I3IPqfIQsv5tLXYIJ.IQTQUe58t',
    'auth0': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQDTNK6hnO6dSvhu2t4ZA15ZajyOlgiKKOBDTHTPD7gr2lcI_dBjFu-jmAbBjB9VPFguUQ1gjXmfm1-AFBvawL5KmY29va2llg6dleHBpcmVz1_8iVRAAZif2wq5vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.%2Fy%2BhTm46DI0nNEPBe%2FGLH2w2uFCKkGmxKJJebOdOI5w',
    'auth0_compat': 's%3Av1.gadzZXNzaW9ugqZoYW5kbGXEQDTNK6hnO6dSvhu2t4ZA15ZajyOlgiKKOBDTHTPD7gr2lcI_dBjFu-jmAbBjB9VPFguUQ1gjXmfm1-AFBvawL5KmY29va2llg6dleHBpcmVz1_8iVRAAZif2wq5vcmlnaW5hbE1heEFnZc4PcxQAqHNhbWVTaXRlpG5vbmU.%2Fy%2BhTm46DI0nNEPBe%2FGLH2w2uFCKkGmxKJJebOdOI5w',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    # 'auth0-client': 'eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIiwiZW52Ijp7ImxvY2suanMtdWxwIjoiMTEuMjAuNCIsImF1dGgwLmpzLXVscCI6IjkuMTIuMiJ9fQ==',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://auth.hivemq.cloud',
    'pragma': 'no-cache',
    'referer': 'https://auth.hivemq.cloud/login?state=hKFo2SBxQkJZQWhXa3ptUDBHTFFVeERMMkZfbDZybkRqY1ozSaFupWxvZ2luo3RpZNkgQUNKTS1zMnpoRGtNRXRFaGFET190SFlEUTVBbHd5VHejY2lk2SBJYWpvNGUzMmp4d1VzOEFkRnhneFFuMlZQM1l3SVpUSw&client=Iajo4e32jxwUs8AdFxgxQn2VP3YwIZTK&protocol=oauth2&scope=openid%20profile%20email&audience=hivemq-cloud-api&redirect_uri=https%3A%2F%2Fconsole.hivemq.cloud&response_type=code&response_mode=query&nonce=TWc4VGJMUnQ1fjNTZm9pa2phRmV0WGdOZ2ZLdVIzMFEyUFk3ejZEQUdvbA%3D%3D&code_challenge=R2zR3F52TDHoLlp1JaojvmSuX6Kd9DpFt0v2tzyAXm0&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0%3D',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

json_data = {
    'client_id': 'Iajo4e32jxwUs8AdFxgxQn2VP3YwIZTK',
    'redirect_uri': 'https://console.hivemq.cloud',
    'tenant': 'hivemq-cloud',
    'response_type': 'code',
    'scope': 'openid profile email',
    'state': 'hKFo2SBxQkJZQWhXa3ptUDBHTFFVeERMMkZfbDZybkRqY1ozSaFupWxvZ2luo3RpZNkgQUNKTS1zMnpoRGtNRXRFaGFET190SFlEUTVBbHd5VHejY2lk2SBJYWpvNGUzMmp4d1VzOEFkRnhneFFuMlZQM1l3SVpUSw',
    'nonce': 'TWc4VGJMUnQ1fjNTZm9pa2phRmV0WGdOZ2ZLdVIzMFEyUFk3ejZEQUdvbA==',
    'connection': 'Username-Password-Authentication',
    'username': '219410002@psu.edu.sa',
    'password': 'hiveMQ4ugv',
    'popup_options': {},
    'sso': True,
    'response_mode': 'query',
    '_intstate': 'deprecated',
    '_csrf': 'nD7K70tg-LnuWIh1t3QMVaM3l3tvMxS0tt1k',
    'audience': 'hivemq-cloud-api',
    'code_challenge_method': 'S256',
    'code_challenge': 'R2zR3F52TDHoLlp1JaojvmSuX6Kd9DpFt0v2tzyAXm0',
    # 'auth0Client': 'eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0=',
    'protocol': 'oauth2',
}

response = requests.post('https://auth.hivemq.cloud/usernamepassword/login', headers=headers, json=json_data)

print(response)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"client_id":"Iajo4e32jxwUs8AdFxgxQn2VP3YwIZTK","redirect_uri":"https://console.hivemq.cloud","tenant":"hivemq-cloud","response_type":"code","scope":"openid profile email","state":"hKFo2SBxQkJZQWhXa3ptUDBHTFFVeERMMkZfbDZybkRqY1ozSaFupWxvZ2luo3RpZNkgQUNKTS1zMnpoRGtNRXRFaGFET190SFlEUTVBbHd5VHejY2lk2SBJYWpvNGUzMmp4d1VzOEFkRnhneFFuMlZQM1l3SVpUSw","nonce":"TWc4VGJMUnQ1fjNTZm9pa2phRmV0WGdOZ2ZLdVIzMFEyUFk3ejZEQUdvbA==","connection":"Username-Password-Authentication","username":"219410002@psu.edu.sa","password":"hiveMQ4ugv","popup_options":{},"sso":true,"response_mode":"query","_intstate":"deprecated","_csrf":"nD7K70tg-LnuWIh1t3QMVaM3l3tvMxS0tt1k","audience":"hivemq-cloud-api","code_challenge_method":"S256","code_challenge":"R2zR3F52TDHoLlp1JaojvmSuX6Kd9DpFt0v2tzyAXm0","auth0Client":"eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0=","protocol":"oauth2"}'
#response = requests.post('https://auth.hivemq.cloud/usernamepassword/login', cookies=cookies, headers=headers, data=data)