
import requests
import json
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import getLogger

__author__ = 'thorstenmueller'

LOGGER = getLogger(__name__)

class SymconSkill(MycroftSkill):
    
    def __init__(self):
        super(SymconSkill, self).__init__(name="SymconSkill")
        self.host = self.config.get('host')
        self.port = self.config.get('port')
        self.user = self.config.get('user')
        self.password = self.config.get('password')

        self.url = "http://%s:%s@%s:%s/api/" % (self.user, self.password,self.host,self.port)

    @intent_handler(IntentBuilder("TemperatureIntent").require("TemperatureKeyword").
        optionally("Room"))
    def handle_temperature_intent(self, message):
        
        room = message.data.get("Room")
        temp = self.symApiReadValue('19920')
        self.speak_dialog("temperature",{'room':room,'degrees':temp})
        # Symcon Script mit mehreren Parametern aufrufen



    def symApiExec(self,Command,Params):
        LOGGER.info('Aufruf Symcon API: ' + Command + ' mit Parametern ' + Params)
        
        try:
            data = '{"jsonrpc":"2.0","id":"0","method":"' + Command + '","params": [' + Params + ']}'
            response = requests.post(self.url, data=data)

            # Check result = true {'id': '0', 'jsonrpc': '2.0', 'result': True}
            tmp = json.loads(response.text)
            if(tmp['result'] == True):
                LOGGER.info('Befehl konnte erfolgreich ausgefuehrt werden')
        except:
            LOGGER.error('Fehler bei der Ausfuehrung des Kommandos')
            LOGGER.error(response.text)

    def symApiReadValue(self, symVar):
        LOGGER.info('Frage Variablen-Wert (' + symVar + ') per Symcon API ab')

        try:
            data = '{"jsonrpc":"2.0","id":"0","method":"GetValue","params": [' + symVar + ']}'
            response = requests.post(self.url, data=data)
        
            # Check result = true {'id': '0', 'jsonrpc': '2.0', 'result': True}
            tmp = json.loads(response.text)
            if(tmp['result'] == True):
                LOGGER.info('Wert konnte erfolgreich abgefragt werden')
            return tmp['result']

        except:
            LOGGER.error('Fehler beim Abfragen des Werts der Variable')
            LOGGER.error(response.text)

    def stop(self):
        pass

def create_skill():
    return SymconSkill()
