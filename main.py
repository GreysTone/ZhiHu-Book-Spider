import urllib.request
from html.parser import HTMLParser

class GTBook:

  def __init__(self):
    self.title = ""
    self.author = ""
    self.price = ""
    self.link = ""

  def setTitle(self, title):
    self.title = title

  def setAuthor(self, author):
    self.author = author

  def setPrice(self, price):
    self.price = price

  def setLink(self, link):
    self.link = link

  def printBook(self):
    print(self.title + "-" + self.author + "/" + self.price)
    print(self.link)

class GTParser(HTMLParser):
  engagedLi = False
  engagedA = False
  engagedSpan = False
  rowling = 0
  book = GTBook()
  bookList = []

  def handle_starttag(self, tag, attr):
    if tag == 'li':
      self.engagedLi = True
    if tag == 'a':
      self.engagedA = True
      if self.engagedLi:
        for name, value in attr:
          if name == 'href':
            link = "https://www.zhihu.com" + value
            self.book.setLink(link)
            # print(link)
    if self.engagedA and tag == 'span':
      self.engagedSpan = True

  def handle_endtag(self, tag):
    if tag == 'li':
      self.engagedLi = False
    if tag == 'a':
      self.engagedA = False
    if tag == 'span':
      self.engagedSpan = False

  def handle_data(self, data):
    if self.engagedSpan:
      if self.rowling == 3:
        self.rowling = 0
      if self.rowling == 2:
        self.book.setPrice(data)
        self.rowling += 1
        # self.book.printBook()
        self.bookList.append(self.book)
      if self.rowling == 1:
        self.book.setAuthor(data)
        self.rowling += 1
      if self.rowling == 0:
        self.book.setTitle(data)
        self.rowling += 1


if __name__ == "__main__":

  url = "https://www.zhihu.com/publications/nacl"
  data = urllib.request.urlopen(url).read()
  page = data.decode('UTF-8')
  # print('decoded ' + url)
  gtParser = GTParser()

  gtParser.feed(page)
  gtParser.close()

  print(len(gtParser.bookList))

  for book in gtParser.bookList:
    book.printBook()

