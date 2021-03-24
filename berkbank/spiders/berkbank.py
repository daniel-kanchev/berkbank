import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from berkbank.items import Article


class BerkbankSpider(scrapy.Spider):
    name = 'berkbank'
    start_urls = ['https://www.berkbank.com/news.php']

    def parse(self, response):
        links = response.xpath('//a[@class="center_area"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//span[@class="standard_text_bold"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//span[@class="standard_text_date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//span[@class="standard_text"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
