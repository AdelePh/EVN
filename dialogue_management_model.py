from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import neo_dlg
from neo_dlg.agent import Agent
from neo_dlg.policies.fallback import FallbackPolicy
from neo_dlg.policies.keras_policy import KerasPolicy
from neo_dlg.policies.memoization import MemoizationPolicy
from neo_dlg.tracker_store import TrackerStore, RedisTrackerStore
from neo_dlg.domain import TemplateDomain, Domain, check_domain_sanity
from neo_dlg.interpreter import NeoNLUInterpreter
from neo_dlg.utils import EndpointConfig
from neo_dlg.run import serve_application

logger = logging.getLogger(__name__)

fallback = FallbackPolicy(fallback_action_name="utter_unclear",
                          core_threshold=0.2,
                          nlu_threshold=0.6)

def train_dialogue(domain_file='EVN_domain.yml',
                   model_path='./models/dialogue',
                   training_data_file='./data/core'):
    external_tracker_store = RedisTrackerStore(domain_file, host='10.252.10.83', port=6379, db=0, password='ai123456',
                                               record_exp=60)
    agent = Agent(domain_file, policies =[fallback,MemoizationPolicy(max_history=6), KerasPolicy()],
                  tracker_store=external_tracker_store)
    data = agent.load_data(training_data_file)
    #data = agent.load_data(training_data_file, augmentation_factor=0)
    agent.train(
        data,
        epochs=15,
        batch_size=50,
        validation_split=0.2)

    agent.persist(model_path)
    return agent

def run_EVN_bot(serve_forever=True):
    interpreter = NeoNLUInterpreter('./models/nlu/default/EVNHANOI')
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    domain_file = 'EVN_domain.yml'
    external_tracker_store = RedisTrackerStore(domain_file, host='10.252.10.83', port=6379, db=0, password='ai123456',
                                               record_exp=60)
    agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint,
                       tracker_store=external_tracker_store)
    neo_dlg.run.serve_application(agent, channel='cmdline')

    return agent

if __name__ == '__main__':
    train_dialogue()
    run_EVN_bot()