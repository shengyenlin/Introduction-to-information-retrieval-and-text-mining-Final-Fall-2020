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

### Usage

```shell
cd crawl
scrapy crawl news -O ../data/news.json
```
