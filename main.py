from pyrogram import Client
import os,requests
from bs4 import BeautifulSoup
import re
def get_app_version(url):
    title = BeautifulSoup(requests.get(url).text, 'html.parser').title.string
    return re.search(r'(\d+(\.\d+)*)', title).group(1)
url = 'https://liteapks.com/youtube-vanced.html'
ver = get_app_version(url)

api_id = 11319462
api_hash = '155d33dec6ee17ca6135c0a6e01c1129'
bot_token="5781017151:AAH3ErhLd1Up3ig_-yyNF4ys9KWZnYhRlVA"
chat_id = 5501736438

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

url = f'https://cloud.liteapks.com/download/YouTube%20Vanced/YouTube%20v{ver}%20(Premium).apk'
print(url)
local_filename = 'YouTube-premium.apk'

cookies = {
    'cf_clearance': 'J2L4doZCfUuybz_RY7CDDlSgadBh5ICSyognk_O6jS0-1696791560-0-1-928c9adc.fdb7e211.c58dc53c-0.2.1696791560',
    '_gid': 'GA1.2.1989942959.1696791606',
    '_gat_gtag_UA_89527130_15': '1',
    '_ga': 'GA1.1.339436850.1696791606',
    '_ga_D4LJMSH8J7': 'GS1.1.1696803445.2.1.1696803469.0.0.0',
}

headers = {
    'authority': 'cloud.liteapks.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://liteapks.com/download/youtube-vanced-134/1',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
}

# حجم الملف الإجمالي
response = requests.head(url, cookies=cookies, headers=headers)
total_size = int(response.headers.get('content-length', 0))

# بدء عملية التحميل
with requests.get(url, stream=True, cookies=cookies, headers=headers) as req, \
        open(local_filename, 'wb') as file:
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)

with app:
    file_path = 'YouTube-premium.apk'
    caption = f'''
size : [`{os.path.getsize(file_path) / (1024 * 1024):.2f} MB`]
version : '''

    app.send_document(chat_id=chat_id, document=file_path, caption=caption)
    os.remove(file_path)
