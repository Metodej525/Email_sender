EmailSender
==============
verze = 0.1.7

Aplikace slouží pro posílání emailů o upozornění vypršení podepisovacího certifikátu.
Email má přednastavený HTML template, kde se mění jen datumy ohledně vypršení cert.

Spusťte soubor:
main.exe
eventuelně traceback_main.exe pro zobrazení error logu v cmd

Není potřeba instalace.

Struktura
=========

main.exe
traceback_main.exe
config.ini
static/
img/
signature_email_logo.png

Konfigurace
===========

Aplikace používá soubor config.ini.
config.ini musí být v root složce jinak se aplikace nespustí

Úpravy
======

- config.ini lze upravovat v libovolném textovém editoru
- po úpravě není potřeba znovu kompilovat aplikaci