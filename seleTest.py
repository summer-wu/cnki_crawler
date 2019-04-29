from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *


class cnki_result_finish(object):
  """ 参考 text_to_be_present_in_element
  """

  def __init__(self, locator, text_):
    self.locator = locator
    self.text = text_

  @staticmethod
  def htmlstrOfIframe(driver,part='body'):
    assert part in ['body','head']
    js = """return (function(){
            var a = document.getElementById('iframeResult');
            var htmlstr = a.contentDocument.{part}.outerHTML;
            return htmlstr;
            })();"""
    js = js.replace("{part}",part)
    htmlstr = driver.execute_script(js)
    return htmlstr

  def __call__(self, driver:webdriver.Chrome):
    try:
      htmlstr = self.htmlstrOfIframe(driver)
      # print(htmlstr)
      return '条结果' in htmlstr
    except StaleElementReferenceException:
      return False

class CNKIDriver:
  def __init__(self):
    self.browser = webdriver.Chrome()
    self.browser.implicitly_wait(2) #在find_by时，最多等待2秒

  def open(self):
    browser = self.browser
    browser.get('http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ')
    browser.set_window_size(1693, 1005)

  def changeSelect(self):
    """修改下拉选项"""
    browser = self.browser

    elem = browser.find_element_by_id('txt_1_sel')
    elem.click()
    Select(elem).select_by_value('RF') #没有select_by_label

    elem = browser.find_element_by_id('txt_2_sel')
    elem.click()
    Select(elem).select_by_value('RF')  # 没有select_by_label

  def inputTextAndSearch(self,bookname,author):
    """输入文字"""
    browser = self.browser
    elem = browser.find_element_by_id('txt_1_value1')
    elem.send_keys(bookname)

    elem = browser.find_element_by_id('txt_2_value1')
    elem.send_keys(author)
    browser.find_element_by_id('__droplist').click()
    browser.find_element_by_id('btnSearch').click()

  def getIFrameURL(self):
    browser = self.browser
    js = """return $('#iframeResult').context.URL"""
    result = browser.execute_script(js)
    print(result)

  def waitRequestFinish(self):
    """等待搜索完成"""
    browser = self.browser
    locator = (By.ID,'iframeResult') #locator是一个tuple
    print(datetime.now(),"will wait")
    method = cnki_result_finish(locator,'条结果') #表面是class，实际是callabel

    try:
      WebDriverWait(browser,10).until(method)
    except TimeoutException:
      print("WebDriverWait TimeoutException")
      return
    print(datetime.now(),"end wait")

    headstr = cnki_result_finish.htmlstrOfIframe(browser,'head')
    bodystr = cnki_result_finish.htmlstrOfIframe(browser,'body')
    fullstr = f"""<html>{headstr}{bodystr}</html>"""
    print(fullstr)

  def quit(self):
    self.browser.quit()

if __name__ == '__main__':
  d=CNKIDriver()
  d.open()
  d.changeSelect()
  d.inputTextAndSearch('aaa','bbb')
  d.waitRequestFinish()
  d.quit()
