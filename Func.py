import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import Library


def open_tabs(browser):
    z = -1
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/'
                                                                                   'div[1]/ul/li[2]/a/div')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="live-table"]/'
                                                                                   'div[1]/ul/li[2]/a/div')))
        else:
            break

    if Library.Select == "LIVE":
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[2]/a/div').click()
    else:
        browser.find_element_by_xpath('//*[@id="live-table"]/div[1]/ul/li[6]/a/div').click()

    List_scroll = browser.find_elements_by_css_selector(".event__expander.icon--expander.expand")
    for x in List_scroll:
        try:
            List_scroll[z].click()
            z -= 1
        except selenium.common.exceptions.ElementClickInterceptedException:
            browser.execute_script("window.scrollTo(0," + str(int(x.location.get("y")) - 100) + ")")
    browser.execute_script("window.scrollTo(0, 0)")


# Сбор необходимых матчей
def select_match(browser, times):
    List_match = browser.find_elements_by_class_name("event__match")
    List_match_edit = []
    for x in List_match:
        try:
            # Выбор матчей со временем игры меньше 15 минут
            if int(str(x.text).strip().split("\n")[0]) < 60:
                Library.List_need_match.append(str(x.text).strip().split("\n")[1])
        except ValueError:
            pass
    # Убираем из списка метчи найденные в первом прогоне
    if times >= 2:
        List_need_match = list(set(Library.List_need_match) - set(List_match_edit))
    else:
        List_match_edit = Library.List_need_match
    # Убираем из списка матчи которые уже есть в результатах
    with open('List_chapter.txt', 'r', encoding='utf-8') as file1:
        text = ' '.join(file1.read().split())
        file1.close()
    for x in Library.List_need_match:
        if x in text:
            Library.List_need_match.remove(x)
    return Library.List_need_match


def open_match(List_need_match, browser):
    # Получаем список всех матчей
    List_match_online = browser.find_elements_by_class_name('event__participant--home')
    # Ищем нужный нам матч и открываем его
    for x in List_need_match:
        for y in List_match_online:
            if x == y.text:
                while True:
                    try:
                        y.click()
                        number_of_matches(browser)
                    except selenium.common.exceptions.ElementClickInterceptedException:
                        browser.execute_script("window.scrollTo(0," + str(int(x.location.get("y")) + 100) + ")")
                    else:
                        break
            else:
                pass

def number_of_matches(browser):
    browser.switch_to.window(browser.window_handles[-1])
    number_match = 0
    while True:
        try:
            WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="li-match-head-2-head"]')))
            browser.find_element_by_class_name("li2").click()
            # Проверка загрузки последних матчей
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH,
                                                                             '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                             'table/thead/tr/td')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
        else:
            break
    # Находим количество матчей
    max_match = browser.find_elements_by_xpath('//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr').__len__()
    if max_match < 5:
        number_match = max_match
    else:
        number_match = 5
    analysis(browser, number_match)

def analysis(browser, number_match):
    for y in range(1, number_match + 1):
        try:
            WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                         '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                         'table/tbody/tr[' + str(
                                                                             y) + ']/td[2]')))
        except selenium.common.exceptions.TimeoutException:
            browser.refresh()
            WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                         '//*[@id="tab-h2h-overall"]/div[1]/'
                                                                         'table/tbody/tr[' + str(
                                                                             y) + ']/td[2]')))
        browser.find_element_by_xpath(
            '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
        browser.switch_to.window(browser.window_handles[-1])
        try:
            try:
                WebDriverWait(browser, 15).until(ec.presence_of_element_located((By.XPATH,
                                                                                 '//*[@id="flashscore"]/div[1]/'
                                                                                 'div[1]/div[2]/div/div/a')))
            except selenium.common.exceptions.TimeoutException:
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                browser.find_element_by_xpath(
                    '//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[' + str(y) + ']/td[2]').click()
                browser.switch_to.window(browser.window_handles[-1])

            if browser.find_element_by_xpath('//*[@id="flashscore"]/div[1]/div[1]/div[2]/div/div/a') \
                    .text.find(name_one_team) == -1:
                try:
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-head-2-head"]')))
                except selenium.common.exceptions.TimeoutException:
                    browser.refresh()
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-summary"]')))
                team_one_goal += int(browser.find_elements_by_class_name("p1_away")[0].text)
                team_one_goal_away += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[2]').text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[1]').text)
            else:
                try:
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-head-2-head"]')))
                except selenium.common.exceptions.TimeoutException:
                    browser.refresh()
                    WebDriverWait(browser, 15).until(ec.element_to_be_clickable((By.XPATH,
                                                                                 '//*[@id="li-match-summary"]')))
                team_one_goal += int(browser.find_elements_by_class_name("p1_home")[0].text)
                team_one_goal_home += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                        'div[1]/div[1]/div[2]/span[1]').text)
                team_one_missing += int(browser.find_element_by_xpath('//*[@id="summary-content"]/'
                                                                      'div[1]/div[1]/div[2]/span[2]').text)
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        except selenium.common.exceptions.NoSuchElementException:
            print("Чет не получилось )")
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            break
        except ImportError:
            print("Не нашел счет, ля!")