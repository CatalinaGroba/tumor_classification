import os

#from colorama import Fore, Style
from tensorflow import keras
from google.cloud import storage


def load_model() -> keras.Model:

    #the storage module provides functionalities to interact with google cloud
    #client = storage.Client() # create new instane of the CLient class
    client = storage.Client.create_anonymous_client()
    #breakpoint()
    bucket = client.bucket('tumor_classification')#, user_project='aqueous-ray-374915') #access bucket from a project_id of another person
    blobs = list(client.get_bucket(bucket).list_blobs()) #retrieve a list with all blobs(objects) that are in the bucket shared with the team members
    try:
        latest_blob = max(blobs, key=lambda x: x.updated) # find the blob with the latest update. Every blob has an update hidden attribute and this command can access to it
        latest_model_path_to_save = os.path.join('tumor_class/ml_logic/models', latest_blob.name) # create a path with the local registry path and the name attribute of the blob
        latest_blob.download_to_filename(latest_model_path_to_save) #download the blob and save it into the path
        latest_model = keras.models.load_model(latest_model_path_to_save) #loads the model from the local path with a built-in function of keras 'load_model'
        print("✅ Latest model downloaded from cloud storage")
        return latest_model
    except:
        print(f"\n❌ No model found on GCS bucket")
        return None

    else:

        return None


if __name__=='__main__':
    load_model()
