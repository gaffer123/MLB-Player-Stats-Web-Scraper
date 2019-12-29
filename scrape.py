import requests
import re
import pandas as pd
import numpy
from bs4 import BeautifulSoup		# need to import pandas for dataframes, beautiful soup for web scraping and tkinter for the ui
from tkinter import *
from tkinter import ttk

i = 1		#Initializing varibles for use later
N = 0


def Pitch_season(year, sort, i):  #This function scrapes MLB.com for pitchers statistics
	#for i in range(1,340,50):
		global label
		if sort == "":
			sort = 'ERA'
		url = 'http://www.espn.com/mlb/history/leaders/_/type/pitching/breakdown/season/year/{}/sort/{}/start/{}'.format(year, sort, i)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header = soup.find('tr', attrs={'class': 'colhead'})  #searches for the column names in the HTML
		columns = [col.get_text() for col in header.find_all('td')]
		pd.set_option('display.max_columns', None)  
		pd.set_option('display.width', None)
		pd.set_option('display.expand_frame_repr', False)
		pd.set_option('max_colwidth', -1)
		final_df = pd.DataFrame(columns = columns)
		players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
		for player in players:				# this for loop finds the list of players and combines it with the columns along with the stats
				stats = [stat.get_text() for stat in player.find_all('td')]

				temp_df = pd.DataFrame(stats).transpose()
				temp_df.columns = columns

				final_df = pd.concat([final_df, temp_df], ignore_index = True)

		label = Label(main, text = final_df.iloc[0:25], font = ('Consolas', 12), bg = 'light grey')		# Label in tkinter to display the dataframe, i used Consolas as the font
		label.place(x=35, y=165)														# because there was less weird spacing, which made the final dataframe look nice


def Bat_season(year, sort, i):
	#for i in range(1,340,50):
		if sort =="":
			sort = 'avg'
		global label
		url = 'http://www.espn.com/mlb/history/leaders/_/breakdown/season/year/{}/sort/{}/start/{}'.format(year, sort, i)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header = soup.find('tr', attrs={'class': 'colhead'})
		columns = [col.get_text() for col in header.find_all('td')]
		pd.set_option('display.max_columns', None)  
		pd.set_option('display.width', None)
		pd.set_option('display.expand_frame_repr', False)
		pd.set_option('max_colwidth', -1)
		final_df = pd.DataFrame(columns = columns)
		players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
		for player in players:
				stats = [stat.get_text() for stat in player.find_all('td')]

				temp_df = pd.DataFrame(stats).transpose()
				temp_df.columns = columns

				final_df = pd.concat([final_df, temp_df], ignore_index = True)

		#final_df.style.set_properties(**{'background-color': 'black', 'color' = 'green'})
		final_df.style.applymap(lambda x:["background-color: red"], subset=['HR'])
		label = Label(main, text = final_df.iloc[0:25], font = ('Consolas', 12), bg = 'light grey')
		label.place(x=35, y=165)	# pretty much the same as Pitch_season just search through a different link

'''
def Batting_Career(sort):
	for i in range(1,500,50):
		url = 'http://www.espn.com/mlb/history/leaders/_/sort/{}/start/{}'.format(sort, i)
		page = requests.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		header = soup.find('tr', attrs={'class': 'colhead'})
		columns = [col.get_text() for col in header.find_all('td')]
		final_df = pd.DataFrame(columns = columns)
		players = soup.find_all('tr', attrs={'class':re.compile('row player-10-')})
		for player in players:
				stats = [stat.get_text() for stat in player.find_all('td')]

				temp_df = pd.DataFrame(stats).transpose()
				temp_df.columns = columns

				final_df = pd.concat([final_df, temp_df], ignore_index = True)


		print(final_df)
'''

def keep_count():
	global N, count
	N += 1
	count = i * (25 * N)
	if count == 350:
		button2a.destroy()
	return keep_count   # keeps count of the page that the user is on

def keep_count_backwards():
	global count
	count -= 25
	if count == 0:
		button4.destroy()
	return count	# also keeps count of the page, in order to have a back button that works

def make_button4():
	global button4
	button4 = Button(main, text="Previous Page", fg="white", bg="black", command = lambda: [label.destroy(), Bat_season(List.get(), stats_(), keep_count_backwards())])	
	button4.place(height = 25, width = 80, x=365, y=680)	#creates the previous page button

def stats_():
	stats_B = tkvar.get()
	return stats_B # getter function for stats


def make_button2a():
	global button2a
	button2a =  Button(main, text="Next Page", fg="white", bg='black', command = lambda: [label.destroy(), Bat_season(List.get(), stats_(), keep_count()), button4.destroy(), make_button4()])
	button2a.place(height = 25, width = 80, x=450, y=680)	#makes a next page button

def Stats_Season_Bat():
	
	global button1, button2, button3, Menu, List, tkvar, button2a, info3, info4
	tkvar = StringVar(main)
	choices = {'avg', 'homeRuns', 'gamesPlayed', 'atBats', 'runs', 'hits', 'doubles', 'triples', 'RBIs', 'walks', 'strikeouts', 'stolenBases', 'caughtStealing'}
	#tkvar.set('avg')
	Menu = OptionMenu(main, tkvar, *choices)				#dropdown menu to pick what stat you want
	Menu.place(height = 20, width=125, x=620, y=100)

	years = []
	yearlist = reversed(range(1900,2020))
	for year in yearlist:
   		years.append(year)

	info3 = Label(main, text = 'Select Specific Stat to Search:', bg = "light grey", fg="blue") 
	info4 = Label(main, text = 'Select Season:', bg = "light grey", fg="blue")  		
	List = ttk.Combobox(main, values = years)			# another dropdown menu to pick the year
	List.place(height = 20, width=125, x=620, y=130)
	info4.place(x = 540, y = 130, height = 20)
	info3.place(x = 460, y = 100, height = 20)
	List.current(0)

	button3 = Button(main, text="Modify Search", fg="white", bg="black", command = lambda: [label.destroy(), Bat_season(List.get(), stats_(), i)])
	button1 = Button(main, text="Display Stats", fg="blue", command = lambda: [Bat_season(List.get(), stats_(), i), button1.destroy()])
	button2 = Button(main, text="Next Page", fg="white", bg='black', command = lambda: [label.destroy(), Bat_season(List.get(), stats_(), keep_count()), make_button4(), button2.destroy(), make_button2a()])
	'''
	buttons to move forward in the search progress
	'''

	button2.place(height = 25, width = 80, x=480, y=680)
	button3.place(height = 25, width=80, x=750, y=125)
	button1.place(height = 25, width=80, x=750, y=125)	#makes the ui for if the user wants season stats



def Stats_Season_Pitch():
	global button1, button2, button3, Menu, List, info3, info4, button2a, tkvar
	tkvar = StringVar(main)
	choices = {'ERA', 'gamesStarted', 'completeGames', 'gamesPlayed', 'shutouts', 'thirdInnings', 'hits', 'earnedRuns', 'triples', 'wins', 'walks', 'strikeouts', 'losses', 'saves'}
	#tkvar.set('ERA')
	Menu = OptionMenu(main, tkvar, *choices)
	Menu.place(height = 20, width=125, x=620, y=100)

	def stats_():
		stats_B = tkvar.get()
		return stats_B

	years = []
	yearlist = reversed(range(1900,2020))
	for year in yearlist:
   		years.append(year)

	info3 = Label(main, text = 'Select Specific Stat to Search:', bg = "light grey", fg="blue") 
	info4 = Label(main, text = 'Select Season:', bg = "light grey", fg="blue")  		
	List = ttk.Combobox(main, values = years)
	List.place(height = 20, width=125, x=620, y=130)
	info4.place(x = 540, y = 130, height = 20)
	info3.place(x = 460, y = 100, height = 20)
	List.current(0)

	button3 = Button(main, text="Modify Search", fg="white", bg="black", command = lambda: [label.destroy(), Pitch_season(List.get(), stats_(), i)])
	button1 = Button(main, text="Display Stats", fg="blue", command = lambda: [Pitch_season(List.get(), stats_(), i), button1.destroy()])
	button2 = Button(main, text="Next Page", fg="white", bg='black', command = lambda: [label.destroy(), Bat_season(List.get(), stats_(), keep_count()), make_button4(), button2.destroy(), make_button2a()])
	

	
	button2.place(height = 25, width = 80, x=480, y=680)
	button3.place(height = 25, width=80, x=750, y=125)
	button1.place(height = 25, width=80, x=750, y=125)


def Stats_Career_Pitch():
	W = 0
	global button1, button2, button3, Menu, tkvar, button2a, info3
	tkvar = StringVar(main)
	choices = {'ERA', 'gamesStarted', 'completeGames', 'gamesPlayed', 'shutouts', 'thirdInnings', 'hits', 'earnedRuns', 'triples', 'wins', 'walks', 'strikeouts', 'losses', 'saves'}
	#tkvar.set('avg')
	Menu = OptionMenu(main, tkvar, *choices)
	Menu.place(height = 20, width=125, x=630, y=115)

	info3 = Label(main, text = 'Select Specific Stat to Search:', bg = "light grey", fg="blue") 
	info3.place(x = 470, y = 115, height = 20)


	button3 = Button(main, text="Modify Search", fg="white", bg="black", command = lambda: [label.destroy(), Pitch_season(W, stats_(), i)])
	button1 = Button(main, text="Display Stats", fg="blue", command = lambda: [Pitch_season(W, stats_(), i), button1.destroy()])
	button2 = Button(main, text="Next Page", fg="white", bg='black', command = lambda: [label.destroy(), Pitch_season(W, stats_(), keep_count()), make_button4(), button2.destroy(), make_button2a()])

	
	button2.place(height = 25, width = 80, x=480, y=680)
	button3.place(height = 25, width=80, x=760, y=115)
	button1.place(height = 25, width=80, x=760, y=115) #makes the ui for career stats search


def Stats_Career_Bat():
	W = 0
	global button1, button2, button3, Menu, tkvar, button2a, info3
	tkvar = StringVar(main)
	choices = {'avg', 'homeRuns', 'gamesPlayed', 'atBats', 'runs', 'hits', 'doubles', 'triples', 'RBIs', 'walks', 'strikeouts', 'stolenBases', 'caughtStealing'}
	#tkvar.set('avg')
	Menu = OptionMenu(main, tkvar, *choices)
	Menu.place(height = 20, width=125, x=630, y=115)

	info3 = Label(main, text = 'Select Specific Stat to Search:', bg = "light grey", fg="blue") 
	info3.place(x = 470, y = 115, height = 20)


	button3 = Button(main, text="Modify Search", fg="white", bg="black", command = lambda: [label.destroy(), Bat_season(W, stats_(), i)])
	button1 = Button(main, text="Display Stats", fg="blue", command = lambda: [Bat_season(W, stats_(), i), button1.destroy()])
	button2 = Button(main, text="Next Page", fg="white", bg='black', command = lambda: [label.destroy(), Bat_season(W, stats_(), keep_count()), make_button4(), button2.destroy(), make_button2a()])

	
	button2.place(height = 25, width = 80, x=480, y=680)
	button3.place(height = 25, width=80, x=760, y=115)
	button1.place(height = 25, width=80, x=760, y=115)


def year():
	#ddvar = IntVar(main)
	global List
	years = []
	yearlist = reversed(range(1900,2020))
	for year in yearlist:
   		years.append(year)

	List = ttk.Combobox(main, values = years)
	List.pack()
	List.current(0)
	return List.get()	#returns the year the user picked to the scraping function

def Logic():
	if Var1() == 'Batting' and Var2() == 'Single-Season':
		main.pack_forget()
		main.pack_propagate(0)
		main.pack(expand = True, fill = BOTH)
		Stats_Season_Bat()
	elif Var1() == 'Pitching' and Var2() == 'Single-Season':
		main.pack_forget()
		main.pack_propagate(0)
		main.pack(expand = True, fill = BOTH)
		Stats_Season_Pitch()
	elif Var1() == 'Batting' and Var2() == 'Career':
		main.pack_forget()
		main.pack_propagate(0)
		main.pack(expand = True, fill = BOTH)
		Stats_Career_Bat()
	elif Var1() == 'Pitching' and Var2() == 'Career':
		main.pack_forget()
		main.pack_propagate(0)
		main.pack(expand = True, fill = BOTH)
		Stats_Career_Pitch()	
	else:	
		pass #see whether the user selects career or season stats
	
def reset():
	button2.destroy()
	button3.destroy()
	button1.destroy()
	label.destroy()
	Menu.destroy()
	info3.destroy()
	info4.destroy()
	List.destroy()
	#button1.destroy()
	#info3.destroy()	#resets the search in order to change search type

def Var1():
	gggg = var1.get()
	return gggg

def Var2():
	bbbb = var2.get()
	return bbbb

'''
This chunk here creates more buttons and labels that make the ui more user friendly and easir to navigate

'''

root = Tk()
root.geometry('1000x750')
main = Frame(root, bg = 'light grey')		# this is our main window that the ui will be in
main.pack_propagate(0)
main.pack(expand = True, fill = BOTH)


var1 = StringVar(main)
option_ = {'Batting', 'Pitching'}
check_Statistics = OptionMenu(main, var1, *option_)

var2 = StringVar(main)
option_2 = {'Single-Season', 'Career'}
check_Statistics2 = OptionMenu(main, var2, *option_2)	

Title = Label(main, text="MLB Statistics Database", font=('calibri', 40), bg = 'light grey')
info = Label(main, text = 'Select Batting or Pitching Statistics:', bg = "light grey", fg="blue")
info2 = Label(main, text = 'Select Season or Career Statistics:', bg = "light grey", fg = "blue")


Go_Button = Button(main, text='Search', fg='white', bg='blue', command = lambda: [Logic(), Go_Button.destroy(), new_butt()])

def new_butt():
	#info5 = Label(main, text = 'Select Reset for a new search:', bg = "light grey", fg="blue")
	Go_Button2 = Button(main, text='Reset Stats', fg='white', bg='blue', command = lambda: [reset(), Logic()])
	Go_Button2.place(height = 24, width = 80, x = 378, y = 125)
	#info5.place(x = 700, y = 95, height = 20)

Title.place(x=200, y=10, height = 75, width = 620)
check_Statistics.place(height = 20, width = 125, x = 250, y = 100)
check_Statistics2.place(height = 20, width = 125, x = 250, y = 130)
info.place(x = 57, y = 100, height = 20)
info2.place(x = 70, y = 130, height = 20)

#Stats_Season_Bat()
Go_Button.place(height = 25, width = 80, x = 385, y = 120)



root.mainloop()
