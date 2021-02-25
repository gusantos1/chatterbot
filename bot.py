from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

class CreateBot:
    def __init__(self, nome):
        #Created Bot
        self.bot = ChatBot(
            name=nome,
            read_only=False,
            preprocessors=
            [
                'chatterbot.preprocessors.clean_whitespace',
                'chatterbot.preprocessors.convert_to_ascii',
            ],
            logic_adapters=
            [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'Não entendi o que você está falando.',
                    'maximum_similarity_threshold': 0.90,
                },
            ]
        )
        # Created Trainer
        self.trainer = ListTrainer(self.bot)

    def list_training(self, name_list):
        with open(f'treinos/{name_list}.txt', 'r') as file:
            training = file.readlines()
            self.trainer.train(training)

if __name__ == '__main__':
    newbot = CreateBot('Zezinho')
    newbot.list_training('lista')
    while True:
        try:
            print('me: ', end='')
            me = input().lower()
            resp = newbot.bot.get_response(me)
            resp2 = newbot.bot.get_latest_response(me)
            print(f'bot get_response: {resp}  tx: {resp.confidence}')
            print(f'bot get_latest_response: {resp2}  tx: {resp.confidence}')

        except:
            pass