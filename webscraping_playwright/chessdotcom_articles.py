# scrape article titles, links, and excerpts from the first 3 pages of Chess.com's article section.
# Outputs the data to the console

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    url='https://www.chess.com/articles?page='

    for n in range(1,4):
        print('>'*10,n,'<'*10)
        print('\n')
        full_url=f"{url}{n}"
        print(full_url,'\n')
        page.goto(full_url)
        articles=page.locator('article')
        count=articles.count()
        for nn in range(count):
            title=articles.nth(nn).locator('a.post-preview-title').inner_text()
            link=articles.nth(nn).locator('a.post-preview-title').get_attribute('href')
            excerpt=articles.nth(nn).locator('p').inner_text()
            print(title)
            print(link)
            print(excerpt,'\n')

    browser.close()
