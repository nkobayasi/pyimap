
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

class IMAP4String(object):
    def __init__(self, value:str|bytes):
        if isinstance(value, bytes):
            self._value = decode_imap_utf7(value)
        elif isinstance(value, str):
            self._value = value
        raise TypeError('should be str or bytes.')
        
    def __repr__(self) ->str:
        return '<{}: "{}">'.format(self.__class__.__name__, self._value)

    def __str__(self) ->str:
        return self.as_str()
        
    def __bytes__(self) ->bytes:
        return self.as_bytes()

    def __eq__(self, value) ->bool:
        if isinstance(value, str):
            return self.as_str() == value
        elif isinstance(value, bytes):
            return self.as_bytes() == value
        return self.as_str() == str(value)

    def __add__(self, other):
        if isinstance(other, str):
            return IMAP4String(self._value + other)
        elif isinstance(other, bytes):
            return IMAP4String(self._value + decode_imap_utf7(other))
        return IMAP4String(self._value + str(other))

    @property
    def value(self) ->str:
        return self._value
    
    def as_str(self) ->str:
        return self._value
    
    def as_bytes(self) ->bytes:
        return encode_imap_utf7(self._value)

def main():
    print(decode_imap_utf7(b'Draft'))
    print(decode_imap_utf7(b'&MMYwuTDI-'))
    print(encode_imap_utf7('Draft'))
    print(encode_imap_utf7('テスト'))
    print(decode_imap_utf7(encode_imap_utf7('テスト')))

if __name__ == '__main__':
    main()
