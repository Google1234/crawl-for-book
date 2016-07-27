import scrapy
import urllib2
class write_block:
    def __init__(self,buff_size,filename):
        self.remain=self.size=buff_size
        self.filename=filename
        file=open(self.filename,'w')
        file.close()
        self.buff=''
    def push(self,content):
        if len(content)>self.remain:
            self.buff+=content[:self.remain+1]
            file=open(self.filename,'a')
            file.write(self.buff)
            file.close()
            del self.buff
            self.buff=''
            self.buff+=content[self.remain+1:]
            self.remain=self.size -(len(content)-self.remain)
        else:
            self.buff+=content
            self.remain-=len(content)
    def close(self):
        file=open(self.filename,'a')
        file.write(self.buff)
        file.close()
        del self.buff
        self.buff=''
        self.remain=self.size

class dangdangSpider(scrapy.Spider):
    name = "dangdang"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://promo.dangdang.com/subject.php?pm_id=3319619&tag_id=&sort=priority_asc&p=1"
    ]
    page_id=already_response=id=0
    max_page_id=2361
    write_data_file='../data/book.txt'
    picture_path='../data/pic/'
    write_buff_size=1024*1024*10
    write_block_data = write_block(write_buff_size, write_data_file)
    def parse(self, response):
        while self.page_id<self.max_page_id:
            self.page_id += 1
            url=self.start_urls[0][:-1]+str(self.page_id)
            yield scrapy.Request(url,self.store)
    def store(self,response):
        self.already_response+=1
        bookname=   response.xpath('//ul[@class="pro_list"]/li/p[@class="name"]/a/@title').extract()
        buy=        response.xpath('//ul[@class="pro_list"]/li/p[@class="name"]/a/@href').extract()
        price=      response.xpath('//ul[@class="pro_list"]/li/p[@class="price_d2"]/span/text()').extract()
        pic_url=    response.xpath('//ul[@class="pro_list"]/li/p[@class="pic"]/a/img/@src').extract()
        for i in range(len(bookname)):
            self.id+=1
            self.write_block_data.push(str(self.id)+ '#####')
            self.write_block_data.push(bookname[i].encode('utf-8')+'#####')
            self.write_block_data.push(buy[i].encode('utf-8')+'#####')
            self.write_block_data.push(price[i].encode('utf-8')+'#####'+'\n')
            picture = urllib2.urlopen(pic_url[i])
            image = open(self.picture_path + str(self.id), 'wb')
            image.write(picture.read())
            image.close()
        print "already_response--->",self.already_response
        if self.already_response>=self.max_page_id:
            self.write_block_data.close()