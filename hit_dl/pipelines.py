import os
from itemadapter import ItemAdapter
from urllib.parse import unquote
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request


class ProcessPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        return [Request(u) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = os.path.basename(unquote(request.url))
        return item['path'] + file_name
