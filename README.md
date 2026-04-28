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

Przykład kodu napisanego w naszym języku znajduje się w pliku 'example.ls' i może on zostać wklejony bezpośrednio do okna w aplikacji.