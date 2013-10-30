from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter
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

		# Get the JSON file initialized
		resultFile = open('results.json', 'w+b')
		exporter = JsonItemExporter(resultFile)
		exporter.start_exporting()

		# Initialize the HTML node selector thingy
		hxs = HtmlXPathSelector(response)

		# Grab all the vehicles listed on the page, they
		# should have the class "srp-listing-body" set
		vehicles = hxs.select('//div[@class="srp-listing-body"]')

		for vehicle in vehicles:

			# Instantiate a new KslItem
			item = KslItem()

			# Grab the link from the listing
			link = vehicle.select('div[@class="srp-listing-body-right"]/div[@class="srp-listing-title"]/a/@href').extract()[0]

			# Extract the Vehicle ID from the link.
			# Should be the number between the last / and the first ?
			item['vid'] = link[link.rfind('/') + 1:link.find('?')]

			# Assemble vehicle page URL
			vurl = 'http://www.ksl.com/auto/listing/' + item['vid']

			# Crawl the vehicle page here...

			# Export the item to the JSON file
			exporter.export_item(item)

		# Finish exporting and close the JSON file
		exporter.finish_exporting()
		resultFile.close()