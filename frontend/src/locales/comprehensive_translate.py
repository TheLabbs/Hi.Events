#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# Omfattande svenska översättningar för Hi.Events
translations = {
    # Grundläggande
    "'There's nothing to show yet'": "'Det finns inget att visa än'",
    "Dashboard": "Instrumentpanel",
    "Events": "Event", 
    "Orders": "Beställningar",
    "Attendees": "Deltagare",
    "Products": "Produkter", 
    "Settings": "Inställningar",
    "Profile": "Profil",
    "Account": "Konto",
    "Users": "Användare",
    "Reports": "Rapporter", 
    "Messages": "Meddelanden",
    "Tools": "Verktyg",
    "Help & Support": "Hjälp & Support",
    "Home": "Hem",
    "Overview": "Översikt",
    "Loading...": "Laddar...",
    "Save": "Spara",
    "Save Changes": "Spara ändringar",
    "Cancel": "Avbryt",
    "Delete": "Ta bort",
    "Edit": "Redigera",
    "Create": "Skapa",
    "Add": "Lägg till",
    "Update": "Uppdatera",
    "Continue": "Fortsätt",
    "Next": "Nästa",
    "Back": "Tillbaka",
    "Close": "Stäng",
    "View": "Visa",
    "Show": "Visa",
    "Hide": "Dölj",
    "Search": "Sök",
    "Filter": "Filtrera",
    "Export": "Exportera",
    "Download": "Ladda ner",
    "Print": "Skriv ut",
    "Share": "Dela",
    "Copy": "Kopiera",
    "Yes": "Ja",
    "No": "Nej",
    "OK": "OK",
    "Apply": "Tillämpa",
    "Select": "Välj",
    "Choose": "Välj",
    "Confirm": "Bekräfta",
    "Preview": "Förhandsgranska",
    
    # Event-hantering
    "Create Event": "Skapa event",
    "Edit Event": "Redigera event",
    "Event Details": "Eventdetaljer",
    "Event Name": "Eventnamn",
    "Event Description": "Eventbeskrivning",
    "Start Date": "Startdatum",
    "End Date": "Slutdatum",
    "Start Date & Time": "Startdatum & tid",
    "End Date & Time": "Slutdatum & tid",
    "Location": "Plats",
    "Address": "Adress",
    "City": "Stad",
    "Country": "Land",
    "Online Event": "Online-event",
    "Venue Name": "Platsnamn",
    "State or Region": "Stat eller region",
    "ZIP / Postal Code": "Postnummer",
    
    # Biljetter/Produkter
    "Tickets": "Biljetter",
    "Ticket": "Biljett",
    "Create Ticket": "Skapa biljett",
    "Edit Ticket": "Redigera biljett",
    "Add tickets": "Lägg till biljetter",
    "Tickets & Products": "Biljetter & produkter",
    "Free Ticket": "Gratis biljett",
    "Paid Ticket": "Betald biljett",
    "Standard ticket with a fixed price": "Standardbiljett med fast pris",
    "Free ticket, no payment information required": "Gratis biljett, ingen betalningsinformation krävs",
    
    # Priser och betalning
    "Price": "Pris",
    "Amount": "Belopp", 
    "Total": "Totalt",
    "Currency": "Valuta",
    "Payment": "Betalning",
    "Stripe": "Stripe",
    "Connect with Stripe": "Anslut till Stripe",
    "Billing Address": "Faktureringsadress",
    
    # Status
    "Active": "Aktiv",
    "Inactive": "Inaktiv",
    "Draft": "Utkast",
    "Live": "Live",
    "Published": "Publicerad",
    "Completed": "Slutförd",
    "Pending": "Väntande",
    "Failed": "Misslyckades",
    "Success": "Framgång",
    "Error": "Fel",
    
    # Användarhantering
    "Login": "Logga in",
    "Register": "Registrera",
    "Email": "E-post",
    "Password": "Lösenord",
    "First Name": "Förnamn",
    "Last Name": "Efternamn",
    "Name": "Namn",
    "Admin": "Admin",
    "User": "Användare",
    "Role": "Roll",
    
    # Datum och tid
    "Date": "Datum",
    "Time": "Tid",
    "Today": "Idag",
    "Yesterday": "Igår",
    "Tomorrow": "Imorgon",
    "Never": "Aldrig",
    
    # Språk
    "Language": "Språk",
    "English": "Engelska",
    "Swedish": "Svenska",
    "German": "Tyska",
    "French": "Franska",
    "Spanish": "Spanska",
    "Italian": "Italienska",
    
    # Allmänna meddelanden
    "Working...": "Arbetar...",
    "Processing": "Bearbetar",
    "Loading": "Laddar",
    "Success!": "Framgång!",
    "Error!": "Fel!",
    "Warning": "Varning",
    "Message": "Meddelande",
    "Title": "Titel",
    "Description": "Beskrivning",
    "Details": "Detaljer",
    "Notes": "Anteckningar",
    
    # Ytterligare översättningar för vanliga termer
    "Order": "Beställning",
    "Status": "Status",
    "Type": "Typ",
    "Category": "Kategori",
    "Code": "Kod",
    "Email address": "E-postadress",
    "Phone": "Telefon",
    "Website": "Webbplats",
    "File": "Fil",
    "Image": "Bild",
    "Document": "Dokument",
    "Link": "Länk",
    "Color": "Färg",
    "Theme": "Tema",
    "Style": "Stil",
    "Design": "Design",
    "Template": "Mall",
    "Content": "Innehåll",
    "Subject": "Ämne",
    
    # Mängder och mätvärden
    "Available": "Tillgänglig",
    "Sold": "Såld",
    "Quantity": "Kvantitet",
    "Count": "Antal",
    "Number": "Nummer",
    "ID": "ID",
    "Value": "Värde",
    "Option": "Alternativ",
    "Options": "Alternativ",
    
    # Mer specifika Hi.Events termer
    "Organizer": "Arrangör",
    "Attendee": "Deltagare",
    "Check-in": "Incheckning",
    "Check In": "Checka in",
    "Check Out": "Checka ut",
    "Promo Code": "Kampanjkod",
    "Discount": "Rabatt",
    "Tax": "Skatt",
    "Fee": "Avgift",
    "Invoice": "Faktura",
    "Receipt": "Kvitto",
    "Refund": "Återbetalning",
    "Revenue": "Intäkter",
    "Sales": "Försäljning",
    "Analytics": "Analys",
    "Statistics": "Statistik",
    "Data": "Data",
    "Report": "Rapport",
    
    # Integration och tekniska termer
    "API": "API",
    "Webhook": "Webhook",
    "Integration": "Integration",
    "Export": "Exportera",
    "Import": "Importera",
    "Backup": "Säkerhetskopia",
    "Restore": "Återställ",
    "Sync": "Synkronisera",
    
    # UI-element
    "Button": "Knapp",
    "Menu": "Meny",
    "Sidebar": "Sidopanel",
    "Header": "Huvud",
    "Footer": "Sidfot",
    "Page": "Sida",
    "Form": "Formulär",
    "Field": "Fält",
    "Label": "Etikett",
    "Placeholder": "Platshållare",
    "Dropdown": "Rullgardinsmeny",
    "Checkbox": "Kryssruta",
    "Radio": "Radioknapp",
    "Modal": "Modal",
    "Dialog": "Dialog",
    "Popup": "Popup",
    "Tab": "Flik",
    "Panel": "Panel",
    "Widget": "Widget",
    "Component": "Komponent",
    
    # Åtgärder och processer
    "Create": "Skapa",
    "Read": "Läs",
    "Update": "Uppdatera",
    "Delete": "Ta bort",
    "Submit": "Skicka",
    "Reset": "Återställ",
    "Clear": "Rensa",
    "Refresh": "Uppdatera",
    "Reload": "Ladda om",
    "Generate": "Generera",
    "Calculate": "Beräkna",
    "Process": "Bearbeta",
    "Validate": "Validera",
    "Verify": "Verifiera",
    "Approve": "Godkänn",
    "Reject": "Avvisa",
    "Enable": "Aktivera",
    "Disable": "Inaktivera",
    "Start": "Starta",
    "Stop": "Stoppa",
    "Pause": "Pausa",
    "Resume": "Återuppta",
    "Complete": "Slutför",
    "Finish": "Avsluta",
    
    # Mer komplexa fraser som kan förekomma
    "Getting Started": "Kom igång",
    "User Management": "Användarhantering",
    "Event Management": "Eventhantering",
    "Payment Processing": "Betalningshantering",
    "Email Settings": "E-postinställningar",
    "SEO Settings": "SEO-inställningar",
    "Privacy Policy": "Integritetspolicy",
    "Terms of Service": "Användarvillkor",
    "Contact Support": "Kontakta support",
    "Documentation": "Dokumentation",
    "FAQ": "Vanliga frågor",
    "Tutorial": "Guide",
    "Help": "Hjälp",
    "Support": "Support",
    "Feedback": "Återkoppling",
    "About": "Om",
    "Version": "Version",
    "Copyright": "Copyright",
    "License": "Licens",
    
    # Felmeddelanden och bekräftelser
    "Something went wrong": "Något gick fel",
    "Please try again": "Försök igen",
    "Are you sure?": "Är du säker?",
    "This action cannot be undone": "Denna åtgärd kan inte ångras",
    "Successfully created": "Skapades framgångsrikt",
    "Successfully updated": "Uppdaterades framgångsrikt",
    "Successfully deleted": "Togs bort framgångsrikt",
    "Operation completed": "Åtgärden slutfördes",
    "Operation failed": "Åtgärden misslyckades",
    "Invalid input": "Ogiltiga uppgifter",
    "Required field": "Obligatoriskt fält",
    "Optional": "Valfritt",
    "Recommended": "Rekommenderat",
    
    # Specifika Hi.Events funktioner
    "Capacity Management": "Kapacitetshantering",
    "Check-In Lists": "Incheckningslistor", 
    "Promo Codes": "Kampanjkoder",
    "Tax & Fees": "Skatter & avgifter",
    "Email Templates": "E-postmallar",
    "Event Homepage": "Eventsida",
    "Order Summary": "Beställningssammanfattning",
    "Attendee Details": "Deltagardetaljer",
    "Event Statistics": "Eventstatistik",
    "Sales Report": "Försäljningsrapport",
    "Attendance Report": "Närvarorapport",
    "Revenue Report": "Intäktsrapport",
    
    # Datum och tidsrelaterade fraser
    "Start time": "Starttid",
    "End time": "Sluttid",  
    "Duration": "Varaktighet",
    "Timezone": "Tidszon",
    "Date & Time": "Datum & tid",
    "All day": "Hela dagen",
    "Custom": "Anpassad",
    "Recurring": "Återkommande",
    "One-time": "Engångshändelse",
    
    # Betalning och ekonomi
    "Free": "Gratis",
    "Paid": "Betald",
    "Fixed": "Fast",
    "Variable": "Variabel",
    "Minimum": "Minimum",
    "Maximum": "Maximum",
    "Subtotal": "Delsumma",
    "Taxes": "Skatter",
    "Fees": "Avgifter",
    "Discount": "Rabatt",
    "Final total": "Slutsumma",
    "Payment method": "Betalningsmetod",
    "Credit card": "Kreditkort",
    "Bank transfer": "Banköverföring",
    "PayPal": "PayPal",
    "Cash": "Kontant",
    "Offline": "Offline",
    "Online": "Online",
    
    # Kommunikation
    "Send": "Skicka",
    "Receive": "Ta emot",
    "Reply": "Svara",
    "Forward": "Vidarebefordra",
    "Compose": "Skriv",
    "Inbox": "Inkorg",
    "Sent": "Skickat",
    "Draft": "Utkast",
    "Trash": "Papperskorg",
    "Archive": "Arkiv",
    "Mark as read": "Markera som läst",
    "Mark as unread": "Markera som oläst",
    "Notification": "Notifikation",
    "Alert": "Varning",
    "Reminder": "Påminnelse",
    "Confirmation": "Bekräftelse",
    
    # Säkerhet och behörigheter  
    "Permission": "Behörighet",
    "Access": "Åtkomst",
    "Security": "Säkerhet",
    "Privacy": "Integritet",
    "Authentication": "Autentisering",
    "Authorization": "Auktorisering",
    "Login": "Logga in",
    "Logout": "Logga ut",
    "Sign up": "Registrera dig",
    "Sign in": "Logga in",
    "Forgot password": "Glömt lösenord",
    "Reset password": "Återställ lösenord",
    "Change password": "Byt lösenord",
    "Current password": "Nuvarande lösenord",
    "New password": "Nytt lösenord",
    "Confirm password": "Bekräfta lösenord",
    
    # Sök och filtrering
    "Search": "Sök",
    "Filter": "Filtrera",
    "Sort": "Sortera",
    "Order by": "Sortera efter",
    "Ascending": "Stigande",
    "Descending": "Fallande",
    "Results": "Resultat",
    "No results": "Inga resultat",
    "Found": "Hittade",
    "matches": "träffar",
    "Clear filters": "Rensa filter",
    "Apply filters": "Tillämpa filter",
    
    # Pagination och listhantering
    "Page": "Sida",
    "of": "av", 
    "First": "Första",
    "Last": "Sista",
    "Previous": "Föregående",
    "Next": "Nästa",
    "Go to page": "Gå till sida",
    "Items per page": "Objekt per sida",
    "Show": "Visa",
    "All": "Alla",
    "Select all": "Välj alla",
    "Deselect all": "Avmarkera alla",
    "Bulk actions": "Massåtgärder",
    
    # Media och filer
    "Upload": "Ladda upp",
    "Download": "Ladda ner",
    "File": "Fil",
    "Image": "Bild",
    "Photo": "Foto",
    "Video": "Video",
    "Audio": "Ljud",
    "PDF": "PDF",
    "Document": "Dokument",
    "Attachment": "Bilaga",
    "Gallery": "Galleri",
    "Library": "Bibliotek",
    "Media": "Media",
    "Size": "Storlek",
    "Format": "Format",
    "Quality": "Kvalitet",
    "Resolution": "Upplösning",
    
    # Färger och design
    "Color": "Färg",
    "Background": "Bakgrund",
    "Foreground": "Förgrund", 
    "Text color": "Textfärg",
    "Primary": "Primär",
    "Secondary": "Sekundär",
    "Accent": "Accent",
    "Theme": "Tema",
    "Dark": "Mörk",
    "Light": "Ljus",
    "Auto": "Auto",
    "Custom": "Anpassad",
    "Transparent": "Transparent",
    "Opacity": "Opacitet",
    "Gradient": "Gradient",
    
    # Layout och positioning
    "Layout": "Layout",
    "Position": "Position",
    "Alignment": "Justering",
    "Left": "Vänster",
    "Right": "Höger", 
    "Center": "Centrum",
    "Top": "Topp",
    "Bottom": "Botten",
    "Middle": "Mitten",
    "Margin": "Marginal",
    "Padding": "Utfyllnad",
    "Border": "Ram",
    "Width": "Bredd",
    "Height": "Höjd",
    "Resize": "Ändra storlek",
    "Move": "Flytta",
    "Rotate": "Rotera",
    "Scale": "Skala",
    
    # Tekniska och utvecklarrelaterade termer
    "Debug": "Felsök",
    "Console": "Konsol",
    "Log": "Logg",
    "Error log": "Fellogg",
    "Warning": "Varning", 
    "Info": "Info",
    "Debug": "Felsök",
    "Trace": "Spår",
    "Stack trace": "Stackspår",
    "Exception": "Undantag",
    "Timeout": "Tidsgräns",
    "Retry": "Försök igen",
    "Cache": "Cache",
    "Database": "Databas",
    "Query": "Fråga",
    "Index": "Index",
    "Schema": "Schema",
    "Migration": "Migration",
    "Rollback": "Rollback",
    
    # Ytterligare vanliga fraser
    "Please wait": "Vänta",
    "Almost done": "Nästan klar",
    "In progress": "Pågår",
    "Not started": "Inte påbörjad",
    "On hold": "Pausad",
    "Cancelled": "Avbruten",
    "Expired": "Utgången", 
    "Active": "Aktiv",
    "Inactive": "Inaktiv",
    "Enabled": "Aktiverad",
    "Disabled": "Inaktiverad",
    "Available": "Tillgänglig",
    "Unavailable": "Otillgänglig",
    "Online": "Online",
    "Offline": "Offline",
    "Connected": "Ansluten",
    "Disconnected": "Frånkopplad",
    "Synced": "Synkroniserad",
    "Not synced": "Inte synkroniserad",
    "Up to date": "Uppdaterad",
    "Out of date": "Föråldrad",
    "Modified": "Modifierad",
    "Unchanged": "Oförändrad",
    "New": "Ny",
    "Updated": "Uppdaterad",
    "Deleted": "Borttagen",
    "Archived": "Arkiverad",
    "Published": "Publicerad",
    "Unpublished": "Opublicerad",
    "Draft": "Utkast",
    "Final": "Slutlig",
    "Approved": "Godkänd",
    "Rejected": "Avvisad",
    "Pending approval": "Väntar på godkännande",
    "Under review": "Under granskning",
    
    # Mer specifika Hi.Events-relaterade termer baserat på contexts
    "Event page": "Eventsida",
    "Event homepage": "Eventstartsida",
    "Registration": "Registrering", 
    "Check-in": "Incheckning",
    "Check-out": "Utcheckning",
    "Attendee list": "Deltagarlista",
    "Guest list": "Gästlista",
    "Waiting list": "Väntelista",
    "Capacity": "Kapacitet",
    "Sold out": "Slutsåld",
    "Available": "Tillgänglig",
    "Limited": "Begränsad",
    "Unlimited": "Obegränsad",
    "Early bird": "Early bird",
    "Regular": "Ordinarie",
    "VIP": "VIP",
    "General admission": "Allmän biljett",
    "Reserved seating": "Reserverade platser",
    "Standing": "Stående",
    "Table": "Bord",
    "Booth": "Monter",
    "Sponsor": "Sponsor",
    "Partner": "Partner",
    "Vendor": "Leverantör",
    "Exhibitor": "Utställare",
    "Speaker": "Talare",
    "Host": "Värd",
    "Moderator": "Moderator",
    "Participant": "Deltagare",
    "Audience": "Publik",
    "Viewer": "Tittare",
    "Subscriber": "Prenumerant",
    "Member": "Medlem",
    "Guest": "Gäst",
    "Visitor": "Besökare",
    "Customer": "Kund",
    "Client": "Klient",
    "Contact": "Kontakt",
    "Lead": "Lead",
    "Prospect": "Prospekt",
    
    # Eventtyper och kategorier
    "Conference": "Konferens",
    "Workshop": "Workshop", 
    "Seminar": "Seminarium",
    "Webinar": "Webbinarium",
    "Meeting": "Möte",
    "Training": "Utbildning",
    "Course": "Kurs",
    "Class": "Klass",
    "Lesson": "Lektion",
    "Tutorial": "Handledning",
    "Demo": "Demo",
    "Presentation": "Presentation",
    "Lecture": "Föreläsning",
    "Talk": "Talk",
    "Panel": "Panel",
    "Discussion": "Diskussion",
    "Forum": "Forum",
    "Q&A": "Frågor & svar",
    "Interview": "Intervju",
    "Podcast": "Podcast",
    "Show": "Show",
    "Performance": "Föreställning",
    "Concert": "Konsert",
    "Festival": "Festival",
    "Party": "Fest",
    "Celebration": "Firande",
    "Ceremony": "Ceremoni",
    "Wedding": "Bröllop",
    "Birthday": "Födelsedag",
    "Anniversary": "Årsdag",
    "Graduation": "Examen",
    "Launch": "Lansering",
    "Opening": "Öppning",
    "Closing": "Stängning",
    "Networking": "Nätverkande",
    "Social": "Social",
    "Fundraiser": "Insamling",
    "Charity": "Välgörenhet",
    "Auction": "Auktion",
    "Competition": "Tävling",
    "Contest": "Tävling",
    "Tournament": "Turnering",
    "Game": "Spel",
    "Sport": "Sport",
    "Match": "Match",
    "Race": "Lopp",
    "Exhibition": "Utställning",
    "Fair": "Mässa",
    "Market": "Marknad",
    "Sale": "Rea",
    "Promotion": "Kampanj",
    "Campaign": "Kampanj",
    "Drive": "Drive",
    "Initiative": "Initiative",
    "Program": "Program",
    "Project": "Projekt",
    "Activity": "Aktivitet",
    "Event": "Event",
    "Occasion": "Tillfälle",
    "Gathering": "Sammankomst",
    "Assembly": "Församling",
    "Convention": "Convention",
    "Summit": "Toppmöte",
    "Symposium": "Symposium",
    "Colloquium": "Kollokium",
    "Congress": "Kongress",
    "Expo": "Expo",
    "Trade show": "Mässor"
}

def translate_po_file(filename):
    """Översätt en .po-fil med svenska översättningar"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    output_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Behåll kommentarer och metadata
        if line.startswith('#') or line.startswith('"') and not line.startswith('"POT-Creation-Date') or line == '':
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
                    if msgid_content in translations and current_msgstr == '':
                        translation = translations[msgid_content]
                        # Escape specialtecken för .po-format
                        escaped_translation = translation.replace('\\', '\\\\').replace('"', '\\"')
                        output_lines.append(f'msgstr "{escaped_translation}"')
                    else:
                        output_lines.append(msgstr_line)
                        # Lägg till eventuella multi-line msgstr rader som redan fanns
                        j = i
                        while j < len(lines) and lines[j].startswith('"'):
                            output_lines.append(lines[j])
                            j += 1
                    
                    continue
        
        # Andra rader kopieras som de är
        output_lines.append(line)
        i += 1
    
    # Skriv tillbaka till filen
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"Översättning av {filename} slutförd!")

if __name__ == "__main__":
    translate_po_file('sv.po')
