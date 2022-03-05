import scrapy


class PlayEasySpider(scrapy.Spider):
    name = "playeasy"
    start_urls = [
        'https://www.playeasy.com.br/board-games.html?p=1',
    ]

    def parse(self, response, **kwargs):
        for game in response.css('ul.products-grid li'):
            discount = game.css('div.price-box p.old-price')
            data = {'with_discount': True if discount else False}
            if discount:
                data['old_price'] = discount.css('span.price::text').get().strip()
            data.update({
                'name': game.css('h2.product-name a::attr("title")').get(),
                'price': game.css('span.priceAvista span.price::text').get(),
                'description': game.css('div.descripthome::text').get().strip(),
                'image': game.css('a.product-image img::attr("src")').get()
            })
            yield data

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
