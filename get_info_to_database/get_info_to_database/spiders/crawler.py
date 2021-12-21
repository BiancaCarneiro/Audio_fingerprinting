import scrapy
import pandas as pd
from ..items import musicInfo


class GetInfoSpider(scrapy.Spider):
    name = "aranha"
    start_urls = [
        "https://www.vagalume.com.br/arctic-monkeys/discografia/am.html",
        "https://www.vagalume.com.br/of-monsters-and-men/discografia/my-head-is-an-animal.html"
    ]

    def parse(self, response):
        data = {
            "Nome" : [],
            "Album" : [],
            "Data" : [],
            "Artista" : [],
            "Genero" : []
        }
        name = response.css(".nameMusic::text").extract()
        data["Nome"] = response.css(".nameMusic::text").extract()
        data["Album"] = [response.css(".albumTitle a::text").get()]*len(name)
        data["Data"] = [response.css(".albumYear::text").get()]*len(name)
        data["Artista"] = [response.css(".long a::text").get()]*len(name)
        data["Genero"] = [response.css(".h14 a::text").extract()]*len(name)
        
        df = pd.DataFrame.from_dict(data)
        df.to_csv("info.csv", index=False, mode='a', header=False)
        
        