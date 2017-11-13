#!/usr/bin/env python
# encoding: utf-8
import re
import os
import scrapy
from getnovel.items import GetnovelItem
# shanjue.com小说爬虫


class GetNovelSj(scrapy.Spider):

    name = 'get_shanjue'
    allowed_domains = ['shanjue.com', ]

    url_base = 'http://www.shanjue.com/nvpinyanqing/index'
    url_end = '.html'

    def start_requests(self):

        for i in range(3):

            if i+ 1 == 1:

                request_url = self.url_base + self.url_end

            else:

                request_url = self.url_base + '_' + str(i + 1) + self.url_end

            yield scrapy.Request(request_url, callback=self.parse_list)

    def parse_list(self, response):

        urllist = response.xpath(
            '*//ul[@class="listul top30"]/li//a/@href').extract()

        for url in urllist:

            complateurl = 'http://www.shanjue.com' + url

            novelcode = re.search('\/(\d+)\.html', url).group(1)

            yield scrapy.Request(complateurl, meta={'novelcode': novelcode},
                                 callback=self.parse_content)

    def parse_content(self, response):

        coverImage = response.xpath(
            '*//div[@class="cover"]/img/@src').extract()[0]
        novelName = response.xpath('*//div[@class="cover"]/img/@alt').extract()
        novelName = re.sub(u'TXT全集下载', '', novelName[0])
        simpleIntro = response.xpath(
            '*//div[@class="novelcon top20"]/p').extract()[0]
        # novelcode = response.meta['novelcode']
        a1 = response.xpath('*//a[@class="favBn"]/@href').extract()[0]
        a = re.search('classid=(\d+)&id=(\d+)', a1)
        a2 = a.group(1)
        a3 = a.group(2)
        to_get_download_url = 'http://www.shanjue.com/e/DownSys/DownSoft/?classid=' + a2 + '&id=' + \
            a3 + '&pathid=0'

        yield scrapy.Request(to_get_download_url, meta={'coverImage': coverImage,
                                                        'novelName': novelName,
                                                        'simpleIntro': simpleIntro},
                             callback=self.getdurl)

    def getdurl(self, response):

        print '$'* 30
        # print response.body
        print '$'* 30

        downurl = response.xpath("*//a[@class='btns btn_org']/@href").extract()[0]
        coverImage_url = response.meta['coverImage']
        novelName = response.meta['novelName']
        simpleIntro = response.meta['simpleIntro']

        item = GetnovelItem()

        item['file_urls'] = ['http://www.shanjue.com/e/DownSys' + re.sub('\.\.', '', downurl)]

        item['image_urls'] = ['http://www.shanjue.com'+ coverImage_url]
        item['novelName'] = novelName
        item['simpleIntro'] = simpleIntro



        yield item
