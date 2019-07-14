# Sitemap Generator Tool

> Based on single threaded web crawler. Implemented in Python3.
The general behaviour can be described as neutral/polite. Sitemap is created in both XML file format, as well as plotted as a graph. Developed as part of the degree specification for BSc Computer Science with Distributed Systems, University of Leeds 2019.
## Table of Contents 

- [Installation](#installation)
  - [Automatic](#automatic)  
  - [Manual](#manual)
- [CLI](#)
  - [Optional parameters](#optional_args)
  - [Accepted seed URLs](#accepted_seed)
- [Crawler behaviour](#behaviour)
  - [Neutral](#neutral_b)
  - [Polite](#polite_b)
  - [Aggressive](#aggresive_b)
- [Features](#features)
  - [Proxies](#proxies)
  - [User Agents](#user-agents)
  - [Page limit](#page-limit)
  - [Depth limit](#depth_limit)
- [Usage](#usage)
- [Issues](#issues)

---

## Installation
Make sure that tkinter is installed on your operating system.

```shell
$ sudo apt-get install python3-tk
```

### Automatic 

Run the basic script that sets up the virtual environment and installs required packages

```shell
$ sh setup.sh
```

### Manual 

Set up virtual environment

```shell
$ python3 -m venv [virtualenv_name]
```
Once in the folder virtualenv_name, the virtual environment must be started.

```shell
$ python3 -m source bin/activate
```

All external packages must be installed. We have included a file called requirements.txt with
all containing all packages to speed up the process.

```shell
$ pip3 install -r requirements.txt
```

## CLI

```shell
> python3 main.py seed_url [--optional_parameter]
```

### Accepted seed URLs

|  | Accepted|
| ---| ---     |
| leeds.ac.uk| :heavy_check_mark: |
| http://www.leeds.ac.uk | :heavy_check_mark:|
| http://leeds.ac.uk | :heavy_check_mark: |
| https://www.leeds.ac.uk/events | :heavy_check_mark: |
| www.leeds.ac.uk | :heavy_check_mark: |

### Optional Parameter

| Parameter | Description| Accepted values|
| ---| --- | ---     |
| limit| Crawl only N URLs       | Positive Integer      |
| depth | Crawl until depth level | Positive Integer      |
| proxies | Enable proxy support | Boolean               |
| crawl_mode | Specify behaviour | `aggressive`/`polite` |


## Crawler behaviour
### Neutral
Default at startup. Crawler will respect the robots exclusion protocol and will set a `Crawl-delay:`, if one is specified.

Ideal for medium to large scale websites that do not impose any politeness policies over the crawler

### Polite
Crawler will respect the robots exclusion protocol and will check for a `Crawl-delay:`. If there is no delay set in `robots.txt`, the crawler will use adaptive delay calculated from the server response time. This prevents slower servers from getting overloaded with requests.

Ideal for small scale websites

### Aggressive
Crawler ignores any specified delays but will respect the `robots.txt` file. Proxies support enabled by default in this mode.

Ideal for large scale websites or for the users that own the target website.

## Features
### Proxies
Proxies are scraped from [SSLproxies](https://www.sslproxies.org/) using BeautifulSoup4. All one hundred proxies are tested by making requests to a random URL and checking the status code for the response. Each request has a TTL of two(2) seconds. Increasing the timeout value in [file](proxyFinder.py) will result in bigger final list of proxies but will increase the time required to test all proxies. Smaller timeouts will result in fewer available proxies, however the testing phase is completed much faster.

### User agents
Requests can be made with randomly generated user-agents using [fake-useragent](https://github.com/hellysmile/fake-useragent)

### Limits
#### Depth Limit
Depth of a webpage is the number of clicks required to visit a page, from the homepage. For example https://www.bbc.com/news is at depth 1 (or 0), while https://www.bbc.com/news/technology, has a depth of 2.
#### Crawl Limit
Used to prevent the crawler from visiting more pages than specified.

## Usage 
### Standard crawling
```shell
> python3 main.py toscrape.com
```

### Crawl with proxies enabled
```shell
> python3 main.py www.leeds.ac.uk --proxies
```

### Crawl only 500 pages from the specified URL
```shell
> python3 main.py www.leeds.ac.uk --limit 500
```

### Crawl aggressively pages until level 3
```shell
> python3 main.py www.leeds.ac.uk --crawl_mode aggressive
```

## Issues
- Graphical sitemaps in PDF format become unreadable if the graph contains thousands of nodes.
- Progress is not saved in case of interrupt. 
- Scraped proxies are not guaranteed to work. Testing for each proxy is introduced with slight time impact.
