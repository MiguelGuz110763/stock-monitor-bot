from twilio.rest import Client

def send_whatsapp(report, whatsapp_to):
    account_sid = "TU_ACCOUNT_SID"
    auth_token = "TU_AUTH_TOKEN"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=report,
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{whatsapp_to}"
    )
