from bs4 import BeautifulSoup

def parseHTML():
    with open("test_50kb.html","r") as fp:
        soup = BeautifulSoup(fp)

    img_list = soup.find_all('img')
    return img_list

def print_list():
    img_list = parseHTML()
    for img in img_list:
        print(img)
print_list()
