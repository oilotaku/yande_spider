import requests
import os
import glob
import threading
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup



def job(link, name, tag):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    img = requests.get(link, headers=headers)  # 下載圖片
    with open(tag + "\\" + name[11:] + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
        file.write(img.content)  # 寫入圖片的二進位碼
        file.close()
    # print(name[11:] + ".jpg")
    # time.sleep(1)

class main_tag_img_downlord:
    def __init__(self, link, tag):
        if tag !='' and tag !='main' :
            self.link = link+tag
            self.tag = tag
        else :
            self.link = link
            self.tag = 'main'

    def maim (self):
        main_tag_img_downlord.tag_img_downlord(self)

    def tag_img_downlord(self):
        link = f"{self.link}"
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "lxml")
        page = soup.find_all("a", {"class": "next_page"}, limit=1)
        results = soup.find_all("a", {"class": "directlink largeimg"}, limit=50)
        results_id = soup.find_all("a", {"class": "thumb"}, limit=50)
        page_link = [result.get("href") for result in page]
        image_links = [result.get("href") for result in results]
        name_link = [result.get("href") for result in results_id]
        name = name_link[0]
        threads = []
        num = 0

        if not os.path.exists(self.tag):
            os.mkdir(self.tag)  # 建立資料夾

        if self.tag != 'main':
            for index, link in enumerate(image_links):
                name = name_link[index]
                ch = glob.glob(self.tag + "\\" + name[11:] + ".jpg")
                threads.append(threading.Thread(target=job, args=(link, name, self.tag,)))
                threads[len(threads) - 1].start()
                num += 1
                if num == 5:
                    for i in range(len(threads) - 1):
                        threads[i].join()
                    num = 0

        else:
            for index, link in enumerate(image_links):
                name = name_link[index]
                ch = glob.glob(self.tag + "\\" + name[11:] + ".jpg")
                threads.append(threading.Thread(target=job, args=(link, name, self.tag,)))
                threads[len(threads) - 1].start()
                num += 1
                if num == 5:
                    for i in range(len(threads) - 1):
                        threads[i].join()
                    num = 0

        if page_link:
            print('clear_' + self.link )
            self.link = "https://yande.re/" + page_link[0]
            main_tag_img_downlord.tag_img_downlord(self)


if __name__ == '__main__':
    tag = input('tag:')
    a = main_tag_img_downlord('https://yande.re/post?tags=', tag)
    a.maim()


