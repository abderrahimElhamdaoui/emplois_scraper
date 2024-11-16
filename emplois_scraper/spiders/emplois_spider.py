import scrapy
from scrapy_splash import SplashRequest
import pandas as pd

class EmploisScraper(scrapy.Spider):
    name = "jobsma"
    
    # URL de départ
    start_urls = [
        'https://myjobalert.ma/jobs/?contract=stage'
    ]
    
    # Utilisation d'un script Lua pour contrôler le comportement de Splash
    lua_script = """
    function main(splash, args)
        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        splash:go(args.url)
        splash:wait(5)  -- Attendre le rendu complet de la page
        return splash:html()  -- Retourner le HTML une fois chargé
    end
    """
    
    lua_script2 = """
    function main(splash, args)
        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        splash:go(args.url)
        splash:wait(2)  -- Attendre le rendu complet de la page
        return splash:html()  -- Retourner le HTML une fois chargé
    end
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = [] 
        self.nb=0
        self.file_name = 'job_offers.xlsx'
        self.data = pd.DataFrame(columns=["title", "company_info", "location", "verified",'contract','type','ville','experience','description'])

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': self.lua_script}, dont_filter=True)
    
    def parse(self, response):
        for job in response.css('div.w-full.md\\:w-3\\/6.mx-1.flex.flex-col'):
            tmp_job_link = job.css('a::attr(href)').get()
            job_link = response.urljoin(tmp_job_link.strip())
            job_title = job.css('h2.text-lg.font-bold::text').get()

            company_info = job.css('p.text-gray-700::text').get()
            location = job.css('p.text-gray-700 span::text').get()

            verified = job.css('span.bg-green-600::text').get()

            if job_link and job_title:
                job_data= {
                    'title': job_title.strip(),
                    'link': response.urljoin(job_link.strip()),
                    'company_info': company_info.strip() if company_info else None,
                    'location': location.strip() if location else None,
                    'verified': verified.strip() if verified else None,
                }
                yield SplashRequest(job_link, callback=self.parse_job_details, endpoint='execute', 
                                args={'lua_source': self.lua_script2, 'url': job_link}, 
                                meta={'job_data': job_data}, dont_filter=True)
                
        next_page = response.css('a.w-auto.p-2.px-4.bg-white.border-2::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_job_details(self, response):
        job_data = response.meta['job_data']
        Contract= response.xpath('.//span[@id="selectedJobcontract_type"]//text()').get().strip()
        type= response.xpath('.//span[@id="selectedJobtype"]//text()').get().strip()
        ville= response.xpath('.//span[@id="selectedJobcity"]//text()').get().strip()
        exp=response.xpath('.//div[@class="experience"]/span[@class="text-lg font-bold"]//text()').get().strip()
        description=response.xpath('.//div[@id="jobDescription "]//text()').getall()
        des = ' '.join(description).strip()
        job_data.update({'contract': Contract,'type':type,'ville':ville,'experience':exp,'description':des})
        self.jobs.append(job_data)
        self.ajouter_donnees()

    def ajouter_donnees(self):
        self.data = pd.DataFrame(self.jobs)
        self.sauvegarder_excel()

    def sauvegarder_excel(self):
        self.data.to_excel(self.file_name, index=False)
        self.log(f'Données enregistrées dans {self.file_name}')