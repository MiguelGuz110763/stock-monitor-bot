import requests
import json


def send_whatsapp(report, whatsapp_to, file_path=None):
    token = "TU_TOKEN_DE_META"
    phone_id = "TU_PHONE_ID"

    base_url = "https://graph.facebook.com/v17.0"
    msg_url = f"{base_url}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Mensaje de texto
    text_payload = {
        "messaging_product": "whatsapp",
        "to": whatsapp_to,
        "type": "text",
        "text": {"body": report},
    }

    requests.post(msg_url, headers=headers, data=json.dumps(text_payload))

    if file_path:
        media_url = f"{base_url}/{phone_id}/media"

        files = {"file": open(file_path, "rb")}
        data = {
            "messaging_product": "whatsapp",
            "type": "application/pdf",
        }

        media_response = requests.post(
            media_url,
            headers={"Authorization": f"Bearer {token}"},
            files=files,
            data=data,
        )

        media_id = media_response.json().get("id")

        doc_payload = {
            "messaging_product": "whatsapp",
            "to": whatsapp_to,
            "type": "document",
            "document": {
                "id": media_id,
                "caption": "Reporte de acciones",
            },
        }

        requests.post(msg_url, headers=headers, data=json.dumps(doc_payload))
