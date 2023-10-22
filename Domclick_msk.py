from bs4 import BeautifulSoup 
import requests
import time 
import pandas as pd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'ns_session=62c2d63c-5b04-4b88-81ec-9c6d417f1112; ftgl_cookie_id=e5d3ac800c5577c26d505a8229f973a9; RETENTION_COOKIES_NAME=a53bdc8636024270be0c2f2f42b3c518:3dTRavrtRMh2jro4dq2ZMQIn4OU; sessionId=8da0993039554ed29ceacad3b4bb51f5:zBHHoziF3PjqNxWp1Du3qC9Mopc; UNIQ_SESSION_ID=642fb90c6cfb4979831f1a18cae155b2:XZcbakjsTLbmIvj1dLzIhp5IfCU; _gcl_au=1.1.1798427841.1697133755; logoSuffix=; _ym_uid=1697133755992986490; _ym_d=1697133755; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; ___dmpkit___=907e926c-f042-4b56-aeb7-e3899d1f152e; adtech_uid=21504db0-0055-46c2-8ed1-0bf28ad38b82%3Adomclick.ru; top100_id=t1.7711713.1032984395.1697133755973; _ga=GA1.1.1630670116.1697133756; tmr_lvid=63f22f4e83dc0b2d92648cb84d40d1c6; tmr_lvidTS=1697133756347; auto-definition-region=false; currentSubDomain=; regionAlert=1; cookieAlert=1; autoDefinedRegion=ac7f923e-9a06-46c3-8f21-c72ae4ea9cac:9930cc20-32c6-4f6f-a55e-cd67086c5171:%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B3%D0%BE%D1%80%D1%81%D0%BA:krasnogorsk; qrator_jsr=1697633637.137.5hoXaHDGSoMWA0jK-ghqilq1m91eb1jqri2adrv2gdvsjku7c-00; qrator_jsid=1697633637.137.5hoXaHDGSoMWA0jK-islt70o14bonjkahjekbj957f9gdn6c4; qrator_ssid=1697633638.723.hqobcMTfK1Pd8nTj-25vd9ci84rfvs9p3l00dp3kseagj3to6; _visitId=9e22246d-ce66-4723-9be3-dee7f88b8bb4-f4f0dcc432ac8ba6; dtCookie=v_4_srv_13_sn_B69F3E0A96D7E09B48EF44310D5D6A18_perc_100000_ol_0_mul_1_app-3Aca312da39d5a5d07_1_rcs-3Acss_0; currentRegionGuid=9930cc20-32c6-4f6f-a55e-cd67086c5171; currentLocalityGuid=9930cc20-32c6-4f6f-a55e-cd67086c5171; _ym_isad=1; last_visit=1697622880691%3A%3A1697633680691; _ga_NP4EQL89WF=GS1.1.1697633641.23.1.1697633680.21.0.0; regionName=9930cc20-32c6-4f6f-a55e-cd67086c5171:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; tmr_detect=0%7C1697633683785; t3_sid_7711713=s1.1131106517.1697633641293.1697633740687.31.13; tmr_reqNum=336',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}




# Функция для получения информации о доме (по ссылке)

def all_info_room(url):
    
    res = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    
    # Цена квартиры
    p = []
    try:
        price = soup.find('div', class_ = 'l2ytJ').text
        p.append(price)
        print(price)
        res.append(p)
    except:
        p.append(None)
        res.append(p)


    # Какое метро рядом
    metro = []
    transport = soup.find_all('a', class_ = 'JFWsg QfBR5')
    for t in transport:
        metro.append(t.text)

    print(metro)
    res.append(metro)



    # Минут до метро
    metro_minutes = []
    minutes = soup.find_all('span', class_ = 'uY_Z9')
    for m in minutes:
        metro_minutes.append(m.text)

    print(metro_minutes)
    res.append(metro_minutes)


    # Информация о квартире  
    apartment_info = {}

    info = soup.find_all('span', class_='ffG_w')
    name = soup.find_all('span', class_='gqoOy')

    for n, i in zip(name, info):
        apartment_info[n.text] = i.text

    print(apartment_info)
    res.append([apartment_info])


    # Адресс где находится
    addres = soup.find_all('a', class_ = 'r3VUA')
    addres_lst = []
    for a in addres:
        addres_lst.append(a.text)

    concatenated_address = ""
    # Цикл для конкатенации элементов списка с добавлением пробелов
    for part in addres_lst:
        concatenated_address += part + " "
    # Удаляем лишний пробел в конце строки
    concatenated_address = concatenated_address.strip()

    print(concatenated_address)
    res.append([concatenated_address])



    # Дополнительная информация 
    dop_info = []
    dop = soup.find_all('div', class_ = 'lDjMF')
    for d in dop:
        dop_info.append(d.text)

    print(dop_info)
    res.append(dop_info) 

    return res




# Функция для получения ссылок по каждому дому
def list_links(url):
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a', class_='NO6xYZ YIdfYp P3YKnR')

    for link in links:
        l = link.get('href')
        # Выводим ссылку 
        print(l)

        extracted_links.append(l)
        time.sleep(2)

    return extracted_links








df = pd.DataFrame()
# Список ссылок которые получили 
extracted_links = []

# Цикл для парсинга нескольких страниц
for num in range(0, 1961, 20):
    url = f'https://domclick.ru/search?deal_type=sale&category=living&offer_type=flat&aids=2298&address=9930cc20-32c6-4f6f-a55e-cd67086c5171&rooms=1&offset={num}'
    l = list_links(url)


for url in l:
    lst = all_info_room(url)
    # Добавляем значение к DataFrame
    df = df.append({'price': lst[0],
                    'metro' : lst[1],
                    'minutes': lst[2],
                    'apartment_info': lst[3],
                    'address': lst[4],
                    'additional_info': lst[5],
                    'links': url}, ignore_index=True)

    df.to_excel('Мособласть 1 комната.xlsx', index=False)

    time.sleep(3)

print(df)