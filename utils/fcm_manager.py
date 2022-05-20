import firebase_admin
from firebase_admin import credentials, messaging

def send_push(title, msg, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    firebase_admin.messaging.AndroidConfig(priority="high")
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        tokens=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

if __name__ == '__main__':
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
