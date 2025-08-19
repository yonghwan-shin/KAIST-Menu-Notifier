import requests
from bs4 import BeautifulSoup
import os
import re
import certifi

# KAIST 메뉴 페이지 URL
URL = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=emp"

def get_menu_lists(url):
    resp = requests.get(url, verify=certifi.where())
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    menus = soup.select("ul.list-1st")  # 점심, 저녁 메뉴 모두 선택
    if len(menus) < 2:
        raise ValueError("점심/저녁 메뉴를 찾을 수 없습니다.")
    return menus

def extract_menu_text(ul_element):
    items = ul_element.find_all("li")
    text = "\n".join([item.get_text(strip=True) for item in items])
    return text

def remove_trailing_numbers(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        # 메뉴 끝에 있는 숫자 괄호만 제거, 단어 포함 괄호는 유지
        clean_line = re.sub(r'\((\d+,?)+\)$', '', line).strip()
        clean_lines.append(clean_line)
    return "\n".join(clean_lines)

def main():
    menus = get_menu_lists(URL)
    
    # 점심 메뉴
    lunch_raw = extract_menu_text(menus[0])
    lunch_clean = remove_trailing_numbers(lunch_raw)
    
    # 저녁 메뉴
    dinner_raw = extract_menu_text(menus[1])
    dinner_clean = remove_trailing_numbers(dinner_raw)

    # Slack 메시지 포맷
    message = (
        "*오늘의 KAIST 메뉴*\n\n"
        "*점심 (1층/2층):*\n" + lunch_clean + "\n\n"
        "*저녁:*\n" + dinner_clean
    )

    print(message)

if __name__ == "__main__":
    main()
