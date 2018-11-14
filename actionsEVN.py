from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
import os
from rasa_core_sdk.events import AllSlotsReset
from rasa_core_sdk.events import Restarted
from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.action_request import RequestAcation

root = os.path.dirname(__file__);
EVNquery = RequestAcation(root=root, debug=True);

class ActionRestarted(Action):
    def name(self):
        return 'action_restarted'
    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

class ActionSlotReset(Action):
    def name(self):
        return 'action_slot_reset'
    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

class GetLICHGCS(Action):
    def name(self):
        #type: () -> Text
        return "action_get_lichgcs"

    def run(self, dispatcher, tracker, domain):
#        type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        #ma_mk = tracker.get_slot('ma_kh')
        #thang = tracker.get_slot('thang')
        #nam = tracker.get_slot('nam')
        ma_kh = 'PD1200T457089'
        thang = '10'
        nam = '2018'

        get_cus_info = EVNquery.request_soap('get_lichgcs', ma_kh=ma_kh, thang=thang, nam=nam)

        if get_cus_info != None :

            MA_KHANG = EVNquery.get_value(get_cus_info, 'MA_KHANG')
            TEN_KHANG = EVNquery.get_value(get_cus_info, 'TEN_KHANG')
            DCHI_HDON = EVNquery.get_value(get_cus_info, 'DCHI_HDON')
            MA_DVIQLY = EVNquery.get_value(get_cus_info, 'MA_DVIQLY')
            TEN_DVIQLY = EVNquery.get_value(get_cus_info, 'TEN_DVIQLY')
            response = """Thành công: Đăng nhập thành công. Quý khách cần hỗ trợ thông tin gì ạ? """
            dispatcher.utter_message(response)
        else:
            response = """Mã khách hàng hoặc mật khẩu không hợp lệ, vui lòng kiểm tra lại hoặc gọi tổng đài CSKH để được hỗ trợ"""
            dispatcher.utter_message(response)
        return []

class SP_LOGIN(Action):
    def name(self):
        #type: () -> Text
        return "action_sp_login"

    def run(self, dispatcher, tracker, domain):
#       type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        user = tracker.get_slot('ma_kh')
        passEVN = tracker.get_slot('ma_kh')
        get_cus_info = EVNquery.request_soap('SP_LOGIN', user=user, passEVN=passEVN)

        if get_cus_info != None :
            response = """Thành công: Đăng nhập thành công. Quý khách cần hỗ trợ thông tin gì ạ? """
            dispatcher.utter_message(response)
        else:
            response = """Mã khách hàng hoặc mật khẩu không hợp lệ, vui lòng kiểm tra lại hoặc gọi tổng đài CSKH để được hỗ trợ"""
            dispatcher.utter_message(response)
        return []
