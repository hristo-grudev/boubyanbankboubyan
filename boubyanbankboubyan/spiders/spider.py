import scrapy

from scrapy.loader import ItemLoader

from ..items import BoubyanbankboubyanItem
from itemloaders.processors import TakeFirst


class BoubyanbankboubyanSpider(scrapy.Spider):
	name = 'boubyanbankboubyan'
	start_urls = ['https://boubyan.bankboubyan.com/en/explore-boubyan/news-press-release/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="item"]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//a[@style="color:#D22630"]/text()[normalize-space()]').get()
		print(title, response)
		description = response.xpath('//div[@id="contentdiv"]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BoubyanbankboubyanItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
