import scrapy
import pandas as pd
from langdetect import detect

dataset = {
    'artist_name': [],
    'music_name': [],
    'genre': [],
    'music_lyric': [],
    'language': []
}

class VagalumeCrawler(scrapy.Spider):
    name = 'vagalume'
    start_urls = [
        'https://www.vagalume.com.br/browse/style/axe.html',
        ]
    
    def parse(self, response):
        global dataset
        artists_urls = []
        genre = response.url.split('/')[-1].split('.')[0]
        for column in response.css('.namesColumn'):
            for line in column.css('li'):
                artists_urls.append(line.css('a::attr(href)').extract_first())
        '''
        artist = { 
            'artist_name': artists_names,
            'artist_url': artists_urls,
            'artist_genre': genre
        }
        pd.DataFrame(artist).to_csv('artists_{}.csv'.format(genre), index=False)
        '''        
        for artist_url in artists_urls:
            yield response.follow(url=artist_url, callback=self.parser_artist, meta={'genre':genre})

        pd.DataFrame(dataset).to_csv('vagalume.csv', index=False)

    def parser_artist(self, response):
        artist_url = response.url
        musics_urls = []
        for item_music in response.css('#alfabetMusicList li .flexSpcBet .lineColLeft'):
            musics_urls.append(item_music.css('a::attr(href)').extract_first())

        for music_url in musics_urls:
            yield response.follow(url=music_url, callback=self.parse_music, meta={'genre':response.meta['genre']})
    
    def parse_music(self, response):
        global dataset
        dataset['artist_name'].append(response.css('.col1-2-1 h2::text').extract_first())
        dataset['music_name'].append(response.css('.col1-2-1 h1::text').extract_first())
        dataset['music_lyric'].append('\n'.join(response.css('.col1-2-1 #lyrics::text').extract()))
        dataset['genre'].append(response.meta['genre'])
        dataset['language'] = detect(' '.join(response.css('.col1-2-1 #lyrics::text').extract()))

        


        