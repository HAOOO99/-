import scrapy
import urllib.parse


class PoiSpider(scrapy.Spider):
    name = 'poi'
    allowed_domains = ['www.poi86.com']
    start_urls = ['https://www.poi86.com/poi/amap/city/370100.html']

    def parse(self, response):
        url_list = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li')
        for i in url_list:
            u = i.xpath("./a/@href").extract_first()
            url = urllib.parse.urljoin(response.url, u)
            yield scrapy.Request(url, callback=self.parse_district)

    def parse_district(self, response):
        elements = response.xpath('//div[@class="panel-body"]/table[@class="table table-bordered table-hover"]/tr')
        # print(elements)
        # item = {}
        for e in elements[1:]:
            item = e.xpath('./td/a/@href').extract_first()
            url = urllib.parse.urljoin(response.url, item)
            # item["type"] = e.xpath('./td/text()').extract()[-1]

            # print(item)
            yield scrapy.Request(url, callback=self.parse_detail)

        next_href = response.xpath('//div[@class="pull-right"]//li/a[contains(text(),"下一页")]/@href').extract_first()

        if next_href is not None:
            next_url = urllib.parse.urljoin(response.url, next_href)
            # print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_district)
        else:
            print("爬取完毕")

    def parse_detail(self,response):
        item = {}
        item["name"] = response.xpath('//div[@class="panel-heading"]/h1/text()').extract_first()
        item["district"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/a/text()')[2].extract()
        item["type"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[5].extract()
        item["coordinate_1"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[6].extract()
        item["coordinate_2"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[7].extract()
        item["coordinate_3"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[8].extract()
        item["coordinate_4"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[9].extract()
        item["coordinate_5"] = response.xpath('//div[@class="panel-body"]/ul[@class="list-group"]/li/text()')[10].extract()

        yield item