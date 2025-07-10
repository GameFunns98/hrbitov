
# Správa hřbitovů

Tato aplikace umožňuje evidenci hřbitovů, hrobů, zesnulých, nájemců, smluv a nově také pracovních zakázek. Je psaná ve Flasku a používá SQLite databázi uloženou v adresáři `instance`.
V navigaci najdete odkazy na přehledy i přidávání jednotlivých entit a možnost jejich úprav či mazání.

## Spuštění

1. Vytvořte a aktivujte virtuální prostředí
2. Nainstalujte závislosti `pip install -r requirements.txt`
3. Spusťte aplikaci `python run.py`

Při prvním spuštění se automaticky vytvoří databáze i testovací data.

## Požadavky

- Python 3.10+
- balíčky uvedené v `requirements.txt`

Aplikace nevyžaduje přihlášení a je vhodná pro malé obce.
