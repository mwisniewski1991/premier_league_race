import time
import pl_goals_wrangling_functions as plgoals_funs


def scrap_goals_data() -> list:

    LINK = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

    matchreports_links = plgoals_funs.get_all_matchreport_links(LINK)

    match_goals_list = []
    for report_link in matchreports_links:
        print(report_link)
        soup = plgoals_funs.get_soup(report_link)
        match_scorers = plgoals_funs.get_match_scorers(soup)
        match_date = plgoals_funs.get_match_date(soup)
        match_goals = plgoals_funs.create_goal_object(match_scorers, match_date) 

        match_goals_list.extend(match_goals)
        time.sleep(3)

    return match_goals_list




if __name__ == '__main__':
    data = scrap_goals_data()
    print(data)

# player
# datetime
# goals