import urllib.parse

import pymysql
import scrapy

from tobacco_data.items import imageItem, product


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['www.etmoc.com']

    # start_urls = ['http://www.etmoc.com/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.conn = pymysql.connect(host='123.57.165.135',
                                    port=50007,
                                    user='xyh',
                                    password='HUjy0b3L4&yu',
                                    db='cigarette_info_temp')
        self.cursor = self.conn.cursor()

    def start_requests(self):
        """
        iterate the database, get the url of each product parse it to the next function, yield each product
        """
        select_sql = """
        select URL,name,pid,uuid from product
        """
        self.cursor.execute(select_sql)
        url_list = self.cursor.fetchall()

        for url in url_list:
            item = {"name": url[1],
                    'pid': url[2],
                    'uuid': url[3],
                    'url': url[0]}
            yield scrapy.Request(url=item["url"], callback=self.parse, meta=item)
        self.cursor.close()
        self.conn.close()

    def parse(self, response):
        meta_product = response.meta
        item = {}

        item["name"] = meta_product["name"]
        item['pid'] = meta_product['pid']
        item['uuid'] = meta_product['uuid']
        tmp_url = response.xpath('//div[@class="proImg proBarshad"]/p/a/@href').extract_first()

        if tmp_url is not None:
            image_url = urllib.parse.urljoin(response.url, tmp_url)
            yield scrapy.Request(url=image_url, callback=self.parse_image, meta=item)

        else:
            image = imageItem()
            tmp_url = response.xpath('//div[@class="proImg proBarshad"]/img/@src').extract_first()
            image["image_url"] = urllib.parse.urljoin(response.url, tmp_url)
            image["product_name"] = response.xpath('//div[@class="proImg proBarshad"]/img/@alt').extract_first()
            image["pid"] = meta_product['pid']
            image["uuid"] = meta_product['uuid']
            image["image_number"] = 0
            image["image_path"] = \
                image["uuid"] + "/" + image["uuid"] + "_" + str(
                    image["image_number"]) \
                + '.jpg'
            yield image

    def parse_image(self, response):
        tmp_img = response.meta

        url_list = response.xpath('//div[@id="picbox"]/div')
        for url in url_list:
            img_item = imageItem()
            img_item["product_name"] = tmp_img["name"]
            img_item["pid"] = tmp_img["pid"]
            img_item["uuid"] = tmp_img["uuid"]

            img_item["image_number"] = url.xpath(".//img/@alt").extract_first()
            img_item["image_path"] = img_item["uuid"] + "/" \
                + img_item["uuid"] + "_" + str(img_item["image_number"]) + '.jpg'
            each_url = url.xpath('./@data-img').extract_first()

            img_item["image_url"] = urllib.parse.urljoin(response.url, each_url)
            yield img_item
