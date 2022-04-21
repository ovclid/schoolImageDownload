#%%
from selenium import webdriver
import urllib.request
import time
import os

dir_name = "./img"
if not os.path.exists(dir_name):    
    os.mkdir(dir_name)

driver = webdriver.Chrome('c:/chromedriver.exe')
#url = "https://yangji.sjedums.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000007611&menuId=MNU_0000000000013161&sso=ok"
url = "https://dodam.sjedums.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000001060&menuId=MNU_0000000000000854&sso=ok"
driver.get(url)
time.sleep(2)
#%%
total_pages_ele = driver.find_element_by_class_name('total')
total_pages = int(total_pages_ele.text.split('/')[-1])
total_next_pages = int(total_pages/10) + 1
total_proceeded_page = 0

for current_page_num in range(total_next_pages):   # one next page -> 10 pages 
    for each_page_num in range(10):
        page_eles = driver.find_elements_by_class_name("page")
        imgs = driver.find_elements_by_class_name("ph_img")
        imgs_info = driver.find_elements_by_class_name("ph_cont")

        for i in range(len(imgs)):
            img_path = imgs[i].find_element_by_tag_name("img").get_attribute("src")
            img_date = imgs_info[i].find_element_by_class_name("ph_date").text
            img_title = imgs[i].find_element_by_tag_name("img").get_attribute("alt")
            img_title = img_title.replace('"', '').replace("<", "").replace(">", "").replace("/", "")
            file_name_ext = img_path.split('.')[-1]
            file_name = img_date.replace('-', '') + '_' + img_title + '.' + file_name_ext

            urllib.request.urlretrieve(img_path, dir_name + "/" + file_name)
            print(img_path, file_name)

        total_proceeded_page = total_proceeded_page  + 1
        if total_proceeded_page == total_pages:
            print("process finished!!!")
            break

        if each_page_num != 9 :  # 마지막 페이지의 경우 'next page' 버튼 클릭
            page_eles[each_page_num].click()
            time.sleep(1)

    print("------------------", current_page_num, "--------------------")
    next_page_ele = driver.find_element_by_class_name("next")
    next_page_ele.click()
    time.sleep(1)