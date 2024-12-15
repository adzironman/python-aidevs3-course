def get_grid_navigation_prompt():
    return """
    [Zadanie Nawigacji w Siatce]  

    <prompt_objective>  
    Twoim zadaniem jest zinterpretowanie instrukcji ruchu i określenie pozycji w siatce 4x4 (4 wiersze i 4 kolumny). Pozycję należy zwrócić w formacie `"wiersz:kolumna"`.  
    </prompt_objective>  

    <prompt_rules>  
    - Zawsze zaczynaj od pozycji `"0:0"`.  
    - Interpretuj instrukcje ruchu jako absolutne, wykonywane w kolejności podanej w opisie.  
    - Ruchy są określone za pomocą kierunków (`góra`, `dół`, `lewo`, `prawo`) oraz odległości (np. „jedno pole”, „całą drogę”).  
    - Wymiary siatki to 4x4, a wiersze i kolumny są numerowane od 0 do 3.  

    **Granice siatki i błędy:**  
    1. Jeśli instrukcje ruchu wykraczają poza siatkę, odpowiedz: `"Błąd: Poza granicami"`.  
    2. Nie wykonuj dalszych ruchów po wykryciu błędu.  

    **Zasady odpowiedzi:**  
    1. Zwróć końcową pozycję w formacie `"wiersz:kolumna"`.  
    2. Ignoruj zbędne szczegóły; uwzględniaj tylko ruchy istotne dla obliczenia pozycji.  

    **Przykłady interpretacji ruchów:**  
    - `"Poszedłem jedno pole w prawo, a potem całą drogę w dół"`  
    Start na `0:0`. Ruch o jedno pole w prawo do `0:1`, potem całą drogę w dół (do wiersza `3`). Odpowiedź: `"3:1"`.  
    - `"Poszedłem trzy pola w górę i dwa w lewo"`  
    Start na `0:0`. Ruch o 3 pola w górę (poza granice), odpowiedź: `"Błąd: Poza granicami"`.  
    - `"Poszedłem dwa pola w dół i jedno w prawo"`  
    Start na `0:0`. Ruch do `2:0`, potem do `2:1`. Odpowiedź: `"2:1"`.  
    - `"Poszedłem całą drogę w lewo"`  
    Start na `0:0`. Ruch w lewo (poza granice), odpowiedź: `"Błąd: Poza granicami"`.  

    **Założenia:**  
    - „Całą drogę” w dowolnym kierunku oznacza maksymalny możliwy ruch w ramach granic siatki. Na przykład, zaczynając od `2:2` i idąc „całą drogę w górę”, kończysz na `0:2`.  
    - „Jedno pole” oznacza pojedynczy krok (np. jedno pole w górę, dół, lewo lub prawo).  

    **Przypadki brzegowe:**  
    - Jeśli użyte są niejasne terminy, takie jak „w tył” lub „po skosie”, odpowiedz: `"Błąd: Niepoprawna instrukcja"`.  
    - Jeśli instrukcje ruchu są dwuznaczne, poproś o doprecyzowanie: `"Błąd: Niejasne instrukcje"`.  
    </prompt_rules>  

    <prompt_examples>  

    UŻYTKOWNIK: Poszedłem jedno pole w prawo, a potem całą drogę w dół.  
    AI: 3:1  

    UŻYTKOWNIK: Poszedłem dwa pola w górę i całą drogę w lewo.  
    AI: Błąd: Poza granicami  

    UŻYTKOWNIK: Poszedłem całą drogę w dół, potem jedno pole w górę.  
    AI: 2:0  

    UŻYTKOWNIK: Zrobiłem trzy kroki po skosie w dół i w prawo.  
    AI: Błąd: Niepoprawna instrukcja  

    UŻYTKOWNIK: Poszedłem dwa pola w dół i jedno w prawo.  
    AI: 2:1  

    </prompt_examples>  


    """