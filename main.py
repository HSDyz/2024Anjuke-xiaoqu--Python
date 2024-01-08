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
        'Cookie': 'Cookie自己获取，不懂看图片或者百度'
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
    """因为只显示50页需要更改m3101（8000元）m3102（8000以上）自己看着设置，还有range(1, 51)如果只有2页那就是range(1, 8)"""
    """                                              注意    注意                                              注意 """
    urls_1 = ['https://chengdu.anjuke.com/community/jinniu/m3103-p' + str(i) + '/#filtersort' for i in range(14, 29)]
    """urls_2 = ['https://chengdu.anjuke.com/community/gaoxin/m3102-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_3 = ['https://chengdu.anjuke.com/community/gaoxin/m3103-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_4 = ['https://chengdu.anjuke.com/community/gaoxin/m3104-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_5 = ['https://chengdu.anjuke.com/community/gaoxin/m3105-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_6 = ['https://chengdu.anjuke.com/community/gaoxin/m3106-p' + str(i) + '/#filtersort' for i in range(1, 51)]
    urls_7 = ['https://chengdu.anjuke.com/community/gaoxin/m3107-p' + str(i) + '/#filtersort' for i in range(1, 51)]"""
    urls = urls_1
    count = 0

    for url in urls:
        page_processed = False  # 标记当前页面是否处理完成
        url_count = 0  # 重置url计数器

        while not page_processed:  # 当前页面未处理完成时持续尝试
            print('正在抓取：', url)
            html = get_page(url)

            # 检查是否被重定向到登录或验证码页面
            if 'https://callback.58.com/antibot/verifycode?' in html or 'https://www.anjuke.com/captcha-verify/' in html:
                print("遇到登录或验证码验证，暂停操作，问题链接：", url)
                input("请在浏览器中完成人工操作后，按回车键继续...")
                continue  # 重新尝试抓取当前页面

            houses_urls = get_houses_url(html)
            invalid_info_count = 0

            for house_url in houses_urls:
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

                # 根据url_count的值决定暂停时间
                pause_seconds = 0
                if url_count == 2:
                    pause_seconds = 2  # 暂停 2 秒
                elif url_count == 6:
                    pause_seconds = 5  # 暂停 5 秒
                elif url_count == 15:
                    pause_seconds = 8  # 暂停 8 秒
                elif url_count == 22:
                    pause_seconds = 10  # 暂停 10 秒

                # 使用进度条显示暂停
                if pause_seconds > 0:
                    with tqdm(total=100, desc="暂停中") as pbar:
                        for i in range(100):
                            time.sleep(pause_seconds / 100)
                            pbar.update(1)

                if url_count >= 30:
                    url_count = 0  # 当url_count达到30，重置计数器

            count += (len(houses_urls) - invalid_info_count)
            page_processed = True  # 当前页面处理完成，退出循环


if __name__ == '__main__':
    main()
