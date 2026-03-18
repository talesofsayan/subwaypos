import hashlib
import os
from dotenv import load_dotenv, set_key

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

existing = os.getenv('ADMIN_PASSWORD')

if existing:
    old = input('Enter current password: ')
    old_hash = hashlib.sha256(old.encode()).hexdigest()
    
    if old_hash != existing:
        print('Wrong password! Access denied.')
        exit()

new = input('Enter new password: ')
confirm = input('Confirm new password: ')

if new != confirm:
    print('Passwords do not match!')
    exit()

new_hash = hashlib.sha256(new.encode()).hexdigest()
set_key(env_path, 'ADMIN_PASSWORD_HASH', new_hash)

print('Admin password updated successfully!')