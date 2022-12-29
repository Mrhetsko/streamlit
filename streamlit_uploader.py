import streamlit as st
import boto3
import s3fs
from os import getenv
import requests


s3 = boto3.client('s3',
                  aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'))

fs = s3fs.S3FileSystem(anon=False,
                       key=getenv('AWS_ACCESS_KEY_ID'),
                       secret=getenv('AWS_SECRET_ACCESS_KEY'))


aws_bucket = getenv('AWS_BUCKET')

st.title('Upload Your photos')

project_name = st.text_input('Enter new project name', placeholder='vacation')


def files_to_bucket(obj, bucket, s3_file, folder_name):
    """Copy images to AWS bucket"""
    s3.upload_fileobj(obj, bucket, f'uploaded_images/{folder_name}/{s3_file}')


uploaded_files = st.file_uploader('Choose images to upload',
                                  accept_multiple_files=True,
                                  type=['png', 'jpg', 'jpeg', 'heif'])  # add more types ?


def download_model(bucket, project):
    """Create the button to download trained point_cloud.ply from AWS bucket to computer"""
    with fs.open(f'/{bucket}/pointcloud/{project}/point_cloud.ply', 'rb') as f:
        download_button = st.download_button(label='Download model',
                                             data=f.read(),
                                             file_name=f'{project}.ply'
                                             )
        return download_button


if uploaded_files is not None:
    if st.button('Upload photos and start training'):
        counter = 0
        for file in uploaded_files:
            files_to_bucket(file, aws_bucket, file.name, project_name)
            counter += 1

        st.success(f'Successfully uploaded {counter} files')
        # Adding new task to QStash by request
        headers = {
            'Authorization': getenv('qstashAuthorization'),
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = f'project_name={project_name}'

        response = requests.post(f'https://qstash.upstash.io/v1/publish/{getenv("qstashTopicName")}',
                                 headers=headers, data=data)
        print(response)


# ----------------Download section

st.subheader('or download already trained 3d models to your computer')
s3_resources = boto3.resource('s3',
                              aws_access_key_id=getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=getenv('AWS_SECRET_ACCESS_KEY'))
finished_projects = s3_resources.Bucket('hoxnabucket')
list_of_ply = [obj.key for obj in finished_projects.objects.all() if obj.key.endswith('.ply')]
project_names = [pr_name.split('/')[-2] for pr_name in list_of_ply]


input_project_name = st.selectbox('Choose', (name for name in project_names))
if input_project_name:
    download_model(aws_bucket, input_project_name)
