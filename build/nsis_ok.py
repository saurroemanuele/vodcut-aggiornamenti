"""Controlla un installer NSIS come fa lui all'avvio (Source/exehead/fileform.c di NSIS): intestazione, lunghezza
e CRC32 di tutto il file tranne i primi 512 byte. L'installer 1.7.7 e' stato pubblicato troncato (mancavano 3,5 MB)
e a chi lo apriva Windows diceva "Installer integrity check has failed": cosi' un file rotto si ferma qui."""
import struct
import sys
import zlib


def check(path):
    with open(path, "rb") as f:
        b = f.read()
    for off in range(0, len(b) - 28, 512):
        if b[off + 4:off + 8] == b"\xef\xbe\xad\xde" and b[off + 8:off + 20] == b"NullsoftInst":
            end = off + struct.unpack_from("<i", b, off + 24)[0]
            if end > len(b):
                return "troncato, mancano %d byte" % (end - len(b))
            if zlib.crc32(b[512:end - 4]) != struct.unpack_from("<I", b, end - 4)[0]:
                return "CRC sbagliato"
            return ""
    return "intestazione NSIS non trovata"


if __name__ == "__main__":
    err = check(sys.argv[1])
    print(sys.argv[1] + ": " + (err or "integro"))
    sys.exit(1 if err else 0)
