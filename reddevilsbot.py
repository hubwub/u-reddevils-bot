#RedDevils BOT by /u/hubwub
import datetime
import time
import urllib2
import HTMLParser
import json
import re
import operator
from praw  import Reddit
from bs4 import BeautifulSoup

class Red_Devils_Bot(object):

	def __init__(self):
		#Ask user for credentials
		self.username = raw_input('Reddit Username: ')
		self.password = raw_input('Reddit Password: ')
		self.subreddit = raw_input('Subreddit - reddevils or reddevilsmods: ')
		self.userAgent = '/r/reddevils bot by /u/Hubwub'

	def __unicode__(self):
   		return unicode(self.some_field) or u''

	def scrape_fixtures(self):
		w = urllib2.urlopen('http://us.soccerway.com/teams/england/manchester-united-fc/662/matches/')
		soup = BeautifulSoup(w.read())

		fixtures = []
		rawdata_fixtures = []
		match_date_list = []
		match_home_team_list = []
		match_away_team_list = []
		match_score_list = []
		match_comp_list = []
		final = []
		results = []
		future = []


		for table in soup.findAll('div', id="page_team_1_block_team_matches_5"):
			rawdata_fixtures = table

		rawdata_fixtures_list = [tr.findAll('td') for tr in rawdata_fixtures.findAll('tr')]

		for row in rawdata_fixtures_list:
			fixtures.append([cell.text for cell in row])

		w.close()

		todays_date = datetime.datetime.today()
		weekstotoday = datetime.datetime.today() - datetime.timedelta(weeks=2)
		weeksfromtoday = datetime.datetime.today() + datetime.timedelta(weeks=3)

		for fix in fixtures:
			for j in range(0, len(fix)):
				if j == 1 and fix[j] != "None":
					match_date = datetime.datetime.strptime(fix[j], "%d/%m/%y")
					if weekstotoday <=  match_date <= weeksfromtoday:
						match_date_list.append(match_date.strftime("%b %d"))
						match_comp_list.append(fix[2])
						home = fix[3]
						home = re.sub("\n","", home)
						home = re.sub("                    ", "", home)
						home = re.sub("                  ", "", home)
						match_home_team_list.append(home)
						match_score = fix[4]
						match_score = re.sub("\n","", match_score)
						match_score = re.sub("                                ", "", match_score)
						match_score = re.sub("                              ", "", match_score)
						match_score = re.sub("                ", "", match_score)
						match_score_list.append(match_score)
						away = fix[5]
						away = re.sub("\n","", away)
						away = re.sub("                  ", "", away)
						away = re.sub("                ", "", away)
						match_away_team_list.append(away)	

		premier_league_teams = ['Arsenal', 'Aston Villa', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
								'Hull City', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United',
								'Newcastle United', 'Queens Park Rangers', 'Southampton', 'Stoke City', 'Sunderland',
								'Swansea City', 'Tottenham Hotspur', 'West Bromwich Albion', 'West Ham United'
								]

		sw_team_name_formating = ['Arsenal', 'Aston Villa', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
								'Hull City', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United',
								'Newcastle United', 'Queens Park Ra', 'Southampton', 'Stoke City', 'Sunderland',
								'Swansea City', 'Tottenham Hotspur', 'West Bromwich', 'West Ham United',
								]			

		for j in range(0, len(match_date_list)):
			match_result  = None
			scores = str(match_score_list[j])
			scores = re.sub(" ", "", scores)
			pretty_score = scores
			pretty_score = re.sub('P', '', pretty_score)
		 	scores = re.split('-', scores)

		 	if len(scores) == 2:
				if "P" in scores[0] and "P" in scores[1]:
					scores[0] = re.sub('P', '', scores[0])
					score_pa = int(scores[0]) 
					scores[1] = re.sub('P', '', scores[1])
					score_pb = int(scores[1])

					if (score_pa > score_pb) and match_home_team_list[j] == "Manchester United":
						match_result = "PW"
					elif (score_pa < score_pb) and match_home_team_list[j] == "Manchester United":
						match_result = "PL"
					elif (score_pa < score_pb) and match_away_team_list[j] == "Manchester United":
						match_result = "PW"
					elif (score_pa > score_pb) and match_away_team_list[j] == "Manchester United":
						match_result = "PL"
					else:
						match_result = "P"
				else:
					score_a = int(scores[0])
		 			score_b = int(scores[1])

		 			if (score_a > score_b) and match_home_team_list[j] == "Manchester United":
						match_result = "W"
					elif (score_a < score_b) and match_home_team_list[j] == "Manchester United":
						match_result = "L"
					elif (score_a < score_b) and match_away_team_list[j] == "Manchester United":
						match_result = "W"
					elif (score_a > score_b) and match_away_team_list[j] == "Manchester United":
						match_result = "L"
					elif (score_a == score_b) and (match_away_team_list[j] == "Manchester United" or match_home_team_list[j] == "Manchester United"):
						match_result = "D"

			final.append({'date': match_date_list[j],'comp': str(match_comp_list[j]), 'home_team': str(match_home_team_list[j]), 'away_team': str(match_away_team_list[j]), 'score': pretty_score, 'result': match_result})


		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		for j in range(0, len(final)):
			if final[j]['result'] != None:
				results.append(final[j])
			else:
				future.append(final[j])

		standings = "\n###Results"
		standings += "\n|Comp | Date | |Opponent | Result"
		standings += "\n|:-----------------------------: | :----: | :-: |  :-: | :-: |"

		for j in range(0, len(results)):
			if results[j]['home_team'] == "Manchester United":
				standings += "\n|{0}|{1}|H|{2}|{3} ({4})|".format(results[j]['comp'], results[j]['date'], results[j]['away_team'], results[j]['score'], results[j]['result'])
			else:
				standings += "\n|{0}|{1}|A|{2}|{3} ({4})|".format(results[j]['comp'], results[j]['date'], results[j]['home_team'], results[j]['score'], results[j]['result'])

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://us.soccerway.com/teams/england/manchester-united-fc/662/matches/)*\n"

		standings +="#[](#break)\n"

		standings += "\n###Fixtures"
		standings += "\n|Comp | Date | |Opponent | Time (GMT)"
		standings += "\n|:-----------------------------: | :----: | :-: |  :-: | :-: |"

		for j in range(0, len(future)):
			if future[j]['home_team'] == "Manchester United":
				standings += "\n|{0}|{1}|H|{2}|{3}|".format(future[j]['comp'], future[j]['date'], future[j]['away_team'], future[j]['score'])
			else:
				standings += "\n|{0}|{1}|A|{2}|{3}|".format(future[j]['comp'], future[j]['date'], future[j]['home_team'], future[j]['score'])

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://us.soccerway.com/teams/england/manchester-united-fc/662/matches/)*\n"

		return standings

	def scrape_league(self):
		w = urllib2.urlopen('http://int.soccerway.com/teams/england/manchester-united-fc/662/')
		soup = BeautifulSoup(w.read())

		league_dict = { 'Arsenal': '[Arsenal](/r/Gunners)', 'Aston Villa': '[Aston Villa](/r/avfc)', 'Burnley': '[Burnley](/r/Burnley)', 'Chelsea': '[Chelsea](/r/chelseafc)', 'Crystal Palace': '[Crystal Palace](/r/crystalpalace)', 'Everton': '[Everton](/r/Everton)', 'Hull City':'[Hull City](/r/HullCity)', 'Leicester City':'[Leicester City](/r/lcfc)','Liverpool':'[Liverpool](/r/LiverpoolFC)', 'Manchester City':'[Manchester City](/r/MCFC)', 'Manchester United':'[Manchester United](/r/reddevils)', 'Newcastle United':'[Newcastle United](/r/nufc)', 'Queens Park Rangers':'[Queens Park Rangers](/r/superhoops)', 'Southampton':'[Southampton](/r/SaintsFC)', 'Stoke City':'[Stoke City](/r/StokeCityFC)', 'Sunderland':'[Sunderland](/r/SAFC)', 'Swansea City':'[Swansea City](/r/swanseacity)', 'Tottenham Hotspur':'[Tottenham Hotspur](/r/coys)', 'West Bromwich Albion':'[West Bromwich Albion](/r/WBAfootball)', 'West Ham United':'[West Ham United](/r/Hammers)' }

		league = []
		premier_league_teams = ['Arsenal', 'Aston Villa', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
						'Hull City', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United',
						'Newcastle United', 'Queens Park Rangers', 'Southampton', 'Stoke City', 'Sunderland',
						'Swansea City', 'Tottenham Hotspur', 'West Bromwich Albion', 'West Ham United'
						]

		sw_team_name_formating = ['Arsenal', 'Aston Villa', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton',
						'Hull City', 'Leicester City', 'Liverpool', 'Manchester City', 'Manchester United',
						'Newcastle United', 'Queens Park Ra', 'Southampton', 'Stoke City', 'Sunderland',
						'Swansea City', 'Tottenham Hotspur', 'West Bromwich', 'West Ham United',
						]

		for table in soup.findAll('div', id="page_team_1_block_team_table_10"):
			rawdata_league = table

		rawdata_league_list = [tr.findAll('td') for tr in rawdata_league.findAll('tr')]

		for row in rawdata_league_list:
			league.append([cell.text for cell in row])

		w.close()

		del league[0]

		for wrong,correct in zip(sw_team_name_formating, premier_league_teams):
			for lst in league:
				if wrong in lst[1]:
					lst[1] = correct

		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		standings = "\n####"
		standings += "\n###Premier League Standings "
		standings += "\n|Pos |    Team    | Pld  | GD | Pts|"
		standings += "\n| :-: | :----------: | :-: | :-: | :-: |"

		for lst in league:

			if lst[1] == "Manchester United":
				standings += "\n|**{0}**|**{1}**|**{2}**|**{3}**|**{4}**|".format(lst[0], league_dict["Manchester United"], lst[2], lst[3],lst[4])
			else:
				standings += "\n|{0}|{1}|{2}|{3}|{4}|".format(lst[0], league_dict[lst[1]], lst[2], lst[3],lst[4])

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://us.soccerway.com/national/england/premier-league/20142015/regular-season/r25191/?ICID=SN_01_01)*\n"
		# standings +="#[](#break)"

		return standings		

	def scrape_scorers(self):
		w = urllib2.urlopen('http://us.soccerway.com/teams/england/manchester-united-fc/662/squad/')
		soup = BeautifulSoup(w.read())

		scorers = []
		players = []
		starts = []
		subs = []
		goals = []
		assists = []
		final = []

		for table in soup.findAll('table', id="page_team_1_block_team_squad_3-table"):
			rawdata_scorers = table

		rawdata_scorers_list = [tr.findAll('td') for tr in rawdata_scorers.findAll('tr')]

		for row in rawdata_scorers_list:
			scorers.append([cell.text for cell in row])

		w.close()

		for lst in scorers:
			for l in  range(0, len(lst)):
				if l == 2 and lst[l] != "None":
					players.append(lst[l])
				if l == 8 and lst[l] != "None":
					starts.append(lst[l])
				if l == 9 and lst[l] != "None":
					subs.append(lst[l])
				if l == 12 and lst[l] != "None":
					goals.append(lst[l])
				if l ==13 and lst[l] != "None":
					assists.append(lst[l])

		mufc_squad = ['D. De Gea', 'A. Lindegaard', 'B. Amos', 'S. Johnstone', 'Rafael', 'P. Evra', 'P. Jones', 'R. Ferdinand', 'J. Evans', 'C. Smalling', 'N. Vidic', 'Fabio', 'A. Buttner', 'M. Keane', 'Anderson', 'R. Giggs', 'M. Carrick', 'Nani', 'A. Young', 'T. Cleverley', 'D. Fletcher', 'A. Valencia', 'M. Fellaini', 'T. Lawrence', 'A. Januzaj', 'J. Lingard', 'J. Mata', 'W. Rooney', 'J. Hernandez', 'D. Welbeck', 'R. van Persie', 'S. Kagawa', 'W. Zaha', 'J. Wilson']

		sw_player_name_formatting = ['De Gea', 'A. Lindegaard', 'B. Amos', 'S. Johnstone', 'Rafael', 'P. Evra', 'P. Jones', 'R. Ferdinand', 'J. Evans', 'C. Smalling', 'N. Vidi', 'bio', 'A. B', 'M. Keane', 'Anderson', 'R. Giggs', 'M. Carrick', 'Nani', 'A. Young', 'T. Cleverley', 'D. Fletcher', 'A. Valencia', 'M. Fellaini', 'T. Lawrence', 'A. Januzaj', 'J. Lingard', 'Mata', 'W. Rooney', 'J. Hern', 'D. Welbeck', 'R. van Persie', 'S. Kagawa', 'W. Zaha', 'J. Wilson']

		for wrong, correct in zip(sw_player_name_formatting, mufc_squad):
			for l in range(0, len(players)):
				if wrong in players[l]:
					players[l] = correct;

		for j in range(0, len(players)):
			total_apps = int(starts[j]) + int(subs[j])
			final.append({'player': players[j], 'start': int(starts[j]), 'sub': int(subs[j]), 'app': total_apps, 'goal': int(goals[j]), 'assist': int(assists[j])})

		final_list = newlist = sorted(final, key=operator.itemgetter('goal'), reverse=True)

		#print final_list[:5]

		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		standings = "\n###Top scorers (Premier League) "
		standings += "\n|Player|Goals|Assists|Games|"
		standings += "\n|:--:|:--:|:--:|:--:|"

		for j in range(0, 5):
			standings += "\n|{0}|{1}|{2}|{3}({4})|".format(final_list[j]['player'], final_list[j]['goal'], final_list[j]['assist'], final_list[j]['start'], final_list[j]['sub'])

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://us.soccerway.com/teams/england/manchester-united-fc/662/squad/)*\n"

		return standings

	def create_sidebar(self):
		h = HTMLParser.HTMLParser()
		#Initialize PRAW and login
		r = Reddit(user_agent='/r/reddevils bot by /u/Hubwub')
		r.login(self.username,self.password)
		#Grab the sidebar template from the wiki
		sidebar = r.get_subreddit(self.subreddit).get_wiki_page('edit_sidebar').content_md
		#Create list from sidebar by splitting at ####
		sidebar_list = sidebar.split('####')
		#Sidebar
		#print sidebar_list
		#sidebar = (sidebar_list[0]+league+sidebar_list[1])
		sidebar = (sidebar_list[0]+league+rfixtures+goals+sidebar_list[1])
		#Fix characters in sidebar
		sidebar = h.unescape(sidebar)
		return sidebar

	def update_reddit(self):
		#Initialize PRAW and login
		r = Reddit(user_agent='/r/reddevils bot by /u/Hubwub')
		r.login(self.username,self.password)
		#Grab the current settings
		settings = r.get_subreddit(self.subreddit).get_settings()
		#Update the sidebar
		#print sidebar
		settings['description'] = sidebar
		settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])

rdb = Red_Devils_Bot()

while(True):
	print 'Getting results and fixtures'
	rfixtures = rdb.scrape_fixtures()
	print rfixtures
	print 'Getting League standings'
	league = rdb.scrape_league()
	print league
	print 'Getting goal scorers'
	goals = rdb.scrape_scorers()
	print goals
	sidebar = rdb.create_sidebar()
	print "Reddit was updated on " + datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')
	rdb.update_reddit()
	print 'Sleeping..\n'
	time.sleep(900)