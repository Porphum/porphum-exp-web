import html
import traceback

from fastapi import FastAPI, Request, HTTPException
import json

from formatter.handler import UPDToXmlHandler
from formatter.settings import settings
from formatter.utils.encrypt import decrypt_data, decompress, compress, encrypt_data, decrypt_and_decompress, \
    encrypt_and_compress

app = FastAPI()
xml_handler = UPDToXmlHandler()


def sanitize_for_xml(json_string):
    # Load the JSON string into a Python dict
    data = json.loads(json_string)

    # Recursively escape special XML characters
    def escape_values(obj):
        if isinstance(obj, dict):
            return {k: escape_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [escape_values(i) for i in obj]
        elif isinstance(obj, str):
            return html.escape(obj, quote=True)  # escapes &, <, >, " and '
        else:
            return obj

    return escape_values(data)


@app.post("/api/convert")
async def convert(request: Request):
    headers = request.headers
    if headers.get("X-Auth-Token") != settings.AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")

    encrypted_payload = await request.body()

    try:
        key = bytes.fromhex(settings.RECEIVE_KEY)
        iv = bytes.fromhex(settings.RECEIVE_IV)
        json_str = decrypt_and_decompress(encrypted_payload, key, iv)
        data = sanitize_for_xml(json_str)

        xml_output = xml_handler.process_data(data)

        key = bytes.fromhex(settings.SEND_KEY)
        iv = bytes.fromhex(settings.SEND_IV)
        encrypted_xml = encrypt_and_compress(xml_output, key, iv)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"{traceback.format_exception(e)}",
        )

    return encrypted_xml
