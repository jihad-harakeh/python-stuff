# Script to scrape player rankings from the Keshmat Circuit website.
# Extracts page title, heading, and player stats (rank, name, points, tournaments played/count).
# Saves the data into a CSV file named 'keshmat_ciruit.csv'

from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page()
    page.goto('https://circuit.keshmat.org/')
    title=page.title().split('-')[1].strip()

    csv_file=open('keshmat_ciruit.csv','w')
    csv_writer=csv.writer(csv_file)
    csv_writer.writerow([title])

    data=page.locator('h2.text-2xl.font-semibold.mb-4').inner_text()
    csv_writer.writerow([data])
    csv_writer.writerow(['Rank', 'Name', 'Points','Tournaments Played','Tournaments Counted'])

    players=page.locator('tbody tr')
    count1=players.count()
    for n in range(count1):
        lst=[]
        player=page.locator('tbody tr').nth(n)
        for nn in range(5):
            lst.append(player.locator('td').nth(nn).inner_text())
        csv_writer.writerow([lst[0],lst[1],lst[2],lst[3],lst[4]])
    browser.close()
