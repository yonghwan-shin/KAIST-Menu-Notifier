import requests
from bs4 import BeautifulSoup
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import re

# KAIST 메뉴 페이지 URL
URL = "https://www.kaist.ac.kr/kr/html/campus/053001.html?dvs_cd=emp"

def get_today_menu(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    # 메뉴 텍스트 추출 (페이지 구조에 맞게 선택자)
    menu_section = soup.select("ul.list-1st")
    if menu_section:
        lunch_menu = menu_section[0]
        dinner_menu = menu_section[1] if len(menu_section) > 1 else None
        return lunch_menu.get_text("\n", strip=True), dinner_menu.get_text("\n", strip=True) if dinner_menu else None
    else:
        return None,None

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

def send_slack_message(token, channel, message):
    if not token:
        raise ValueError("Slack token is not set. Please export SLACK_BOT_TOKEN.")
    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print("Message sent:", response["ts"])
    except SlackApiError as e:
        print("Error sending message:", e.response["error"])
        raise
def main():
    menu_text,dinner_text = get_today_menu(URL)
    first_floor, second_floor = split_floors(menu_text)
    first_floor_clean = remove_trailing_numbers(first_floor)
    second_floor_clean = remove_trailing_numbers(second_floor)
    if dinner_text:
        dinner_text = remove_trailing_numbers(dinner_text)
    else:
        dinner_text = "저녁 메뉴는 제공되지 않습니다."
    message = f"*오늘의 KAIST 메뉴*\n{first_floor_clean}\n\n\n{second_floor_clean}"
    
    slack_token = os.getenv("xoxb-5926746863873-9360352196599-mxh5iIheZkNGFAqTfyerhRvi")
    channel_id = "D06MM0RUE85"  # 본인 Slack ID
    send_slack_message(slack_token, channel_id, message)

if __name__ == "__main__":
    main()
