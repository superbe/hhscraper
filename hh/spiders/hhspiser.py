# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from hh.items import HhItem
from scrapy.loader import ItemLoader


class HhSpider(scrapy.Spider):
    name = 'hhspiser'
    allowed_domains = ['perm.hh.ru']
    start_urls = [
        'https://perm.hh.ru/search/vacancy?clusters=true&enable_snippets=true&only_with_salary=true&specialization=1&' +
        'L_save_area=true&area=113&from=cluster_area&showClusters=true']

    def parse(self, response: HtmlResponse):
        clusters = response.xpath(
            '//ul[contains(@class, "clusters-list")]/li[contains(@class, "clusters-list__item")]/a[contains(@class, ' +
            '"clusters-value")]/@href').extract()

        for area in clusters:
            if "&area=" in area:
                if "area=1&" in area or "area=2&" in area:
                    yield response.follow(area, callback=self.big_city_parse)
                else:
                    yield response.follow(area, callback=self.city_parse)

    def big_city_parse(self, response: HtmlResponse):
        by_metro = response.xpath(
            '//ul[contains(@class, "clusters-list")]/li[contains(@class, "clusters-list__item")]/a[contains(@class, ' +
            '"clusters-value")]/@href').extract()

        for metro in by_metro:
            if "$metro=" in metro:
                yield response.follow(metro, callback=self.city_parse)

    def city_parse(self, response: HtmlResponse):
        next_page = response.xpath(
            '//div[contains(@data-qa, "pager-block")]/a[contains(@data-qa, "pager-next")]/@href').extract_first()
        vacancies = response.xpath(
            '//span[contains(@class, "g-user-content")]/a[contains(@data-qa, "vacancy-serp__vacancy-title")]/@href').extract()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for vacancy in vacancies:
            yield response.follow(vacancy[18:], callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        item = ItemLoader(HhItem(), response)

        item.add_value('url', response.url)
        item.add_xpath('title', '//h1[contains(@data-qa, "vacancy-title")]')
        item.add_xpath('salary', '//p[contains(@class, "vacancy-salary")]')
        item.add_xpath('organisation',
                       '//a[contains(@class, "vacancy-company-name")]/span[contains(@itemprop, "name")]')
        item.add_xpath('organisation_url', '//a[contains(@class, "vacancy-company-name")]/@href')
        item.add_xpath('description', '//div[contains(@data-qa, "vacancy-description")]')

        yield item.load_item()
