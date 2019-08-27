from typing import List, Any
import Func
import selenium
import re
import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

ua = dict(DesiredCapabilities.CHROME)
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x935')
# options.add_argument("--no-startup-window")
browser = webdriver.Chrome(chrome_options=options)

team_one_goal = 0
team_two_goal = 0
team_one_missing = 0
team_two_missing = 0

team_one_goal_home = 0
team_two_goal_home = 0
team_one_goal_away = 0
team_two_goal_away = 0
team_one_missing_home = 0
team_one_missing_away = 0
team_two_missing_home = 0
team_two_missing_away = 0

The_end = []
garbage = 0

Select = ""
List_need_match = []
