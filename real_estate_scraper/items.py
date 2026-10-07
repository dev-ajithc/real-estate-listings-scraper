import scrapy


class PropertyItem(scrapy.Item):
    listing_id = scrapy.Field()
    title = scrapy.Field()
    status = scrapy.Field()
    price = scrapy.Field()
    price_period = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    area_sqft = scrapy.Field()
    property_type = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    postal_code = scrapy.Field()
    agent = scrapy.Field()
    listing_url = scrapy.Field()
    scraped_at = scrapy.Field()
