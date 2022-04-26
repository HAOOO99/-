# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class brand(scrapy.Item):
    brand_name = scrapy.Field()  # 品牌名
    region = scrapy.Field()  # 品牌地区
    is_history = scrapy.Field()  # 是否为历史品牌 1 -> 现存, 2 -> 历史
    description = scrapy.Field()  # 品牌简介
    company = scrapy.Field()  # 所属公司
    URL = scrapy.Field()  # URL 链接


class product(scrapy.Item):
    name = scrapy.Field()  # 产品名称
    brand = scrapy.Field()
    type = scrapy.Field()  # 产品种类
    tar_content = scrapy.Field()  # 焦油量
    nicotine = scrapy.Field()  # 烟碱量
    Co_amount = scrapy.Field()  # 一氧化碳量
    package_pattern = scrapy.Field()  # 包装形式
    cig_size = scrapy.Field()  # 烟支规格
    single_code = scrapy.Field()  # 小盒条码
    package_code = scrapy.Field()  # 条盒条码
    single_price = scrapy.Field()  # 小盒零售价 元/盒
    package_price = scrapy.Field()  # 条盒零售价 元/盒
    description = scrapy.Field()  # 产品简介
    participant = scrapy.Field()
    taste = scrapy.Field()
    performance = scrapy.Field()
    general = scrapy.Field()
    package = scrapy.Field()

    URL = scrapy.Field()
    ID = scrapy.Field()


class rating(scrapy.Item):
    taste = scrapy.Field()
    package = scrapy.Field()
    cost_performance = scrapy.Field()
    general = scrapy.Field()
    participants = scrapy.Field()


class imageItem(scrapy.Item):
    image_url = scrapy.Field()
    product_name = scrapy.Field()
    pid = scrapy.Field()
    image_path = scrapy.Field()
    image_number = scrapy.Field()
    uuid = scrapy.Field()


class yanyue(scrapy.Item):
    name = scrapy.Field()
    brand = scrapy.Field()
    type = scrapy.Field()
    dimension = scrapy.Field()  # 烟支
    tar_content = scrapy.Field()
    nicotine = scrapy.Field()
    CO = scrapy.Field()
    perimeter = scrapy.Field()  # 周长
    filter_length = scrapy.Field()  # 过滤嘴长
    length = scrapy.Field()  # 长度
    package = scrapy.Field()
    main_color = scrapy.Field()
    side_color = scrapy.Field()
    number = scrapy.Field()
    single_price = scrapy.Field()
    package_price = scrapy.Field()
    single_code = scrapy.Field()
    package_code = scrapy.Field()
    participant = scrapy.Field()
    taste = scrapy.Field()
    outlook = scrapy.Field()
    performance = scrapy.Field()
    general = scrapy.Field()
    URL = scrapy.Field()


class Comment(scrapy.Item):
    name = scrapy.Field()
    user = scrapy.Field()
    time = scrapy.Field()
    region = scrapy.Field()
    content = scrapy.Field()

class poi(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    district = scrapy.Field()
    coordinate_1 = scrapy.Field()
    coordinate_2 = scrapy.Field()
    coordinate_3 = scrapy.Field()
    coordinate_4 = scrapy.Field()
    coordinate_5 = scrapy.Field()
