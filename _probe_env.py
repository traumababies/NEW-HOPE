import re, urllib.parse

url = None
for line in open('.env', encoding='utf-8', errors='replace'):
    s = line.strip()
    if s.startswith('DATABASE_URL='):
        url = s.split('=', 1)[1]
        break
if not url:
    print('NO DATABASE_URL')
    raise SystemExit

print('raw url first 60:', repr(url[:60]))
m = re.match(r'[a-z0-9+]+://([^:]+):([^@]+)@([^/:]+)(?::(\d+))?/([^?]+)', url)
user, pwd_enc, host, port, db = m.group(1), m.group(2), m.group(3), m.group(4) or 1433, m.group(5)
pwd = urllib.parse.unquote(pwd_enc)
print('user   :', repr(user))
print('host   :', repr(host))
print('db     :', repr(db))
print('rawpwd :', repr(pwd_enc))
print('decpwd len:', len(pwd))
print('is 7Jumpycat7! :', pwd == '7Jumpycat7!')
