import scrapy
import pandas as pd

dataset = {
    'artist_name': [],
    'genre': [],
    'music_tite': [],
    'music_lyric': []
}

def is_portuguese(response):
    for option in response.css('#songTab li'):
        if option.css('a::text').extract_first().strip() == 'Original' and option.css('a i').xpath('@class').extract_first().strip() != 'lang langBg-bra':
            return False
    return True

def is_instrumental(response):
    return response.css('.instrumental-icon').extract_first() != None

class VagalumeCrawler(scrapy.Spider):
    name = 'vagalume'
    start_urls = [
        'https://www.vagalume.com.br/browse/style/axe.html',
        'https://www.vagalume.com.br/browse/style/bossa-nova.html',
        'https://www.vagalume.com.br/browse/style/forro.html',
        'https://www.vagalume.com.br/browse/style/funk-carioca.html',
        'https://www.vagalume.com.br/browse/style/gospel.html',
        'https://www.vagalume.com.br/browse/style/infantil.html',
        'https://www.vagalume.com.br/browse/style/jovem-guarda.html',
        'https://www.vagalume.com.br/browse/style/mpb.html',
        'https://www.vagalume.com.br/browse/style/pagode.html',
        'https://www.vagalume.com.br/browse/style/samba.html',
        'https://www.vagalume.com.br/browse/style/sertanejo.html',
        'https://www.vagalume.com.br/browse/style/velha-guarda.html',
        'https://www.vagalume.com.br/browse/style/pop.html',
        'https://www.vagalume.com.br/browse/style/rock.html'
    ]
    
    def parse(self, response):
        global dataset
        artists_urls = []
        genre = response.url.split('/')[-1].split('.')[0]
        for column in response.css('.namesColumn'):
            for line in column.css('li'):
                artists_urls.append(line.css('a::attr(href)').extract_first())
        
        for artist_url in artists_urls:
            yield response.follow(url=artist_url, callback=self.parser_artist, meta={'genre':genre})

    def parser_artist(self, response):
        artist_url = response.url
        musics_urls = []
        for item_music in response.css('#alfabetMusicList li .flexSpcBet .lineColLeft'):
            musics_urls.append(item_music.css('a::attr(href)').extract_first())

        for music_url in musics_urls:
            yield response.follow(url=music_url, callback=self.parse_music, meta={'genre':response.meta['genre']})
    
    def parse_music(self, response):
        global dataset
        if is_portuguese(response) and not is_instrumental(response):
            dataset['artist_name'].append(response.css('.col1-2-1 h2 a::text').extract_first().strip())
            dataset['music_title'].append(response.css('.col1-2-1 h1::text').extract_first().strip())
            dataset['music_lyric'].append('\n'.join(response.css('.col1-2-1 #lyrics::text').extract()))
            dataset['genre'].append(response.meta['genre'])

    def closed(self, reason):
        global dataset
        pd.DataFrame(dataset).to_csv('vagalume.csv', index=False)
