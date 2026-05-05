# Instrukcja uruchomienia:

## libraries:
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt

## java path:
readlink -f $(which java) -- Przykładowo zwraca: /home/kamila/.local/lib/java/jdk-21.0.2/bin/java
export JAVA_HOME=/home/kamila/.local/lib/java/jdk-21.0.2 -- (bez /bin/java na końcu)

## run:
python3 src/main/python/main.py

# Przykład 

Przykład kodu napisanego w naszym języku znajduje się w plikach 'adder.ls', 'multiplexer.ls' oraz 'comparator.ls'.
Mogą one zostać wklejone bezpośrednio do okna w aplikacji.

# Jak napisać kod

W programie są zdefiniowane proste bramki: not, and, or, xor, nand, nor, xnor
a także nawiasy: (a and b) or (c xor d)

Można tworzyć zmienne za pomocą 'signal [id] = ...'
PRZYKŁAD:
{
    signal s = a and b
}

Komponenty zawierają wejścia oraz wyjścia. W kodzie komponentu można odnosić się do nich po ich nazwie.
Komponenty definuje się poprzez:
component [id](
    input [id]
    ...
    output [id]
    ...
) {
    ...
}
PRZYKŁAD:
{
    component half_adder(
        input a
        input b

        output sum
        output carry
    ) {
        sum = a xor b
        carry = a and b
    }
}

W powyższym przykładzie, zdefiniowane są dwa wyjścia 'output sum' oraz 'output carry'.
Aby wynik logiki pojawił się na danym wyjściu komponentu, trzeba mu przypisać wartość obliczeń:
{
    sum = a xor b                       # <--- TUTAJ
    carry = a and b                     # <--- TUTAJ
}

Stworzone komponenty można używać w innych komponentach. Wtedy trzeba stworzyć obiekt za pomocą 'component [id] = [id](...)'.
W nawiasach, do nazw wejść, trzeba przypisać wartości.
PRZYKŁAD:
{
    component full_adder(
        input a
        input b
        input cin

        output sum
        output cout
    ) {
        component ha1 = half_adder(     # <--- TUTAJ
            a = a
            b = b
        )

        component ha2 = half_adder(     # <--- TUTAJ
            a = ha1.sum
            b = cin
        )

        sum = ha2.sum
        cout = ha1.carry or ha2.carry
    }
}

Po stworzeniu obiektu, można odnosić się do jego wyjść za pomocą operatora '.' oraz nazwy wyjścia.
{
    component ha2 = half_adder(
            a = ha1.sum                 # <--- TUTAJ
            b = cin
        )

        sum = ha2.sum                   # <--- TUTAJ
        cout = ha1.carry or ha2.carry   # <--- TUTAJ
}


Każdy program musi zawierać 'main component [id](...){...}', to on jest sercem programu.