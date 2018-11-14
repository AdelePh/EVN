from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
import json
from neo_dlg.agent import Agent
from neo_dlg.policies.keras_policy import KerasPolicy
from neo_dlg.policies.memoization import MemoizationPolicy
from neo_dlg.policies.fallback import FallbackPolicy
from neo_dlg.interpreter import NeoNLUInterpreter
from neo_dlg.tracker_store import TrackerStore, RedisTrackerStore
from neo_dlg.domain import TemplateDomain, Domain, check_domain_sanity
from neo_dlg.train import online
from neo_dlg.utils import EndpointConfig
import redis

logger = logging.getLogger(__name__)

fallback = FallbackPolicy(fallback_action_name="utter_unclear",
                          core_threshold=0.2,
                          nlu_threshold=0.6)
def run_EVN_online(interpreter,
                          domain_file="EVN_domain.yml",
                          training_data_file='./data/core'):
                          #training_data_file='data/storiesEVN.md'):
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    external_tracker_store = RedisTrackerStore(domain_file, host='10.252.10.83', port=6379, db=0, password = 'ai123456',
                                               record_exp=60)
    agent = Agent(domain_file,
                  policies=[fallback,
                            MemoizationPolicy(max_history=6),
                            KerasPolicy()],
                  interpreter=interpreter,
                  action_endpoint=action_endpoint,tracker_store = external_tracker_store)

    data = agent.load_data(training_data_file)
    agent.train(data,
                       batch_size=50,
                       epochs=100,
                       max_training_samples=500)
    online.run_online_learning(agent)
    return agent

if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = NeoNLUInterpreter('./models/nlu/default/EVNHANOI')
    run_EVN_online(nlu_interpreter)