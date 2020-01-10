from chatterbot import ChatBot
import os
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

bot = ChatBot('Candice')

bot.set_trainer(ListTrainer)

for files in os.listdir('./english/'):
    data = open('./english/' + files, 'r').readlines()
    bot.train(data)

while True:
    message = input('\t\t\tYou: ')
    message = message.lower()

    if message.strip() != 'bye':
        reply = bot.get_response(message)
        print('Candice: ', reply)

    else:
        print('Candice: Bye')
        break