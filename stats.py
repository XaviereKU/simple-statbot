import discord
import requests
from bs4 import BeautifulSoup
import lxml
import json
from collections import OrderedDict
import math

def getrank(rankpt):
	if rankpt == 0:
		rank = 'unranked'
	elif rankpt < 1400:
		rank = 'Bronze'
	elif 1400 <= rankpt < 1500:
		rank = 'Silver'
	elif 1500 <= rankpt < 1600:
		rank = 'Gold'
	elif 1600 <= rankpt < 1700:
		rank = 'Platinum'
	elif 1700 <= rankpt < 1800:
		rank = 'Diamond'
	elif 1800 <= rankpt < 1900:
		rank = 'Elite'
	elif 1900 <= rankpt < 2000:
		rank = 'Master'
	else:
		rank = 'Grandmaster'
	return rank

def getseason(header):
	getseason = "https://api.pubg.com/shards/pc-krjp/seasons"
	seasonsourse = requests.get(getseason, headers=header)
	seasonstring = seasonsourse.text
	seasondic = json.loads(seasonstring)
	i = 0
	seasonlength = len(seasondic['data'])
	while i < seasonlength:
		checkcurrent = seasondic['data'][i]['attributes']['isCurrentSeason']
		if checkcurrent == True:
			season = seasondic['data'][i]['id']
		i = i + 1
	return season

def getname(name):
    url = 'https://pubg.op.gg/user/{}'.format(name)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.find_all(name='div', attrs={'class':'player-summary'}):
        nameraw = link.find(name='div', attrs={'class':'player-summary__name'}).text
        name = nameraw.strip()
    return name

def getstat(message, header, season):

	x = message.split()

	if len(x) < 3:
		region = None
		embedstat = discord.Embed(color=0x4e7ecf)
		embedstat.add_field(name='검색방법', value='/전적 Playername region Playlist\n eg : /전적 Xaviereku 1 3', inline=False)
		embedstat.add_field(name='Regions', value='1 : Steam, 2 : Kakao', inline=False)
		embedstat.add_field(name='Playlists(optional)', value='1 : solo, 2 : duo, 3 : squad, 4 : solo-fpp, 5 : duo-fpp, 6 : squad-fpp', inline=False)
		
	if len(x) >= 3:	
		if x[2] == '1':
			idregion = 'pc-krjp'
			region = 'steam'
			regiontitle = 'Steam'
		else:
			idregion = 'pc-kakao'
			region = 'kakao'
			regiontitle = 'Kakao'

	#get name and id
		name = getname(x[1])
		getid = "https://api.playbattlegrounds.com/shards/{}/players?filter[playerNames]={}".format(idregion, name)
		getidjson = requests.get(getid, headers=header)
		idjson = getidjson.text
		iddic = json.loads(idjson)
		plid = iddic['data'][0]['id']

		try:
			if name != None:
				embedstat = discord.Embed(color=0x4e7ecf, title='Player : {} | Region : {}'.format(name,regiontitle))

				getstaturl ="https://api.playbattlegrounds.com/shards/{}/players/{}/seasons/{}".format(region, plid, season)
				getstatjson = requests.get(getstaturl, headers=header)
				statjson = getstatjson.text
				statdic = json.loads(statjson)

				solo = statdic['data']['attributes']['gameModeStats']['solo']
				solofpp = statdic['data']['attributes']['gameModeStats']['solo-fpp']
				duo = statdic['data']['attributes']['gameModeStats']['duo']
				duofpp = statdic['data']['attributes']['gameModeStats']['duo-fpp']
				squad = statdic['data']['attributes']['gameModeStats']['squad']
				squadfpp = statdic['data']['attributes']['gameModeStats']['squad-fpp']

				if solo['roundsPlayed'] != 0:
					#gathering stat data
					sorankpt = int(solo['rankPoints'])
					sogames = solo['roundsPlayed']
					sowins = solo['wins']
					sowinratio = round((sowins*100/sogames),2) 
					sodmg = round(solo['damageDealt'],0)
					soavgdmg = round((sodmg/sogames),0)
					sokills = solo['kills']
					soheads = solo['headshotKills']
					# get solorank
					sorank = getrank(sorankpt)
					# k/d calc
					if sogames != sowins:
						sokd = round((sokills/(sogames-sowins)),2)
					else:
						sokd = 'inf'
					# headshot ratio calc
					if sokills != 0:
						soheadratio = round((soheads*100/sokills),1)
					else:
						soheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '1':
						embedstat.add_field(name='solo', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sorankpt, sorank, sowinratio, sokd, soavgdmg, soheadratio, sogames))
					elif len(x) == 3:
						embedstat.add_field(name='solo', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sorankpt, sorank, sowinratio, sokd, soavgdmg, soheadratio, sogames))
					
				if solofpp['roundsPlayed'] != 0:
					#gathering stat data
					sorankpt = int(solofpp['rankPoints'])
					sogames = solofpp['roundsPlayed']
					sowins = solofpp['wins']
					sowinratio = round((sowins*100/sogames),2) 
					sodmg = round(solofpp['damageDealt'],0)
					soavgdmg = round((sodmg/sogames),0)
					sokills = solofpp['kills']
					soheads = solofpp['headshotKills']
					# get solorank
					sorank = getrank(sorankpt)
					# k/d calc
					if sogames != sowins:
						sokd = round((sokills/(sogames-sowins)),2)
					else:
						sokd = 'inf'
					# headshot ratio calc
					if sokills != 0:
						soheadratio = round((soheads*100/sokills),1)
					else:
						soheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '4':
						embedstat.add_field(name='solo-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sorankpt, sorank, sowinratio, sokd, soavgdmg, soheadratio, sogames))
					elif len(x) == 3:
						embedstat.add_field(name='solo-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sorankpt, sorank, sowinratio, sokd, soavgdmg, soheadratio, sogames))		

				if duo['roundsPlayed'] != 0:
					durankpt = int(duo['rankPoints'])
					dugames = duo['roundsPlayed']
					duwins = duo['wins']
					duwinratio = round((duwins*100/dugames),2) 
					dudmg = round(duo['damageDealt'],0)
					duavgdmg = round((dudmg/dugames),0)
					dukills = duo['kills']
					duheads = duo['headshotKills']
					# get duorank
					durank = getrank(durankpt)
					# k/d calc
					if dugames-duwins != 0:
						dukd = round((dukills/(dugames-duwins)),2)
					else :
						dukd = 'inf'
					# headshot ratio calc
					if dukills != 0:
						duheadratio = round((duheads*100/dukills),1)
					else:
						duheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '2':
						embedstat.add_field(name='duo', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'.
							format(durankpt, durank, duwinratio, dukd, duavgdmg, duheadratio, dugames))
					elif len(x) == 3:
						embedstat.add_field(name='duo', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'.
							format(durankpt, durank, duwinratio, dukd, duavgdmg, duheadratio, dugames))
					
				if duofpp['roundsPlayed'] != 0:
					durankpt = int(duofpp['rankPoints'])
					dugames = duofpp['roundsPlayed']
					duwins = duofpp['wins']
					duwinratio = round((duwins*100/dugames),2) 
					dudmg = round(duofpp['damageDealt'],0)
					duavgdmg = round((dudmg/dugames),0)
					dukills = duofpp['kills']
					duheads = duofpp['headshotKills']
					# get duofpprank
					durank = getrank(durankpt)
					# k/d calc
					if dugames-duwins != 0:
						dukd = round((dukills/(dugames-duwins)),2)
					else :
						dukd = 'inf'
					# headshot ratio calc
					if dukills != 0:
						duheadratio = round((duheads*100/dukills),1)
					else:
						duheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '5':
						embedstat.add_field(name='duo-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'.
							format(durankpt, durank, duwinratio, dukd, duavgdmg, duheadratio, dugames))
					elif len(x) == 3:
						embedstat.add_field(name='duo-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'.
							format(durankpt, durank, duwinratio, dukd, duavgdmg, duheadratio, dugames))		

				if squad['roundsPlayed'] != 0:
					#gathering stat data
					sqrankpt = int(squad['rankPoints'])
					sqgames = squad['roundsPlayed']
					sqwins = squad['wins']
					sqwinratio = round((sqwins*100/sqgames),2) 
					sqdmg = round(squad['damageDealt'],0)
					sqavgdmg = round((sqdmg/sqgames),0)
					sqkills = squad['kills']
					sqheads = squad['headshotKills']
					# get squad rank
					sqrank = getrank(sqrankpt)
					# k/d calc
					if sqgames != sqwins:
						sqkd = round((sqkills/(sqgames-sqwins)),2)
					else:
						sqkd = 'inf'
					# headshot ratio calc
					if sqkills != 0:
						sqheadratio = round((sqheads*100/sqkills),1)
					else:
						sqheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '3':
						embedstat.add_field(name='squad', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sqrankpt, sqrank, sqwinratio, sqkd, sqavgdmg, sqheadratio, sqgames))
					elif len(x) == 3:
						embedstat.add_field(name='squad', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sqrankpt, sqrank, sqwinratio, sqkd, sqavgdmg, sqheadratio, sqgames))

				if squadfpp['roundsPlayed'] != 0:
					#gathering stat data
					sqrankpt = int(squadfpp['rankPoints'])
					sqgames = squadfpp['roundsPlayed']
					sqwins = squadfpp['wins']
					sqwinratio = round((sqwins*100/sqgames),2) 
					sqdmg = round(squadfpp['damageDealt'],0)
					sqavgdmg = round((sqdmg/sqgames),0)
					sqkills = squadfpp['kills']
					sqheads = squadfpp['headshotKills']
					# get squadfpp rank
					sqrank = getrank(sqrankpt)
					# k/d calc
					if sqgames != sqwins:
						sqkd = round((sqkills/(sqgames-sqwins)),2)
					else:
						sqkd = 'inf'
					# headshot ratio calc
					if sqkills != 0:
						sqheadratio = round((sqheads*100/sqkills),1)
					else:
						sqheadratio = 0
					#add to embed
					if len(x) == 4 and x[3] == '6':
						embedstat.add_field(name='squad-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sqrankpt, sqrank, sqwinratio, sqkd, sqavgdmg, sqheadratio, sqgames))
					elif len(x) == 3:
						embedstat.add_field(name='squad-fpp', value='rating : {}\nrank : {}\nwinratio : {}%\nk/d : {}\navgdmg : {}\nheads : {}%\ngames : {}'
							.format(sqrankpt, sqrank, sqwinratio, sqkd, sqavgdmg, sqheadratio, sqgames))

				if solo['roundsPlayed'] == 0 and duo['roundsPlayed'] == 0 and squad['roundsPlayed'] == 0 and solofpp['roundsPlayed'] == 0 and duofpp['roundsPlayed'] == 0 and squadfpp['roundsPlayed'] == 0:
					embedstat = '플레이 기록이 없습니다.'
		except:
			embedstat = '오류가 발생했습니다. 잠시 후 다시 시도해주세요.'


	return embedstat