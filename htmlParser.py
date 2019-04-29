import csv
import glob
import os
from collections import defaultdict

c_filename = "bookdata/onlyBookName.txt"
c_DestDir = 'fetchedHTML'
class Parser:
  def __init__(self):
    self.d = None
    self.dirFilelist = None

  def get_booknames(self):
    names = []
    with open(c_filename) as f:
      for line in f.readlines():
        line = line.strip()
        if len(line) >= 2:
          names.append(line)
    return names

  def filenameFromBookname(self,bookname):
    filename = f"{c_DestDir}/result{bookname}.html"
    return filename

  def get_dirFilelist(self):
    if self.dirFilelist is None:
      self.dirFilelist = glob.glob(f"{c_DestDir}/*")
    return self.dirFilelist

  def isBookDownloaded(self, name):
    dirFilelist = self.get_dirFilelist()
    for filename in dirFilelist:
      if name in filename:
        return True
      else:
        continue
    return False



  def start(self):
    """先创建dict，打印csv格式"""
    name2count = defaultdict(int)
    for index,name in enumerate(self.get_booknames()):
      print(f"index={index},name={name}")
      if self.isBookDownloaded(name):
        try:
          count = self.parseHTML_getCount(name)
          name2count[name] = count
        except:
          print(f"{name}未找到，因为名字太短，被其他书名匹配")
      else:
        print(f"{name}未下载")
        continue


    for name,count in name2count.items():
      print(f"{name},{count}")


  def parseHTML_getCount(self,bookname):
    filename = self.filenameFromBookname(bookname)
    with open(filename) as f:
      content = f.read()
      loc = content.find('&nbsp;条结果')
      content = content[loc-20:loc]
      loc = content.find('找到&nbsp;')
      content = content[loc+len('找到&nbsp;'):]
      content = content.replace(",","")
      return int(content)



if __name__ == '__main__':
  f = Parser()
  f.start()