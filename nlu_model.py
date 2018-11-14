from neo_nlu.training_data import load_data
from neo_nlu import config
from neo_nlu.model import Trainer
from neo_nlu.model import Metadata, Interpreter
import json

def train_nlu(data, configs, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(configs))
    trainer.train(training_data)
    model_directory = trainer.persist(model_dir, fixed_model_name='EVNHANOI')

def run_nlu():
    interpreter = Interpreter.load('./models/nlu/default/EVNHANOI')
    message = u"pd1200T000000"
    result = interpreter.parse(message)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    train_nlu('./data/dataEVN.json', 'config_spacy.json', './models/nlu')
    run_nlu()
