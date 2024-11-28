
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UnsplItem
from itemloaders.processors import MapCompose

class UnsplashItemSpider(CrawlSpider):
    name = "unsplash_rule"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/"]

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class="NHQ0m"]/div[@class="d95fI"]'), callback="parse_item", follow=True),
            Rule(LinkExtractor(restrict_xpaths='//*[@class="oaSYM ZR5jm"]/@href'))
    )
    
    def parse_item(self, response):
        for category in response.xpath('//div[@class="NHQ0m"]/div[@class="d95fI"]/figure//div/a[@class="Prxeh"]/@href').extract():
            yield scrapy.Request(response.urljoin(category), callback=self.parse_category)
            
        loader = ItemLoader(item=UnsplItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath('name_image', '//div[@class="VgSmN"]//div/h1/text()')

        categori_selectors = response.xpath('//div[@class="rx3zu _UNLg"]//div[@class="uK_kT"]/div//span/a/text()')
        categori = [s.get().strip() for s in categori_selectors if s.get().strip()]
        if categori:
            loader.add_value('featured_in', categori)

        image_urls = response.xpath('//div[@class="NHQ0m"]/div[@class="d95fI"]/figure//div/a[@class="Prxeh"]/@href').extract()
        full_image_urls = []
        for url in image_urls:
            full_url = response.urljoin(url)
            full_image_urls.append(full_url)
        loader.add_value('image_urls', full_image_urls)

        

        yield loader.load_item()




# //div[@class="NHQ0m"]/div[@class="d95fI"] - прямая ссылка на изображение...
# //div[@class="NHQ0m"]/div[@class="d95fI"]/figure//div/a[@class="Prxeh"]/@href


# 3. Определите элемент (Item) в Scrapy, который будет представлять изображение. Ваш элемент должен включать такие детали,
#  как URL изображения, название изображения и категорию, к которой оно принадлежит.
# 4. Используйте Scrapy ImagesPipeline для загрузки изображений. Обязательно установите параметр IMAGES_STORE в файле settings.py. Убедитесь, что ваш паук правильно выдает элементы изображений, которые может обработать ImagesPipeline.
# 5. Сохраните дополнительные сведения об изображениях (название, категория) в CSV-файле. Каждая строка должна соответствовать одному изображению и содержать URL изображения, локальный путь к файлу (после загрузки), название и категорию.
# //*[@class="oaSYM ZR5jm"]//div[@class="NHQ0m"]/div[@class="d95fI"]/figure//div/a[@class="Prxeh"]/@href


