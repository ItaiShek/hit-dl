import scrapy
import logging
from hit_dl.items import MoodleItem
from urllib.parse import unquote


def remove_forbidden_chars(str1):
    forbidden_chars_win = {'\\': '.', '/': '.', ':': '.', '*': '', '?': '', '"': '', '<': '', '>': '', '|': ''}
    for key, value in forbidden_chars_win.items():
        str1 = str1.replace(key, value)
    return str1


class HITSpider(scrapy.Spider):
    name = "moodle_spider"

    allowed_domains = ['hit.ac.il']

    start_urls = ['https://md.hit.ac.il']

    def __init__(self, username, password, urls):
        super(HITSpider, self).__init__()
        self.username = username
        self.password = password
        self.urls = urls

    # go to login page
    def parse(self, response, **kwargs):
        return scrapy.FormRequest.from_response(response,
                                                formxpath='//form',
                                                callback=self.login_page1
                                                )

    # log in with username and password
    def login_page1(self, response):
        # enter data to moodle's login form
        yield scrapy.FormRequest.from_response(response,
                                               formxpath='//form',
                                               formdata={'Ecom_User_ID': self.username,
                                                         'Ecom_Password': self.password
                                                         },
                                               callback=self.login_page2
                                               )

    # check authentication and redirect
    def login_page2(self, response):
        # authentication failed
        if 'Invalid Credentials' in response.text:
            logging.error("Login failed! - Invalid Credentials")
            return
        else:  # logged in
            print('Logged in to md.hit.ac.il')

        # get redirection url
        redirect = response.xpath('//script/text()').re_first(r'href=[\']?([^\']+)')
        if not redirect:
            logging.error('Could not find redirection url')
            return

        # redirect to the last login page
        yield scrapy.Request(url=redirect, callback=self.login_page3)

    # last login page - enter the csrf token to stay logged in
    def login_page3(self, response):
        # scrape login token
        logintoken = response.xpath('//form/input[@name="logintoken"]/@value').get()

        if not logintoken:
            logging.error('Could not find the csrf token')
            return

        yield scrapy.FormRequest.from_response(response,
                                               formxpath='//form',
                                               formdata={'username': self.username,
                                                         'password': self.password,
                                                         'logintoken': logintoken
                                                         },
                                               callback=self.after_login
                                               )

    def after_login(self, response):
        for url in self.urls:
            print(f'Scraping: {url}')
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        course_name = response.xpath('//h1/text()').get()

        if course_name:
            course_name = remove_forbidden_chars(course_name)

        for subject in response.xpath('//div[@class="content"]'):
            title = subject.xpath('.//h3/span/text()').get()

            if title:
                title = f'{remove_forbidden_chars(title)}/'
            else:
                title = ''

            path = f"{course_name}/{title}"

            for li in subject.xpath('.//li'):
                url = li.xpath('.//a/@href').get()

                table = li.xpath('.//table[@class="MsoNormalTable"]')
                if table:
                    urls = table.xpath('.//a/@href').getall()
                    for url in urls:
                        if url:
                            if 'folder' in url:
                                yield scrapy.Request(url=url, meta={'path': path}, callback=self.download_folder)
                            else:
                                yield scrapy.Request(url=url, meta={'path': path}, callback=self.download_file)
                elif url:
                    if 'folder' in li.xpath('@class').get():
                        yield scrapy.Request(url=url, meta={'path': path}, callback=self.download_folder)
                    else:
                        yield scrapy.Request(url=url, meta={'path': path}, callback=self.download_file)

    def download_folder(self, response):
        folder = response.xpath('//div[@role="main"]')
        folder_name = folder.xpath('.//h2/text()').get()
        if folder_name:
            folder_name = f'{remove_forbidden_chars(folder_name)}/'
        else:
            folder_name = ''
        path = f"{response.request.meta['path']}{folder_name}"
        for url in folder.xpath('.//a/@href').getall():
            url = url.replace('?forcedownload=1', '')
            yield scrapy.Request(url=url,
                                 meta={'redirect_urls': response.url, 'path': path},
                                 callback=self.download_file)

    def download_file(self, response):
        if '?' not in response.url:
            print(f'\rDownloading: {unquote(response.url)}', end='')
            moodle_file = MoodleItem()
            download_link = response.url
            moodle_file['file_urls'] = [download_link]
            moodle_file['path'] = response.request.meta['path']
            yield moodle_file


# Only for pyinstaller:

import scrapy.utils.misc
import scrapy.core.scraper


def warn_on_generator_with_return_value_stub(spider, callable):
    pass


scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
