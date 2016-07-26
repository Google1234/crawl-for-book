
import scrapy

class dangdangSpider(scrapy.Spider):
    name = "dangdang"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://promo.dangdang.com/subject.php?pm_id=3319619&tag_id=&sort=priority_asc&p=1"
    ]
    page_id=1
    max_page_id=2361
    bookname=[]
    buy=[]
    price=[]
    def parse(self, response):
        while self.page_id<=self.max_page_id:
            self.page_id+=1
            url=self.start_urls[0][:-1]+str(self.page_id)
            yield scrapy.Request(url,self.store)
    def store(self,response):
        self.bookname.append(response.xpath('//ul[@class="pro_list"]/li/p[@class="name"]/a/@title').extract())
        self.buy.append(response.xpath('//ul[@class="pro_list"]/li/p[@class="name"]/a/@href').extract())
        self.price.append(response.xpath('//ul[@class="pro_list"]/li/p[@class="price_d2"]/span/text()').extract())


