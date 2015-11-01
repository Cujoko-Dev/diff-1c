Утилита для сравнения *epf*-, *erf*-, *ert*- и *md*-файлов
===

Что делает
---

*epf*- и *erf*-файлы разбираются с помощью [v8Reader](https://github.com/xDrivenDevelopment/v8Reader), а *ert*- и 
*md*-файлы — с помощью [GComp](http://1c.alterplast.ru/gcomp/) в каталоги, которые сравниваются внешней программой. 
Поддерживаются KDiff3, AraxisMerge, WinMerge, ExamDiff.

Пути к платформе 1С:Предприятие 8, сервисной информационной базе, *V8Reader.epf* и GComp указывается в файле настроек 
*diff-1c.ini*, который сначала ищется в рабочем каталоге, а потом в каталоге со скриптом.

Требования
---

- Windows
- Python 3.5
- Пакет [decompiler1cwrapper](https://github.com/Cujoko/decompiler1cwrapper) с необходимыми настройками

Состав
---

- *diff1c.py* — собственно скрипт
- *diff1c.ini.sample* — образец файла с настройками
