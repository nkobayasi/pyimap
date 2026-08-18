# pyimap

Encode/Decode IMAP4 modified UTF-7.

## Description

IMAP mailbox names are encoded in a modified UTF7 when names contains international characters outside of the printable ASCII range. The modified UTF-7 encoding is defined in RFC2060 (section 5.1.3).

## Synopsis

* `encode_imap_utf7(s: str) -> bytes`

    Return the str encoded to IMAP modified UTF-7 bytes.

* `decode_imap_utf7(b: bytes) -> str`

    Return the IMAP modified UTF-7 bytes decoded to a str.
    
## Example

```
>>> encode_imap_utf7('テスト')
b'&MMYwuTDI-'
>>> decode_imap_utf7(b'&MMYwuTDI-')
'テスト'
```