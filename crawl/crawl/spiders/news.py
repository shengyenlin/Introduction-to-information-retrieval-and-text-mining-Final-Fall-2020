import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['kmw.chinatimes.com']
    start_urls = ['http://kmw.chinatimes.com/Login.aspx']
    y_list = list(reversed(range(2015, 2021)))

    def parse(self, response):
        self.total = int(getattr(self, 'total', 30))
        self.query = getattr(self, 'query', '韓國瑜')

        formdata = {
            '__EVENTTARGET': 'lbInfotimesLogin',
            '__EVENTARGUMENT': '',
        }

        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.afterLogin,
            dont_click=True
        )

    def afterLogin(self, response):
        if 'Index.aspx' not in response.request.url:
            self.logger.error('Login error.')
        else:
            url = 'http://kmw.chinatimes.com/News/NewsSearch.aspx?searchkind=s'
            yield response.follow(url, callback=self.startSearch)

    def startSearch(self, response):
        for y in self.y_list:
            if self.total < 0:
                break

            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    'ctl00$ContentPlaceHolder1$btnSearch': '執行檢索',
                    'ctl00$ContentPlaceHolder1$DateScope1$ddlRange': 'Y:-1',
                    'ctl00$ContentPlaceHolder1$DateScope1$txtSDate': str(y)+'/01/01',
                    'ctl00$ContentPlaceHolder1$DateScope1$txtEDate': str(y)+'/12/31',
                    'ctl00$ContentPlaceHolder1$txtKeyword': self.query,
                    'ctl00$ContentPlaceHolder1$ckChina': '1',
                    'ctl00$ContentPlaceHolder1$ckBines': None,
                    'ctl00$ContentPlaceHolder1$ckWang': None,
                },
                callback=self.setSearchOptions,
                dont_click=True
            )

    def setSearchOptions(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$UCPage1$ddlPageSize',
                'ctl00$ContentPlaceHolder1$UCPage1$ddlPageSize': '30',
            },
            callback=self.parseNewsList,
            dont_click=True
        )

    def parseNewsList(self, response):
        if self.total < 0:
            return

        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$UCPage1$lbtnPageNext',
                '__EVENTARGUMENT': '',
            },
            callback=self.parseNewsList,
            dont_click=True
        )

        for news in response.css('.temp-gvList-row'):
            self.total -= 1
            if self.total < 0:
                return

            url = news.css('td')[4].css('a::attr(href)').get()
            url = url.replace('sKeyword='+self.query, 'sKeyword=')
            yield response.follow(url, callback=self.parseNewsPage)

    def parseNewsPage(self, response):
        title = response.css('h1::text').get()
        date = response.css(
            '#ctl00_ContentPlaceHolder1_UCNewsContent1_lbldateAuth::text').get().split('-')[0]
        txt = response.css('article#dvContainer').getall()[0]
        txt = txt.replace('<article class="clear-fix" id="dvContainer">', '')
        txt = txt.split('<style>')[0]
        txt = txt.split('<br><br>')
        author = txt[0].split()[0]
        content_block = txt[1:]
        content_block = [c.replace('\n', '').replace('\u3000', '').split()[0]
                         for c in content_block if len(c.split()) > 0]
        content = ''
        for c in content_block:
            content += '  ' + c + '\n'
        content = content.rsplit(maxsplit=0)[0]

        yield {
            'title': title,
            'date': date,
            'author': author,
            'content': content
        }
