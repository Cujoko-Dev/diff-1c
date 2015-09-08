Утилита для сравнения *epf*-, *erf*-, *md*- и *ert*-файлов
===

Что делает
---

*epf*- и *erf*-файлы разбираются с помощью [v8Reader](https://github.com/xDrivenDevelopment/v8Reader), а *md*- и 
*ert*-файлы — с помощью [GComp](http://1c.alterplast.ru/gcomp/) в каталоги, которые сравниваются внешней программой. 
Поддерживаются KDiff3, AraxisMerge, WinMerge, ExamDiff.

Пути к платформе 1С:Предприятия 8, сервисной информационной базе, *V8Reader.epf* и GComp указывается в файле настроек 
*diff-1c.ini*, который сначала ищется в рабочем каталоге, а потом в каталоге со скриптом.

Требования
---

- Python 3.4.
- Платформа 1С:Предприятия 8.3
- Сервисная информационная база
- [v8Reader](https://github.com/xDrivenDevelopment/v8Reader) и в частности *V8Reader.epf*
- [GComp](http://1c.alterplast.ru/gcomp/)

Состав
---

- *diff-1c.py* — собственно скрипт
- *diff-1c.ini.sample* — образец файла с настройками