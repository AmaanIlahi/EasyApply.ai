from firebase_admin import storage

# def upload_resume(file, filename):
#     print(file, "  ---  ", filename)
#     bucket = storage.bucket()
#     print(bucket)
#     blob = bucket.blob(f"resumes/{filename}")
#     print(blob)
#     blob.upload_from_file(file.file)
#     blob.make_public()
#     print(blob)
#     return blob.public_url



from firebase_admin import storage, credentials, initialize_app
import firebase_admin

# Only initialize once
if not firebase_admin._apps:
    cred = credentials.Certificate("../serviceAccountKey.json")  # <-- path to your .json
    initialize_app(cred, {
        'storageBucket': 'easyapplyai-e16cc.firebasestorage.app'
    })

def upload_resume(file, filename):
    bucket = storage.bucket()
    print(bucket)
    blob = bucket.blob(f"resumes/{filename}")
    print(blob)
    blob.upload_from_file(file.file)
    blob.make_public()
    print(blob)
    return blob.public_url
