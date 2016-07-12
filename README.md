Утилита для сравнения *epf*-, *erf*-, *ert*- и *md*-файлов
===

Что делает
---

Файлы разбираются с помощью пакета [decompiler1cwrapper](https://github.com/Cujoko/decompiler1cwrapper) в каталоги,
которые затем сравниваются указанной в аргументах командной строки утилитой сравнения. Поддерживаются KDiff3,
AraxisMerge, WinMerge, ExamDiff.

При установке пакета в папке скриптов каталога интерпретатора Python создаётся исполняемый файл *diff1c.exe*.

Требования
---

- Windows
- Python 3.5
- Пакет [decompiler1cwrapper](https://github.com/Cujoko/decompiler1cwrapper) с необходимыми настройками

Состав
---

- *diff1c.py* — собственно скрипт
- *diff1c.ini.sample* — образец файла с настройками
