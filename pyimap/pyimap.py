
from __future__ import annotations
import re
import base64

def encode_imap_utf7(s:str) ->bytes:
    def repl(m:re.Match) ->str:
        return '&' + base64.b64encode(m.group(0).encode('UTF-16BE'), altchars=b'+,').rstrip(b'=').decode('ascii') + '-'
    if not isinstance(s, str):
        raise TypeError('should be str')
    return re.sub(r'[^\u0020-\u007e]+', repl, s.replace('&', '&-')).encode('ascii')

def decode_imap_utf7(b:bytes) ->str:
    def repl(m:re.Match) ->str:
        return base64.b64decode(m.group(1) + '='*(-len(m.group(1))%4), altchars='+,').decode('UTF-16BE')
    if not isinstance(b, bytes):
        raise TypeError('should be bytes')
    return re.sub(r'&([A-Za-z0-9+,]+)-', repl, b.decode('ascii')).replace('&-', '&')

def main():
    print(decode_imap_utf7(b'Draft'))
    print(decode_imap_utf7(b'&MMYwuTDI-'))
    print(encode_imap_utf7('Draft'))
    print(encode_imap_utf7('テスト'))
    print(decode_imap_utf7(encode_imap_utf7('テスト')))

if __name__ == '__main__':
    main()
