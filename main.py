"""
Created on 2024/1/7
@Author: YZ
"""
import requests
import time
from tqdm import tqdm
from pyquery import PyQuery as pq
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['Anjuke']
collection = db['xiaoqu']
def get_page(url):
    global url_count
    """获取页面源码"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Cookie': 'SECKEY_ABVK=bj/8NG10HRBh0z7uBPDPR4FvoohwiojUhaTglYnDiyw%3D; BMAP_SECKEY=bj_8NG10HRBh0z7uBPDPRw3bV5OgVlXTtfM7a60uYC5XAJ7iu_azzcqwStHb1W_4apsRnCfGDpDVZrOTPI-nCMZnQgbOQ42FM3MFxDnoMWUzV1I2WoaiBuiloOQKXgpsWe09bsSB4BUw5R4Bwq8o2RQ3UZisdovhlQYUew5tPdM51MocEQHZamb1JsdoRiSx; aQQ_ajkguid=BA62A3CA-2135-BFBE-4D8B-686611E2B9D6; ajk-appVersion=; seo_source_type=0; id58=CrIgxGWVOAazb1qWhH3MAg==; 58tj_uuid=a5e004ce-76a8-4ccf-ba79-a3d762393742; als=0; _ga=GA1.2.1614032322.1704284323; new_uv=3; _ga_DYBJHZFBX2=GS1.2.1704346004.3.0.1704346004.0.0.0; sessid=0432A3E4-7991-8F2E-2198-B50C68976242; ctid=15; twe=2; fzq_h=f439b7a82996131bb7593f25aaaa274e_1704615281308_5512e0e990894866a8ad77d68303a088_3063315387; ajk_member_verify=uQxQd%2BRMyDT5fR37iNzK9DsDS5iGcAv9izL2TnzKD6A%3D; ajk_member_verify2=MjI3NDA5NzAyfFJ5cEpNOVh8MQ%3D%3D; fzq_js_anjuke_ershoufang_pc=3124231f637ccc31773647f9ea069107_1704626337441_25; obtain_by=2; fzq_js_anjuke_xiaoqu_pc=b51ed6c851ebcb714056669f48b7acea_1704626375666_23; ajk_member_id=227409702; ajkAuthTicket=TT=45eabf34cc9277c09c7b4ef5d64424dd&TS=1704626376727&PBODY=AR_5OnHYXSuV4Az2Bu5S6WsxML9-46s4lFPiMad6MCoAA2LZkd4lZoLYd7_doGd29iSh_U7B6F924q1cCtqegdRJWBRyxIPW9nx87dhW8nWX9pGfa33LJ53APsze4edHdb7RiA-5TWlhTJhmD9wisepV_Fpo9H5jrsXjWjbXQZI&VER=2&CUID=5W2wnUVnBkt-PePU1fb61Qj5svAO2gEh; xxzl_cid=bd4f3c5b58d342d5b5df15970a188616; xxzl_deviceid=nNEgjhyhWaWTRhrYHFMiprcIS1DdsTrlKEZitMUIYvFmUXCli15aACIIFe1gaIxM'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


def get_houses_url(html):
    """获取一页中的房子URL，只包括以'https://chengdu.anjuke.com/community/view/'开头的链接"""
    doc = pq(html)
    target_div = doc('.list-cell')
    urls = []
    for a in target_div('a').items():
        url = a.attr('href')
        if url.startswith('https://chengdu.anjuke.com/community/view/') and not url.endswith('/jiedu/'):
            urls.append(url)
    return urls


def get_house_info(html):
    """获取房子信息"""
    try:
        doc = pq(html)
    except:
        return
    else:
        title = doc('.community-title .title').text()  # 小区名
        type = doc('.info-list .column-2:nth-child(1) .value').text()  # 物业类型
        time = doc('.info-list .column-2:nth-child(3) .value').text()  # 竣工时间
        owner = doc('.info-list .column-2:nth-child(4) .value').text()  # 产权年限
        number = doc('.info-list .column-2:nth-child(5) .value').text()  # 总户数
        space = doc('.info-list .column-2:nth-child(6) .value').text()  # 建筑面积
        ratio = doc('.info-list .column-2:nth-child(7) .value').text()  # 容积率
        bulid = doc('.info-list .column-2:nth-child(9) .value').text()  # 建筑类型
        commercial = doc('.info-list .column-2:nth-child(10) .value').text()  # 所属商圈
        company = doc('.info-list .column-1:nth-child(17) .value').text()  # 物业公司
        addr = doc('.community-title .sub-title').text()  # 小区地址
        develop = doc('.info-list .column-1:nth-child(19) .value').text()  # 开发商

        scrape_time = datetime.datetime.now().strftime('%Y/%m/%d')  # 抓取时间

        return {
            'title': title,
            'type': type,
            'time': time,
            'owner': owner,
            'number': number,
            'space': space,
            'ratio': ratio,
            'bulid': bulid,
            'commercial': commercial,
            'company': company,
            'addr': addr,
            'develop': develop,
            'scrape_time': scrape_time,
        }


def main():
    """因为只显示50页需要更改m3101（8000元）m3102（8000以上）自己看着设置，还有range(1, 51)如果只有2页那就是range(1, 3)"""
    urls_1 = ['https://chengdu.anjuke.com/community/wuhou/m3106-p' + str(i) + '/#filtersort' for i in range(2, 8)]
    """urls_2 = ['https://chengdu.anjuke.com/community/gaoxin/m3102-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_3 = ['https://chengdu.anjuke.com/community/gaoxin/m3103-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_4 = ['https://chengdu.anjuke.com/community/gaoxin/m3104-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_5 = ['https://chengdu.anjuke.com/community/gaoxin/m3105-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_6 = ['https://chengdu.anjuke.com/community/gaoxin/m3106-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_7 = ['https://chengdu.anjuke.com/community/gaoxin/m3107-p' + str(i) + '/#filtersort' for i in range(1, 51)]"""
    urls = urls_1
    count = 0
    url_count = 0
    for url in urls:
        print('正在抓取：', url)
        html = get_page(url)

        # 检查是否被重定向到登录或验证码页面
        if 'https://callback.58.com/antibot/verifycode?' in html or 'https://www.anjuke.com/captcha-verify/' in html:
            print("遇到登录或验证码验证，暂停操作，问题链接：", url)
            input("请在浏览器中完成人工操作后，按回车键继续...")
            continue  # 跳过当前循环，处理下一个URL

        houses_urls = get_houses_url(html)
        invalid_info_count = 0

        for i, house_url in enumerate(houses_urls):
            house_html = get_page(house_url)
            house_info = get_house_info(house_html)
            if house_info:
                house_info['url'] = house_url
                info = list(house_info.values())
                print('\n' + str(info[4]))
                collection.insert_one(house_info)
            else:
                invalid_info_count += 1

            url_count += 1

            if 1 <= url_count <= 2:
                for _ in tqdm(range(10), desc="暂停中"):
                    time.sleep(2 / 10)
            elif 4 <= url_count <= 5:
                for _ in tqdm(range(10), desc="暂停中"):
                    time.sleep(5 / 10)
            elif 10 <= url_count <= 18:
                for _ in tqdm(range(10), desc="暂停中"):
                    time.sleep(20 / 10)

        count += (len(houses_urls) - invalid_info_count)


if __name__ == '__main__':
    main()
