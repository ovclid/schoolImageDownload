#%%
#######################################################################
# 학교 '포토갤러리'에 등록된 사진들을 모두 자동으로 'img' 폴더에 다운로드
# 각 페이지는 명시적인 URL로 하나씩 접근하며 대표 사진인 '썸네일'만 저장
#######################################################################
from selenium import webdriver
import urllib.request
import time
import os

dir_name = "./img"                
if not os.path.exists(dir_name):   # img 폴더가 없으면 새로 만들기  
    os.mkdir(dir_name)

driver = webdriver.Chrome('c:/chromedriver.exe')
#base_url = "https://dodam.sjedums.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000001060&menuId=MNU_0000000000000854&"
base_url = "https://neulbom.sjedues.kr/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000007630&menuId=MNU_0000000000025639&"
url = base_url + "pageIndex=1&sso=ok"
driver.get(url)
#%%
total_pages_ele = driver.find_element_by_class_name('total')
total_pages = int(total_pages_ele.text.split('/')[-1])

for page_num in range(total_pages):   # 보통 4~5 next page
    page_eles = driver.find_elements_by_class_name("page")
    imgs = driver.find_elements_by_class_name("ph_img")
    imgs_info = driver.find_elements_by_class_name("ph_cont")

    for i in range(len(imgs)):        # 한번에 8개의 사진 다운로드
        img_path = imgs[i].find_element_by_tag_name("img").get_attribute("src")
        img_date = imgs_info[i].find_element_by_class_name("ph_date").text
        img_title = imgs[i].find_element_by_tag_name("img").get_attribute("alt")

        img_title = img_title.replace('"', '').replace("<", "").replace(">", "").replace("/", "")  # 파일명에 특수 문자는 포함될 수 없음

        file_name_ext = img_path.split('.')[-1]   # 파일의 확장자 가져오기 (jpg, png, pdf 등)

        file_name = img_date.replace('-', '') + '_' + img_title + '.' + file_name_ext   # 파일형태를 '등록날짜_사진타이틀.확장자명' 만듦

        # 해당 URL 주소로 접근하여 파일 다운로드하기
        urllib.request.urlretrieve(img_path, dir_name + "/" + file_name)
        print(img_path, file_name)

    if page_num != total_pages - 1 :  # 마지막 페이지는 더이상 url를 오픈하지 않음
        url = f'{base_url}&pageIndex={page_num+2}&sso=ok'
        driver.get(url)
        time.sleep(1)