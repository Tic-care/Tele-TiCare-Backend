import pyrebase

config = {
    "apiKey": "AIzaSyC5SXaswgBSnsRvfByglfWrKxlAVpvrX3E",
    "authDomain": "grad-trail.firebaseapp.com",
    "databaseURL": "https://grad-trail-default-rtdb.europe-west1.firebasedatabase.app",
    "storageBucket": "grad-trail.appspot.com",
    "serviceAccount": "firebase-connection/grad-trail-firebase-adminsdk-3xlme-d41c3126a8.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def stream_handler(message):
    # Process the data change (e.g., print, trigger actions)
    print(f"Event type: {message['event']}")
    print(f"Data: {message['data']}")
    print(message)
    


# Listen for changes at a specific path
my_stream = db.child("clips").stream(stream_handler=stream_handler)

# Keep the stream alive (replace with your main application loop)
while True:
    pass
