from .tenki import TenkiCrawler

class Crawler:
  @classmethod
  def crawl_all(cls):
    TenkiCrawler.crawl('関東・甲信', '神奈川', '横浜')
