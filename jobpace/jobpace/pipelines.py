# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import codecs
class JobpacePipeline(object):
    def __init__(self):
        self.file = codecs.open('shanghai51job.csv','w',encoding='utf-8')
        self.wr = csv.writer(self.file, dialect='excel')
        self.wr.writerow(['jobname','workadd','salary'])

    def process_item(self, item, spider):
        self.wr.writerow([item['jobname'],item['workadd'],item['salary']])
        return item

"""

jobname = scrapy.Field()
    companyname = scrapy.Field()
    workadd = scrapy.Field()
    salary = scrapy.Field()
    pubtime = scrapy.Field()
"""