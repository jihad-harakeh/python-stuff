"""
Chess.com Player Stats Scraper

This script uses Playwright to:
- Check if a given Chess.com username exists
- Take a full-page screenshot of the user's profile
- Extract and display:
    - Username
    - Join date
    - Last online status
    - Blitz, Bullet, and Rapid ratings

It navigates through the profile and stats pages using CSS selectors,
demonstrating real-world web scraping and DOM interaction.
"""


from playwright.sync_api import sync_playwright

username=input('enter username: ')
url=f'https://www.chess.com/member/{username}'

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    resp=page.goto(url)
    if resp and resp.status!=200:
        print("username doesn't exist")
        exit()
    page.screenshot(path='fullpage.png', full_page=True)
    user=page.locator('h1.profile-card-username').inner_text()
    joined=page.locator('div.profile-header-details-value').nth(0).inner_text()
    last_online=page.locator('div.profile-header-details-value').nth(2).inner_text()
    stats_link=page.locator('a.profile-header-tabs-tab').nth(2).evaluate("el => el.href")
    print('username: ',user)
    print('joined: ',joined)
    print('last online: ',last_online)

    page.goto(stats_link)
    blitzpage=page.locator('a.overview-item').nth(2).evaluate('el => el.href')
    page1=browser.new_page()
    page1.goto(blitzpage)
    blitz_rating=page1.locator('div.rating-block-container').inner_text().split()[0]
    print('Blitz: ',blitz_rating)
    rapidpage=page.locator('a.overview-item').nth(4).evaluate('el => el.href')
    page1.goto (rapidpage)
    rapid_rating=page1.locator('div.rating-block-container').inner_text().split()[0]
    print('Rapid: ',rapid_rating)
    bulletpage=page.locator('a.overview-item').nth(3).evaluate('el => el.href')
    page1.goto(bulletpage)
    bullet_rating=page1.locator('div.rating-block-container').inner_text().split()[0]
    print('Bullet: ',bullet_rating)


    browser.close()
