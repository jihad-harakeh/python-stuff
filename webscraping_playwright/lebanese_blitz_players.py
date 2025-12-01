"""
Chess.com Lebanese Blitz Players Scraper
--------------------------------------------

This script uses Playwright to scrape all blitz
leaderboard pages for players from Lebanon on Chess.com. It automatically:

1. Navigates through all pages until the 'Next Page' button is disabled
2. Waits for table rows to fully load
3. Extracts rank, title, username, rating, win/draw/loss stats, and profile link
4. Writes all results into a CSV file

The code reliably scrapes more than 19K players across 390+ pages.

Output:
    blitz_players.csv
"""

from playwright.sync_api import sync_playwright
import csv
import time

def extract_and_write(players):
    for player in players:
        rank=player.query_selector('span.leaderboard-row-rank').inner_text().lstrip()
        title=player.query_selector('div.cc-user-block-component > a.cc-user-title-component').inner_text() if player.query_selector('div.cc-user-block-component > a.cc-user-title-component') else None
        name=player.query_selector('div.cc-user-block-component > div.cc-user-username-component').inner_text()
        rating=player.query_selector('td + td.leaderboard-table-text-right a.leaderboard-main-link').inner_text()
        won=player.query_selector_all('td.leaderboard-row-rating.leaderboard-table-text-right')[0].query_selector('span.leaderboard-row-regular-stats').inner_text()
        draw=player.query_selector_all('td.leaderboard-row-rating.leaderboard-table-text-right')[1].query_selector('span.leaderboard-row-regular-stats').inner_text()
        lost=player.query_selector_all('td.leaderboard-row-rating.leaderboard-table-text-right')[2].query_selector('span.leaderboard-row-regular-stats').inner_text()
        link=player.query_selector('a.leaderboard-main-link').get_attribute('href')
        fulllink=f'https://www.chess.com{link}'
        if title:
            csv_writer.writerow([rank, title+' '+ name, rating, won, draw, lost, fulllink])
        else:
            csv_writer.writerow([rank, name, rating, won, draw, lost, fulllink])





with open('blitz_players.csv','w', newline='', encoding="utf-8") as csvfile:
    csv_writer=csv.writer(csvfile)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto('https://www.chess.com/leaderboard/live?country=LB')
        csv_writer.writerow([page.title()])
        csv_writer.writerow(['Rank', 'Name', 'Rating', 'Won', 'Draw', 'Lost', 'Link'])


        total_number_of_players=0
        pages_scraped=0

        while True:
            page.wait_for_selector('tbody > tr.leaderboard-row-show-on-hover', state='visible')
            page.evaluate('window.scrollTo(0,document.documentElement.scrollHeight)')
            time.sleep(1.5)
            lst=page.query_selector_all('tbody > tr.leaderboard-row-show-on-hover')
            if len(lst)<50 and not page.query_selector('button[aria-label="Next Page"].cc-button-disabled'):
                sec=1
                while True:
                    sec+=1
                    time.sleep(sec)
                    lst=page.query_selector_all('tbody > tr.leaderboard-row-show-on-hover')
                    if len(lst)==50 or sec>60:
                        break
            pages_scraped+=1
            total_number_of_players+=len(lst)
            print(f'page: {pages_scraped}, players: {len(lst)}')
            extract_and_write(lst)
            if page.query_selector('button[aria-label="Next Page"].cc-button-disabled'):
                print('Done, no more pages left to scrape.')
                break
            else:
                page.click('button[aria-label="Next Page"]')

        print(f'total numbers of players: {total_number_of_players}')
