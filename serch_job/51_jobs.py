import requests
import re
import time
import threadpool
from serch_job.insert_db import insertDB
from scrapy import Selector


class SerachJob:
    def index(self):
        """
        获取所有页
        :return: 总共多少页
        """
        url = 'https://search.51job.com/list/080200,000000,0000,00,9,99,%2520,2,1.html'
        params = {
            'lang': 'c',
            'stype': '',
            'postchannel': '0000',
            'workyear': '99',
            'cotype': '99',
            'degreefrom': '99',
            'jobterm': '99',
            'companysize': '99',
            'providesalary': '99',
            'lonlat': '	0,0',
            'radius': '-1',
            'ord_field': '0',
            'confirmdate': '9',
            'fromType': '',
            'dibiaoid': '0',
            'address': '',
            'line': '',
            'specialarea': '00',
            'from': '',
            'welfare': ''
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }
        index_res = requests.get(url=url, headers=headers, params=params)
        index_selector = Selector(text=index_res.content.decode('gbk'))
        details_url = index_selector.xpath('//p[@class="t1 "]//a/@href').extract()
        self.details(details_url)
        all_page = index_selector.xpath('//span[@class="td"]/text()').extract_first()
        all_page_number = re.findall(r'共(\d+)页', all_page)[0]
        nex_url = index_selector.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if nex_url:
            self.loop_page(nex_url)

    def loop_page(self, nex_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }
        index_res = requests.get(url=nex_url, headers=headers)
        try:
            index_selector = Selector(text=index_res.content.decode('gbk'))
        except BaseException as e:
            print(e)
        details_url = index_selector.xpath('//p[@class="t1 "]//a/@href').extract()
        self.details(details_url)
        nex_url = index_selector.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if nex_url:
            self.loop_page(nex_url)
        else:
            print('采集结束..........')
            exit()

    def details(self, all_url):
        for each_url in all_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
            }
            details_res = requests.get(url=each_url, headers=headers)
            try:
                details_selector = Selector(text=details_res.content.decode('gbk'))
            except BaseException as e:
                print(e)
            position = details_selector.xpath('//div[@class="cn"]/h1/@title').extract_first()
            company = details_selector.xpath('//p[@class="cname"]/a/@title').extract_first()
            price = details_selector.xpath('//div[@class="cn"]/strong/text()').extract_first()
            all_infos = details_selector.xpath('//p[@class="msg ltype"]/@title').extract_first()
            if all_infos:
                all_infos = all_infos.split('|')
                if len(all_infos) == int(7):
                    address = re.findall(r'(.*)\xa0\xa0', all_infos[0])[0]
                    work_year = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[1])[0]
                    education = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[2])[0]
                    nedd_people = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[3])[0]
                    pubtime = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[4])[0]
                    english = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[5])[0]
                    major = re.findall(r'\xa0\xa0(.*)', all_infos[6])[0]
                if len(all_infos) == int(6):
                    address = re.findall(r'(.*)\xa0\xa0', all_infos[0])[0]
                    work_year = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[1])[0]
                    education = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[2])[0]
                    nedd_people = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[3])[0]
                    pubtime = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[4])[0]
                    english = re.findall(r'\xa0\xa0(.*)', all_infos[5])[0]
                    major = ''
                if len(all_infos) == int(5):
                    address = re.findall(r'(.*)\xa0\xa0', all_infos[0])[0]
                    work_year = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[1])[0]
                    education = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[2])[0]
                    nedd_people = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[3])[0]
                    pubtime = re.findall(r'\xa0\xa0(.*)', all_infos[4])[0]
                    english = ''
                    major = ''
                if len(all_infos) == int(4):
                    print('this %s 岗位无学历' % position)
                    address = re.findall(r'(.*)\xa0\xa0', all_infos[0])[0]
                    work_year = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[1])[0]
                    education = ''
                    nedd_people = re.findall(r'\xa0\xa0(.*)\xa0\xa0', all_infos[2])[0]
                    pubtime = re.findall(r'\xa0\xa0(.*)', all_infos[3])[0]
                    english = ''
                    major = ''
                update_time = time.strftime('%Y-%m-%d')
                each_infos = (
                    None, position, company, price, address, work_year, education, nedd_people, pubtime, english, major,
                    each_url, update_time)
                insertDB(each_infos, 'test', 'search_jobs')

    def use_threadpool(self):
        task_pool = threadpool.ThreadPool(5)  # 准备5个线程池
        requests = threadpool.makeRequests(self.index())
        for req in requests:
            task_pool.putRequest(req)
        task_pool.wait()


if __name__ == '__main__':
    job = SerachJob()
    job.use_threadpool()
