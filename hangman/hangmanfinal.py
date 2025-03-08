import random
from words import wrds

def display_hangman(wrong_guesses):
    stages=[
    """
    -----------
    |          |
    |          O
    |
    |
    |
    """,
    """
    -----------
    |          |
    |          O
    |          |
    |          |
    |
    """,
    """
    -----------
    |          |
    |          O
    |         /|
    |          |
    |
    """,
    """
    -----------
    |          |
    |          O
    |         /|\\
    |          |
    |
    """,
    """
    -----------
    |          |
    |          O
    |         /|\\
    |          |
    |         /
    """,
    """
    -----------
    |          |
    |          O
    |         /|\\
    |          |
    |         / \\
    """
    ]
    return stages[wrong_guesses]

while True:
    the_word=random.choice(wrds)
    if ' ' in the_word or '-' in the_word:
            continue
    break

blank='_ '*len(the_word)

while True:
    players=input('choose how many players (1,2,3,4):  ')
    print('\n')
    try:
        plyrs=int(players)
    except:
        continue
    if plyrs<1 or plyrs>4:
        continue
    break

print(blank)

dct={}
for p in range(plyrs):
    dct['player'+' '+str(p+1)]=0

the_guess=''
while the_guess!=the_word and min(dct.values())<6:
    for plyr in dct:
        if the_guess==the_word:
            break
        if dct[plyr]<6:
            print('\n')
            print(plyr,',','wrong guesses:', dct[plyr])
            guess=input('guess a letter or guess the whole word:  ')
            if guess==the_word:
                the_guess=the_word
                print('Congrats')
                print('The word is', the_word)
                print(plyr,'wins!')
                break
            elif len(guess)>1 and guess!=the_word:
                print(plyr,'is out of the game')
                dct[plyr]=6
                print('\n')
                print(display_hangman(dct[plyr]-1))
                break
            elif guess!=the_word and guess not in the_word:
                dct[plyr]+=1
                print('\n')
                print(display_hangman(dct[plyr]-1))
                if dct[plyr]==6:
                    print(plyr,'is out of the gameee')
                continue
            while guess in the_word:
                for i,c in enumerate(the_word):
                    if guess==c:
                        blank=blank.split()
                        blank[i]=c
                        the_guess=''.join(blank)
                        blank=' '.join(blank)
                print(blank)
                if the_guess==the_word:
                    print('Congrats')
                    print('The word is', the_word)
                    print(plyr,'wins!')
                    break
                guess=input('guess a letter or guess the whole word:  \n')
                if guess==the_word:
                    the_guess=the_word
                    print('Congrats')
                    print('The word is', the_word)
                    print(plyr,'wins!')
                    break
                elif len(guess)>1 and guess!=the_word:
                    print(plyr,'is out of the game')
                    dct[plyr]=6
                    print('\n')
                    print(display_hangman(dct[plyr]-1))
                    break
                elif guess!=the_word and guess not in the_word:
                    dct[plyr]+=1
                    print('\n')
                    print(display_hangman(dct[plyr]-1))
                    if dct[plyr]==6:
                        print(plyr,'is out of the gameee')

if the_guess!=the_word:
    print('none of the players were able to guess the word')
    print('it was',the_word)
quit()
