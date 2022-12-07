import requests
import re
import json
import os
from tqdm import tqdm


class KuGou:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        self.ssurl = 'http://songsearch.kugou.com/song_search_v2'
        self.songs = []
        self.singers = []
        self.hash = []
        self.albumid = []
        self.album_audio_id = []  # SingerId > ID
        self.session = requests.session()
        self.music_name = None
        self.music_singer = None

    def search_songs(self):
        song_name = str(input('请输入要下载的歌曲名称：'))
        search_data = {
            "callback": "jQuery191034642999175022426_1489023388639",
            "keyword": song_name,
            "page": "1",
            "pagesize": "30",
            "userid": "-1",
            "clientver": "",
            "platform": "WebFilter",
            "tag": "em",
            "filter": "2",
            "iscorrection": "1",
            "privilege_filter": "0",
            "_": "1489023388641"
        }
        search = requests.get(self.ssurl, headers=self.headers, params=search_data).text
        search_text = re.findall('jQuery\d*\D\d*[(](.*)[)]', search, re.S)[0]
        search_res = json.loads(search_text)
        select_songs = search_res['data']['lists']
        for i in range(len(select_songs)):
            song = select_songs[i]['SongName'].replace('<em>', '').replace('</em>', '').replace(' ', '')
            singer = select_songs[i]['SingerName'].replace('<em>', '').replace('</em>', '').replace(' ', '')
            hash = select_songs[i]['FileHash']
            albumid = select_songs[i]['AlbumID']
            album_audio_id = select_songs[i]['ID']
            self.songs.append(song)
            self.singers.append(singer)
            self.hash.append(hash)
            self.albumid.append(albumid)
            self.album_audio_id.append(album_audio_id)
        i = 1
        for song_name, sing_name in zip(self.songs, self.singers):
            print(i, song_name, sing_name)
            i += 1
        get_song = int(input('请输入需要下载的歌曲的序号：')) - 1
        hash = self.hash[get_song]
        albumid = self.albumid[get_song]
        album_audio_id = self.album_audio_id[get_song]
        self.music_name = self.songs[get_song]
        self.music_singer = self.singers[get_song]
        self.open_download(hash, albumid, album_audio_id)

    def open_download(self, hash, albumid, album_audio_id):  # 哈希,AlbumID,ID
        open_download_url = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19108036737730556804_1670342099521&hash={hash}&dfid=1bnc2l47gg8g2wTimF3MfCsA&appid=1014&mid=69f326cd7f3ae0b72a615219bd61cdbc&platid=4&album_id={albumid}&album_audio_id={album_audio_id}'
        res = self.session.get(open_download_url).text
        song_link = re.findall('"play_backup_url":"(.+?)","', res, re.S)[0]
        # print(song_link)
        end_song_link = song_link.replace(r"\/", "/")
        self.save_song(end_song_link)

    def save_song(self, end_song_link):
        song_content = self.session.get(end_song_link, headers=self.headers,stream=True)
        total = int(song_content.headers.get('content-length', 0))
        if not os.path.exists(r'.\下载音乐'):  # os模块判断并创建
            os.makedirs(r'.\下载音乐')
        music_name = self.music_name + " " + self.music_singer
        with open(r'.\下载音乐\{}.mp3'.format(music_name), 'wb') as file, tqdm(
                desc=music_name,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in song_content.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
        print('\n')
        print('如果出现只有一分钟的情况，那么这个歌曲是付费歌曲。')

if __name__ == '__main__':
    a = KuGou()
    a.search_songs()
