import feedparser
import datetime
from dateutil.parser import parse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_security_news():
    # 현재 날짜 및 1일 전 날짜 계산
    today = datetime.datetime.now()
    current_weekday = today.weekday()

    # 월요일인 경우에는 지난 주 일요일부터 기사를 가져옴
    if current_weekday == 0:
        today_diff = today + datetime.timedelta(days=-2)  # 지난 주 토요일로 설정
    else:
        today_diff = today + datetime.timedelta(days=-1)  # 1일 전으로 설정

    feeds = {'1': '사건사고', '2': '보안컬럼', '5': '긴급경보', '6': '보안정책'}
    filter_keywords = ['유출', '해킹', '피싱', '스미싱', '큐싱', '해커', '디도스', '랜섬웨어', '침해', '악성코드', '공격']

    # Slack API 토큰
    slack_token = 'xoxb-1479059087923-6517297280724-ka1TF1mNOHHwzucDpDrBHlIB'
    client = WebClient(token=slack_token)

    # 현재 날짜 문자열로 변환
    current_date_str = today.strftime("%m월 %d일")

    # 메시지를 모을 리스트
    messages = ["*\u2728정보보호 경각심 고취 및 보안 동향 공유\u2728*\n"+f"{current_date_str} 보안뉴스 클리핑 공유드립니다.\n"]

    # 각 RSS 피드에 대한 처리
    for key in feeds:
        # RSS 피드의 URL 생성
        url = 'http://www.boannews.com/media/news_rss.xml?kind=' + key

        # RSS 피드 파싱
        f = feedparser.parse(url)
        articles = f['entries']

        # 각 뉴스 기사에 대한 처리
        for article in articles:
            article_title = article['title']
            article_published = article['updated']
            article_link = article['link']

            # 기사 발행일을 파싱하여 datetime 객체로 변환
            article_date = parse(article_published)

            # 필터링할 키워드가 기사 제목에 포함되어 있는지 확인
            if any(keyword in article_title for keyword in filter_keywords):
                # 현재 날짜와 1일 전 날짜 사이에 발행된 기사만 처리
                if article_date.date() >= today_diff.date():
                    message = f"\u2022 <{article_link}|{article_title}>\n\n>"
                    messages.append(message)

    # 리스트에 메시지가 있을 경우 슬랙에 전송
    if messages:
        # 슬랙 메시지 전송
        try:
            # 메시지 리스트를 개행 문자로 연결하여 전체 메시지 생성
            combined_message = "\n".join(messages)
            response = client.chat_postMessage(channel="#황선호_테스트", text=combined_message)
            print("Slack Message Sent")
        except SlackApiError as e:
            print(f"Error sending Slack message: {e.response['error']}")

send_security_news()

