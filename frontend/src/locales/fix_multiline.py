#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Fixa de sista multi-line strängarna
multiline_translations = {
    "Only important emails, which are directly related to this event, should be sent using this form.\nAny misuse, including sending promotional emails, will lead to an immediate account ban.": "Endast viktiga e-postmeddelanden som är direkt relaterade till detta event bör skickas med detta formulär.\nAll missbruk, inklusive att skicka reklame-post, kommer att leda till omedelbar kontosuspensjon.",
    "Provide additional context or instructions for this question. Use this field to add terms\nand conditions, guidelines, or any important information that attendees need to know before answering.": "Ge ytterligare sammanhang eller instruktioner för denna fråga. Använd detta fält för att lägga till villkor\noch regler, riktlinjer eller viktig information som deltagare behöver veta innan de svarar."
}

def fix_sv_po():
    # Läs filen
    with open('sv.po', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ersätt de specifika multi-line strängarna
    for original, translation in multiline_translations.items():
        content = content.replace(f'msgid ""\n"{original.split(chr(10))[0]}\\n"\n"{original.split(chr(10))[1]}"\nmsgstr ""', 
                                f'msgid ""\n"{original.split(chr(10))[0]}\\n"\n"{original.split(chr(10))[1]}"\nmsgstr ""\n"{translation.split(chr(10))[0]}\\n"\n"{translation.split(chr(10))[1]}"')
    
    # Skriv tillbaka
    with open('sv.po', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Multi-line strängar fixade!")

if __name__ == "__main__":
    fix_sv_po()
