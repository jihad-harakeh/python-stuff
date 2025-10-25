# Chess.com article scraper: extracts title, author, date, excerpt, and link into a CSV.

from playwright.sync_api import sync_playwright
import csv
import time

with open('chessarticles.csv','w', newline='', encoding="utf-8") as csvfile:
    csv_writer=csv.writer(csvfile)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto('https://www.chess.com/articles')
        csv_writer.writerow([page.title()])
        csv_writer.writerow(['Title', 'Author', 'Date published', 'Excerpt', 'Link'])
        page_number=0

        while True:
            page_number+=1
            page.wait_for_selector('article.post-preview-component')
            page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(1.5)
            articles=page.query_selector_all('article.post-preview-component')
            if not articles:
                break
            for article in articles:
                title=article.query_selector('a.post-preview-title').inner_text() if article.query_selector('a.post-preview-title') else None
                author=article.query_selector('a.post-preview-meta-username').inner_text() if article.query_selector('a.post-preview-meta-username') else None
                date_published=article.query_selector('span time').inner_text() if article.query_selector('span time') else None
                excerpt=article.query_selector('p.post-preview-excerpt').inner_text() if article.query_selector('p.post-preview-excerpt') else None
                link=article.query_selector('a.post-preview-title').get_attribute('href')
                csv_writer.writerow([title, author, date_published, excerpt, link])
            print(f"Page {page_number}: {len(articles)} articles found")

            next_page=page.query_selector('a[aria-label="Next Page"]')
            if next_page:
                page.click('a[aria-label="Next Page"]')
            else:
                print(f"That's it, scraped {page_number} pages, no more pages left.")
                break
