Скрипт сортує папку вказану через командну строку. 
Для встановлення використати команду pip install -e . в папці з setup файлом. 
Має бути наступний результат https://prnt.sc/jFSSNdC0TqU6

Скріпт запускається через команду clean-folder [шлях до папки]

При першому проходженні створює файл results з результатами сканування: 
Список файлів у кожній категорії (музика, відео, фото та ін.)
Перелік усіх відомих скрипту розширень, які зустрічаються в цільовій папці.
Перелік всіх розширень, які скрипту невідомі.
Також кількіть файлів кожної категорії виведеться в консоль.(опціонально)

При повторному проходженні файл буде змінено відповідно до актуального стану папки, 
старий файл results переміститься в папку documents а новий з'явиться в цільовій папці.

Відрізнятись файли results першого і другого циклу будуть кількістю архівів, 
бо при другому проходжені їх вже не буде :)
