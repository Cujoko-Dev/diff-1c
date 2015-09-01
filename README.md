### Утилита для сравнения epf-, erf-, md- и ert-файлов

epf- и erf-файлы разбираются с помощью [V8Reader](https://github.com/xDrivenDevelopment/v8Reader), а md- и 
ert-файлы — с помощью [GComp](http://1c.alterplast.ru/gcomp/) в каталоги, которые сравниваются внешней программой.  
Поддерживаются KDiff3, AraxisMerge, WinMerge, ExamDiff.

Пути к платформе 1С:Предприятия 8, сервисной информационной базе, V8Reader.epf и GComp указывается в файле настроек 
diff-1c.ini, который сначала ищется в рабочем каталоге, а потом в каталоге со скриптом.

Требуется Python 3.4.