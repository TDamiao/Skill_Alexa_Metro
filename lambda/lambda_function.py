import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

# Definindo a URL de status
STATUS_URL = "https://www.viamobilidade.com.br/"

# Mapeamento de status
statuses = {
    "green": "Operação Normal",
    "yellow": "Operação Parcial",
    "red": "Operação Interrompida"
}

# Função para buscar o status
def get_status():
    response = requests.get(STATUS_URL)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    lines = []

    for line in soup.select("li[class*='line-']"):
        name = line.select_one("span[title]").get("title") if line.select_one("span[title]") else None
        line_number = next((c.split('-')[1] for c in line.get("class", []) if c.startswith("line-")), None)
        reason = line.select_one("p").text if line.select_one("p") else None
        status_element = line.select_one(".status")
        status_description = status_element.text if status_element else None
        status_color = next((c for c in status_element.get("class", []) if c != "status"), None) if status_element else None
        status = statuses.get(status_color)

        lines.append({
            "name": name,
            "number": line_number,
            "reason": reason,
            "statusDescription": status_description,
            "status": status
        })

    raw_date = soup.select_one(".lines p strong").text if soup.select_one(".lines p strong") else None
    updated_at = datetime.strptime(raw_date, "%d/%m/%Y %H:%M:%S").isoformat() if raw_date else None

    return {
        "lines": lines,
        "updatedAt": updated_at
    }

# Classe para lidar com a intenção CheckStatusIntent
class CheckStatusIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "CheckStatusIntent"

    def handle(self, handler_input):
        status_data = get_status()
        if status_data["lines"]:
            speech_text = "Aqui está o status das linhas: "
            for line in status_data["lines"]:
                speech_text += f"A linha {line['name']} está com status de {line['status']}. "
                if line["reason"]:
                    speech_text += f"Motivo: {line['reason']}. "
            speech_text += f"Última atualização foi em {datetime.fromisoformat(status_data['updatedAt']).strftime('%d/%m/%Y %H:%M:%S')}."
        else:
            speech_text = "Não consegui encontrar o status das linhas no momento."

        return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response

# Classe para lidar com a intenção HelpIntent
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.type == "IntentRequest" and \
               handler_input.request_envelope.request.intent.name == "AMAZON.HelpIntent"

    def handle(self, handler_input):
        speech_text = "Você pode me perguntar sobre o status das linhas de transporte. Como posso ajudar?"
        return handler_input.response_builder.speak(speech_text).ask(speech_text).response

# Classe para lidar com a intenção Cancel/Stop
class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name in ["AMAZON.CancelIntent", "AMAZON.StopIntent"]

    def handle(self, handler_input):
        speech_text = "Até logo!"
        return handler_input.response_builder.speak(speech_text).response

# Classe para lidar com erros
class ErrorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        return handler_input.response_builder.speak("Desculpe, houve um erro. Tente novamente.").response

# Construir a skill
sb = SkillBuilder()
sb.add_request_handler(CheckStatusIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(ErrorHandler())

lambda_handler = sb.lambda_handler()
