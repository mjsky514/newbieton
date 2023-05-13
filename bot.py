import os
import slack_sdk
from time import time
#import newbieton
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_APP_TOKEN = "xapp-1-A05778VB2ET-5257127898021-2c18cc657ec6fae1e07b193480ae918b779c83fcce49dbea2a1de43546fd32d2"
SLACK_BOT_TOKEN = "xoxb-5250661758005-5272492731361-kamWppTHSfY0H2wud6Iz5qv1"
client = WebClient(token=SLACK_BOT_TOKEN)

#SLACK_APP_SECRET = "SLACK_APP_SECRET"

# Bolt 앱 인스턴스 생성
app = App(token=SLACK_BOT_TOKEN)
@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)
# 맨션된 이벤트를 처리하는 핸들러 함수

@app.event("app_mention")
def handle_app_mention(body, say, logger):
    # 맨션한 사용자 정보
    user = body["event"]["user"]

    # 맨션된 채널 정보
    channel = body["event"]["channel"]

    # 맨션된 메시지 내용
    text = body["event"]["text"]

    # 슬랙 채널에 응답
    #say(f"안녕하세요, <@{user}>! 봇이 맨션을 받았습니다.")
    if text[15:]=='방테':
        create_private_channel_and_invite_users('U05858U6KFS', 'U057FHUDGT0')
        print('done')
        return
    if text[15:]=='매칭 도움' or text[15:]=='매칭도움' or text[15:]=='도움':
        say("<이름 잘하는과목 실력(1~9) 못하는과목 실력(1~9)> 의 형태로 입력해주세요!\n예시) @Veritas Luxmea 안시영 수학 9 국어 1")
        return
    lis=text[15:].split()#안시영 수학 9 국어 1
    if len(lis) != 5:
        say('입력 오류')
        return
    print(lis)
    trait=[]
    trait.append(user)
    trait.extend(lis)
    sub=['국어','수학','영어','한국사']
    if trait[2] not in sub or trait[4] not in sub:
        say('입력오류')
        return
    for i,na in enumerate(sub):
        if trait[2]==na:
            trait[2]=i
        if trait[4]==na:
            trait[4]=i
    trait[3]=int(trait[3])
    trait[5] = int(trait[5])
    trait.append(time())
    trait.append(100)
    print(trait)
    say(' '.join(str(s) for s in trait))
    # user2_id = newbieton.apply(trait)

def create_private_channel_and_invite_users(user1_id, user2_id):#U05858U6KFS,U058BG3CYN4
    print('start')
    response = client.conversations_create(
        name="비밀방"+str(int(time()*10)),
        is_private=True
    )
    channel_id = response["channel"]["id"]
    # invite users to the private channel
    client.conversations_invite(channel=channel_id, users=[user1_id, user2_id])
    # return the channel id
    print('done')
    return channel_id

    #(id, name, give, givenum, take, takenum, time, min_score = 100)

if __name__ == "__main__":
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    handler.start()
