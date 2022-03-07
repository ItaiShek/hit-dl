BOT_NAME = 'hit_dl'

SPIDER_MODULES = ['hit_dl.spiders']
NEWSPIDER_MODULE = 'hit_dl.spiders'


# downloads folder
FILES_STORE = 'moodle_downloads'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Minimum logging level
LOG_LEVEL = 'WARNING'


# Configure item pipelines
ITEM_PIPELINES = {
    'hit_dl.pipelines.ProcessPipeline': 1,
}