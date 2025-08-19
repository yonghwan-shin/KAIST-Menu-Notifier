import requests
from bs4 import BeautifulSoup
import os
import re
import certifi

# KAIST 메뉴 페이지 URL
URL = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=emp"

def get_today_menu(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 메뉴 텍스트 추출 (페이지 구조에 맞게 선택자)
    menu_section, dinner = soup.select("ul.list-1st")
    if menu_section:
        return menu_section.get_text("\n", strip=True), dinner.get_text("\n", strip=True)
    else:
        return "오늘의 메뉴 정보를 찾을 수 없습니다."

def split_floors(menu_text):
    parts = menu_text.split("2층 ")
    first_floor = parts[0].replace("오늘의 메뉴: ", "").strip()
    second_floor = "2층 " + parts[1].strip()
    return first_floor, second_floor

def remove_trailing_numbers(text):
    lines = text.splitlines()
    clean_lines = []
    for line in lines:
        # 끝에 있는 숫자 괄호만 제거, 단어 포함 괄호는 유지
        clean_line = re.sub(r'\((\d+,?)+\)$', '', line).strip()
        clean_lines.append(clean_line)
    return "\n".join(clean_lines)

def main():
    menu_text,dinner_text = get_today_menu(URL)
    first_floor, second_floor = split_floors(menu_text)
    first_floor_clean = remove_trailing_numbers(first_floor)
    second_floor_clean = remove_trailing_numbers(second_floor)
    dinner_text_clean = remove_trailing_numbers(dinner_text)
    first_lines = [line.strip() for line in first_floor_clean.splitlines() if line.strip()]
    second_lines = [line.strip() for line in second_floor_clean.splitlines() if line.strip()]
  
    common = set(first_lines) & set(second_lines)
    second_final = []
    for i,item in enumerate(second_lines):
        if (item not in common) and i!=0 and i!=len(second_lines)-1:
            second_final.append("++"+str(item))
        else:
            second_final.append(str(item))
    second_floor_clean = "\n".join(second_final)
    message = f"{first_floor_clean}\n\n{second_floor_clean}\n\n저녁\n{dinner_text_clean}"
    print(message)

if __name__ == "__main__":
    main()
