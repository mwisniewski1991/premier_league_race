from bs4 import BeautifulSoup
import requests
import pandas as pd
from pl_goals_wrangling_functions import get_all_matchreport_links



def scrap_goals_data() -> list:

    LINK = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

    matchreports_links = get_all_matchreport_links(LINK)

    for report_link in matchreports_links[:3]:
        print(report_link)




if __name__ == '__main__':
    scrap_goals_data()

# player
# datetime
# goals