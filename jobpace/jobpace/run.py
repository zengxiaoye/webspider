from scrapy import cmdline
name = "wuyaojob"
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())