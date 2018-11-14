from neo_dlg.channels.slack import SlackInput
from neo_dlg.channels.facebook import FacebookInput
from neo_dlg.agent import Agent
from neo_dlg.interpreter import NeoNLUInterpreter
import yaml
from neo_dlg.utils import EndpointConfig

nlu_interpreter = NeoNLUInterpreter('./models/nlu/default/EVNHANOI')
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('./models/dialogue', interpreter = nlu_interpreter, action_endpoint = action_endpoint)

#input_channel = SlackInput('xoxb-440443779024-441295926787-pL3hOfwLYJgZQrxdrRwxLit2')
#agent.handle_channels([input_channel], 5004, serve_forever=True)

input_channel = FacebookInput(fb_verify="nguyentrinam",
                              fb_secret="d8a35080def455e8dee3xxxx",
                              fb_access_token="xxxjChm4hsRPPrIEXxbw41r8GrZCA7mz7TRCYTmOw9XClWn3L3R5Mt3M0jQtV50AlkCEHavhuQBmgGseGrWeaaHtnZCSO9gFANvZAEkvc34V1ZBXRB6pMx3w274Pmixx")
agent.handle_channels([input_channel], 5004, serve_forever=True)
