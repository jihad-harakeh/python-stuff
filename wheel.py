import json
import random
import time

class Player:

    def __init__(self,name):
        self.__name=name
        self.__money=0
        self.__prizes=[]

    def __str__(self):
        return f"{self.__name}"

    def spin_the_wheel(self):
        with open('prizes.txt') as file:
            lst=json.loads(file.read())
            dct=random.choice(lst)
            return dct

    def getmoney(self):
        return self.__money
    def getprizes(self):
        return self.__prizes

    def guess_or_pass(self):
        answer=input(f"\n{self}, you can guess a letter or the whole phrase or pass your turn: ").lower()
        return answer


    def add_money(self,answer,phrase,wheel):
        num=phrase.count(answer)
        amount=wheel['value']
        self.__money+=amount*num

    def add_prize(self,wheel):
        if wheel['prize']:
            self.__prizes.append(wheel['prize'])
            wheel['prize']=None

    def lose_money(self,buyorbankrupt='bankrupt'):
        if buyorbankrupt=='bankrupt':
            self.__money=0
        elif buyorbankrupt=='buy':
            self.__money-=250



def category_phrase():
    with open('categories&phrases.txt') as file:
        dct=json.loads(file.read())
        category=random.choice(list(dct.keys()))
        phrase=random.choice(dct[category])
        return (category,phrase.lower())

def display(phrase,right_guesses=''):
    punct='''!@#$%^&*()-=\|/?'",.:; '''
    blank=''
    for chr in phrase:
        if chr not in right_guesses and chr not in punct:
            blank+='_'+' '
        elif chr in right_guesses or chr in punct:
            blank+=chr + ' '
    return blank

def compare(phrase,right_guesses=''):
    punct='''!@#$%^&*()-=\|/?'",.:; '''
    blank=''
    for chr in phrase:
        if chr not in right_guesses and chr not in punct:
            blank+='_'
        elif chr in right_guesses or chr in punct:
            blank+=chr
    return blank

def check_wrong_right(letter,wrong_guesses,right_guesses):
    if letter in wrong_guesses:
        return "already_w"
    elif letter in right_guesses:
        return "already_r"

def check_vowels(player,answer,phrase,wheel,vowels='aeiou'):
    if answer in vowels and player.getmoney()<250:
        return 'answer in vowels & no enough money'
    elif answer in vowels and answer in phrase and player.getmoney()>=250:
            return 'answer in vowels & in phrase & enough money'
    elif answer in vowels and answer not in phrase and player.getmoney()>=250:
            return 'answer in vowels & enough money but not in phrase'
    else:
        return 'not in vowels'

def check_letter(player,answer,phrase,wheel,right_guesses,wrong_guesses):
    if answer in phrase:
        return 'answer in phrase'
    else:
        return 'answer not in phrase'

def spin_pass():
    action=input('Would you like to spin the wheel again or pass your turn? ').lower()
    if action=='pass':
        return 'pass'
    else:
        return 'spin'

def wheel_process():
    print('wheel spining')
    time.sleep(1)
    print('....')
    time.sleep(1)
    print('...')
    time.sleep(1)
    print('..')
    time.sleep(1)
    print('wheel landed on: ')


def cash(player,wheel):
    global right_guesses
    global wrong_guesses

    answer=player.guess_or_pass()
    if answer=='pass':
        print(f"{player}'s turn passed to the next player")
        return 'next player'
    elif answer==phrase:
        player.add_money(answer,phrase,wheel)
        player.add_prize(wheel)
        return 'won'
    elif len(answer)>1 and answer!=phrase:
        player.lose_money()
        return 'next player'
    else:
        first_step=check_wrong_right(answer,wrong_guesses,right_guesses)
        if first_step=='already_r':
            print("This letter has already been guessed; pick another letter.")
            return cash(player,wheel)
        elif first_step=='already_w':
            print("This letter has been picked before and it's not correct; pick another letter.")
            return cash(player,wheel)
        second_step=check_vowels(player,answer,phrase,wheel,vowels='aeiou')
        if second_step=='answer in vowels & no enough money':
            print(f"Sorry {player}, you don't have enough money to use a vowel")
            return cash(player,wheel)
        elif second_step=='answer in vowels & in phrase & enough money':
            player.lose_money('buy')
            right_guesses+=answer
            player.add_money(answer,phrase,wheel)
            player.add_prize(wheel)
            comp=compare(phrase,right_guesses)
            if comp==phrase:
                return 'won'
            print('\n')
            print(display(phrase,right_guesses),'\n')
            s_p=spin_pass()
            if s_p=='pass':
                return 'next player'
            elif s_p=='spin':
                print(f"{player}, you have ${player.getmoney()} and {player.getprizes()}")
                wheel=player.spin_the_wheel()
                wheel_process()
                if wheel['type']=='cash':
                    print('cash: ',wheel['text'])
                    if wheel['prize']:
                        print('prize: ',wheel['prize'])
                    return cash(player,wheel)
                elif wheel['type']=='loseturn':
                    print(wheel['type'])
                    print(f"sorry {player}, you lost your turn.")
                    return 'next player'
                elif wheel['type']=='bankrupt':
                    player.lose_money()
                    print(wheel['type'])
                    if player.getmoney()>0:
                        print(f"Sorry {player}, you lost all your money")
                    return 'next player'
        elif second_step=='answer in vowels & enough money but not in phrase':
            player.lose_money('buy')
            wrong_guesses+=answer
            print('wrong guess')
            return 'next player'
        third_step=check_letter(player,answer,phrase,wheel,right_guesses,wrong_guesses)
        if third_step=='answer in phrase':
            right_guesses+=answer
            player.add_money(answer,phrase,wheel)
            player.add_prize(wheel)
            comp=compare(phrase,right_guesses)
            if comp==phrase:
                return 'won'
            print('\n')
            print(display(phrase,right_guesses),'\n')
            s_p=spin_pass()
            if s_p=='pass':
                return 'next player'
            elif s_p=='spin':
                print(f"{player}, you have ${player.getmoney()} and {player.getprizes()}")
                wheel=player.spin_the_wheel()
                wheel_process()
                if wheel['type']=='cash':
                    print('cash: ',wheel['text'])
                    if wheel['prize']:
                        print('prize: ',wheel['prize'])
                    return cash(player,wheel)
                elif wheel['type']=='loseturn':
                    print(wheel['type'])
                    print(f"sorry {player}, you lost your turn.")
                    return 'next player'
                elif wheel['type']=='bankrupt':
                    player.lose_money()
                    print(wheel['type'])
                    if player.getmoney()>0:
                        print(f"Sorry {player}, you lost all your money")
                    return 'next player'
        elif third_step=='answer not in phrase':
            wrong_guesses+=answer
            print('wrong guess')
            return 'next player'



category_and_phrase=category_phrase()
category=category_and_phrase[0]
phrase=category_and_phrase[1]
Theguess=''
right_guesses=''
wrong_guesses=''
print('category: ',category)

p1=Player('Sarah')
p2=Player('John')
players=[p1,p2]
winners=[]
while Theguess!=phrase:
    for player in players:
        print('player: ',player)
        print(f"cash: ${player.getmoney()}")
        print(f"prizes: {player.getprizes()}")
        time.sleep(2)
        print('\n', display(phrase,right_guesses),'\n')
        wheel=player.spin_the_wheel()
        wheel_process()
        print('cash: ', wheel['text'])
        if wheel['prize']:
            print('prize: ', wheel['prize'])
        if wheel['type']=='cash':
            result=cash(player,wheel)
            if result=='won':
                Theguess=phrase
                print('\n',display(phrase,phrase),'\n')
                print(f"Congratulations {player}, you won.")
                print(f"You earned ${player.getmoney()}")
                if player.getprizes():
                    print(f"You also won some prizes: {player.getprizes()}")
                winners.append(player)
                for player in players:
                    player.lose_money()
                break
            elif result=='next player':
                print('\n')
                continue
        elif wheel['type']=='loseturn':
            print('\n')
            continue
        elif wheel['type']=='bankrupt':
            player.lose_money('bankrupt')
            print('\n')
            continue
