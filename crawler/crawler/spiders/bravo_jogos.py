import scrapy


class PlayEasySpider(scrapy.Spider):
    name = "bravo_jogos"
    start_urls = [
        'https://bravojogos.com.br/jogos-de-tabuleiro-e-cardgames?page=1',
    ]
    base_url = 'https://bravojogos.com.br'

    def parse(self, response, **kwargs):

        for game in response.css('ul#product-list li'):
            discount = game.css('div.product-info p.product-old-price')
            data = {'with_discount': True if discount else False}
            if discount:
                data['old_price'] = discount.css('span.product-strikethrough-price del::text').get().strip()
            data.update({
                'name': game.css('div.product-name h2::text').get(),
                'price': game.css('div.product-info p.product-cash-price span::text').get().strip(),
                'url': self.base_url + game.css('div.product-name a.product-link::attr("href")').get(),
                'image': game.css('div.product-image picture img::attr("src")').get()
            })
            yield data

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
