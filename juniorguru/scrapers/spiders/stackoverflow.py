import re

from scrapy import Spider as BaseSpider
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, MapCompose, TakeFirst

from juniorguru.scrapers.items import (Job, absolute_url,
                                       parse_relative_time, split)


class Spider(BaseSpider):
    name = 'stackoverflow'
    start_urls = [
        'https://stackoverflow.com/jobs?mxs=Junior&sort=p&l=Seč%2C+Czechia&d=350&u=Km'
    ]

    def parse(self, response):
        links = response.css('.-job h2 a')
        yield from response.follow_all(links, callback=self.parse_job)

        links = response.xpath("//a[contains(@class, 's-pagination--item')]")
        yield from response.follow_all(links, callback=self.parse)

    def parse_job(self, response):
        loader = Loader(item=Job(), response=response)
        loader.add_css('title', 'h1 a::text')
        loader.add_value('link', response.url)
        loader.add_css('company_name', 'h1 ~ div a::text')
        loader.add_css('company_link', 'h1 ~ div a::attr(href)')
        loader.add_xpath('location', '//h1/following-sibling::div/*[last()]/text()')
        loader.add_xpath('employment_types', "//span[contains(., 'Job type:')]/following-sibling::span/text()")
        loader.add_xpath('experience_levels', "//span[contains(., 'Experience level:')]/following-sibling::span/text()")
        loader.add_xpath('posted_at', "//div[contains(./text(), 'Posted')]/text()")
        loader.add_xpath('description_html', "//section[contains(.//h2/text(), 'Job description')]")
        yield loader.load_item()


def clean_location(text):
    return re.sub(r'^–\s*', '', re.sub(r'[\n\r]+', ' ', text.strip()))


class Loader(ItemLoader):
    default_output_processor = TakeFirst()
    company_link_in = MapCompose(absolute_url)
    employment_types_out = Identity()
    location_in = MapCompose(clean_location)
    posted_at_in = MapCompose(parse_relative_time)
    experience_levels_in = MapCompose(str.lower, split)
    experience_levels_out = Identity()
