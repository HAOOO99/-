import json
import urllib.parse

import scrapy

from tobacco_data.items import brand, product, imageItem

class BrandSpider(scrapy.Spider):
    name = 'brand'
    allowed_domains = ['www.etmoc.com']
    start_urls = ['http://www.etmoc.com/Firms/BrandAll']

    def parse(self, response):

        host_name = 'http://www.etmoc.com/Firms/'
        ul_list = response.xpath('//div[@class="detail98"]/ul')
        region = response.xpath('//div[@class="detail98"]/div/h4/text()').extract()

        i = 0
        for ul in ul_list:
            brands = ul.xpath('./li/a/text()')
            # brand href included brand ID of the website
            next_href = ul.xpath('./li/a/@href').extract()
            j = 0
            for brand in brands:
                item = {"brand_name": brand.extract().strip(),
                        "region": region[i]}
                if item["region"] == "历史品牌":
                    item["is_history"] = 2
                else:
                    item["is_history"] = 1
                # brand URL (combined with host name and detail href)
                item['URL'] = host_name + next_href[j]
                # jump into the brand detail page
                yield scrapy.Request(url=item["URL"], callback=self.parse_detail, meta=item)
                j += 1
            i += 1

    def parse_detail(self, response):

        meta_dict = response.meta
        brand_item = brand()
        # migrate dictionary of brand item
        brand_item["brand_name"] = meta_dict["brand_name"]
        brand_item["region"] = meta_dict["region"]
        brand_item["is_history"] = meta_dict["is_history"]
        brand_item["URL"] = meta_dict["URL"]
        # get the description detail
        des = response.xpath('//div[@class="detail f16"]/p//text()')
        if len(des) == 0:
            brand_item["description"] = None
        else:
            brand_item["description"] = des.extract_first().strip()
        # get company message on the brand page
        brand_item["company"] = ''.join(
            response.xpath(
                '//div[@class="brand-header clearfix"]//div[@class="right"]//text()').extract()).strip()

        # get whole product stored as a list on the brand page
        product_list = response.xpath('//div[@class="li-p"]')
        # loop the product list to get each product item

        for pro in product_list:
            product_item = product()
            product_item["name"] = pro.xpath('.//div[@class="li-p-t"]/a/text()').extract_first().strip()
            product_item["brand"] = response.xpath('//div[@class="left"]/h3/text()').extract_first()
            # get the page url of each product
            product_url = pro.xpath('.//div[@class="li-p-t"]/a/@href').extract_first()
            # check whether there is a message for 小盒条码  on the brand page
            if pro.xpath('.//div[@class="li-p-b"]/p[contains(text(),"小盒条码")]/text()').extract_first() is None:
                product_item["single_code"] = None
            else:
                product_item["single_code"] = pro.xpath(
                    './/div[@class="li-p-b"]/p[contains(text(),"小盒条码")]/text()').extract_first().split("：")[1]
            # check whether there is a message for  条盒条码  on brand page
            if pro.xpath('.//div[@class="li-p-b"]/p[contains(text(),"条盒条码")]/text()').extract_first() is None:
                product_item["package_code"] = None
            else:
                product_item["package_code"] = pro.xpath(
                    './/div[@class="li-p-b"]/p[contains(text(),"条盒条码")]/text()').extract_first().split("：")[1]
            # check whether there is a message for 售价 on the brand page
            if pro.xpath('.//div[@class="li-p-p"]/p/text()').extract_first() is None:
                product_item["package_price"] = None
            else:
                product_item["package_price"] = pro.xpath(
                    './/div[@class="li-p-p"]/p/text()').extract_first()
            # get the completed url for each product
            product_item['URL'] = urllib.parse.urljoin(response.url, product_url)
            # jump to the page of detail page of each product
            yield scrapy.Request(
                url=product_item["URL"], callback=self.parse_product_detail, meta=product_item)

        # get the href of  下一页  button
        next_href = response.xpath(
            '//ul[@class="pagination"]/li/a[contains(text(),"下一页")]/@href').extract_first()
        # # 通过判断是否next 为none，来判断是否是最后一页
        if next_href is not None:
            next_url = urllib.parse.urljoin(response.url, next_href)
            # url:下一页的url地址
            # callback：需要交由那个parse方法处理（可以自定义），因为下一页的数据结构，和当前页的数据一样，所以处理方式都是一样的。若不一样，那么需要自定义
            yield scrapy.Request(url=next_url, callback=self.parse_detail, meta=meta_dict)
        else:
            yield brand_item
            print("爬取完毕")



    def parse_product_detail(self, response):

        meta_product = response.meta
        product_item = product()
        product_item["name"] = meta_product["name"]
        product_item["brand"] = meta_product["brand"]
        product_item["single_code"] = meta_product["single_code"]
        product_item["package_code"] = meta_product["package_code"]
        product_item["package_price"] = meta_product["package_price"]
        product_item['URL'] = meta_product["URL"]

        product_item['ID'] = product_item['URL'].split('=')[1]
        first_line_message = response.xpath(
            '//div[@class="proBars"]/div[@class="proBar proBarB proBar2"]')
        # print(first_line_message[0])
        # if first_line_message[0].xpath['./div/text()'] is not None:\
        detail = first_line_message[0].xpath('./div')
        # print(detail)
        # print(detail[0])
        # print(detail[0].xpath('./text()').extract_first())
        product_item["type"] = detail[0].xpath('./text()').extract_first()

        # else:
        #     product_item["type"] = None
        # if first_line_message[1].xpath['./div/text()'] is not None:
        product_item['tar_content'] = detail[1].xpath('./text()').extract_first()
        # # else:
        # #     product_item['tar_content'] = None
        # nicotine line + sales line
        second_message = response.xpath(
            '//div[@class="proBars"]/div[@class="proBar proBar2"]')
        ##nicotine line
        detail_message_1 = second_message[0].xpath("./div")
        product_item["nicotine"] = detail_message_1[0].xpath("./text()").extract_first()
        product_item["Co_amount"] = detail_message_1[1].xpath("./text()").extract_first()
        # sales_line
        detail_message_2 = second_message[1].xpath("./div")
        product_item["single_price"] = detail_message_2[0].xpath("./strong/text()").extract_first()
        product_item["package_price"] = detail_message_2[1].xpath("./strong/text()").extract_first()

        product_item["package_pattern"] = response.xpath(
            '//div[@class="proBars"]/div[@class="proBar proBarB"]/text()').extract_first().strip() + \
                                          response.xpath(
                                              '//div[@class="proBars"]/div[@class="proBar proBarB"]/span[@class="lbl1"]/text()').extract_first()

        product_item["cig_size"] = ''.join(response.xpath(
            '//div[@class="proBars"]/div[@class="proBar"]/text()').extract()) + \
                                   ''.join(response.xpath(
                                       '//div[@class="proBars"]/div[@class="proBar"]/span[@class="lbl"]/text()').extract())

        if len(response.xpath('//div[@id="productsumm"]/p[not(contains(@style,"font-size: 12px"))]')) == 0:
            product_item["description"] = None
        else:
            product_item["description"] =''.join(response.xpath(
                '//div[@id="productsumm"]/p[not(contains(@style,"font-size: 12px"))]//text()').extract()).strip("\r\n")

        product_item["participant"] = response.xpath(
            '//div[@class="proPj"]/div[@class="proPjbart"]/text()').extract_first().split(" ")[0]
        rating = response.xpath('//div[@class="proPj"]/div[@class="proPjbar"]')
        product_item["taste"] = rating[0].xpath('./div[@class="c"]/text()').extract_first()
        product_item["package"] = rating[1].xpath('./div[@class="c"]/text()').extract_first()
        product_item["performance"] = rating[2].xpath('./div[@class="c"]/text()').extract_first()
        product_item["general"] = rating[3].xpath('./div[@class="c"]/text()').extract_first()

        print(product_item)

        yield product_item
        # image part



