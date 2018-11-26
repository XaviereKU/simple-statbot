import asyncio
import discord
import requests
from bs4 import BeautifulSoup
import lxml
import json
from collections import OrderedDict
import random
import datetime
import math
import time
import stats

client = discord.Client()

token = os.environ["token"]
API_KEY = os.environ["API_KEY"]

#API header
header = {
    "Authorization": API_KEY,
    "Accept": "application/vnd.api+json"
}

season = stats.getseason(header)

@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print("===========")
    await client.change_presence(game=discord.Game(name="배그도우미", type=1))

# @client.event
# async def on_member_join(member):
#     server = member.server
#     channel = discord.Object('437610447810854923')
#     fmt = 'Welcome {0.mention} to {1.name}!'
#     await client.send_message(channel, fmt.format(member, server))


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    id = message.author.id
    channel = message.channel

    # if message.content == '/test':
    #     print('')

    if message.content == '/구직' or message.content == '/구인' or message.content == '/ㄱㅇ' or message.content == '/ㄱㅈ' or message.content == '/RW' or message.content == '/rw' or message.content == '/RD' or message.content == '/rd':
        member = message.author
        voice = message.author.voice.voice_channel

        if voice == None:
            fmt = '@here {0.display_name} 구직합니다!'
            await client.send_message(channel, fmt.format(member))
        else:
            member = voice.voice_members                         
            cnt = max(4 - len(member), 0)
            if cnt > 0:
                fmt = '@here {0.name} 에서 ' + cnt.__str__() + ' 명 구인합니다!'
            else:
                fmt = '{0.name} 풀방입니다!'
            await client.send_message(channel, fmt.format(voice))
        
    if message.content == '/test':
        if message.author.id == '328859649069809664':
            await client.send_message(channel, '/Running')
        else:
            return None

    if message.content == '/슈리':
        await client.send_message(channel, '메이플아줌마')

    if message.content == '/아임쿡':
        await client.send_message(channel, '대용량퀵스모커')

    if message.content == '/주사위' or message.content == '/ㅈㅅㅇ':
        if message.author.id == '328859649069809664':
            dicenum = random.randrange(1,6)
            await client.send_message(channel, '주사위 숫자 : {}'.format(dicenum))
        else:
            dicenum = random.randrange(1,6)
            await client.send_message(channel, '주사위 숫자 : {}'.format(dicenum))

    if message.content.startswith('/전적') or message.content.startswith('/stat') or message.content.startswith('/핵'):
        global season
        text = message.content
        result = stats.getstat(text,header,season)
        if type(result) == str:
            await client.send_message(channel,result)
        else:
            await client.send_message(channel, embed=result)
        
    if message.content == '/랭크' or message.content == '/rank':
        rankembed = discord.Embed()
        rankembed.add_field(name='Rank Table', value='Bronze : 1~1399\n Silver : 1400~1499\n Gold : 1500~1599\n Platinum : 1600~1699\n Diamond : 1700~1799\n Elite : 1800~1899\n Master : 1900~1999\n Grandmaster : 2000~', inline=False)
        await client.send_message(channel,embed=rankembed)

client.run(token)

#2018.02.11 최초 작성자 - SBS84
#2018.02.15 최종 수정 - XaviereKU
#2018.02.16 핵 의심 검색 추가 - XaviereKU
#2018.02.19 embed가 None이 아닐때만 출력됨 - XaviereKU
#2018.02.23 각종 오류 해결, /서버 명령어 추가
#2018.02.26 노가리방에서 구직시 구직 메시지 띄움. 구인 명령어시 노가리깔 사람 구하는 메시지 띄움.
#2018.02.28 주사위 기능 추가, 전적 검색 오류 수정, 서버 상태에 접속 불가 추
#2018.03.08 전적 검색 알리미 두 번 나오는 것 해결
#2018.03.15 카카오 핵 검색 추가
#2018.03.17 핵 전적 검색시 nickname 존재여부 확인
#2018.03.26 망겜 명령어 추가
#2018.04.24 오타 수정
#2018.04.25 핵에 평댐과 게임수 추가
#2018.05.10 공식 API로 변경
#2018.05.18 로또기능 제거, embed footer 추가.
#2018.08.20 서버 명령어 삭제
#2018.08.20 시즌 자동화
#2018.09.18 핵 명령어 수정
#2018.09.20 전적에 판수 추가.
