import gzip
import io

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import zlib

from formatter.settings import settings

MAIN_ENCODING = 'windows-1251'


def decrypt_and_decompress(encrypted_base64: str, key: bytes, iv: bytes) -> str:
    # Step 1: Decode from Base64
    encrypted_bytes = base64.b64decode(encrypted_base64)

    # Step 2: Decrypt using AES-GCM
    aesgcm = AESGCM(key)
    decrypted_bytes = aesgcm.decrypt(iv, encrypted_bytes, None)

    # Step 3: Decompress with zlib
    # decompressed_bytes = zlib.decompress(decrypted_bytes)

    with gzip.GzipFile(fileobj=io.BytesIO(decrypted_bytes), mode='rb') as f:
        decompressed_bytes = f.read()  # Decompress and decode to UTF-8 string

    # Step 4: Decode to string with 1251 encoding
    return decompressed_bytes.decode('cp1251')  # windows-1251


def encrypt_and_compress(data: str, key: bytes, iv: bytes) -> str:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as f:
        f.write(data.encode('cp1251'))  # Ensure it's encoded to bytes
    compressed = buf.getvalue()

    aesgcm = AESGCM(key)
    enc = aesgcm.encrypt(iv, compressed, None)
    return base64.b64encode(enc).decode()



def decrypt_data(enc_data_b64: str, key: bytes, iv: bytes) -> bytes:
    aesgcm = AESGCM(key)
    enc_data = base64.b64decode(enc_data_b64)
    return aesgcm.decrypt(iv, enc_data, None)


def encrypt_data(plain_data: bytes, key: bytes, iv: bytes) -> str:
    aesgcm = AESGCM(key)
    enc = aesgcm.encrypt(iv, plain_data, None)
    return base64.b64encode(enc).decode()


def compress(data: str) -> bytes:
    return zlib.compress(data.encode(MAIN_ENCODING))


def decompress(data: bytes) -> str:
    return zlib.decompress(data).decode(MAIN_ENCODING)
