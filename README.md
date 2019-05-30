# Sitemap Generator Tool

> Based on single threaded web crawler. Implemented in Python3.
The general behaviour can be described as neutral/polite. Sitemap is created in both XML file format, as well as plotted as a graph. Developed as part of the degree specification for BSc Computer Science with Distributed Systems, University of Leeds 2019.
## Table of Contents 

- [Installation](#installation)
  - [Automatic](#automatic)  
  - [Manual](#manual)
- [Crawler behaviour](#behaviour)
- [Features](#features)
  - [Proxies](#proxies)
  - [User Agents](#user-agents)
  - [Page limit](#page-limit)
  - [Depth limit](#depth_limit)
- [Sitemaps](#)
  - [XML](#xml)
  - [Graphical](#graph)
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
## Crawler behaviour
### Neutral
Default at startup. Crawler will respect the robots exclusion protocol and will set a `Crawl-delay:`, if one is specified.

### Polite
Crawler will respect the robots exclusion protocol and will check for a `Crawl-delay:`. If there is no delay set in `robots.txt`, the crawler will use adaptive delay calculated from the server response time. This prevents slower servers from getting overloaded with requests.

### Aggressive
Crawler ignores any specified delays but will respect the `robots.txt` file. Proxies support enabled by default in this mode.

## Features
### Proxies
Proxies are scraped from [SSLproxies](https://www.sslproxies.org/) using BeautifulSoup4. All one hundred proxies are tested by making requests to a random URL and checking the status code for the response. Each request has a TTL of two(2) seconds. Increasing the timeout value in file [proxyFinder.py] will result in bigger final list of proxies but will increase the time required to test all proxies. Smaller timeouts will result in fewer available proxies, however the testing phase is completed much faster.

### User agents
Requests can be made with randomly generated user-agents using [fake-useragent](https://github.com/hellysmile/fake-useragent)

### Limits
#### Depth Limit

## Optional Arguments


| Argument | Description| Accepted values|
| ---| --- | ---     |
| limit| Crawl only N URLs       | Positive Integer      |
| depth | Crawl until depth level | Positive Integer      |
| proxies | Enable proxy support | Boolean               |
| crawl_mode | Specify behaviour | `aggressive`/`polite` |

## Usage 
### Standard crawling
```shell
> python3 main.py toscrape.com
```

### Crawl only 500 pages from the specified URL
```shell
> python3 main.py www.leeds.ac.uk --proxies
```




