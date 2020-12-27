import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['kmw.chinatimes.com']
    start_urls = ['http://kmw.chinatimes.com/Login.aspx']
    total = 100

    def parse(self, response):
        formdata = {
            '__EVENTTARGET': 'lbInfotimesLogin',
            '__EVENTARGUMENT': '',
        }

        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            callback=self.after_login,
            dont_click=True
        )

    def after_login(self, response):
        if 'Index.aspx' not in response.request.url:
            self.logger.error('Login error.')
        else:
            url = 'http://kmw.chinatimes.com/KMTree/TaiwanNews.aspx?query=&attr=MA0'
            yield response.follow(url, callback=self.setSearchOptions)

    def setSearchOptions(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '__EVENTTARGET': 'ctl00$content$ddlPageSize',
                '__EVENTARGUMENT': '',
                'ctl00$content$ddlPageSize': '30',
                'ctl00$content$DateScope$ddlRange': 'Y:-2',
                'ctl00$content$DateScope$txtSDate': '2018/12/01',
                'ctl00$content$DateScope$txtEDate': '2020/12/01',
                'ctl00$content$hfKeyword': '韓國瑜',
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
                '__EVENTTARGET': 'ctl00$content$lbPagerNext',
                '__EVENTARGUMENT': '',
            },
            callback=self.parseNewsList,
            dont_click=True
        )

        for news in response.css('tr'):
            if self.total < 0:
                return

            if '中時' in news.css('td::text')[-1].get():
                self.total -= 1
                url = news.css('td')[2].css('a::attr(href)').get()
                url = url.split('\'')[1].replace(
                    '\\\\', '\\').replace('sKeyword=韓國瑜', 'sKeyword=')
                print(url)
                print(news.css('td::text')[-1].get())
                yield response.follow(url, callback=self.parseNewsPage)

    def parseNewsPage(self, response):
        print(response.css('font::text').getall())
        title = response.css('h1::text').get()
        txt = response.css('article#dvContainer').getall()[0]
        txt = txt.replace('<article class="clear-fix" id="dvContainer">', '')
        txt = txt.split('<style>')[0]
        txt = txt.split('<br><br>')
        author = txt[0].split()[0]
        content_block = txt[1:]
        content_block = [c.replace('\n', '').replace('\u3000', '').split()[0]
                         for c in content_block]
        content = ''
        for c in content_block:
            content += '  ' + c + '\n'
        content = content.rsplit(maxsplit=0)[0]

        yield {
            'title': title,
            'author': author,
            'content': content
        }
