import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

validaGuilherme = re.compile(r'(G|g)(u|i)i?l[he]e?(rme|rmi|me)')
bot = ChatBot(
    'Norman',
    torage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.convert_to_ascii',
    ],

)
trainer = ListTrainer(bot)

def list_training(name_list):
    with open(f'treinos/{name_list}.txt', 'r') as file:
        training = file.readlines()
        tiraBarraN = [tira.replace('\n', '') for tira in training]
        return tiraBarraN
trainer.train(list_training('lista'))

# while True:
#     try:
#         bot_input = bot.get_response(input())
#         print(bot_input)
#
#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break
