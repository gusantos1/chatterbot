from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Oi')

lista = [
    'testando',
    'flamengo'
]

trainer = ListTrainer(bot)

print(trainer.train(lista))