# -*- coding: utf-8 -*-
import scrapy
from jobpace.items import JobpaceItem


class WuyaojobSpider(scrapy.Spider):
    name = 'wuyaojob'
    allowed_domains = ['51job.com']
    start_urls = ["https://search.51job.com/list/080200,000000,0000,00,9,99,python%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]
    def parse(self, response):

        joblist = response.xpath("//div[@class='dw_table']//div[@class='el']")
        for each in joblist:
            jobname = each.xpath("./p/span/a/text()").extract()
            if len(jobname)>0:
                jobname = jobname[0].strip()
                print(jobname)
            companyname = each.xpath("./span[@class='t2']/a/text()").extract()
            if len(companyname) > 0:
                companyname = companyname[0]
                print(companyname)
            workadd = each.xpath("./span[@class='t3']/text()").extract()
            if len(workadd) > 0:
                workadd = workadd[0]
                print(workadd)
            salary = each.xpath("./span[@class='t4']/text()").extract()
            if len(salary) > 0:
                salary = salary[0]
                print(salary)
            else:
                salary = ''
                print(salary)
            pubtime = each.xpath("./span[@class='t5']/text()").extract()
            if len(pubtime)> 0:
                pubtime = pubtime[0]
                print(pubtime)
            item = JobpaceItem()
            item["jobname"] = jobname
            item["companyname"] = companyname
            item["workadd"] = workadd
            item["salary"] = salary
            item["pubtime"] = pubtime
            yield item
        next = response.xpath("//div[@class='p_in']/ul/li[last()]/a/@href").extract()
        if len(next)>0:
            url = response.urljoin(next[0])
            yield scrapy.Request(url=url, callback=self.parse)
"""

jobname = scrapy.Field()
    companyname = scrapy.Field()
    workadd = scrapy.Field()
    salary = scrapy.Field()
    pubtime = scrapy.Field()
"""