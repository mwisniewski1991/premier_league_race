import bs4
from bs4 import BeautifulSoup
import requests

def get_soup(link:str) -> BeautifulSoup:
    page = requests.get(link)
    return BeautifulSoup(page.text, features='html.parser')

def parse_matchreport_links(matchreports_links:list[str]) -> list[str]:
    prefix:str = 'https://fbref.com'
    return [prefix + link for link in matchreports_links]

def get_all_matchreport_links(link:str) -> list:
    soup: BeautifulSoup = get_soup(link)
    matchreports_href:list = soup.find_all('a', text='Match Report')
    matchreports_links = [matchreport['href']  for matchreport in  matchreports_href]

    return parse_matchreport_links(matchreports_links)

def get_scorebox_div(soup:BeautifulSoup, home_away:str) -> bs4.Tag:
    if home_away == 'home':
        div_id:str = 'a'
    elif home_away == 'away':
        div_id:str = 'b'
    else:
        raise ValueError('Choose beetwen "home" and "away".')

    return soup.find('div', class_='scorebox').find('div', id=div_id)

def find_goals_scorers(scorebox: bs4.Tag, home_away:str) -> list[str]:
    all_goals = [
        *scorebox.find_all('div', class_='event_icon goal'),
        *scorebox.find_all('div', class_='event_icon penalty_goal'),
    ]

    if home_away == 'home':
        return [goal.find_previous_siblings()[0].get_text() for goal in all_goals]
    elif home_away == 'away':
        return [goal.find_next_siblings()[0].get_text() for goal in all_goals]
    else:
        raise ValueError('Choose beetwen "home" and "away".')


def get_match_scorers(link:str) -> list:
   soup:BeautifulSoup = get_soup(link)

   scorebox_a = get_scorebox_div(soup, 'home')
   scorebox_b = get_scorebox_div(soup, 'away')

   goals_scorers = [
       *find_goals_scorers(scorebox_a, 'home'),
       *find_goals_scorers(scorebox_b, 'away'),
    ]
   return goals_scorers


if __name__ == '__main__':
    LINK:str = 'https://fbref.com/en/matches/8ff2f8fe/Newcastle-United-Aston-Villa-August-12-2023-Premier-League'
    get_match_scorers(LINK)
