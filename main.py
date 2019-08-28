import Library
import Func
import time
url = "https://www.myscore.ru/"
Library.browser.get(url)

# Написать "LIVE" для парсинга лайв матчей. По умолчанию пасинг происходит по "Расписание"
Library.Select = "LIVE"
for times in range(100):
    Func.open_tabs(Library.browser)
    if Library.Select == "LIVE":
        Func.open_match(Func.select_match(Library.browser, times), Library.browser)
    else:
        Func.open_match(Func.select_match_schedule(Library.browser), Library.browser)
    print("Цикл пройден!")
    time.sleep(300)
