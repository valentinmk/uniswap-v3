import json
import base64


def decode_nft_URI(data: dict) -> dict:
    data_encoded = data.split(",")[1]
    data_decoded = json.loads(base64.b64decode(data_encoded).decode())
    image = base64.b64decode(data_decoded["image"].split(",")[1]).decode()
    data_decoded["image"] = image
    return data_decoded


def normalize_tick_by_spacing(tick: int, spacing: int) -> int:
    return tick // spacing * spacing
