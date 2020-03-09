# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import re
import dateutil.parser

regex_html = re.compile(r'(\<(/?[^>]+)>)')
regex_s = re.compile(r'\s+')
regex_d = re.compile(r'\d+')


def clear_description(value):
    return regex_s.sub(' ', regex_html.sub('', value)).strip()


def clear_vacancy(value):
    return clear_description(value).split('(')[0].strip()


def clear_salary(value):
    return regex_d.findall(clear_description(value).replace(' ', ''))


def clear_min_salary(value):
    return int(clear_salary(value)[0])


def clear_max_salary(value):
    result = clear_salary(value)
    return int(result[1]) if len(result) == 2 else int(result[0])


def clear_city(value):
    return clear_description(value).split(',')[0].strip()


def clear_address(value):
    result = clear_description(value).split(',')
    return int(result[1].strip()) if len(result) == 2 else 'Без адреса'


def clear_tags(value):
    return clear_description(value).split(', ')


def clear_date(value):
    return dateutil.parser.parse(value)


class HhItem(scrapy.Item):
    # Идентификатор записи.
    _id = scrapy.Field()
    # Ссылка на вакансию.
    url = scrapy.Field(output_processor=TakeFirst())
    # Дата парсинга.
    parse_date = scrapy.Field(output_processor=TakeFirst())
    # Регион.
    region = scrapy.Field(output_processor=TakeFirst())
    # Заголовок вакансии.
    # title = scrapy.Field(input_processor=MapCompose(clear_description), output_processor=TakeFirst())
    # Вакансия.
    vacancy = scrapy.Field(input_processor=MapCompose(clear_vacancy), output_processor=TakeFirst())
    # Описание.
    # description = scrapy.Field(input_processor=MapCompose(clear_description), output_processor=TakeFirst())
    # Зарплата.
    # salary = scrapy.Field(input_processor=MapCompose(clear_description), output_processor=TakeFirst())
    # Минимальная величина вакансии.
    min_salary = scrapy.Field(input_processor=MapCompose(clear_min_salary), output_processor=TakeFirst())
    # Максимальная величина вакансии.
    max_salary = scrapy.Field(input_processor=MapCompose(clear_max_salary), output_processor=TakeFirst())
    # Город.
    city = scrapy.Field(input_processor=MapCompose(clear_city), output_processor=TakeFirst())
    # Адрес.
    address = scrapy.Field(input_processor=MapCompose(clear_address), output_processor=TakeFirst())
    # Опыт работы.
    experience = scrapy.Field(input_processor=MapCompose(clear_tags), output_processor=TakeFirst())
    # Занятость.
    employment = scrapy.Field(input_processor=MapCompose(clear_tags), output_processor=TakeFirst())
    # Дата публикации
    publication_date = scrapy.Field(input_processor=MapCompose(clear_date), output_processor=TakeFirst())
    # Организация.
    # organisation = scrapy.Field(input_processor=MapCompose(clear_description), output_processor=TakeFirst())
    # Урла организации.
    # organisation_url = scrapy.Field(output_processor=TakeFirst())
