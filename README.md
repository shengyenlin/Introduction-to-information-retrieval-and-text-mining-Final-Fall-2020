# IRTM Final Project - China Times style news generator 中時新聞產生器

## Final project introduction
Our team developed a "news generator" in the style of China Times, as a proactive measure in case China Times news is taken down in the future. This generator will allow us to input keywords and generate news articles that we want to see. To achieve this, we used language models such as N-gram Model, LSTM, and GPT-2, which were discussed in class. In addition, we gathered news content from the internet to create a China Times-style news generator. We tested the effectiveness of this generator by inputting text data based on both "characters" (character-level model) and "terms" (term-level model) into the models separately.

For detailed experiment results, observations, and model comparisons, please refer to the `final_report.pdf` (In Chinese). The report will describe the motivation behind choosing this topic, possible usage scenarios for this model, the dataset used for training, the model used for training, the experimental results, the design of the user interface, and directions for future improvements.

## Model reproduce
Please refer to `./experiment/`

## Tree

```
├── README.md
├── crawl
|  └── crawl
|     └── spiders
|        └── news.py                        <-- Web crawler program
└── data
   └── news.json                            <-- Web crawler result
```

## Web Crawler

### Install

```shell
pip install scrapy
```

### Usage

> To use this program, you need to access the internet through the National Taiwan University network or use the NTU VPN

```shell
cd crawl
scrapy crawl news -O ../data/news.json -a total=100 -a query=韓國瑜
```

- Run the web crawler program.
- `-O` specifies the output file path for the web crawler results.
- `-a total`sets the number of articles to crawl, with a default value of 100.
- `-a query`sets the search keyword, with a default value of "韓國瑜".

This web crawler program will scrape news articles from the [Knowledge Master website](http://kmw.chinatimes.com/) published between 2015 and 2020.
