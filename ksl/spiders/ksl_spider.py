from scrapy import signals
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ksl.items import KslItem
import string, re, time, datetime

class KslSpider(BaseSpider):
	name = "ksl"
	allowed_domains = ['ksl.com']
	start_urls = [
		'http://www.ksl.com/auto/search/index'
	]

	def parse(self, response):

		# Initialize the HTML node selector thingy
		hxs = HtmlXPathSelector(response)

		# Grab all the vehicles listed on the page, they
		# should have the class "srp-listing-body" set
		vehicles = hxs.select('//div[@class="srp-listing-body"]')

		items = []

		for vehicle in vehicles:

			# Instantiate a new KslItem
			item = KslItem()

			# Grab the link from the listing
			link = vehicle.select('div[@class="srp-listing-body-right"]/div[@class="srp-listing-title"]/a/@href').extract()[0]

			# Extract the Vehicle ID from the link.
			# Should be the number between the last / and the first ?
			item['ksl_id'] = link[link.rfind('/') + 1:link.find('?')]

			url = "http://www.ksl.com/auto/listing/" + item['ksl_id']

			yield Request(url, callback=self.vehicle)

		yield Request('http://www.ksl.com/auto/search/index', callback=self.parse)

	def vehicle(self, response):
		hxs = HtmlXPathSelector(response)
		item = KslItem()

		# Build a regex expression consisting of punctuation
		# so we can strip it from appropriate fields
		p_regex = re.compile('[%s]' % re.escape(string.punctuation))

		# Check if vehicle listing is still good

		item['ksl_id'] = hxs.select('//*[@id="ad_id"]/text()').extract()[0]
		item['year'] = hxs.select('//*[@id="specificationsTable"]/tr[1]/td[2]/text()').extract()[0]
		item['make'] = hxs.select('//*[@id="specificationsTable"]/tr[2]/td[2]/text()').extract()[0]
		item['model'] = hxs.select('//*[@id="specificationsTable"]/tr[3]/td[2]/text()').extract()[0]
		item['trim'] = hxs.select('//*[@id="specificationsTable"]/tr[4]/td[2]/text()').extract()[0]
		item['body'] = hxs.select('//*[@id="specificationsTable"]/tr[5]/td[2]/text()').extract()[0]
		item['mileage'] = hxs.select('//*[@id="specificationsTable"]/tr[6]/td[2]/text()').extract()[0]

		# VIN numbers are sometimes provided as links, try to get it as plaintext first,
		# and if that fails, try to grab it from a link
		try:
			item['vin'] = hxs.select('//*[@id="specificationsTable"]/tr[7]/td[2]/text()').extract()[0]
		except IndexError:
			item['vin'] = hxs.select('//*[@id="specificationsTable"]/tr[7]/td[2]/a/text()').extract()[0]

		item['title_type'] = hxs.select('//*[@id="specificationsTable"]/tr[8]/td[2]/text()').extract()[0]
		item['exterior_color'] = hxs.select('//*[@id="specificationsTable"]/tr[9]/td[2]/text()').extract()[0]
		item['interior_color'] = hxs.select('//*[@id="specificationsTable"]/tr[10]/td[2]/text()').extract()[0]
		item['transmission'] = hxs.select('//*[@id="specificationsTable"]/tr[11]/td[2]/text()').extract()[0]
		item['liters'] = hxs.select('//*[@id="specificationsTable"]/tr[12]/td[2]/text()').extract()[0]
		item['cylinders'] = hxs.select('//*[@id="specificationsTable"]/tr[13]/td[2]/text()').extract()[0]
		item['fuel'] = hxs.select('//*[@id="specificationsTable"]/tr[14]/td[2]/text()').extract()[0]
		item['doors'] = hxs.select('//*[@id="specificationsTable"]/tr[15]/td[2]/text()').extract()[0]
		item['exterior_condition'] = hxs.select('//*[@id="specificationsTable"]/tr[16]/td[2]/text()').extract()[0]
		item['interior_condition'] = hxs.select('//*[@id="specificationsTable"]/tr[17]/td[2]/text()').extract()[0]
		item['drive'] = hxs.select('//*[@id="specificationsTable"]/tr[18]/td[2]/text()').extract()[0]

		# The fsbo class contains a string indicating both the seller and new/used
		# status of the vehicle like this "Used Vehicle For Sale By Dealer". Just check
		# for the presence of New/Used and Dealer/Owner
		fsbo = hxs.select('//*[@id="titleMain"]/div[2]').extract()[0]
		if("Used" in fsbo):
			item['used'] = 1
		if("New" in fsbo):
			item['used'] = 0
		if("Owner" in fsbo):
			item['seller'] = "Owner"
		if("Dealer" in fsbo):
			item['seller'] = "Dealer"

		# Strip the punctuation from the list price
		list_price = hxs.select('//*[@id="titleMain"]/h3/text()').extract()[0]
		item['list_price'] = p_regex.sub('', list_price)

		item['description'] = hxs.select('//*[@id="description"]/text()').extract()

		item['created_at'] = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
		item['modified_at'] = item['created_at']
		item['active'] = 1
		item['crawled'] = 1

		# Get rid of the garbage fields so as not to fuck up the database
		for key in item.keys():
			if item[key]=='\t\t\t\t\t\t\t':
				item[key] = ''

		return item