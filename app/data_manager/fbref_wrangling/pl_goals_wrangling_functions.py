import bs4
from bs4 import BeautifulSoup
import requests

def get_soup(link:str) -> BeautifulSoup:
    page = requests.get(link)
    return BeautifulSoup(page.text, features='html.parser')

def parse_matchreport_links(matchreports_links:list[str]) -> list[str]:
    '''
        Add prefix to all links to create whole http page.
    '''
    prefix:str = 'https://fbref.com'
    return [prefix + link for link in matchreports_links]

def get_all_matchreport_links(link:str) -> list:
    '''
        Find all links to matches reports.
    '''
    soup: BeautifulSoup = get_soup(link)
    matchreports_href:list = soup.find_all('a', text='Match Report')
    matchreports_links = [matchreport['href']  for matchreport in  matchreports_href]

    return parse_matchreport_links(matchreports_links)

def get_scorebox_div(soup:BeautifulSoup, home_away:str) -> bs4.Tag:
    '''
        Get from page div with list of scores from Home and Away team.    
    '''
    if home_away == 'home':
        div_id:str = 'a'
    elif home_away == 'away':
        div_id:str = 'b'
    else:
        raise ValueError('Choose beetwen "home" and "away".')

    return soup.find('div', class_='scorebox').find('div', id=div_id)

def find_goals_scorers(scorebox: bs4.Tag, home_away:str) -> list[str]:
    '''
        Find on page player which scored goal from play and from penalty.
    '''
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

def get_match_scorers(soup: BeautifulSoup) -> list[str]:
   '''
        Extract list scorers from page.
   '''
   scorebox_a = get_scorebox_div(soup, 'home')
   scorebox_b = get_scorebox_div(soup, 'away')

   goals_scorers = [
       *find_goals_scorers(scorebox_a, 'home'),
       *find_goals_scorers(scorebox_b, 'away'),
    ]
   return goals_scorers

def parse_match_date(raw_date:str) -> str:
    '''
        Remove prefix from raw date to create date string 'yyyy-mm-dd'
    '''
    if not '/en/matches/' in raw_date:
        raise ValueError("Raw match date string has change format. Check current page settings.") 

    return raw_date.removeprefix('/en/matches/')

def get_match_date(soup:BeautifulSoup) -> str:
    '''
        Return raw match date. 
        Raw match date should look like: "/en/matches/2023-08-12"
    '''
    return parse_match_date(soup.find('div', class_='scorebox_meta').find('a')['href'])

def create_goal_object(match_scorers:list[str], match_date: str) -> list[tuple]:
    '''
        Create list of tuples which will be insert into DB.
        Each event is one goal.
    '''
    return [(scorer, match_date, 1) for scorer in match_scorers] 


if __name__ == '__main__':
    LINK:str = 'https://fbref.com/en/matches/8ff2f8fe/Newcastle-United-Aston-Villa-August-12-2023-Premier-League'
    soup = get_soup(LINK)
    match_scorers = get_match_scorers(soup)
    match_date = get_match_date(soup)
    parsed = create_goal_object(match_scorers, match_date) 
    
    print(parsed)