# Sketch
База устойчивых синтаксических связей между лексемами в НКРЯ

__
Работа сайта

https://sketchy-sketch.herokuapp.com/  тестовая страница проекта

Для работы с тестовыми словами введите "долететь"\"закаменеть"\"постыдиться". 
На странице "портрет" портрет представлены отсортированные связи слов. (Без применения словаря, в скором времени будет подключен)
На странице "метрики сочетаемости" представлены индексы pmi\t-score, произведена сортировка по pmi, выделены релевантные отношения.
Для последнего слова неактивна страница "метрики сочетаемости" в связи с избыточно строгим отбором связей (будет улучшаться).

__
Программная составляющая

Формирование корпусов биграммов и триграммов из распарсенного корпуса НКРЯ:
1. testbigra.py - биграммы => bigrams.json
2. extract_prep_trigrams_2json.py, trigrams_prep_full.py => trigrams.json

Результат на небольшом корпусе в 500 мб: https://yadi.sk/d/cl8TpRJr3GN5Sr

3. Sketch.py + 
(dictofallwords.txt - словарь всех обработанных слов с их индексами;
dictpartsspeech.txt - словарь всех слов с указанием на часть речи;
freqdict.json - распарсенный частотный словарь О.Н.Ляшевской
relationfreqdict.json - частота отношений по корпусу)
=> %number%.csv(релевантные отношения слова + pmi, t-score), %number%.txt(сгруппированные отношения слова связь-подсвязь)
