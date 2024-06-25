import requests

base_url = "http://localhost:8000"

recipi = "チョコレートケーキ"
allergy_list = ["卵", "乳", "小麦"]

# パラメータをクエリに変換
params = {
    "recipi": recipi,
    "allergy_list": allergy_list,
}


# GETリクエストを送信
print(params)
response = requests.get(base_url, params=params)


print(f"Status code: {response.status_code}")

if response.status_code == 200:
    print("Response JSON:")
    print(response.json())
else:
    print("Failed to get a response")
