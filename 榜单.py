import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
dict1 = {}


def get_xx(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    ranks = soup.select('span.pc_temp_num')
    titles = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_time')
    # print(times)
    for rank, title, time in zip(ranks, titles, times):
        dict1['排名'] = rank.get_text().replace("\t", '').replace("\n", '')
        title_songer = title.get_text().replace("\t", '').replace("\n", '').split('-')
        dict1['名称'] = title_songer[0].replace(" ", '')
        dict1['歌手'] = title_songer[1].replace(" ", '')
        dict1['时长'] = time.get_text().replace("\t", '').replace("\n", '')
        # print(rank, title, songer, time)
        print(dict1)


if __name__ == '__main__':
    urls = [f'https://www.kugou.com/yy/rank/home/{i + 1}-6666.html?from=rank' for i in range(5)]
    for url in urls:
        get_xx(url)
