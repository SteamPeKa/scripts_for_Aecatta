# scripts_for_Aecatta

A collection of python tricks for Aecatta

## kpolyakov_parsing

Пакет для упрощения доступа к ответам через форму на https://kpolyakov.spb.ru/school/ege.htm

Пакет использует недокументированную ручку HTTP API https://kpolyakov.spb.ru/school/ege/getanswer.php

Чтобы воспользоваться пакетом

1. Скачайте содержимое папки kpolyakov_parsing (из корне репозитория)
2. Перейдите в терминале в каталог, куда было помещено скачанное содержимое
3. Выполните
    ```bash
    python setup.py install
    ```
4. Теперь из терминала доступна следующий синтаксис
    ```bash
    python -m kpolyakov_parsing -i tests\test_data.txt -o test_output.txt
    ```
   Данная последовательность комманд собирает ответы для заданий, указанных в файле tests\test_data.txt и складывает их
   в виде текста в файл test_output.txt
