import datetime

import requests
from bs4 import BeautifulSoup
import urllib

class LunchRequestHandler:

    mensa_dashboard_url = "http://www.bo.cnr.it/mensa/bacheca/"

    def find_month(self, menu_string):
        month_pos = menu_string.find('/')
        return menu_string[month_pos:]

    def find_day_interval(self, menu_string):
        first_day_pos = menu_string.find('DAL ')
        last_day_pos = menu_string.find('AL ')
        first_day = int(menu_string[first_day_pos:].replace(' ', ''))
        last_day = int(menu_string[last_day_pos:].replace(' ', ''))
        return first_day, last_day

    def select_first_week_page(self, ):
        # Configure this to be your first request URL
        r = requests.get(self.mensa_dashboard_url)
        soup = BeautifulSoup(r.content, features="html.parser")
        for link in soup.body.find_all('a'):
            if "MENU'" in str(link.string):
                weekly_menu_link = link.get('href')
                break
        return weekly_menu_link

    def find_doc_file_in_page(self, weekly_menu_link):
        r = requests.get(self.mensa_dashboard_url + weekly_menu_link)
        soup = BeautifulSoup(r.content, features="html.parser")
        for link in soup.body.p.find_all('a'):
            return link['href']

    def find_lunch_program_in_doc_by_weekday(self, doc_file_link, weekday):
        lunch_doc, _ = urllib.request.urlretrieve(self.mensa_dashboard_url + doc_file_link)
        lunch_doc = open(lunch_doc, encoding='ansi').read()
        weekday = self._translate_week_day(weekday)
        lunch_menu = self._select_weekday(lunch_doc, weekday)
        return lunch_menu

    def _select_weekday(self, lunch_doc:str, weekday:str):
        menu_pos = lunch_doc.find("MENU")
        if menu_pos == -1:
            menu_pos = lunch_doc.find("MENÙ")
        if menu_pos == -1: return "No MENU keyword found in doc"
        reduced_lunch_doc = lunch_doc[menu_pos:menu_pos+2000]

        weekday_lunch_start_pos = reduced_lunch_doc.find(weekday)
        weekday_lunch_end_pos = reduced_lunch_doc.find("", weekday_lunch_start_pos, weekday_lunch_start_pos+500) #self._find_all_indexes(reduced_lunch_doc, "", start=weekday_lunch_pos, end=weekday_lunch_pos+500)
        if weekday_lunch_end_pos == -1:
            return "No lunch menu was found"
        return reduced_lunch_doc[weekday_lunch_start_pos:weekday_lunch_end_pos].replace('', '\t')

    # def _find_all_indexes(self, input_str, search_str, start=None, end=None):
    #     l1 = []
    #     length = len(input_str)
    #     index = start
    #     while index < length:
    #         i = input_str.find(search_str, index, end)
    #         if i == -1:
    #             return l1
    #         l1.append(i)
    #         index = i + 1
    #     return l1

    def _translate_week_day(self, date_argum):
        date_argum = datetime.datetime.strptime(date_argum, '%y-%m-%d')
        date_argum = date_argum.strftime("%A")[:-1].lower()
        eng_to_ita_weekday = {"monda":"luned", "tuesda":"marted", "wednesda":"mercoled", "thursda":"gioved", "frida":"venerd"}
        return eng_to_ita_weekday.get(date_argum, "No day was found")

    def lunch_handler(self, weekday):
        weekly_menu_page_link = self.select_first_week_page()
        doc_file_link = self.find_doc_file_in_page(weekly_menu_page_link)
        return self.find_lunch_program_in_doc_by_weekday(doc_file_link, weekday)

# for ul_list in soup.body.find_all('ul'):
#     for li_link_list in ul_list.find_all('li'):
#         for a_link_list in li_link_list.find_all('a'):
#             menu_string = a_link_list.string
#             # month = find_month(menu_string)
#             # first_day, last_day = find_day_interval(menu_string)
#             if menu_string.contains("MENU'"):
#
#                 print(a_link_list.string)


if __name__ == "__main__":
    l = LunchRequestHandler().lunch_handler("19-10-28")