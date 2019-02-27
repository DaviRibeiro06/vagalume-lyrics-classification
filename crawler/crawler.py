import scrapy
import pandas as pd

class VagalumeCrawler(scrapy.Spider):
    
    dataset = {
        'artist_name': [],
        'music_name': [],
        'genre': [],
        'music_lyric': [],
        'language': []
    }

    name = 'vagalume'
    start_urls = [
        'https://www.vagalume.com.br/browse/style/axe.html',
        'https://www.vagalume.com.br/browse/style/bossa-nova.html',
        'https://www.vagalume.com.br/browse/style/forro.html'
        ]
    
    def parse(self, response):
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
            yield response.follow(url=artist_url, callback=self.parser_artist)

        pd.DataFrame(VagalumeCrawler.dataset).to_csv('vagalume.csv', index=False)

    def parser_artist(self, response):
        artist_url = response.url
        musics_urls = []
        for item_music in response.css('#alfabetMusicList li .flexSpcBet .lineColLeft'):
            musics_urls.append(item_music.css('a::attr(href)'))

        for music_url in musics_urls:
            yield response.follow(url=music_url, callback=self.parse_music)
    
    def parse_music(self, response):
        VagalumeCrawler.dataset['artist_name'].append(response.css('.col1-2-1 h2::text').extract_first())
        VagalumeCrawler.dataset['music_name'].append(response.css('.col1-2-1 h1::text').extract_first())
        VagalumeCrawler.dataset['music_lyric'].append(response.css('.col1-2-1 #lyrics::text').extract_first())
        #VagalumeCrawler.dataset['genre'].append(response.meta['genre'])
        VagalumeCrawler.dataset['genre'].append(None)
        VagalumeCrawler.dataset['language'].append(None)

        


        