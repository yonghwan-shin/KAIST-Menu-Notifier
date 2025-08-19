import requests
from bs4 import BeautifulSoup
import os
import re
import certifi

# KAIST 메뉴 페이지 URL
URL = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=emp"

def get_menu_lists(url):
    resp = requests.get(url, verify=certifi.where())  # SSL 인증서 지정
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 모든 ul.list-1st 선택 (점심, 저녁 등)
    menus = soup.select("ul.list-1st")
    return menus

def extract_menu_text(ul_element):
    items = ul_element.find_all("li")
    text = "\n".join([item.get_text(strip=True) for item in items])
    return text

def remove_trailing_numbers(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        # 끝에 있는 숫자 괄호만 제거, 단어 포함 괄호는 유지
        clean_line = re.sub(r'\((\d+,?)+\)$', '', line).strip()
        clean_lines.append(clean_line)
    return "\n".join(clean_lines)


def main():
    menus = get_menu_lists(URL)

    lunch_menu_raw = extract_menu_text(menus[0])
    dinner_menu_raw = extract_menu_text(menus[1])

    lunch_menu = remove_trailing_numbers(lunch_menu_raw)
    dinner_menu = remove_trailing_numbers(dinner_menu_raw)

    message = f"*오늘의 KAIST 메뉴*\n\n*점심:*\n{lunch_menu}\n\n*저녁:*\n{dinner_menu}"
    print(message)

if __name__ == "__main__":
    main()
