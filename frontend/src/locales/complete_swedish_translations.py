#!/usr/bin/env python3
import re
import time
import urllib.request
import urllib.parse
import json
import html

def parse_po_file(filename):
    """Parse a PO file and return a dictionary of msgid -> msgstr mappings."""
    translations = {}
    current_context = []
    current_msgid = None
    current_msgstr = None
    multiline_msgid = False
    multiline_msgstr = False
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle comments and context
        if line.startswith('#:'):
            current_context = [l.strip() for l in line[2:].strip().split()]
        
        # Handle msgid
        elif line.startswith('msgid '):
            current_msgid = line[6:].strip()
            if current_msgid.startswith('"') and current_msgid.endswith('"'):
                current_msgid = current_msgid[1:-1]
            multiline_msgid = True
            multiline_msgstr = False
        
        # Handle msgstr
        elif line.startswith('msgstr '):
            current_msgstr = line[7:].strip()
            if current_msgstr.startswith('"') and current_msgstr.endswith('"'):
                current_msgstr = current_msgstr[1:-1]
            multiline_msgid = False
            multiline_msgstr = True
            
            # Store complete translation if not a header
            if current_msgid != '':
                translations[current_msgid] = {
                    'msgstr': current_msgstr,
                    'context': current_context
                }
                
            # Reset for next entry
            current_context = []
            current_msgid = None
            current_msgstr = None
            multiline_msgid = False
            multiline_msgstr = False
        
        # Handle multiline strings
        elif line.startswith('"') and line.endswith('"') and (multiline_msgid or multiline_msgstr):
            content = line[1:-1]
            if multiline_msgid and current_msgid is not None:
                current_msgid += content
            elif multiline_msgstr and current_msgstr is not None:
                current_msgstr += content
        
        i += 1
    
    return translations

def machine_translate(text, source_lang="en", target_lang="sv"):
    """Use Google Translate API to translate text."""
    if not text or text == "":
        return ""
    
    # Simple HTML tag extraction to protect them from translation
    html_tags = []
    tag_pattern = r'<[^>]+>'
    
    def replace_tag(match):
        tag = match.group(0)
        html_tags.append(tag)
        return f"TAG{len(html_tags) - 1}"
    
    # Replace HTML tags with placeholders
    text_with_placeholders = re.sub(tag_pattern, replace_tag, text)
    
    try:
        # Use Google Translate API
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={urllib.parse.quote(text_with_placeholders)}"
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )
        
        # Try with exponential backoff
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(request) as response:
                    data = response.read().decode('utf-8')
                    break
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Translation failed for: {text}")
                    return text  # Return original text if translation fails
        
        # Parse the response
        translation_data = json.loads(data)
        translated_text = ''.join(item[0] for item in translation_data[0] if item[0])
        
        # Replace placeholders with original HTML tags
        for i, tag in enumerate(html_tags):
            translated_text = translated_text.replace(f"TAG{i}", tag)
        
        return translated_text
    except Exception as e:
        print(f"Translation error: {e} for text: {text}")
        return text  # Return original text if translation fails

def create_complete_swedish_po(english_file, swedish_file, output_file):
    """Create a complete Swedish PO file based on English structure."""
    # Parse existing files
    english_translations = parse_po_file(english_file)
    swedish_translations = parse_po_file(swedish_file)
    
    # Read the English file to preserve structure
    with open(english_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Get header from Swedish file
    with open(swedish_file, 'r', encoding='utf-8') as f:
        sv_lines = f.readlines()
    
    header_end = 0
    for i, line in enumerate(sv_lines):
        if line.strip() == "":
            header_end = i + 1
            break
    
    swedish_header = sv_lines[:header_end]
    
    # Prepare output file
    output_lines = swedish_header
    
    # Process the rest of the file
    i = 0
    while i < len(lines):
        if i < header_end:
            # Skip header in English file as we already have Swedish header
            i += 1
            continue
        
        line = lines[i]
        
        # Copy comments and context lines
        if line.startswith('#'):
            output_lines.append(line)
            i += 1
            continue
        
        # Process msgid and msgstr pairs
        if line.startswith('msgid '):
            msgid_lines = [line]
            i += 1
            
            # Collect multiline msgid
            while i < len(lines) and lines[i].strip().startswith('"'):
                msgid_lines.append(lines[i])
                i += 1
            
            # Extract msgid value
            msgid_value = msgid_lines[0][6:].strip()
            if msgid_value.startswith('"') and msgid_value.endswith('"'):
                msgid_value = msgid_value[1:-1]
            
            for j in range(1, len(msgid_lines)):
                line_content = msgid_lines[j].strip()
                if line_content.startswith('"') and line_content.endswith('"'):
                    msgid_value += line_content[1:-1]
            
            # Process msgstr line
            msgstr_line = lines[i]
            if msgstr_line.startswith('msgstr '):
                msgstr_lines = [msgstr_line]
                i += 1
                
                # Collect multiline msgstr
                while i < len(lines) and lines[i].strip().startswith('"'):
                    msgstr_lines.append(lines[i])
                    i += 1
                
                # Extract English msgstr value
                english_msgstr = msgstr_lines[0][7:].strip()
                if english_msgstr.startswith('"') and english_msgstr.endswith('"'):
                    english_msgstr = english_msgstr[1:-1]
                
                for j in range(1, len(msgstr_lines)):
                    line_content = msgstr_lines[j].strip()
                    if line_content.startswith('"') and line_content.endswith('"'):
                        english_msgstr += line_content[1:-1]
                
                # Use existing Swedish translation, English fallback, or translate
                if msgid_value in swedish_translations and swedish_translations[msgid_value]['msgstr']:
                    swedish_msgstr = swedish_translations[msgid_value]['msgstr']
                else:
                    # Try to machine translate if not empty
                    if msgid_value and msgid_value != '':
                        swedish_msgstr = machine_translate(msgid_value, 'en', 'sv')
                        # Add a small delay to avoid API rate limits
                        time.sleep(0.1)
                    else:
                        swedish_msgstr = english_msgstr  # Use English for empty msgid
                
                # Add msgid lines to output
                output_lines.extend(msgid_lines)
                
                # Format the msgstr line (handle multiline if needed)
                if len(swedish_msgstr) > 77:  # Break long lines
                    output_lines.append(f'msgstr "{swedish_msgstr[:77]}"\n')
                    remaining = swedish_msgstr[77:]
                    while remaining:
                        chunk = remaining[:77]
                        remaining = remaining[77:]
                        output_lines.append(f'"{chunk}"\n')
                else:
                    output_lines.append(f'msgstr "{swedish_msgstr}"\n')
                
                # Add a blank line after each entry
                if i < len(lines) and lines[i].strip() == "":
                    output_lines.append(lines[i])
                    i += 1
            else:
                # If no msgstr found, just copy the current line
                output_lines.append(line)
                i += 1
        else:
            # Copy any other lines
            output_lines.append(line)
            i += 1
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

def main():
    print("Starting Swedish translation completion process...")
    
    english_file = 'en.po'
    swedish_file = 'sv.po'
    output_file = 'sv.po'
    
    # First, analyze files
    english_translations = parse_po_file(english_file)
    swedish_translations = parse_po_file(swedish_file)
    
    print(f"Found {len(english_translations)} strings in English file")
    print(f"Found {len(swedish_translations)} strings in Swedish file")
    print(f"Missing {len(english_translations) - len(swedish_translations)} strings")
    
    # Create complete Swedish file
    print("Creating complete Swedish translation file...")
    create_complete_swedish_po(english_file, swedish_file, output_file)
    
    print("Done! Swedish translations completed.")

if __name__ == "__main__":
    main()
