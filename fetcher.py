import urllib
import csv
import selenium
import glob
from cnkiDriver import CNKIDriver
import os,sys

c_filename = "bookdata/onlyBookName.txt"
c_DestDir = 'fetchedHTML'
class Fetcher:
  def __init__(self):
    self.d = None
    self.dirFilelist = None

  def get_d(self):
    """lazy create CNKIDriver"""
    if self.d is None:
      self.d = CNKIDriver()
      self.d.open()
      self.d.changeSelect()
    return self.d

  def get_booknames(self):
    names = []
    with open(c_filename) as f:
      for line in f.readlines():
        line = line.strip()
        if len(line)>=2:
          names.append(line)
    path = os.getenv('PWD')
    print(path)
    assert 'zhongYaoTop' in path
    n = int(path[-2])
    print(f"n={n}")
    start = (n-1)*1000
    end = n*1000
    print(f"start={start},end={end}")
    names = names[start:end]
    return names

  def get_dirFilelist(self):
    if self.dirFilelist is None:
      self.dirFilelist =  glob.glob(f"{c_DestDir}/*")
    return self.dirFilelist

  def isBookDownloaded(self,name):
    dirFilelist = self.get_dirFilelist()
    for filename in dirFilelist:
      if name in filename:
        return True
      else:
        continue
    return False

  def startFetchCNKIhtml(self):
    for name in self.get_booknames():
      if self.isBookDownloaded(name):
        print(f"{name}已下载")
      else:
        print(f"{name}未下载，即将下载")
        self.getHTMLOfName(name)
        print(f"{name}未下载，下载完毕")
        self.d.browser.back()

  def getHTMLOfName(self,name):
    d = self.get_d()
    d.inputTextAndSearch(name)
    d.waitRequestFinishAndSaveToFile()

if __name__ == '__main__':
  f = Fetcher()
  f.startFetchCNKIhtml()