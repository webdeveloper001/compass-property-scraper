import scrapy
import urllib
import json
from compass_agent.items import CompassAgentItem
import datetime
import time
import pdb

class Compass(scrapy.Spider):
    name = "compass_agent"
    count = 0
    def start_requests(self):
        url = "https://www.compass.com/agents/"
            # referer: https://www.alamo.com/en_US/car-rental/reservation/selectCar.html
        yield scrapy.Request(url=url, callback=self.parse_regions, method="GET")

    def parse_regions(self, response):
        for atag in response.css('a.geographyMosaicTile::attr(href)').getall():

            url = "https://www.compass.com{}".format(atag)
            # print(url)
            yield scrapy.Request(url= url, callback=self.parse_agents, method="GET")

    def parse_agents(self, response):
        for atag in response.css('a.agentCards-imageWrapper::attr(href)').getall():
            url = "https://www.compass.com{}".format(atag)
            yield scrapy.Request(url= url, callback=self.parse_agent, method="GET")

    def parse_agent(self, response):
        item = CompassAgentItem()
        item['Name'] = response.css('h1.agents1506-profile-cardName::text').get()
        item['Email'] = response.css('div.agents1506-profile-cardEmail a.agents1506-profile-link::text').get()
        item['Cell'] = response.css('div.agents1506-profile-cardPhone a.agents1506-profile-link::text').get()
        body = response.body.decode("utf-8").split("sales: [")[1].split("rentals: [")[0]
        item['Sales'] = body.count("priceStatusUpdated")
        yield item
        # print(response.css('div.agents1506-profile-cardEmail a.agents1506-profile-link::text').get())
