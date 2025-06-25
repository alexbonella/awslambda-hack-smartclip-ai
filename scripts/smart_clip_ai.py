import streamlit as st
from PIL import Image
import boto3

image = Image.open('media/app2_aws.png')
st.sidebar.image(image, caption="AWS Smart Clip AI", width=256)
app_mode = st.sidebar.selectbox("Choose app mode", ["Run App", "About Me"])

S3_BUCKET_NAME = st.secrets['aws']['S3_BUCKET_NAME']
S3_RAW_BUCKET = st.secrets['aws']['S3_RAW_BUCKET']

s3 = boto3.client(
    's3',
    aws_access_key_id=st.secrets['aws']['AWS_ACCESS_KEY'],
    aws_secret_access_key=st.secrets['aws']['AWS_SECRET_KEY'],
    region_name='us-east-1'
)

if app_mode == 'Run App':
    st.title("Welcome to AWS Smart Clip AI App")
    st.success(" Summarize your video using AI and AWS power infrastratcture👇 ")
    c1,c2,c3,c4 = st.columns((20,10,8,1))
    uploaded_file = c1.file_uploader("Upload Video to S3", type=["mp4"]) 
    audience_objectives = ["Entertain","Educate","Inspire","Build Community","Social Impact","Promote a Product","Showcase Expertise","Awareness"]
    choose_audience =  c2.selectbox("Choose Audience Goals", audience_objectives)
    if c3.button('Upload Video'):

        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())   
        try:
            s3.upload_file(uploaded_file.name, S3_RAW_BUCKET, Key=f'video-input/{uploaded_file.name.split(".mp4")[0]}_audience-{choose_audience.replace(" ","")}.mp4')
            st.success(f'The {uploaded_file.name.split(".mp4")[0]}_audience-{choose_audience.replace(" ","")}.mp4 file upload succesfully to the {S3_BUCKET_NAME} Bucket')
        except Exception as e:
            st.error(f"Error al subir el archivo: {e}")

elif app_mode == "About Me":
    st.title('Smart Clip AI App')
    st.success("Feel free to contacting me here 👇 ")
    col1, col2, col3, col4 = st.columns((2, 1, 2, 1)) 
    col1.page_link("https://datexland.medium.com/", label="**Blog**", icon="🗒️")
    col1.page_link("https://alexbonella.github.io/", label="**Website**", icon="🌎")
    col1.page_link("https://www.linkedin.com/in/alexanderbolano/", label="**LinkedIn**", icon="📌")
    col1.page_link("https://twitter.com/datexland", label="**X**", icon="📝")
    image2 = Image.open('media/perfil_2.jpeg')
    col3.image(image2, width=230)