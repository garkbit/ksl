from twisted.enterprise import adbapi
from scrapy import log
import datetime
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MySQLPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('pymysql',
			db="ksl",
			user="ksl",
			passwd="password",
			unix_socket="/Applications/MAMP/tmp/mysql/mysql.sock"
			# cursorclass=pymysql.cursors.DictCursor,
			# charset="utf8",
			# use_unicode=True
		)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		# return item

	def _conditional_insert(self,tx,item):
		tx.execute("select * from vehicles where ksl_id = %s", (item['ksl_id'], ))
		result = tx.fetchone()
		if result:
			log.msg("Item already exists: %s" % item['ksl_id'], level=log.DEBUG)
		else:
			tx.execute(\
				"insert into vehicles (ksl_id, crawled, year, make, model, trim, body, mileage, vin, title_type, exterior_color, interior_color, drive, transmission, liters, cylinders, fuel, doors, exterior_condition, interior_condition, seller, list_price, created_at, modified_at, active, used, description) "
				"values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
				(item['ksl_id'], 
				 item['crawled'], 
				 item['year'], 
				 item['make'], 
				 item['model'], 
				 item['trim'], 
				 item['body'], 
				 item['mileage'], 
				 item['vin'], 
				 item['title_type'], 
				 item['exterior_color'], 
				 item['interior_color'], 
				 item['drive'], 
				 item['transmission'], 
				 item['liters'], 
				 item['cylinders'], 
				 item['fuel'], 
				 item['doors'], 
				 item['exterior_condition'], 
				 item['interior_condition'], 
				 item['seller'], 
				 item['list_price'], 
				 item['created_at'], 
				 item['modified_at'], 
				 item['active'], 
				 item['used'],
				 item['description'][0])
			)
			log.msg("Item stored in db: %s" % item['ksl_id'], level=log.DEBUG)

	def handle_error(self,e):
		print e
		log.err(e)