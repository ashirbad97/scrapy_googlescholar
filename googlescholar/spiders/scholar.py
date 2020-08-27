import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime

API_KEY = 'd461f965fc01ee740a57fb8bb1b0bc01'

def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

class ScholarSpider(scrapy.Spider):
    name = 'scholar'
    allowed_domains = ['scholar.google.com']
    start_urls = ['http://scholar.google.com/']
    

    def start_requests(self):
        queries = ['congenital blind AND (depth perception OR sight restoration OR monocular cues OR binocular cues OR critical period OR Sensory recovery OR brain plasticity)']
        for query in queries:
            url = 'https://scholar.google.com/scholar?start=0' + urlencode({'hl': 'en', 'q': query,'as_ylo': '2000','as_yhi': '2020'})
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'position': 0})

    def parse(self, response):
        print(response.url)
        position = response.meta['position']
        for res in response.xpath('//*[@data-rp]'):
            link = res.xpath('.//h3/a/@href').extract_first()
            temp = res.xpath('.//h3/a//text()').extract()
            if not temp:
                title = "[C] " + "".join(res.xpath('.//h3/span[@id]//text()').extract())
            else:
                title = "".join(temp)
            snippet = "".join(res.xpath('.//*[@class="gs_rs"]//text()').extract())
            cited = res.xpath('.//a[starts-with(text(),"Cited")]/text()').extract_first()
            temp = res.xpath('.//a[starts-with(text(),"Related")]/@href').extract_first()
            related = "https://scholar.google.com" + temp if temp else ""
            num_versions = res.xpath('.//a[contains(text(),"version")]/text()').extract_first()
            published_data = "".join(res.xpath('.//div[@class="gs_a"]//text()').extract())
            position += 1
            item = {'title': title, 'link': link, 'cited': cited, 'relatedLink': related, 'position': position,
                    'numOfVersions': num_versions, 'publishedData': published_data, 'snippet': snippet}
            yield item
        next_page = response.xpath('//td[@align="left"]/a/@href').extract_first()
        if next_page:
            url = "https://scholar.google.com" + next_page
            print(url)
            yield scrapy.Request(get_url(url), callback=self.parse,dont_filter=True,meta={'position': position})





    

