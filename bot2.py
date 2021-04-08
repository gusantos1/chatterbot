import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class Bot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.trainer = ListTrainer(self)

    def listTraining(self, name_list):
        with open(f'treinos/{name_list}.txt', 'r') as _file:
            training = _file.readlines()
            statements = [re.sub(r'\n', '', statement) for statement in training]
            return self.trainer.train(statements)

    def searchReplaceGuilherme(self, statement):
        possibleNames = re.compile(r'(G|g)(u|i)i?l[he]e?(rme|rmi|me)')
        if possibleNames.search(statement):
            return re.sub(possibleNames, 'Guilherme', statement)
        else:
            return statement

if __name__ == '__main__':
    serverBot = Bot(
        name='ServerBot',
        preprocessors=[
                'chatterbot.preprocessors.clean_whitespace',
                'chatterbot.preprocessors.convert_to_ascii',
            ],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': 'Não entendi o que você está falando.',
                'maximum_similarity_threshold': 0.8,
            },
        ],
    )
    serverBot.listTraining('lista')

    while True:
        try:
            clientStatement = serverBot.get_response(serverBot.searchReplaceGuilherme(input().capitalize()))
            print(clientStatement)

        except(KeyboardInterrupt, EOFError, SystemExit):
            break