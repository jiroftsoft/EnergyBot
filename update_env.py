"""Update .env file with Zarinpal Merchant ID."""
from pathlib import Path

env_file = Path('.env')
merchant_id = '156be6cd-e0a4-4af8-9113-83647771376f'

if env_file.exists():
    content = env_file.read_text(encoding='utf-8')
    lines = content.split('\n')
    updated = False
    new_lines = []
    
    for line in lines:
        if line.startswith('ZARINPAL_MERCHANT_ID='):
            new_lines.append(f'ZARINPAL_MERCHANT_ID={merchant_id}')
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f'ZARINPAL_MERCHANT_ID={merchant_id}')
    
    env_file.write_text('\n'.join(new_lines), encoding='utf-8')
    print('Updated .env with Zarinpal Merchant ID')
else:
    print('.env file not found')

