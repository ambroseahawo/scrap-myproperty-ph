# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import os
from datetime import datetime

from scrapy.utils.log import configure_logging

from helper import setup_project_folders

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

setup_project_folders()

# set logging
file_path = os.path.join(os.getcwd(), "logs")
timestamp = f'{BOT_NAME}_{datetime.today().strftime("%Y-%m-%d_%H-%M-%S")}.log'

LOG_FILE = os.path.join(file_path, timestamp)
LOG_LEVEL = "DEBUG"

# Configure Scrapy's logging
configure_logging(install_root_handler=False)

# Set up your custom logging
logging.basicConfig(
    level=logging.DEBUG, format="[%(asctime)s] %(name)s %(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logging.getLogger("scrapy-playwright").setLevel(logging.INFO)
logging.getLogger("scrapy_user_agents").setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

# Ensure only one handler is added
if not logger.hasHandlers():
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

CONCURRENT_ITEMS = 100

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

DOWNLOAD_TIMEOUT = 300  # 5 minutes

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# REDIRECT_ENABLED = True

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [301, 302, 429, 500, 502, 503, 504, 408]

COMPRESSION_ENABLED = True

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "scraper.middlewares.PropertyScraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": 300,
    "scraper.middlewares.RotateUserAgentMiddleware": 300,
    "scraper.middlewares.TimeoutMiddleware": 400,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 500,
    "scraper.middlewares.PropertyScraperDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     "scraper.pipelines.PropertyScraperPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

REDIRECT_ENABLED = False
