import scrapy 
import hashlib
import json


class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = [
        'https://bangla.bdnews24.com/'
    ]


    def parse(self, response):
        #get all the article links
        post_link_list = response.xpath('//a[contains(@href, "article")]/@href').extract()
        
        #follow link one by one 
        for post in post_link_list:
            yield scrapy.Request(post, callback=self.parse_post)


    def parse_post(self, response):
        items = {}
        items['title'] = response.css('#news-details-page .print-only::text').get(),
        items['date'] = response.css('#article_notations span:nth-child(2)::text').get(),
        items['content'] = response.css('#storyBody p::text , .article_lead_text .print-only::text').extract()
        
        #get the current page url and encode it 
        hashed_url = self.hashcodes(response.request.url).upper()
        direc = hashed_url + '.json'

        #write single page scraped data onto individual files
        with open(direc, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False)
        
        yield items


    def hashcodes(self, url):
        hc = hashlib.md5(url.encode())
        return hc.hexdigest()