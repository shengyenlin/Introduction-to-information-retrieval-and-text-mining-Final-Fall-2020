# IRTM Final Project - 中時新聞產生器

## Tree

```
├── README.md
└── crawl
   ├── crawl
   |  └── spiders
   |     └── news.py                        <-- Web crawler program
   ├── news.json                            <-- Web crawler result
   └── scrapy.cfg
```

## Web Crawler

### Install

```shell
pip install scrapy
```

- 使用 python 3 安裝 `scrapy`

### Usage

```shell
cd crawl
scrapy crawl news -O ../data/news.json
```

- 執行趴蟲程式
- `-O`後的路徑為爬蟲結果輸出的檔案路徑
