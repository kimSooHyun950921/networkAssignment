from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
driver = webdriver.Chrome('chromedriver')

driver.get('http://gall.dcinside.com/board/lists/?id=cat')

actions = ActionChains(driver)
post = driver.find_element_by_xpath('//td/a')

actions.move_to_element(post)
actions.click(post)
actions.perform()

def get_title_of_post(driver,url):
    title_list = []
    driver.get(url)

    posts = driver.find_elements_by_class_name('ub-content')
    for i in range(0,len(posts)):
        if posts[i].find_element_by_class_name('gall_date').text == '10/19':
            post_title = posts[i].find_element_by_tag_name('a').text
            title_list.append(post_title)
    return title_list

def isTodayPostOnPage(driver,url,date):
    driver.get(url)
    posts = driver.find_elements_by_class_name('gall_date')

    for i in range(0,len(posts)):
        if posts[i].text == date:
            return True

    return False

def main():
    url = 'http://gall.dcinside.com/board/lists/?id=cat&page='
    driver.get('http://gall.dcinside.com/board/lists/?id=cat')
    page_Number = 1
    while True:
        if isTodayPostOnPage(driver,url+str(page_Number),'10/19'):
            print(get_title_of_post(driver,url+str(page_Number)))
            page_Number+=1
        else:
            break
if __name__ =="__main__":
    main()

 
