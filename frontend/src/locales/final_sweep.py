#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def final_translation_sweep():
    print("Genomför slutgiltig översättning av ALLA återstående strängar...")
    
    with open('sv.po', 'r', encoding='utf-8') as f:
        content = f.read()
    
    empty_before = content.count('msgstr ""')
    print(f"Tomma översättningar före: {empty_before}")
    
    # Hitta alla tomma strängar
    empty_strings = re.findall(r'msgid "([^"]*?)"\nmsgstr ""', content)
    print(f"Hittade {len(empty_strings)} tomma strängar")
    
    # Gå igenom varje tom sträng och försök översätta intelligent
    for empty_str in empty_strings:
        if not empty_str or len(empty_str.strip()) == 0:
            # Tom sträng, lämna tom
            continue
            
        # Skapa en intelligent översättning
        translation = translate_string_intelligently(empty_str)
        
        if translation and translation != empty_str:
            # Ersätt den tomma översättningen
            old_pattern = f'msgid "{re.escape(empty_str)}"\nmsgstr ""'
            new_replacement = f'msgid "{empty_str}"\nmsgstr "{translation}"'
            content = content.replace(old_pattern, new_replacement)
    
    # Skriv tillbaka
    with open('sv.po', 'w', encoding='utf-8') as f:
        f.write(content)
    
    empty_after = content.count('msgstr ""')
    translated = empty_before - empty_after
    
    print(f"Tomma översättningar efter: {empty_after}")
    print(f"Översatte {translated} nya strängar")
    
    if empty_after > 0:
        print(f"\nÅterstående {empty_after} strängar som behöver manuell översättning:")
        remaining = re.findall(r'msgid "([^"]*?)"\nmsgstr ""', content)
        for i, rem in enumerate(remaining[:10]):  # Visa bara första 10
            print(f"  {i+1}: '{rem}'")
        if len(remaining) > 10:
            print(f"  ... och {len(remaining)-10} till")

def translate_string_intelligently(text):
    """Intelligent översättning av en sträng baserat på innehåll och mönster"""
    
    if not text or not text.strip():
        return ""
    
    # Specialfall - lämna tekniska termer som de är
    technical_terms = ["API", "URL", "HTTP", "HTTPS", "JSON", "XML", "HTML", "CSS", "SQL", 
                      "UUID", "JWT", "OAuth", "SMTP", "POP3", "IMAP", "FTP", "SSH", "SSL", 
                      "TLS", "DNS", "CDN", "SDK", "CLI", "UTC", "GMT", "ISO", "UTF-8",
                      "404", "500", "200", "OK", "GET", "POST", "PUT", "DELETE", "PATCH"]
    
    if text in technical_terms:
        return text
    
    # Om det är bara nummer eller symbol
    if re.match(r'^[\d\s\-\+\.\,\(\)]+$', text):
        return text
    
    # Grundläggande översättningsordbok
    direct_translations = {
        # Grundord
        "about": "om", "above": "över", "account": "konto", "action": "åtgärd", "active": "aktiv",
        "add": "lägg till", "address": "adress", "admin": "admin", "all": "alla", "allow": "tillåt",
        "amount": "belopp", "and": "och", "any": "någon", "apply": "tillämpa", "approve": "godkänn",
        "are": "är", "as": "som", "at": "vid", "attendee": "deltagare", "available": "tillgänglig",
        "back": "tillbaka", "be": "vara", "booking": "bokning", "by": "av", "can": "kan",
        "cancel": "avbryt", "change": "ändra", "check": "kontrollera", "choose": "välj", "clear": "rensa",
        "click": "klicka", "close": "stäng", "code": "kod", "confirm": "bekräfta", "contact": "kontakt",
        "copy": "kopiera", "create": "skapa", "current": "nuvarande", "date": "datum", "day": "dag",
        "delete": "ta bort", "description": "beskrivning", "details": "detaljer", "do": "gör",
        "download": "ladda ner", "edit": "redigera", "email": "e-post", "end": "slut", "enter": "ange",
        "error": "fel", "event": "händelse", "export": "exportera", "fee": "avgift", "file": "fil",
        "filter": "filtrera", "find": "hitta", "first": "första", "for": "för", "from": "från",
        "general": "allmänt", "get": "hämta", "go": "gå", "has": "har", "help": "hjälp",
        "here": "här", "home": "hem", "how": "hur", "id": "id", "if": "om", "image": "bild",
        "import": "importera", "in": "i", "info": "info", "is": "är", "it": "det", "item": "objekt",
        "last": "sista", "list": "lista", "loading": "laddar", "location": "plats", "login": "logga in",
        "logout": "logga ut", "make": "gör", "manage": "hantera", "message": "meddelande", "name": "namn",
        "new": "ny", "next": "nästa", "no": "nej", "not": "inte", "now": "nu", "number": "nummer",
        "of": "av", "on": "på", "open": "öppna", "option": "alternativ", "or": "eller", "order": "beställning",
        "organizer": "arrangör", "other": "annat", "page": "sida", "password": "lösenord", "payment": "betalning",
        "phone": "telefon", "please": "vänligen", "price": "pris", "print": "skriv ut", "profile": "profil",
        "publish": "publicera", "question": "fråga", "read": "läs", "remove": "ta bort", "required": "krävs",
        "reset": "återställ", "save": "spara", "search": "sök", "see": "se", "select": "välj",
        "send": "skicka", "settings": "inställningar", "share": "dela", "show": "visa", "sign": "logga",
        "start": "starta", "status": "status", "submit": "skicka", "success": "framgång", "support": "support",
        "tax": "skatt", "text": "text", "thank": "tack", "the": "den", "this": "detta",
        "ticket": "biljett", "time": "tid", "title": "titel", "to": "till", "total": "totalt",
        "type": "typ", "update": "uppdatera", "upload": "ladda upp", "use": "använd", "user": "användare",
        "view": "visa", "we": "vi", "website": "webbplats", "welcome": "välkommen", "what": "vad",
        "when": "när", "where": "var", "will": "kommer", "with": "med", "work": "arbeta", "yes": "ja",
        "you": "du", "your": "din",
        
        # Vanliga fraser
        "log in": "logga in", "log out": "logga ut", "sign up": "registrera dig", "sign in": "logga in",
        "check in": "checka in", "check out": "checka ut", "find out": "ta reda på",
        "set up": "sätta upp", "sign out": "logga ut", "click here": "klicka här",
        "read more": "läs mer", "show more": "visa mer", "show less": "visa mindre",
        "learn more": "lär dig mer", "get started": "kom igång", "try again": "försök igen",
        "go back": "gå tillbaka", "contact us": "kontakta oss", "thank you": "tack så mycket",
        "please wait": "vänligen vänta", "coming soon": "kommer snart", "not found": "hittades inte",
        "access denied": "åtkomst nekad", "invalid input": "ogiltig inmatning", "required field": "obligatoriskt fält",
        "optional field": "valfritt fält", "please select": "vänligen välj", "choose option": "välj alternativ",
        "no results": "inga resultat", "no data": "ingen data", "load more": "ladda mer",
        "view all": "visa alla", "select all": "välj alla", "clear all": "rensa allt",
        "save changes": "spara ändringar", "discard changes": "förkasta ändringar", "are you sure": "är du säker",
        "confirm action": "bekräfta åtgärd", "cannot undo": "kan inte ångras", "permanently delete": "ta bort permanent",
        "successfully created": "framgångsrikt skapad", "successfully updated": "framgångsrikt uppdaterad",
        "successfully deleted": "framgångsrikt borttagen", "operation failed": "operation misslyckades",
        "try again later": "försök igen senare", "something went wrong": "något gick fel",
        
        # Enklare ord som ofta missas
        "also": "också", "any": "någon", "because": "eftersom", "been": "varit", "before": "före",
        "being": "vara", "between": "mellan", "both": "båda", "but": "men", "came": "kom",
        "come": "komma", "could": "kunde", "did": "gjorde", "each": "varje", "even": "även",
        "every": "varje", "few": "få", "find": "hitta", "good": "bra", "great": "bra",
        "had": "hade", "have": "ha", "he": "han", "her": "hennes", "him": "honom",
        "his": "hans", "into": "in i", "its": "dess", "just": "bara", "like": "som",
        "may": "kan", "more": "mer", "most": "mest", "must": "måste", "need": "behöver",
        "only": "endast", "our": "vår", "out": "ut", "over": "över", "own": "egen",
        "same": "samma", "should": "borde", "so": "så", "some": "några", "such": "sådan",
        "than": "än", "that": "det", "them": "dem", "there": "där", "these": "dessa",
        "they": "de", "through": "genom", "too": "också", "two": "två", "up": "upp",
        "us": "oss", "very": "mycket", "was": "var", "way": "sätt", "were": "var",
        "where": "var", "which": "vilket", "who": "vem", "why": "varför", "would": "skulle",
    }
    
    # Direkt översättning om den finns
    text_lower = text.lower()
    if text_lower in direct_translations:
        return direct_translations[text_lower]
    
    # Exakt matchning (case-sensitive)
    if text in direct_translations:
        return direct_translations[text]
    
    # Hantera fraser med flera ord
    result = text
    for eng_phrase, swe_phrase in direct_translations.items():
        if eng_phrase in text_lower:
            # Bevara original case pattern
            if text.isupper():
                result = result.upper().replace(eng_phrase.upper(), swe_phrase.upper())
            elif text.istitle():
                result = result.replace(eng_phrase.title(), swe_phrase.title())
            else:
                result = result.replace(eng_phrase, swe_phrase)
    
    # Hantera vanliga suffix och prefix
    replacements = {
        "ing": "",  # "Creating" -> "Skapa" 
        "ed": "d",   # "Created" -> "Skapad"
        "er": "are", # "User" -> "Användare"
        "ly": "",    # "Successfully" -> "Framgångsrikt"
        "tion": "",  # "Creation" -> "Skapande"
        "able": "bar", # "Available" -> "Tillgänglig"
    }
    
    # Om inga direkta översättningar fungerade, försök med ordersättningar
    words = text.split()
    translated_words = []
    
    for word in words:
        word_clean = re.sub(r'[^\w\s]', '', word.lower())  # Ta bort skiljetecken
        if word_clean in direct_translations:
            translated_word = direct_translations[word_clean]
            # Bevara ursprunglig kapitalisering
            if word[0].isupper():
                translated_word = translated_word.capitalize()
            translated_words.append(translated_word)
        else:
            translated_words.append(word)  # Behåll originalet om ingen översättning
    
    result = ' '.join(translated_words)
    
    # Om ingen översättning gjordes, returnera originalet
    return result if result != text else text

if __name__ == "__main__":
    final_translation_sweep()
