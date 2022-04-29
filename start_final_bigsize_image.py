#%%
#import selenium
from selenium import webdriver
import time
import os
import urllib.request

dir_name = "./img"
if not os.path.exists(dir_name):    
    os.mkdir(dir_name)

driver= webdriver.Chrome("c:\chromedriver\chromedriver.exe")

base_url = "https://neulbom.sjedues.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000007630&menuId=MNU_0000000000025639&"
url = base_url + "pageIndex=1&sso=ok"

#url = 'https://yangji.sjedums.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000007611&menuId=MNU_0000000000013161&sso=ok'

driver.get(url)
# %%

total_pages_ele = driver.find_element_by_class_name('total')
total_pages = int(total_pages_ele.text.split('/')[-1])

for page_num in range(total_pages):   # 보통 4~5 next page
    #page_eles = driver.find_elements_by_class_name("page")
    imgs = driver.find_elements_by_class_name("ph_img")
    #imgs_info = driver.find_elements_by_class_name("ph_cont")

    for i in range(len(imgs)):
        xpath = f'//*[@id="listForm"]/div[2]/ul/li[{i+1}]/div[1]/a/img'
        print(xpath)
        ele = driver.find_element_by_xpath(xpath)
        ele.click()
        time.sleep(1)    

        file_list = driver.find_element_by_class_name("file_box").find_elements_by_tag_name("a")
        date = driver.find_element_by_class_name('date').text[:10].replace('.', '')
        title = driver.find_element_by_xpath('//*[@id="bbs_wrap"]/div[1]/dl[1]/dd').text

        #file_name_list = driver.find_element_by_class_name("file_box").find_elements_by_tag_name("img")
        for j in range(len(file_list)):
            try:
                file = file_list[j].get_attribute("onclick").split("'")
                file_name = file_list[j].text 
                print(file_name)

                ext_name = file_name.split('.')[-1]
                #file_path = f'https://yangji.sjedums.kr/cmm/fms/getImage.do?siteId=SITE_000000000000407&appendPath={file[5]}&atchFileNm={file[1]}_{file[3]}.{ext_name}'
                file_path = f'https://neulbom.sjedues.kr/cmm/fms/FileDown.do?atchFileId={file[1]}&fileSn={file[3]}&bbsId={file[5]}'

                print(file_path)

                urllib.request.urlretrieve(file_path, f'{dir_name}/{date}_{title}_{file_name}')
            except:
                print("error : file_name  retrive failed")

        driver.back()

    if page_num != total_pages - 1 :  # 마지막 페이지는 더이상 url를 오픈하지 않음
        url = f'{base_url}&pageIndex={page_num+2}&sso=ok'
        driver.get(url)
        time.sleep(1)
# %%
