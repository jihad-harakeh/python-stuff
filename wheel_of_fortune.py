import json

with open('prizes.txt', 'r') as file:
    file_contents = file.read()

try:
    prizes_list = json.loads(file_contents)
    print(prizes_list)  # Now prizes_list is a Python list
except json.JSONDecodeError as e:
    print("Invalid JSON format:", e)
