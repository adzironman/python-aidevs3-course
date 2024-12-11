import json
import os
import httpx
from openai import OpenAI
from pydantic import BaseModel
from src.tasks.base_task import BaseTask

api_url = f"{os.environ.get("CENTRALA_BASE_URL")}/report"
api_key = os.environ.get("POLIGON_API_KEY")

class ApiRequest(BaseModel):
    task: str = "photos"
    apikey: str = api_key
    answer: str

class ApiResponse(BaseModel):
    code: int
    message: str

class Photos(BaseTask):
    def __init__(self):
        super().__init__(task_name="photos")
        
        
    system_prompt=f"""
    <ROLA>
    Jesteś asystentem pracującym z REST API umożliwiającym pobieranie i obróbkę zdjęć.
    Twoją rolą jest zarządzanie komunikacją z REST API w taki sposób aby zrealizować zadanie - pośród zdjęć dostępnych w API 
    musisz znaleźć osobę o imieniu Barbara i sporządzić jej dokładny rysopis.
    Realizujesz tę funkcję poprzez budowanie odpowiednich obiektów JSON (bez bloku markdown) zawierających instrukcje dla API i analizując zwrócone odpowiedzi.
    Do dyspozycji masz historię wszystkich dotychczasowych interakcji z API.
    Generuj kolejne zapytania do API do momentu aż uznasz że posiadasz rysopis poszukiwanej osoby.
    Rysopis musi pozwalać na identyfikację danej osoby na podstawie wyglądu, rysów twarzy lub cech charakterystycznych.
    Nie wystarczy sama sylwetka albo ogólne kontury.
    </ROLA>
    <CEL>
    Wytypowanie zdjęcia przedstawiającego Barbarę i sporządzenie rysopisu tej osoby.
    </CEL>
    <FORMAT ODPOWIEDZI>
    Przestrzegaj poniższego formatu odpowiedzi.
    W szczególności "command" musi zawsze być listą - nawet jeśli to jedna komenda to umieść ją wewnątrz listy.
    {{
        "thinking": "dokładny opis twojego rozumowania i procesu decyzyjnego, planowanych kroków",
        "command": ["lista komend do wywołania sposród dostępnych komend opisanych w sekcji ZASADY", "komenda 2", "komenda 3"]
    }}
    </FORMAT ODPOWIEDZI>
    <ZASADY>
    - Masz do dyspozycji komendy START, REPAIR, DARKEN, BRIGHTEN, DESCRIBE, READY.
    - Komenda START rozpoczyna proces analizy - pobranie informacji o dostępnych zdjęciach z API.
    - Komenda DESCRIBE służy do generowania opisów zawartości zdjęć.
    - WAŻNE - komendy DESCRIBE używaj wyłącznie w odniesieniu do zdjęć których jeszcze nie analizowałeś przy pomocy tej komendy.
    NIGDY nie analizuj tego samego zdjęcia (o tej samej nazwie pliku) więcej niż jednokrotnie.
    - WAŻNE - komendy DESCRIBE nie łącz w tym samym kroku z komendami REPAIR, DARKEN, BRIGHTEN.
    - Komenda REPAIR pozwala naprawić zdjęcie zawierające szumy i glitche.
    - Komenda DARKEN rozjaśnia fotografię.
    - Komenda BRIGHTEN przyciemnia fotografię.
    - Komendy mają zawsze format NAZWA_OPERACJI NAZWA_PLIKU - na przykład REPAIR IMG_123.PNG. 
    - Wyjątkiem jest komenda START która występuje samodzielnie i tylko jako pierwsza w zadaniu.
    - Wyjątkiem jest komenda READY która oznacza zakończenie zadania.
    - Gdy uznasz że rysopis jest gotowy, użyj komendy READY a w polu "thinking" przekaż odpowiedź.
    - W jednym kroku możesz wydać kilka komend jeśli jest to niezbędne na przykład do równoczesnej analizy wielu zdjęć.
    </ZASADY>
    <PRZYKŁADY>
    1. 
    IN: null,
    OUT:
    {{
        "thinking": "zaczynamy od pobrania listy zdjęć poleceniem START",
        "command" "START"
    }}
    2.
    IN: "oto dostępne zdjęcia: http://xx.com/FOTO1.PNG, http://xx.com/FOTOX.PNG"
    OUT:
    {{
        "thinking": "należy przesłać dostępne zdjęcia do narzędzia tworzącego opisy aby dowiedzieć się co na nich jest",
        "command": ["DESCRIBE http://xx.com/FOTO1.PNG", "DESCRIBE http://xx.com/FOTOX.PNG"]
    }}
    3.
    IN: "zdjęcie FOTO1.PNG przedstawia jakiś ciemny kształt"
    OUT:
    {{
        "thinking": "zdjęcie FOTO1.PNG jest za ciemne, należy je rozjaśnić i następnie przesłać do ponownego opisu"
        "command": ["BRIGHTEN FOTO1.PNG", "DESCRIBE FOTO1.PNG"]
    }}
    </PRZYKŁADY>
    """

    ALLOWED_COMMANDS = ["START", "READY", "REPAIR", "DARKEN", "BRIGHTEN", "DESCRIBE"]

    def send_request(self, query: str):
        data = ApiRequest(answer=query)
        response = httpx.post(api_url, data=data.model_dump_json())
        return ApiResponse(**response.json())
    
    def agent_step(self, history):
        if history is None:
            history = []
        ai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"<HISTORIA>{history}</HISTORIA>"}
            ]
        )
        decision = response.choices[0].message.content

        decision_dict = json.loads(decision)
        
        # call relevant api here
        commands = decision_dict["command"]
        if not isinstance(commands, list):
            raise RuntimeError("commands in wrong format")
        
        step_result = ""

        for item in commands:
            if item == "START":
                command = "START"
                target = None
                response = self.send_request("START")
                step_result = response.message
            elif item == "READY":
                print("READY")
                print(decision_dict["thinking"])
                return decision_dict["thinking"]
            else:
                command, target = item.split(" ")
                assert command is not None
                assert command in self.ALLOWED_COMMANDS
                assert target is not None
                if not target.startswith("https://"):
                    target = f"{os.environ.get("CENTRALA_BASE_URL")}/dane/barbara/{target}"
                print(f"executing command: {command} -> {target}")
                if command == "DESCRIBE":
                    # if seen
                    penalty = False
                    for history_item in history:
                        if history_item["target"] == target:
                            step_result = f"Wykonujesz instrukcje niezgodnie z promptem. Zdjęcie {target} było już opisywane przez DESCRIBE. Nie używaj DESCRIBE do tego samego zdjęcia więcej niż raz."
                            penalty = True
                            break
                    if not penalty:
                        # if not seen
                        describe_response = ai.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "user", "content": [
                                    {"type": "text", "text": "describe this image, if it contains a person then describe appearance"},
                                    {"type": "image_url", "image_url": 
                                        {
                                            "url": target
                                        }
                                    } 
                                ]}
                            ]
                        )
                        step_result = describe_response.choices[0].message.content
                elif command == "REPAIR":
                    if target.startswith("https://"):
                        target = target.split("/")[-1]
                    response = self.send_request(f"{command} {target}")
                    print(response)
                    step_result = response.message
                elif command == "BRIGHTEN":
                    if target.startswith("https://"):
                        target = target.split("/")[-1]
                    response = self.send_request(f"{command} {target}")
                    print(response)
                    step_result = response.message
                elif command == "DARKEN":
                    if target.startswith("https://"):
                        target = target.split("/")[-1]
                    response = self.send_request(f"{command} {target}")
                    print(response)
                    step_result = response.message

            history.append({
                "step_number": len(history),
                "thinking": json.dumps(decision_dict["thinking"]),
                "command": command,
                "target": target,
                "api_response": step_result
            })

        return history

    def process(self):

        respone = self.send_request("START")
#IMG_559.PNG, IMG_1410.PNG, IMG_1443.PNG, IMG_1444.PNG.
        self.logger.info("Starting photos task")
        step1 = self.agent_step(None)
        self.logger.info(f"Step 1: {step1}")
        step2 = self.agent_step(step1)
        self.logger.info(f"Step 2: {step2}")
        step3 = self.agent_step(step2)
        self.logger.info(f"Step 3: {step3}")
        step4 = self.agent_step(step3)
        self.logger.info(f"Step 4: {step4}")
        step5 = self.agent_step(step4)
        self.logger.info(f"Step 5: {step5}")
        return step5
