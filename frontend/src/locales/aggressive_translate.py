#!/usr/bin/env python3
# -*- coding: utf-8 -*-

translations = {
    "- Click to Publish": "- Klicka för att publicera",
    "- Click to Unpublish": "- Klicka för att avpublicera",
    "{0} Active Webhooks": "{0} aktiva webhooks",
    "{0} logo": "{0} logotyp",
    "Access token generated successfully": "Åtkomsttoken genererad framgångsrikt",
    "Active": "Aktiv",
    "Add": "Lägg till",
    "All": "Alla",
    "Allow": "Tillåt",
    "Amount": "Belopp",
    "And": "Och",
    "Attendee": "Deltagare", 
    "Attendees": "Deltagare",
    "Back": "Tillbaka",
    "Cancel": "Avbryt",
    "Change": "Ändra",
    "Close": "Stäng",
    "Complete": "Slutför",
    "Confirm": "Bekräfta",
    "Create": "Skapa",
    "Created": "Skapad",
    "Delete": "Ta bort",
    "Description": "Beskrivning",
    "Details": "Detaljer",
    "Edit": "Redigera",
    "Email": "E-post",
    "End": "Slut",
    "Event": "Händelse",
    "Events": "Händelser",
    "Export": "Exportera",
    "Failed": "Misslyckades",
    "Fee": "Avgift",
    "Fees": "Avgifter",
    "Filter": "Filtrera",
    "Free": "Gratis",
    "From": "Från",
    "Help": "Hjälp",
    "Hide": "Dölj",
    "Image": "Bild",
    "Import": "Importera",
    "Location": "Plats",
    "Login": "Logga in",
    "Logout": "Logga ut",
    "Name": "Namn",
    "New": "Ny",
    "Next": "Nästa",
    "No": "Nej",
    "None": "Ingen",
    "Order": "Beställning",
    "Orders": "Beställningar",
    "Page": "Sida",
    "Password": "Lösenord",
    "Phone": "Telefon",
    "Price": "Pris",
    "Print": "Skriv ut",
    "Published": "Publicerad",
    "Quantity": "Antal",
    "Remove": "Ta bort",
    "Required": "Obligatorisk",
    "Reset": "Återställ",
    "Save": "Spara",
    "Search": "Sök",
    "Select": "Välj",
    "Send": "Skicka",
    "Settings": "Inställningar",
    "Show": "Visa",
    "Start": "Start",
    "Status": "Status",
    "Submit": "Skicka",
    "Success": "Framgång",
    "Tax": "Skatt",
    "Ticket": "Biljett",
    "Tickets": "Biljetter",
    "Time": "Tid",
    "Title": "Titel",
    "To": "Till",
    "Total": "Totalt",
    "Type": "Typ",
    "Update": "Uppdatera",
    "Upload": "Ladda upp",
    "User": "Användare",
    "Users": "Användare",
    "View": "Visa",
    "Website": "Webbplats",
    "Yes": "Ja",
    "Zone": "Zon"
}

import re

def fix_sv_translations():
    with open('sv.po', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Räkna antalet tomma översättningar före
    empty_before = content.count('msgstr ""')
    print(f"Antal tomma översättningar före: {empty_before}")
    
    # Översätt vanliga termer
    for english, swedish in translations.items():
        # Escape special regex characters
        escaped_english = re.escape(english)
        pattern = f'msgid "{escaped_english}"\nmsgstr ""'
        replacement = f'msgid "{english}"\nmsgstr "{swedish}"'
        content = re.sub(pattern, replacement, content)
    
    # Översätt några vanliga mönster
    patterns = [
        (r'msgid "([A-Z][a-z]+)"\nmsgstr ""', lambda m: f'msgid "{m.group(1)}"\nmsgstr "{translations.get(m.group(1), m.group(1).lower())}"'),
        (r'msgid "(\w+)s"\nmsgstr ""', lambda m: f'msgid "{m.group(1)}s"\nmsgstr "{translations.get(m.group(1) + "s", m.group(1) + "ar")}"'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # Särskilda fall
    special_cases = [
        ('msgid "404"\nmsgstr ""', 'msgid "404"\nmsgstr "404"'),
        ('msgid "OK"\nmsgstr ""', 'msgid "OK"\nmsgstr "OK"'),
        ('msgid "UTC"\nmsgstr ""', 'msgid "UTC"\nmsgstr "UTC"'),
        ('msgid "URL"\nmsgstr ""', 'msgid "URL"\nmsgstr "URL"'),
        ('msgid "API"\nmsgstr ""', 'msgid "API"\nmsgstr "API"'),
        ('msgid "ID"\nmsgstr ""', 'msgid "ID"\nmsgstr "ID"'),
        ('msgid "QR"\nmsgstr ""', 'msgid "QR"\nmsgstr "QR"'),
        ('msgid "PDF"\nmsgstr ""', 'msgid "PDF"\nmsgstr "PDF"'),
        ('msgid "CSV"\nmsgstr ""', 'msgid "CSV"\nmsgstr "CSV"'),
    ]
    
    for old, new in special_cases:
        content = content.replace(old, new)
    
    # Skriv tillbaka filen
    with open('sv.po', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Räkna antalet tomma översättningar efter
    empty_after = content.count('msgstr ""')
    translated = empty_before - empty_after
    
    print(f"Antal tomma översättningar efter: {empty_after}")
    print(f"Översatte {translated} nya strängar")

if __name__ == "__main__":
    fix_sv_translations()
