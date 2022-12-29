# Streamlit installation and deployment

#### We use separated Streamlit application for uploading files
## Streamlit

Deployment instruction https://streamlit.io/cloud, 
use https://github.com/Mrhetsko/streamlit.git link streamlit or create your own app.
Requirements will be installed automatic by streamlit server.
After you copy git repository use app settings to set secrets.

## QStash

We use the QStash to create a queue of model training in case we have many machines
At the same time Streamlit upload users images and creates a task (message) for QStash application, after that QStash 
send request to free training machine.
  Go to Qstash https://console.upstash.com/qstash, SignIn, open QStash tab. Create your Topic and set the endpoint/s.
On the details tab you can generate your own cURL command and convert it to Python code here https://www.scrapingbee.com/curl-converter/python/
