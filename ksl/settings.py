# Scrapy settings for ksl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ksl'

SPIDER_MODULES = ['ksl.spiders']
NEWSPIDER_MODULE = 'ksl.spiders'
ITEM_PIPELINES = {
	'ksl.pipelines.MySQLPipeline': 500
}
DOWNLOAD_DELAY = 0.25

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ksl (+http://www.yourdomain.com)'
