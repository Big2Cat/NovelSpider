# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GetnovelPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        for image_url in item['image_urls']:

            yield Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):

        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:

            raise DropItem('ImageItem contains no images')

        # item['image_paths'] = image_paths

        return item

    def file_path(self, request, response=None, info=None):

        item = request.meta['item']

        image_guid = request.url.split('/')[-1]

        image_path = u'full/{0[novelName]}/{1}'.format(item, image_guid)

        print image_path

        print '#'*30

        return image_path


class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):

        for file_url in item['file_urls']:

            yield Request(file_url, meta={'item': item})

    def item_completed(self, results, item, info):

        file_paths = [x['path'] for ok, x in results if ok]

        print file_paths

        if not file_paths:

            raise DropItem('FileItem contains no files')

        return item

    def file_path(self, request, response=None, info=None):

        item = request.meta['item']
        folder = item['novelName']
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder, image_guid)

        return filename
