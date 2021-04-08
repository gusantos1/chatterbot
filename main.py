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


    def removeSpecialCharacters(self, statement):
        remove = re.compile(r'[^a-zA-Z]')
        if remove.search(statement):
            return re.sub(remove, '', statement)
        else:
            return statement


    def filterStatement(self, statement):
        statementClean = self.removeSpecialCharacters(statement)
        return self.searchReplaceGuilherme(statementClean).lower()


if __name__ == '__main__':
    serverBot = Bot(
        name='ServerBot',
        read_only=False,
        preprocessors=[
                'chatterbot.preprocessors.clean_whitespace',
                'chatterbot.preprocessors.convert_to_ascii',
            ],
        logic_adapters=[
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'maximum_similarity_threshold': 0.95,
                'default_response': 'Não entendi o que você perguntou.',
            },
        ],
    )
    serverBot.listTraining('lista')
    print('Olá, eu sou o chatbot.')
    while True:
        try:
            clientStatement = serverBot.get_response(serverBot.filterStatement(input()))
            print(f'{clientStatement} {clientStatement.confidence}')
            print()

        except(KeyboardInterrupt, EOFError, SystemExit):
            break