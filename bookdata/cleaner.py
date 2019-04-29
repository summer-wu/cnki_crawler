"""清洗员。用来清理有错的数据"""
import csv
from collections import defaultdict

c_filename = "A古籍名和作者-full..csv"
class Cleaner:
  def __init__(self):
    pass

  def do_clean(self):
    """去重，然后在打印为csv格式"""
    #先获取name2count
    name2count = defaultdict(int)
    with open(c_filename) as f:
      r = csv.reader(f)
      for row in r:
        bookName = row[0]
        author = row[1]
        # print(bookName,author)
        key = f"{bookName},{author}"
        name2count[key] +=1

    for name,count in name2count.items():
      print(name)

  def onlyBookname(self):
    booknames = []
    with open(c_filename) as f:
      r = csv.reader(f)
      for row in r:
        bookName = row[0]
        if bookName in booknames:continue
        else:booknames.append(bookName)

    for b in booknames:
      print(b)

if __name__ == '__main__':
    c = Cleaner()
    c.onlyBookname()