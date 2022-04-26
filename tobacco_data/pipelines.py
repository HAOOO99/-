# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from tobacco_data.items import brand, product, imageItem, Comment, yanyue, poi


class TobaccoDataPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='123.57.165.135', port=50007, user='xyh', password='HUjy0b3L4&yu',
                                    db='cigarette_info_temp')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # if isinstance(item, brand):
        #
        #     data_item = {"brand_name": item["brand_name"],
        #                  "region": item["region"],
        #                  "is_history": int(item["is_history"]),
        #                  "description": item["description"],
        #                  "company": item["company"],
        #                  "URL": item["URL"]}
        #     print(data_item)
        #     if self.cursor.execute('select * from brand where URL = %(URL)s limit 1', data_item):
        #         return
        #     # 3. 将Item数据放入数据库，默认是同步写入。
        #     # 4. 更新
        #     insert_sql = """
        #             insert into brand (brand_name,region,is_exist,description,company,URL) VALUES (%(brand_name)s,
        #                     %(region)s,%(is_history)s,%(description)s,%(company)s,%(URL)s);
        #             """
        #
        #     try:
        #         self.cursor.execute(insert_sql, data_item)
        #         # 4. 提交操
        #         self.conn.commit()
        #         print('插入成功')
        #         print("item is brand")
        #
        #     except Exception as e:
        #         print('插入失败')
        #         print(e)
        #
        # if isinstance(item, product):
        #     data_item = {"name": item["name"],
        #                  "brand_name": item["brand"],
        #                  "type": item["type"],
        #                  "tar_content": item["tar_content"],
        #                  "nicotine": item["nicotine"],
        #                  "Co_amount": item["Co_amount"],
        #                  "package_pattern": item["package_pattern"],
        #                  "cig_size": item["cig_size"],
        #                  "single_code": item["single_code"],
        #                  "package_code": item["package_code"],
        #                  "single_price": item["single_price"],
        #                  "package_price": item["package_price"],
        #                  "description": item["description"],
        #                  "participant": item["participant"],
        #                  "taste": item["taste"],
        #                  "package": item["package"],
        #                  "performance": item["performance"],
        #                  "general": item["general"],
        #                  "ID": item["ID"],
        #                  "URL": item["URL"]}
        #     print(data_item)
        #     if self.cursor.execute('select * from product where URL = %(URL)s limit 1', data_item):
        #         return
        #     # 3. 将Item数据放入数据库，默认是同步写入。
        #     # 4. 更新
        #     insert_sql = """
        #      insert into product
        #      (name,brand_name,type,tar_content,nicotine,Co_amount,package_pattern,cig_size,
        #      single_code,package_code,single_price,package_price,description,
        #      participant,taste,package,performance,general,ID,URL)
        #      VALUES
        #      (%(name)s,%(brand_name)s,%(type)s,%(tar_content)s,%(nicotine)s,%(Co_amount)s,%(package_pattern)s,
        #         %(cig_size)s,%(single_code)s,%(package_code)s,%(single_price)s,%(package_price)s,%(description)s,
        #         %(participant)s,%(taste)s,%(package)s,%(performance)s,%(general)s,%(ID)s,%(URL)s);
        #      """
        #
        #     try:
        #         self.cursor.execute(insert_sql, data_item)
        #         # 4. 提交操作
        #         self.conn.commit()
        #         print('插入成功')
        #         print("the item is product")
        #     except Exception as e:
        #         print('插入失败')
        #         print(e)
        # if isinstance(item, imageItem):
        #     data_item = {"product_name": item["product_name"],
        #                  "pid": item["pid"],
        #                  "image_path": "cigarette_images/"+item["image_path"],
        #                  "URL": item["image_url"]}
        #     print(data_item)
        #     if self.cursor.execute('select * from image where URL = %(URL)s limit 1', data_item):
        #         return
        #     # 3. 将Item数据放入数据库，默认是同步写入。
        #     # 4. 更新
        #     insert_sql = """
        #      insert into image
        #      (product_name,pid,image_path,URL)
        #      VALUES
        #      (%(product_name)s,%(pid)s,%(image_path)s,%(URL)s);
        #      """
        #
        #     try:
        #         self.cursor.execute(insert_sql, data_item)
        #         # 4. 提交操作
        #         self.conn.commit()
        #         print('插入成功')
        #         print("the item is image")
        #     except Exception as e:
        #         print('插入失败')
        #         print(e)

        # print(11111)
        data_item = {"name": item["name"],
                     "type": item["type"],
                     "district": item["district"],
                     "coordinate_1": item["coordinate_1"],
                     "coordinate_2": item["coordinate_2"],
                     "coordinate_3": item["coordinate_3"],
                     "coordinate_4": item["coordinate_4"],
                     "coordinate_5": item["coordinate_5"]}
        print(data_item)
        # if self.cursor.execute('select * from poi where URL = %(URL)s limit 1', data_item):
        #     return
        # 3. 将Item数据放入数据库，默认是同步写入。
        # 4. 更新
        insert_sql = """
         insert into poi_jinan(name,district,type,coordinate_1,coordinate_2,coordinate_3,coordinate_4,coordinate_5)
         VALUES
         (%(name)s,%(district)s,%(type)s,%(coordinate_1)s,%(coordinate_2)s,%(coordinate_3)s,%(coordinate_4)s,%(coordinate_5)s);
         """

        try:
            self.cursor.execute(insert_sql, data_item)
            # 4. 提交操作
            self.conn.commit()
            print('插入成功')
            print("the item is poi")
        except Exception as e:
            print('插入失败')
            print(e)
        # pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class TobaccoDataYanYuePipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='123.57.165.135', port=50007, user='xyh', password='HUjy0b3L4&yu',
                                    db='cigarette_info_temp')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, yanyue):

            data_item = {"name": item["name"],
                         "brand": item["brand"],
                         "type": item["type"],
                         "tar_content": item["tar_content"],
                         "dimension": item["dimension"],
                         "nicotine": item["nicotine"],
                         "CO": item["CO"],
                         "perimeter": item["perimeter"],
                         "filter_length": item["filter_length"],
                         "length": item["length"],
                         "package": item["package"],
                         "main_color": item["main_color"],
                         "side_color": item["side_color"],
                         "number": item["number"],
                         "single_code": item["single_code"],
                         "package_code": item["package_code"],
                         "single_price": item["single_price"],
                         "package_price": item["package_price"],
                         "participant": item["participant"],
                         "taste": item["taste"],
                         "outlook": item["outlook"],
                         "performance": item["performance"],
                         "general": item["general"],
                         "URL": item["URL"]}
            # print(data_item)
            if self.cursor.execute('select * from yanyue where URL = %(URL)s limit 1', data_item):
                return
            # 3. 将Item数据放入数据库，默认是同步写入。
            # 4. 更新
            insert_sql = """
                        insert into yanyue
                        (name,brand,type,tar_content,nicotine,dimension,CO,perimeter,package,filter_length,length,
                        main_color,side_color,number,single_code,package_code,single_price,package_price,participant,
                        taste,outlook,performance,general,URL)
                        VALUES
                        (%(name)s,%(brand)s,%(type)s,%(tar_content)s,%(nicotine)s,%(dimension)s,%(CO)s,%(perimeter)s,%(package)s,
                        %(filter_length)s,%(length)s,%(main_color)s,%(side_color)s,%(number)s,%(single_code)s,%(package_code)s,
                        %(single_price)s,%(package_price)s,%(participant)s,%(taste)s,%(outlook)s,%(performance)s,%(general)s,%(URL)s);
                        """

            try:
                self.cursor.execute(insert_sql, data_item)
                # 4. 提交操作
                self.conn.commit()
                print(data_item)
                print('插入成功')
                print("item is brand")

            except Exception as e:
                print('插入失败')
                print(e)

        if isinstance(item, Comment):
            data_item = {"name": item["name"],
                         "user": item["user"],
                         "time": item["time"],
                         "region": item["region"],
                         "content": item["content"]}
            print(data_item)
            # if self.cursor.execute('select * from product where URL = %(URL)s limit 1',data_item):
            #     return
            # 3. 将Item数据放入数据库，默认是同步写入。
            # 4. 更新
            insert_sql = """
             insert into comment
             (name,user,time,region,content)
             VALUES
             (%(name)s,%(user)s,%(time)s,%(region)s,%(content)s);
             """

            try:
                self.cursor.execute(insert_sql, data_item)
                # 4. 提交操作
                self.conn.commit()
                print('插入成功')
                print("the item is product")
            except Exception as e:
                print('插入失败')
                print(e)

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class TobaccoDataImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["image_url"], meta={'path': item["image_path"]})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("item contains no image")

        return item

    def file_path(self, request, response=None, info=None):
        name = request.meta['path']
        return name
