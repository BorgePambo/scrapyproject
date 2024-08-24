import scrapy

class MercadoLivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ['https://lista.mercadolivre.com.br/tenis-corrida-masculino']

    page_count = 1
    max_page = 10

    def parse(self, response):
        items = response.css('div.ui-search-result__content')

        for item in items:
            brand_name = item.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get()
            name = item.css('h2.ui-search-item__title::text').get()

            prices = item.css('span.andes-money-amount__fraction::text').getall()
            cents = item.css('span.andes-money-amount__cents::text').getall()

            old_price_reais = prices[0] if len(prices) > 0 else None
            new_price_reais = prices[1] if len(prices) > 1 else None

            old_price_centavos = cents[0] if len(cents) > 0 else None
            new_price_centavos = cents[1] if len(cents) > 1 else None

            reviews_rating_number = item.css('span.ui-search-reviews__rating-number::text').get()
            reviews_amount = item.css('span.ui-search-reviews__amount::text').get()

            if brand_name and name:
                yield {
                    'brand': brand_name,
                    'name': name,
                    'old_price_reais': old_price_reais,
                    'new_price_reais': new_price_reais,
                    'old_price_centavos': old_price_centavos,
                    'new_price_centavos': new_price_centavos,
                    'rating': reviews_rating_number,
                    'reviews': reviews_amount
                }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page: 
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
