import scrapy
from scrapy.http import headers
from ..items import Petpros1Item

def locsort(loc):
    loclist = []
    for i in range(2):
        loc[i] = loc[i].strip()
        loclist.append(loc[i].split('= "')[1])
    return loclist


class Petproscrape1Spider(scrapy.Spider):
    name = 'petproscrape1'
    allowed_domains = ['petpros.net']
    start_urls = ['http://petpros.net/']

    def start_requests(self):
        url = 'https://shop.petpros.net/stores/search/?page={}&latitude=&longitude=&keyword=10010'
        headers = {
            'Host': 'shop.petpros.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers'
        }
        for i in range(1,3):
            yield scrapy.Request(url=url.format(i), callback=self.parse_page, headers=headers)

    def parse_page(self,response):
        products = response.xpath('//a[@class="pull-right"]/@href').extract()
        headers = {
            'Host': 'shop.petpros.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers'
        }
        for product_url in products:
            yield scrapy.Request(url='https://shop.petpros.net'+ product_url, callback=self.parse_product, headers= headers)


    def parse_product(self, response):
        items = Petpros1Item()
        addr = response.xpath('//div[@class="stre-icns-dtl"]/text()').extract()
        email = addr[-1].strip()  
        addr = addr[-2].strip()
        addr = addr.split(', ')
        loc = response.xpath('//div[@class="location-detail-map"]/script/text()').extract()
        loc = loc[0].split(';')[0:2]
        loc = locsort(loc)
        phone = response.xpath('//div[@class="stre-icns-dtl arial-font"]/text()').extract()
        # StoreName = response.xpath('//div[@class="col-sm-8"]/h3[@class="desc-store"]/text()').extract() 
        timing = response.xpath('//div[@class="row stre-opn-tmngs"]/div/text()').extract() 
        StoreTimings = []
        for m in range(0,21,3):
            StoreTimings.append(timing[m] +' ' + timing[m+1] +' ' +timing[m+2])
        items = {
            # 'StoreID':, 
            'StoreName': 'Pet Pros ' + addr[-3], 
            'Street': ','.join(addr[0:-3]), 
            'City': addr[-3], 
            'State': addr[-2], 
            'StoreTiminings': ' | '.join(StoreTimings),
            'Phone': ''.join(phone).strip(),
            'EmailId' : email,
            'Latitude': loc[0].replace('"',''),
            'Longitude': loc[1].replace('"',''),
            'ZipCode' : addr[-1]
            }
        yield items



# class="col-sm-5 col-md-4  stre-pl"
# https://shop.petpros.net/stores/search/?page={}&latitude=&longitude=&keyword=10010
# $x('//li[@class="list-bgico"]/a[@tabindex="0"]/text()') address email
# $x('//li[@class="list-bgico arial-font"]/a[@tabindex="0"]/text()') phone
# $x('//div[@class="row stre-opn-tmngs"]/div/text()' storetiming
# $x('//div[@class="col-sm-8"]/h3[@class="desc-store"]/text()') storename
# '//div[@class="stre-icns-dtl"]/text()' address email
# $x('//div[@class="stre-icns-dtl arial-font"]/text()') phone
# '//div[@class="location-detail-map"]/script/text()' loc 