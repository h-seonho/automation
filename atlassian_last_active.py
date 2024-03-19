import requests
from datetime import datetime, timedelta

atlassian_token = 'ATCTT3xFfGN0_xqSOm-ES5NiirVWoUHM5TTcmvE7hD-_baNnqlMs3jhid5P0faiCWNYak0X0QHt--UX4L_vlEVQ7JxWt5TeCzmmwoh186MECVa7segNIrEVqh8gCJs0854BBa8o49guiuyQJLbglJ3nRrKdEWjwpUCAa7HvvBeRdtMRasz1If_I=1E193909'
webhook_url = 'https://hooks.slack.com/services/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'

def send_slack_message(messages):
    message = "\n".join(messages)
    data = {
        'text': message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 200:
        print("Messages sent successfully")
    else:
        print(f"Error sending message to Slack: {response.text}")

if __name__ == "__main__":
    # 텍스트 파일에서 데이터 읽어오기
    with open('conf_user.txt', 'r') as file:
        lines = file.readlines()
        excel_data = [line.strip().split('/') for line in lines]

    url_base = 'https://api.atlassian.com/admin/v1/orgs/c237080k-56d2-18aj-k714-08643dkk6cc5/directory/users/{}/last-active-dates'
    headers = {
        'Authorization': f'Bearer {atlassian_token}'
    }

    # 메시지를 모아둘 리스트 초기화
    messages1 = ["*\u2728Conf 30일 이상 미접속자\u2728*\n"]
    messages2 = ["*\u2728Jira 30일 이상 미접속자\u2728*\n"]

    for data in excel_data:
        user_id, email = data
        url = url_base.format(user_id)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            product_access = data.get('data', {}).get('product_access', [])
            confluence_data = [access_data for access_data in product_access if access_data.get('key') == 'confluence']
            jira_data = [access_data for access_data in product_access if access_data.get('key') == 'jira-software']

            if confluence_data:
                last_active_date_str = confluence_data[0].get('last_active')
                last_active_date = datetime.strptime(last_active_date_str, "%Y-%m-%d")
                thirty_days_ago = datetime.now() - timedelta(days=30)
                if last_active_date <= thirty_days_ago:
                    message = f"사용자 : {email}\nConfluence 마지막 접속일: {last_active_date_str}\n"
                    messages1.append(message)

            if jira_data:
                last_active_date_str = jira_data[0].get('last_active')
                last_active_date = datetime.strptime(last_active_date_str, "%Y-%m-%d")
                thirty_days_ago = datetime.now() - timedelta(days=30)
                if last_active_date <= thirty_days_ago:
                    message = f"사용자 : {email}\nJira 마지막 접속일: {last_active_date_str}\n"
                    messages2.append(message)

        else:
            print(f"Error for account {email}: {response.status_code}")

    # Slack으로 메시지 보내기
    send_slack_message(messages1)
    send_slack_message(messages2)