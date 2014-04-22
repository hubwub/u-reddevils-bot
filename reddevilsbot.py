#RedDevils BOT by /u/hubwub
import datetime
import time
import urllib2
import HTMLParser
import json
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
		w = urllib2.urlopen('http://espnfc.com/team/fixtures?id=360&cc=5901')
		soup = BeautifulSoup(w.read())

		fixtures= []
		flist = []
		
		for table in soup.findAll('div', id="my-teams-table"):
			rawdata_fixtures = table

		rawdatafixtures_list = [tr.findAll('td') for tr in rawdata_fixtures.findAll('tr')]

		for row in rawdatafixtures_list:
		 	flist.append([cell.text for cell in row])

		#lst[0].find("Jan") !=  -1) or
		for lst in flist:
			if  (((lst[0].find("Apr") !=  -1) or (lst[0].find("May") !=  -1))):
				fixtures.append([val.replace(u'\n', u'') .replace(u'\xa0', u'').replace(u'\t', u'').replace(u'Angleterre', u'').replace(u'English FA Cup (Round 3)', u'FA').replace(u'Capital One Cup (Semi-finals)', u'LC').replace(u'UEFA Champions League (Round of 16)', u'CL').replace(u'Premier League','PL').replace(u'UEFA Champions League (Quarter-finals)', u'CL').replace(u'UEFA Champions League (Quarterfinals)', u'CL') for val in lst])

		w.close()

		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		standings = "\n#Results and Fixtures"
		standings += "\n|Comp | Date | |Opponent | Result"
		standings += "\n|:-----------------------------: | :----: | :-: |  :-: | :-: |"

		for lst in fixtures:
			if (lst[2] == "Manchester United"):
				standings += "\n|{0}|{1}|H|{2}|{3}|".format(lst[-1], lst[0], lst[4], lst[3].replace(u'v', u'-'))
			else:
				standings += "\n|{0}|{1}|A|{2}|{3}|".format(lst[-1] , lst[0], lst[2], lst[3].replace(u'v', u'-'))

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://www.manutd.com/en/Fixtures-And-Results/United-Fixtures-And-Results.aspx?pageNo=4)*\n"
		standings +="#[](#break)"

		return standings

	def scrape_league(self):
		w = urllib2.urlopen('http://int.soccerway.com/teams/england/manchester-united-fc/662/')
		soup = BeautifulSoup(w.read())

		league = []

		for table in soup.findAll('div', id="page_team_1_block_team_table_10"):
			rawdata_league = table

		rawdata_league_list = [tr.findAll('td') for tr in rawdata_league.findAll('tr')]

		for row in rawdata_league_list:
			league.append([cell.text for cell in row])

		w.close()

		del league[0]

		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		standings = "\n####"
		standings += "\n#Premier League Standings "
		standings += "\n|Pos |    Team    | Pld  | GD | Pts|"
		standings += "\n| :-: | :----------: | :-: | :-: | :-: |"

		for lst in league:
			if lst[1] == "Manchester United":
				standings += "\n|**{0}**|**{1}**|**{2}**|**{3}**|**{4}**|".format(lst[0], lst[1], lst[2], lst[3],lst[4])
			else:
				standings += "\n|{0}|{1}|{2}|{3}|{4}|".format(lst[0], lst[1], lst[2], lst[3],lst[4])

		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://www.premierleague.com/en-gb/matchday/league-table.html)*\n"
		standings +="#[](#break)"

		return standings		

	def scrape_scorers(self):
		w = urllib2.urlopen('http://espnfc.com/team/squad/_/id/360/league/all/manchester-united?cc=5901')
		soup = BeautifulSoup(w.read())

		scorers = []
		final = []
		final_list = []

		for table in soup.findAll('tbody', id="statsBody_1"):
			rawdata_scorers = table

		rawdata_scorers_list = [tr.findAll('td') for tr in rawdata_scorers.findAll('tr')]

		for row in rawdata_scorers_list:
			scorers.append([cell.text for cell in row])

		w.close()

		for lst in scorers:
			if int(lst[4])  >= 1:
				final.append([val.replace(u'Javier Hern\xc3\xa1ndez', u'Javier Hernandez') for val in lst])

		final_list = sorted(final, key=lambda score: int(score[4]), reverse=True)

		updated = datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')

		standings = "\n#Top scorers (All Competitions) "
		standings += "\n|Player|Goals|Assists|Games|"
		standings += "\n|:--:|:--:|:--:|:--:|"

		for lst in final_list[:5]:
			standings += "\n|{0}|{1}|{2}|{3}({4})|".format(lst[1], lst[4], lst[7], lst[2], lst[3])
		
		standings += "\n\n*Last Updated: " + updated +  " | [Full](http://espnfc.com/team/squad/_/id/360/league/all/manchester-united?cc=5901)*\n"

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
	#print rfixtures
	print 'Getting League standings'
	league = rdb.scrape_league()
	#print league
	print 'Getting goal scorers'
	goals = rdb.scrape_scorers()
	#print goals
	sidebar = rdb.create_sidebar()
	print "Reddit was updated on " + datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')
	rdb.update_reddit()
	print 'Sleeping..\n'
	time.sleep(900)