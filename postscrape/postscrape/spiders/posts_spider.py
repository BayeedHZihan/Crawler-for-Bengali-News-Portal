import scrapy 
import hashlib

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
            hashed_url = self.hashcodes(post).upper()
            self.direc = hashed_url + '.json'
            yield response.follow(post, callback=self.parse_post)

    def parse_post(self, response):
        items = {}
        items['title'] = response.css('#news-details-page .print-only::text').get(),
        items['date'] = response.css('#article_notations span:nth-child(2)::text').get(),
        items['content'] = response.css('#storyBody p::text , .article_lead_text .print-only::text').extract()
        with open(self.direc, 'w', encoding="utf-8") as f:
            f.write(str(items))
        yield items

    def hashcodes(self, string):
        hc = hashlib.md5(string.encode())
        return hc.hexdigest()