# -*- coding: utf-8 -*-
import scrapy
from sunSpider.items import SunspiderItem


# http://wz.sun0769.com/political/index/politicsNewest?id=1&page=2
# http://wz.sun0769.com/political/index/politicsNewest?id=1&page=0 编号 状态 问政标题 响应时间 问政时间
# http://wz.sun0769.com/political/politics/index?id=461034 <span class="state1">250414</span> <span class="state2"
# style="color: #00C5AA">已受理</span> <span class="state3"><a target="_blank"
# href="/political/politics/index?id=460974" class="color-hover">东城花街十八堑头路路灯都不开，群众不方便</a></span>
# http://wz.sun0769.com/political/politics/index?id=461034

# <div class="details-box">
#               <pre>东莞市常平镇金田花园，物业不作为，利用疫情，乱收费，寒了业主的心。1、疫情期间，水表不抄，每户估算，滑天下之大稽，买的新房没住过一天，物业那里有登记，水费照收不误。2、银行卡余额充足，不按时扣费，管理费逾期，没有一次提醒，直接强制缴纳3个月滞纳金，骗取滞纳金。3、收取高昂停车费，没经过业主同意，毫无理由的提高停车费价格，将疫情期间损失转接到业主身上。4、物业管理混乱，外人随便进入，疫情期间也是如此。5、花园内，狗猫随地大小便。建议有意向购买的请三思还而后行！</pre>
#           </div>
class SunspideritemSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 取出每个链接的列表
        links = response.xpath('//span[@class="state3"]/a/@href').extract()
        # 发送每个帖子的请求
        for link in links:
            yield scrapy.Request("http://wz.sun0769.com" + link, callback=self.parse_item)
        # 设置自动翻页
        if self.offset < 5:
            self.offset += 1
            # 重新发送新的页面
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    # 爬取帖子内容
    def parse_item(self, response):
        item = SunspiderItem()
        item["url"] = response.url
        item["title"] = response.xpath('//div/p[@class="focus-details"]/text()').extract()[0]
        item["content"] = "".join(response.xpath('//div[@class="details-box"]/pre/text()').extract())
        yield item
