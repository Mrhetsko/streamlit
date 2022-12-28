import streamlit as st
import boto3
import s3fs
import os
from streamlit_request import request_to_server


s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

fs = s3fs.S3FileSystem(anon=False,
                       key=os.getenv('AWS_ACCESS_KEY_ID'),
                       secret=os.getenv('AWS_SECRET_ACCESS_KEY'))

aws_bucket = os.getenv('AWS_BUCKET')

st.title('Upload Your photos')

project_name = st.text_input('Enter new project name', placeholder='vacation')


def files_to_bucket(obj, bucket, s3_file, folder_name):
    s3.upload_fileobj(obj, bucket, f'uploaded_images/{folder_name}/{s3_file}')


uploaded_files = st.file_uploader('Choose images to upload',
                                  accept_multiple_files=True,
                                  type=['png', 'jpg', 'jpeg', 'heif'])  # add more types ?


if uploaded_files is not None:

    if st.button('Upload photos and start training'):
        counter = 0
        for file in uploaded_files:
            files_to_bucket(file, aws_bucket, file.name, project_name)
            counter += 1

        st.success(f'Successfully uploaded {counter} files')
        print(request_to_server(project_n=project_name))


# ----------------Download section

st.subheader('or download already trained 3d models to your computer')
s3_resources = boto3.resource('s3',
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
finished_projects = s3_resources.Bucket('hoxnabucket')
list_of_ply = [obj.key for obj in finished_projects.objects.all() if obj.key.endswith('.ply')]
project_names = [pr_name.split('/')[-2] for pr_name in list_of_ply]


def download_model(project):
    with fs.open(f'/hoxnabucket/pointcloud/{project}/point_cloud.ply', 'rb') as f:
        download_button = st.download_button(label='Download model',
                                             data=f.read(),
                                             file_name=f'{project}.ply'
                                             )
        return download_button


input_project_name = st.selectbox('Choose', (name for name in project_names))
if input_project_name:
    download_model(input_project_name)



