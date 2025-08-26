import gzip
import json
from io import BytesIO


async def unpack_gzip(raw_body: bytes) -> dict | list:
    """
    Unpacks gzip-packed json-serialized data and deserializes it

    :param raw_body: request body
    :type raw_body: bytes
    :return: json-serialized data
    :rtype: dict | list
    """

    with gzip.GzipFile(fileobj=BytesIO(raw_body)) as f:
        decompressed_data = f.read()
        decoded_json = json.loads(decompressed_data)
    return decoded_json
