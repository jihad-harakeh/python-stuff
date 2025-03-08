import requests
import json

def author_name():
    book=input('enter the book name: ')
    if len(book)==0:
        return 'not a valid input'
    base_url='https://openlibrary.org/search.json'
    dct={'title': book}
    full_url=requests.get(base_url,params=dct)
    bk=full_url.json()
    if len(bk['docs'])==0:
        return 'book not found'
    bk1=bk['docs']
    bk2=bk1[0]
    return (bk2['author_name'][0],bk2['first_publish_year'])


print(author_name())
