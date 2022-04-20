#%%
#import selenium
from selenium import webdriver
import time
import urllib.request

driver= webdriver.Chrome("c:\chromedriver\chromedriver.exe")

url = 'https://yangji.sjedums.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000007611&menuId=MNU_0000000000013161&sso=ok'

driver.get(url)
# %%

imgs = driver.find_elements_by_class_name('ph_img')

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
        file = file_list[j].get_attribute("onclick").split("'")
        file_name = file_list[j].text 
        print(file_name)

        file_path = f'https://yangji.sjedums.kr/cmm/fms/getImage.do?siteId=SITE_000000000000407&appendPath={file[5]}&atchFileNm={file[1]}_{file[3]}.jpg'
        print(file_path)

        urllib.request.urlretrieve(file_path, f'{date}_{title}_{file_name}')

    
    driver.back()
    time.sleep(1)