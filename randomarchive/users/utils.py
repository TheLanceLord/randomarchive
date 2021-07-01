# Copyright 2021 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################
import os
import secrets
from PIL import Image
from flask import current_app
from google.cloud import storage
from randomarchive.config import Config

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    picture_fn = upload_blob(picture_path, picture_fn)
    
    return picture_fn

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket_name = Config.GCS_BUCKET_NAME

    gcs_upload_string = 'gsutil cp ' + source_file_name + ' gs://' + bucket_name + '/'

    # Upload the file to GCS
    os.system(gcs_upload_string)

    # Clean up the file from the server since it is now on GCS
    os.remove(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
    
    return destination_blob_name
