#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# Slutgiltiga översättningar för de sista 47 strängarna i Hi.Events
final_translations = {
    # Kvotade strängar 
    "'There\\'s nothing to show yet'": "'Det finns inget att visa än'",
    
    # Parametriserade strängar
    "A default {type} is automaticaly applied to all new products. You can override this on a per product basis.": "En standard {type} tillämpas automatiskt på alla nya produkter. Du kan åsidosätta detta per produkt.",
    "Add products": "Lägg till produkter",
    "Amount paid ({0})": "Betalt belopp ({0})",
    "Applies to {0} products": "Gäller {0} produkter",
    "Applies to 1 product": "Gäller 1 produkt",
    "Apply this {type} to all new products": "Tillämpa denna {type} på alla nya produkter",
    "Are you sure you would like to delete this Capacity Assignment?": "Är du säker på att du vill ta bort denna kapacitetstilldelning?",
    "Are you sure you would like to delete this Check-In List?": "Är du säker på att du vill ta bort denna incheckningslista?",
    "Cancel Order {0}": "Avbryt beställning {0}",
    "Check in {0} {1}": "Checka in {0} {1}",
    "Connect your Stripe account to start receiving payments.": "Anslut ditt Stripe-konto för att börja ta emot betalningar.",
    "Create {0}": "Skapa {0}",
    "Create an account or <0>{0}</0> to get started": "Skapa ett konto eller <0>{0}</0> för att komma igång",
    "Description for check-in staff": "Beskrivning för incheckningspersonal",
    "Discount in {0}": "Rabatt i {0}",
    "Edit {0}": "Redigera {0}",
    "Enter an amount excluding taxes and fees.": "Ange ett belopp exklusive skatter och avgifter.",
    "Filters ({activeFilterCount})": "Filter ({activeFilterCount})",
    "Free product, no payment information required": "Gratis produkt, ingen betalningsinformation krävs",
    "Hi {0} 👋": "Hej {0} 👋",
    "Hi.Events Conference {0}": "Hi.Events Konferens {0}",
    "HTML character limit exceeded: {htmlLength}/{maxLength}": "HTML-teckengräns överskriden: {htmlLength}/{maxLength}",
    "If a new tab did not open, please  <0><1>{0}</1>.</0>": "Om en ny flik inte öppnades, vänligen <0><1>{0}</1>.</0>",
    "If blank, the address will be used to generate a Google Mapa link": "Om tom kommer adressen att användas för att generera en Google Maps-länk",
    "Includes {0} products": "Inkluderar {0} produkter",
    "Includes 1 product": "Inkluderar 1 produkt",
    "No {0} available.": "Inga {0} tillgängliga.",
    "Option {i}": "Alternativ {i}",
    "Promo {promo_code} code applied": "Kampanjkod {promo_code} tillämpad",
    "Refund amount ({0})": "Återbetalningsbelopp ({0})",
    "Select {0}": "Välj {0}",
    "Send a copy to <0>{0}</0>": "Skicka en kopia till <0>{0}</0>",
    "Success! {0} will receive an email shortly.": "Framgång! {0} kommer att få ett e-postmeddelande inom kort.",
    "Successfully {0} attendee": "Framgångsrikt {0} deltagare",
    "The maximum number of products for {0}is {1}": "Det maximala antalet produkter för {0} är {1}",
    "Tier {0}": "Nivå {0}",
    "Update {0}": "Uppdatera {0}",
    "We couldn't find any tickets matching {0}": "Vi kunde inte hitta några biljetter som matchar {0}",
    "Welcome back{0} 👋": "Välkommen tillbaka{0} 👋",
    "Welcome to Hi.Events, {0} 👋": "Välkommen till Hi.Events, {0} 👋",
    "You are changing your email to <0>{0}</0>.": "Du ändrar din e-post till <0>{0}</0>.",
    "You're going to {0}! 🎉": "Du ska till {0}! 🎉",
    "Your email request change to <0>{0}</0> is pending. Please check your email to confirm": "Din begäran om e-poständring till <0>{0}</0> väntar. Kontrollera din e-post för att bekräfta"
}

def translate_po_file(filename):
    """Översätt de sista strängarna i .po-filen"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    output_lines = []
    i = 0
    translated_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Behåll kommentarer och metadata
        if line.startswith('#') or (line.startswith('"') and 'POT-Creation-Date' not in line) or line == '':
            output_lines.append(line)
            i += 1
            continue
        
        # Hitta msgid rader
        if line.startswith('msgid '):
            output_lines.append(line)
            # Extrahera msgid innehåll
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_content = msgid_match.group(1)
                # Hantera escape-sekvenser
                msgid_content = msgid_content.replace('\\"', '"').replace('\\\\', '\\')
                
                i += 1
                # Hantera multi-line msgid
                while i < len(lines) and lines[i].startswith('"'):
                    output_lines.append(lines[i])
                    additional_content = lines[i].strip().strip('"')
                    additional_content = additional_content.replace('\\"', '"').replace('\\\\', '\\')
                    msgid_content += additional_content
                    i += 1
                
                # Nu förväntar vi oss msgstr
                if i < len(lines) and lines[i].startswith('msgstr '):
                    msgstr_line = lines[i]
                    msgstr_match = re.match(r'msgstr "(.*)"', msgstr_line)
                    current_msgstr = msgstr_match.group(1) if msgstr_match else ""
                    
                    i += 1
                    # Hantera multi-line msgstr
                    while i < len(lines) and lines[i].startswith('"'):
                        additional_msgstr = lines[i].strip().strip('"')
                        additional_msgstr = additional_msgstr.replace('\\"', '"').replace('\\\\', '\\')
                        current_msgstr += additional_msgstr
                        i += 1
                    
                    # Översätt om vi har en översättning och msgstr är tom
                    if msgid_content in final_translations and current_msgstr == '':
                        translation = final_translations[msgid_content]
                        # Escape specialtecken för .po-format
                        escaped_translation = translation.replace('\\', '\\\\').replace('"', '\\"')
                        output_lines.append(f'msgstr "{escaped_translation}"')
                        translated_count += 1
                        print(f"Översatte: '{msgid_content}' -> '{translation}'")
                    else:
                        output_lines.append(msgstr_line)
                        # Lägg till eventuella multi-line msgstr rader som redan fanns
                        j = i - 1
                        while j > 0 and lines[j].startswith('"'):
                            j -= 1
                            break
                        while j < i and lines[j].startswith('"'):
                            if j != i - 1:  # Undvik dubbletter
                                output_lines.append(lines[j])
                            j += 1
                    
                    continue
        
        # Andra rader kopieras som de är
        output_lines.append(line)
        i += 1
    
    # Skriv tillbaka till filen
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nSlutig översättning av {filename} slutförd!")
    print(f"Översatte {translated_count} sista strängar")
    return translated_count

if __name__ == "__main__":
    translate_po_file('sv.po')
