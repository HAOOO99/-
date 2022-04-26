import urllib.parse
from io import BytesIO
import requests as req
import scrapy
from PIL import Image
import pytesseract

from tobacco_data.items import yanyue, Comment

class YanyueSpider(scrapy.Spider):
    name = 'yanyue'
    allowed_domains = ['yanyue.cn']
    start_urls = ['https://www.yanyue.cn/tobacco']

    def parse(self, response):
        mainland = response.xpath('//div[@id="mainland"]/ul/li/ul/li/a/@href').extract()  # 大陆品牌
        for i in mainland:
            url = 'https://www.yanyue.cn' + i
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response):
        urls = response.xpath('//div[@class="name2"]/a/@href')
        for i in urls:
            url = 'https://www.yanyue.cn' + i.get()
            yield scrapy.Request(url, callback=self.parse_detail)

        next_href = response.xpath(
            '//a[@class="page-link"][contains(text(),"下一页")]/@href').extract_first()
        if next_href is not None:
            next_url = urllib.parse.urljoin(response.url, next_href)
            yield scrapy.Request(next_url, callback=self.parse_product)
        else:
            print("爬取完毕")

    def parse_detail(self, response):
        # 放的是数值和url
        item = {}
        list1 = []
        # 标题
        qq = response.xpath('//div[@id="basicinfo"]/ul/li[@class="info_title"]/text()').getall()
        hh = response.xpath('//div[@id="basicinfo"]/ul/li[@class="info_content"]')
        for i in hh:
            if i.xpath('./img/@src'):

                list1.append(i.xpath('./img/@src').get())
            elif i.xpath('./font/text()'):
                list1.append(i.xpath('./font/text()').get())
            elif i.xpath('./span/img/@src'):
                list1.append(i.xpath('./span/img/@src').get())
            else:
                list1.append(i.xpath('./text()').get())
        # 口味，外观，性价比，综合
        pingfen = response.xpath('//div[@class="subcontent3"]/div[@class="a"]/text()').getall()
        for i in pingfen:
            qq.append(i.strip())
        # 口味，外观，性价比，综合 具体数值
        fenzhi = response.xpath('//div[@class="subcontent3"]/div[@class="c"]/text()').getall()
        for i in fenzhi:
            list1.append(i)

        item = yanyue()
        map = dict(zip(qq, list1))

        item["name"] = response.xpath("//div[@class='edition_wrap']//h3/text()").extract_first()
        item["brand"] = map.get("品牌:")

        if map.get("产品类型:") == "雪茄":
            if map.get("雪茄类型:") is None:
                item["type"] = map.get("产品类型:")
            else:
                item["type"] = map.get("雪茄类型:")

            if map.get("公制长度:") is None:
                item["length"] = None
            else:
                res = req.get(map.get("公制长度:"))
                image = Image.open(BytesIO(res.content))
                item["length"] = "".join(pytesseract.image_to_string(image, lang="font", config="--psm 8").split())

        else:
            item["type"] = map.get("类型:")
            # print(map.get("长度:"))
            if map.get("长度:") is None:
                item["length"] = None
            else:
                res = req.get(map.get("长度:"))

                image = Image.open(BytesIO(res.content))
                item["length"] = "".join(pytesseract.image_to_string(image, lang="font", config="--psm 8").split())


        # item["tar_content"] = map.get("焦油:")  # url
        if map.get("焦油:") is None:
            item["tar_content"] = None
        else:
            res1 = req.get(map.get("焦油:"))
            image1 = Image.open(BytesIO(res1.content))
            item["tar_content"] = "".join(pytesseract.image_to_string(image1, lang="font", config="--psm 8").split())

        # item["nicotine"] = map.get("烟碱:")  # url
        if map.get("烟碱:") is None:
            item["nicotine"] = None
        else:
            res = req.get(map.get("烟碱:"))
            image = Image.open(BytesIO(res.content))
            item["nicotine"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["CO"] = map.get("一氧化碳:")  # url
        if map.get("一氧化碳:") is None:
            item["CO"] = None
        else:
            res = req.get(map.get("一氧化碳:"))
            image = Image.open(BytesIO(res.content))
            item["CO"] = "".join(pytesseract.image_to_string(image, lang="font",config="--psm 8").split())

        item["dimension"] = response.xpath(
            '//div[@id="basicinfo"]//li[@class="info_content_lg"]/span/text()').extract_first()

        # item["perimeter"] = map.get("周长:")  # url
        if map.get("周长:") is None:
            item["perimeter"] = None
        else:
            res = req.get(map.get("周长:"))
            image = Image.open(BytesIO(res.content))
            # print("周长", pytesseract.image_to_string(image,lang="font",  config="--psm 8"))
            item["perimeter"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["filter_length"] = map.get("过滤嘴长:")  # url
        if map.get("过滤嘴长:") is None:
            item["filter_length"] = None
        else:
            res = req.get(map.get("过滤嘴长:"))
            image = Image.open(BytesIO(res.content))
            item["filter_length"] = "".join(pytesseract.image_to_string(image, lang="font",config="--psm 8").split())

        item["package"] = map.get("包装形式:")
        item["main_color"] = map.get("主颜色:")
        item["side_color"] = map.get("副颜色:")

        # item["number"] = map.get("每盒数量:")  # url
        if map.get("每盒数量:") is None:
            item["number"] = None
        else:
            res = req.get(map.get("每盒数量:"))
            image = Image.open(BytesIO(res.content))
            item["number"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["single_price"] = map.get("小盒价格:")  # url
        if map.get("小盒价格:") is None:
            item["single_price"] = None
        else:
            res = req.get(map.get("小盒价格:"))
            image = Image.open(BytesIO(res.content))
            item["single_price"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["package_price"] = map.get("条装价格:")  # url
        if map.get("条装价格:") is None:
            item["package_price"] = None
        else:
            res = req.get(map.get("条装价格:"))
            image = Image.open(BytesIO(res.content))
            item["package_price"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["single_code"] = map.get("小盒条码:")  # url
        if map.get("小盒条码:") is None:
            item["single_code"] = None
        else:
            res = req.get(map.get("小盒条码:"))
            image = Image.open(BytesIO(res.content))
            item["single_code"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        # item["package_code"] = map.get("条装条码:")  # url
        if map.get("条装条码:") is None:
            item["package_code"] = None
        else:
            res = req.get(map.get("条装条码:"))
            image = Image.open(BytesIO(res.content))
            item["package_code"] = "".join(pytesseract.image_to_string(image,lang="font", config="--psm 8").split())

        item["participant"] = response.xpath(
            '//div[@id="evaluate"]//span[@id="pingfenarea_pingnum"]/text()').extract_first()
        item["taste"] = map.get("口\u3000味:")
        item["outlook"] = map.get("外\u3000观:")
        item["performance"] = map.get("性价比:")
        item["general"] = map.get("综\u3000合:")
        item["URL"] = response.url

        yield item

        comment = response.xpath('//p[@class="commentmore"]/a/@href').extract_first()
        comment_url = urllib.parse.urljoin(response.url, comment)
        # yield scrapy.Request(comment_url, callback=self.parse_comment_detail)

    def parse_comment_detail(self, response):
        comment_item = {}
        comment_list = response.xpath('//ul[@id="commentswrap"]//li')
        for comment in comment_list:
            comment_item = Comment()
            comment_item["name"] = response.xpath('//div[@id="productname"]/p/a/text()').extract_first()
            comment_item["region"] = comment.xpath('./@title').extract_first()
            comment_item["user"] = comment.xpath(
                './p[@class="commentinfo"]/span[@class="username"]/text()').extract_first()
            comment_item["time"] = comment.xpath('./p[@class="commentinfo"]/span/text()').extract()[1]
            comment_item["content"] = comment.xpath('./p[@class="commenttext"]/span/text()').extract_first().strip()
            print(comment_item)
            yield comment_item

        href = response.xpath(
            '//ul[@class="pagination"]/li[@class="page-item"]/a[contains(text(),"下一页")]/@href').extract_first()
        # # 通过判断是否next 为none，来判断是否是最后一页
        if href is not None:
            next_url = urllib.parse.urljoin(response.url, href)
            # url:下一页的url地址
            # callback：需要交由那个parse方法处理（可以自定义），因为下一页的数据结构，和当前页的数据一样，所以处理方式都是一样的。若不一样，那么需要自定义
            yield scrapy.Request(url=next_url, callback=self.parse_comment_detail, meta=comment_item)
        else:
            # yield comment_item
            print("爬取完毕")
