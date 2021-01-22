# Esercizio sull'algoritmo di ricerca locale Simulated Annealing
Questa repository contiene l'elaborato richiesto per l'esame del corso di Intelligenza Artificiale nella Facolta' di Ingegneria Informatica.

L'esercizio richiesto e' l'implementazione dell'algoritmo di ricerca locale _simulated annealing_ e l'applicazione ai problemi delle _n_-regine, del quadrato magico e del commesso viaggiatore.

Il linguaggio di programmazione scelto e' Python, versione 3.9.1 (testato anche con versione 3.6.2). Non e' stato fatto uso di librerie esterne.

Oltre al branch `master`, questa repository contiene un altro branch, `copyless`, che sfrutta la reversibilita' delle azioni per velocizzare la ricerca (che, essendo possibile solo in determinati casi come i problemi trattati, ho preferito non utilizzare nel branch principale, che contiene invece una versione dell'algoritmo applicabile in generale).

## Installazione
Per scaricare l'esercizio utilizzando `git` basta' scrivere:
```
git clone https://github.com/a-rium/esercizio-ia
```

Per passare al branch `copyless` usare il comando:
```
git checkout copyless
```
Viceversa, per tornare al branch principale scrivere:
```
git checkout master
```

## Struttura dell'elaborato
Il programma e' composto da un'interfaccia utente (`launch_ui.py`) e da 4 moduli:
- `search.py`: contiene l'implementazione dell'algoritmo di ricerca
- `queens.py`: contiene il codice relativo al problema delle _n_-regine
- `magic.py`: contiene il codice relativo al problema delle quadrato magico
- `queens.py`: contiene il codice relativo al problema del commesso viaggiatore

All'interno della cartella `data` sono contenuti i file .graph con le coordinate dei vertici delle instanze dei problemi del commesso viaggiatore.

## Come provare l'algoritmo
Per applicare l'algoritmo su uno dei problemi, lanciare l'interfaccia utente (a linea di comando) con il comando
```
python3 launch_ui.py
```
Tale interfaccia richiedera' di inserire il tipo di problema da risolvere (es. _n_-regine), i dettagli sulla particolare istanza (es. specificare _n_), quale _schedule_ (es. logaritmica) da utilizzare insieme ai relativi parametri, ed infine il numero massimo di iterazioni ammesso.

Nell'inserimento dei parametri della _schedule_ sara' possibile selezionare dei valori di default (usati per scrivere le considerazioni viste nella relazione) premendo semplicemente `<ENTER>` senza scrivere nulla.

L'esecuzione dell'interfaccia utente o della ricerca puo' essere fermata attraverso la combinazione di tasti `CTRL-C`.
