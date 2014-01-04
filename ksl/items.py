# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class KslItem(Item):
    id = Field()
    ksl_id = Field()
    crawled = Field()
    year = Field()
    make = Field()
    model = Field()
    trim = Field()
    body = Field()
    mileage = Field()
    vin = Field()
    title_type = Field()
    exterior_color = Field()
    interior_color = Field()
    transmission = Field()
    liters = Field()
    cylinders = Field()
    fuel = Field()
    doors = Field()
    exterior_condition = Field()
    interior_condition = Field()
    drive = Field()
    seller = Field()
    list_price = Field()
    edmunds_price = Field()
    description = Field()
    created_at = Field()
    modified_at = Field()
    active = Field()
    used = Field()