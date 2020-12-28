# IRTM Final Project - China Times Generator 中時新聞產生器

## Tree

```
├── README.md
└── crawl
   ├── crawl
   |  └── spiders
   |     └── news.py                        <-- Web crawler program
   └── news.json                            <-- Web crawler result
```

## Web Crawler

### Install

```shell
pip install scrapy
```

- 使用 python 3 安裝 `scrapy`

### Usage

> 要在台大網路或是使用台大 VPN 下才能使用

```shell
cd crawl
scrapy crawl news -O ../data/news.json -a total=100 -a query=韓國瑜
```

- 執行爬蟲程式
- `-O`後的路徑為爬蟲結果輸出的檔案路徑
- `-a total`為爬下來的文章數量，預設為 100
- `-a query`為搜尋的關鍵字，預設為「韓國瑜」

此爬蟲程式將會從知識數網站抓下 2015 到 2020 年的新聞
