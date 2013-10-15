from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ksl.items import KslItem

class KslSpider(BaseSpider):
	name = "ksl"
	allowed_domains = ['ksl.com']
	start_urls = [
		'http://www.ksl.com/auto/search/index'
	]

	def parse(self, response):
		filename = response.url.split("/")[-2]
		hxs = HtmlXPathSelector(response)
		vehicles = hxs.select('//div[@class="srp-listing-body"]')
		items = []
		for vehicle in vehicles:
			item = KslItem()
			item['title'] = vehicle.select('div[@class="srp-listing-body-right"]/div[@class="srp-listing-title"]/a/text()').extract()
			link = vehicle.select('div[@class="srp-listing-body-right"]/div[@class="srp-listing-title"]/a/@href')
			item['link'] = link.extract()
			item['vid'] = link.select('string()').extract();
			items.append(item)
		return items
		# open(filename, 'wb').write(response.body)