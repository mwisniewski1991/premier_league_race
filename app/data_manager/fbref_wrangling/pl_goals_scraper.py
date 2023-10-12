import time
import pl_goals_scraper_functions as plgoals_funcs


def scrap_goals_data() -> list[tuple]:

    LINK = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

    matchreports_links = plgoals_funcs.get_all_matchreport_links(LINK)

    match_goals_list = []
    for report_link in matchreports_links[:4]:
        print(report_link)
        soup = plgoals_funcs.get_soup(report_link)
        match_scorers = plgoals_funcs.get_match_scorers(soup)
        match_date = plgoals_funcs.get_match_date(soup)
        match_goals = plgoals_funcs.create_goal_object(match_scorers, match_date) 

        match_goals_list.extend(match_goals)
        time.sleep(3)
    



    return match_goals_list




if __name__ == '__main__':
    data = scrap_goals_data()
    print(data)

# player
# datetime
# goals