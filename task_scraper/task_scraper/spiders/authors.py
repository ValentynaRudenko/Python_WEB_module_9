import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        authors = []
        for quote in response.xpath("/html//div[@class='quote']"):
            author = quote.xpath("span/small/text()").get()
            if author not in authors:
                authors.append(author)
                author_link = quote.xpath(".//span/a/@href").get()
                yield response.follow(author_link, callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        yield {
                "fullname": response.xpath("//h3/text()").get(),
                "born_date": response.xpath(
                    "//span[@class='author-born-date']/text()").get(),
                "born_location": response.xpath(
                    "//span[@class='author-born-location']/text()").get(),
                "description": response.xpath(
                    "//div[@class='author-description']/text()").get()
                }
