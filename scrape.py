import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from tkinter import *

i = 1
global Label


def Pitch_season(year, sort):
	for i in range(1,340,50):
		url = 'http://www.espn.com/mlb/history/leaders/_/type/pitching/breakdown/season/year/{}/sort/{}/start/{}'.format(year, sort, i)
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

def Bat_season(year, sort, i):
	#for i in range(1,340,50):
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
		label = Label(main, text = final_df.iloc[0:25], font = ('Consolas', 12))
		label.pack()


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

	

root = Tk()
root.geometry('1000x900')
main = Frame(root, bg = 'blue')
main.pack_propagate(0)
main.pack(expand = True, fill = BOTH)


button1 = Button(main, text="Display Stats", fg="blue", command = lambda: Bat_season(2011, 'avg', i))
button2 = Button(main, text="Next Page", fg="red", command = lambda: [label.destroy(), Bat_season(2011, 'avg', i+25)])
#button3 = Button(topFrame, text="click fssshere", fg="yellow")

button1.pack(side=TOP)
button2.pack(side=BOTTOM)
#button3.pack(side=BOTTOM)


root.mainloop()
