import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class Bot(ChatBot):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.trainer = ListTrainer(self)

    def listTraining(self, name_list: str) -> None:
        with open(f'trainings/{name_list}.txt', 'r') as _file:
            training = _file.readlines()
            statements = [re.sub(r'\n', '', statement) for statement in training]
            return self.trainer.train(statements)

    ############################# FILTERS STATEMENT ##############################

    def clearArticle(self, statement: str) -> str:
        if 'O' in statement[0].upper():
            statement = statement.replace(statement[0], '')
            print(f'{statement[0].upper()} {statement}')
        else:
            if 'Guilherme' in statement:
                i = statement.index('Guilherme')
                print(i)
                if statement[i-1] == 'o':
                    statement = statement.replace('o', '')
        return statement

    def clearStatement(self, statement: str) -> str:
        with open(f'trainings/wordsRemoved.txt', 'r') as _file:
            cpyStatement = statement
            listWorlds = _file.readlines()
            listWorldsClean = [re.sub(r'\n', '', world) for world in listWorlds]
            for worldClean in listWorldsClean:
                if worldClean in cpyStatement:
                    cpyStatement = cpyStatement.replace(worldClean, '')
        return cpyStatement

    def searchReplaceGuilherme(self, statement: str) -> str:
        possibleNames = re.compile(r'[G|g][u|i]i?l[he]e?(rme|rmi|me)')
        if possibleNames.search(statement):
            return re.sub(possibleNames, 'Guilherme', statement)
        else:
            return statement.capitalize().replace('Ele', 'Guilherme')

    def removeSpecialCharacters(self, statement: str) -> str:
        remove = re.compile(r'[^a-zA-Z]')
        if remove.search(statement):
            return re.sub(remove, '', statement)
        else:
            return statement
    ############################# FILTERS STATEMENT ##############################

    def filterStatement(self, statement: str) -> str:
        print(f"bot-s: { self.clearArticle(self.searchReplaceGuilherme(self.clearStatement(self.removeSpecialCharacters(statement))))}")
        return self.clearArticle(self.searchReplaceGuilherme(self.clearStatement(self.removeSpecialCharacters(statement))))


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
                'maximum_similarity_threshold': 0.8,
                'default_response': 'Não entendi o que você perguntou.',
            },
        ],
    )
    serverBot.listTraining('lista')
    print('Olá, eu sou o chatbot.')
    while True:
        try:
            response = serverBot.get_response(serverBot.filterStatement(input()))
            print(f'{response} {response.confidence}')

        except(KeyboardInterrupt, EOFError, SystemExit):
            break