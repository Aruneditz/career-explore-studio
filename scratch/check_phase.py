import json
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open(r'C:\Users\ELCOT\.gemini\antigravity\brain\e189c26a-07f3-490e-931e-87020591e9fa\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        if i == 1461:
            data = json.loads(line)
            content = str(data.get('content', ''))
            idx = content.find('12. ACCESSIBILITY')
            if idx != -1:
                print(content[idx:idx+2500])
