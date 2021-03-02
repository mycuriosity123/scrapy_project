import scrapy
from arabhealth.items import ArabhealthItem

class Companydetails(scrapy.Spider):
    name = "health"
    allowed_domains = ["www.omnia-health.com"]

    def start_requests(self):
        a="https://www.omnia-health.com/exhibitordirectory/arab-health?alpha=all"
        b="https://www.omnia-health.com/exhibitordirectory/arab-health?page={no}&alpha=all"
        urls = [a if i==0 else b.format(no=i) for i in range(0,168)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.xpath('//*[@class="directory-exhibitor exhibitor-pkg-enhanced-extended exhibitor-pkg-wt--5"]//h3/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = ArabhealthItem()
        item['name'] = response.xpath('//*[@class="section-two"]/h1/text()').extract_first()
        item['telephone'] = "".join(response.xpath('//*[@class="section-two"]/text()').extract()).replace("\n","")
        sub_data = response.xpath('//*[@class="section-two"]')
        ss = sub_data.xpath('.//*[@class="company-address"]')
        item['address'] = " ".join([" ".join([p.extract() for p in ss.xpath('.//div//text()')]),ss.xpath('.//*[@class="country"]/text()').extract_first()]).replace("\n","")
        item['website']=sub_data.xpath('.//*[@class="field-item even"]/a/@href').extract_first()
        yield item




