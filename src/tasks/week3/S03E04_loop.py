
from enum import Enum
import json
from pprint import pprint
import os

import httpx
from openai import OpenAI
from src.tasks.base_task import BaseTask

class QueryType(str, Enum):
    people = "people"
    places = "places"

class Lopp(BaseTask):
    def __init__(self):
        super().__init__("loop")


    notatka = f"""
        Podczas pobytu w Krakowie w 2019 roku, Barbara Zawadzka poznała swojego ówczesnego narzeczonego, a obecnie męża, Aleksandra Ragowskiego. Tam też poznali osobę prawdopodobnie powiązaną z ruchem oporu, której dane nie są nam znane. Istnieje podejrzenie, że już wtedy pracowali oni nad planami ograniczenia rozwoju sztucznej inteligencji, tłumacząc to względami bezpieczeństwa. Tajemniczy osobnik zajmował się także organizacją spotkań mających na celu podnoszenie wiedzy na temat wykorzystania sztucznej inteligencji przez programistów. Na spotkania te uczęszczała także Barbara.

        W okolicach 2021 roku Ragowski udał się do Warszawy celem spotkania z profesorem Andrzejem Majem. Prawdopodobnie nie zabrał ze sobą żony, a cel ich spotkania nie jest do końca jasny.

        Podczas pobytu w Warszawie, w instytucie profesora doszło do incydentu, w wyniku którego, jeden z laborantów - Rafał Bomba - zaginął. Niepotwierdzone źródła informacji podają jednak, że Rafał spędził około 2 lata, wynajmując pokój w pewnym hotelu. Dlaczego zniknął?  Przed kim się ukrywał? Z kim kontaktował się przez ten czas i dlaczego ujawnił się po tym czasie? Na te pytania nie znamy odpowiedzi, ale agenci starają się uzupełnić brakujące informacje.

        Istnieje podejrzenie, że Rafał mógł być powiązany z ruchem oporu. Prawdopodobnie przekazał on notatki profesora Maja w ręce Ragowskiego, a ten po powrocie do Krakowa mógł przekazać je swojej żonie. Z tego powodu uwaga naszej jednostki skupia się na odnalezieniu Barbary.

        Aktualne miejsce pobytu Barbary Zawadzkiej nie jest znane. Przypuszczamy jednak, że nie opuściła ona kraju.
        """

    instrukcja = f"""
        Co należy zrobić w zadaniu?
        Ściągnij notatkę (plik TXT) na temat Barbary.
        Zastanów się jakie osoby i jakie nazwy miast są wspomniane w notatce
        Odpytaj o wspomniane poszlaki odpowiednie API
        Istnieje szansa, że z danych otrzymanych przez API otrzymasz kolejne imiona lub nazwy miast
        Odpytuj o nie kolejno tak długo, aż znajdziesz miasto, w którym znajduje się BARBARA
        Istnieje szansa, że idąc jakąś pokrętną drogą natrafisz na sekretną flagę.
        Gdy namierzysz miasto, w którym znajduje się BARBARA, wyślij nazwę miasta do centrali (/report) do zadania loop. Nazwa miasta ma być w tym samym formacie jak została zwrócona z API czyli np. LODZ. Wysyłka nazwy Łódź nie zostanie zaliczona. 
        Podpowiedź: tego zadania nie da się rozwiązać z użyciem, zaledwie jednego prompta. Wymagane jest pewne zapętlenie zapytań, ale uważaj, aby nie zapętlić się w nieskończoność. Pamiętaj, że API odpytujemy słowami w mianowniku i bez polskich znaków (SLASK, a nie ŚLĄSKIEGO i GRZESIEK, a nie GRZEŚKOWI).
        """


    def query_db(qry_type, qry: str):
        """Send prompt to ApiDb"""
        if qry_type == QueryType.people:
            url = f"{os.environ.get("CENTRALA_BASE_URL")}/people"
        elif qry_type == QueryType.places:
            url = f"{os.environ.get("CENTRALA_BASE_URL")}/places"
        else:
            raise ValueError("Invalid query type")
        data = {
            "apikey": os.environ.get("POLIGON_API_KEY"),
            "query": qry
        }
        response = httpx.post(url, data=json.dumps(data))
        return response.json()
    
    tools = [
        {
        "type": "function",
        "function": {
            "name": "query_db",
            "description": "Zapytaj bazę danych o osobę lub miejsce",
            "parameters": {
                "type": "object",
                "properties": {
                    "qry_type": {
                        "type": "string",
                        "description": "Typ zapytania (people/places)",
                    },
                    "qry": {
                        "type": "string",
                        "description": "Zapytanie (jedno słowo dużymi literami bez polskich znaków)"
                    }
                },
                "required": ["qry_type", "qry"],
                    "additionalProperties": False
                }
            }
        }
    ]

    system_prompt = f"""
        Twoim zadaniem jest wskazanie prawdopodobnego miejsca pobytu osoby (BARBARA).

        Do dyspozycji masz:

        1. Notatkę z informacjami na temat różnych osób i miast.
        2. Możliwość zapytania bazy danych o osoby i miejsca (tool query_db).
        3. Instrukcję zadania zawierającą wskazówki.

        <INSTRUKCJA>
        {instrukcja}
        </INSTRUKCJA>

        <NOTATKA>
        {notatka}
        </NOTATKA>

        Korzystając z powyższych informacji, odpytaj bazę danych o osoby i miejsca, aby znaleźć miejsce pobytu BARBARY.
        Pamiętaj, żeby zwracać uwagę na odpowiedzi API, ponieważ mogą zawierać dodatkowe informacje, które pomogą Ci w odnalezieniu celu.
        Historia dotychczasowych zapytań i odpowiedzi zostanie przekazana w wiadomościach systemowych.

        Zwróć wiadomość GOTOWE gdy uznasz, że znalazłeś miejsce pobytu BARBARY.
        """

    messages = [
    {
        "role": "system",
        "content": system_prompt,
    },
    {
        "role": "system",
        "content": f"<HISTORY></HISTORY>"
        }
    ]

    llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = llm.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )
    
    def handle_tool_choice(self, completion):
        calls = None
        for choice in completion.choices:
            if choice.finish_reason == "tool_calls":
                calls = choice.message.tool_calls # list of tool calls {id, function{arguments}, name}
        return calls or []

    def agent_step(self, history):
        if history is None:
            history = []

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
        },
        {
            "role": "system",
                "content": f"<HISTORY>{json.dumps(history)}</HISTORY>"
            }
        ]

        response = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=self.tools
        )
        calls = self.handle_tool_choice(response)
        if calls:
            print(calls)
        else:
            print("NO CALLS IN THIS STEP")
            return

        call_map = [
            {
                "call_id": call_.id,
                "call_kwargs": json.loads(call_.function.arguments),
                "call_result": self.query_db(**json.loads(call_.function.arguments))
            }
            for call_ in calls
        ]

        places_queried = []
        people_queried = []

        history.append({"history_step_num": len(history), "calls": call_map})
        return history

    def process(self):
        history = None
        for i in range(25):
            history = self.agent_step(history)
            pprint(history[-1])
