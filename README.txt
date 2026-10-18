# Email Sender

Desktopová aplikace pro odesílání upozorňovacích e-mailů o blížícím se vypršení podepisovacích certifikátů.

Aplikace načítá data z Excelu, umožňuje rychlé vyhledávání osob a automaticky generuje a odesílá HTML e-maily s nastavitelnou úrovní důležitosti.

---

## Funkce

Načítání a filtrování dat z Excelu (certifikáty typu Q-TW-CZ)
Live search s autocomplete (vyhledávání podle jména, příjmení nebo loginu)
Dynamické generování HTML e-mailů
Nastavitelná úroveň důležitosti e-mailu (nízká / střední / vysoká)
Náhled e-mailu před odesláním
Odesílání přes SMTP včetně inline obrázku (logo v podpisu)
Konfigurace přes `config.ini` (není potřeba znovu kompilovat)
Logging

Technologie

Python
Tkinter – GUI
Pandas + openpyxl – práce s Excel soubory
smtplib + email.mime – odesílání HTML e-mailů
configparser – konfigurace
logging

## Spuštění

### Pro koncové uživatele (doporučeno)
Stačí spustit:

```bash
main.exe

## Sruktura projektu
Email_sender/
├── app.py                  # Vstupní bod aplikace
├── config.ini              # Konfigurace
├── constants.py
├── core/                   # Inicializace, stav aplikace, utility
├── gui/                    # Tkinter okna a komponenty
├── Service/                # Business logika (e-mail, Excel, podpis)
├── infra/                  # SMTP odesílání
├── static/img/             # Logo pro podpis
└── tests/