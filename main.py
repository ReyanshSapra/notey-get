import streamlit as st
import string
import random
from minio import Minio
from minio.error import S3Error
from io import BytesIO

if 'currentScreen' not in st.session_state:
    st.session_state.currentScreen = "home"

if "mainUploadButton" not in st.session_state:
    st.session_state.mainUploadButton = None

if "mainGetButton" not in st.session_state:
    st.session_state.mainGetButton = None

if "uploaderName" not in st.session_state:
    st.session_state.uploaderName = None

if "uploaderTopic" not in st.session_state:
    st.session_state.uploaderTopic = None

if "nextUploaderButton" not in st.session_state:
    st.session_state.nextUploaderButton = None

if "uploader" not in st.session_state:
    st.session_state.uploader = None

if "finalUploadButton" not in st.session_state:
    st.session_state.finalUploadButton = None

if "recieveNameEntry" not in st.session_state:
    st.session_state.recieveNameEntry = None

if "recieveTopicEntry" not in st.session_state:
    st.session_state.recieveTopicEntry = None

if "recieveNextButton" not in st.session_state:
    st.session_state.recieveNextButton = None

if "found_file" not in st.session_state:
    st.session_state.found_file = None

if "bucketName" not in st.session_state:
    st.session_state.bucketName = "noteyget"

client = Minio(
    endpoint="play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    secure=True
)

hide_st_style = """
    <style>
        .stApp {background-color: #07de11;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

MainHeading = """
    <h1 style='text-align: center; color: black;'>
        Notey
        <span style='color: #4A55A2; font-size: 1.3em'>
            Get
        </span>
        <hr style='padding:0; margin:0; width: 50%; left:25%; position:absolute; border: none; border-top: 2px solid black;'>
    </h1>"""
st.markdown(MainHeading, unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.session_state.mainUploadButton = st.button("Upload Notes")
    if st.session_state.mainUploadButton:
        st.session_state.currentScreen = "upload"
        print("upload")
        st.experimental_rerun()

with col2:
    st.session_state.mainGetButton = st.button("Get Notes")
    if st.session_state.mainGetButton:
        st.session_state.currentScreen = "get"
        print("get")
        st.experimental_rerun()

if st.session_state.currentScreen == "upload":
    st.title("Upload Notes")

    st.session_state.uploaderName = st.text_input("Enter your name")
    print(st.session_state.uploaderName)

    st.session_state.uploaderTopic = st.text_input("Notes Topic")
    print(st.session_state.uploaderTopic)

    st.session_state.nextUploaderButton = st.button("Next >>")
    if st.session_state.nextUploaderButton:
        st.session_state.currentScreen = "upload2"
        print("upload2")
        st.experimental_rerun()

elif st.session_state.currentScreen == "upload2":
    st.title("Upload Notes")

    st.session_state.uploader = st.file_uploader("Upload File",
                                                 type=['png', 'jpg', 'jpeg', 'mp4', 'mp3', 'pdf', 'docx', 'txt', 'xlsx',
                                                       "pptx", "zip", "rar"],
                                                 accept_multiple_files=False,
                                                 label_visibility="collapsed",
                                                 on_change=None)

    st.session_state.finalUploadButton = st.button("Send")

    if st.session_state.finalUploadButton:
        st.session_state.currentScreen = "final upload"
        st.experimental_rerun()

elif st.session_state.currentScreen == "final upload":
    if st.session_state.uploader is None:
        st.session_state.currentScreen = "upload"
        print("select file")

    else:
        if client.bucket_exists(st.session_state.bucketName):
            new_object_name = f"{st.session_state.uploaderName}'s {st.session_state.uploaderTopic}"
            client.put_object(st.session_state.bucketName,
                              new_object_name,
                              data=st.session_state.uploader,
                              length=st.session_state.uploader.size,
                              content_type=st.session_state.uploader.type)
        else:
            client.make_bucket(st.session_state.bucketName)
            new_object_name = f"{st.session_state.uploaderName}'s {st.session_state.uploaderTopic}"
            client.put_object(st.session_state.bucketName,
                              new_object_name,
                              data=st.session_state.uploader,
                              length=st.session_state.uploader.size,
                              content_type=st.session_state.uploader.type)

        st.subheader("File Uploaded Successfully")
        print("uploaded")

elif st.session_state.currentScreen == "get":
    st.title("Receive Notes")
    st.session_state.recieveNameEntry = st.text_input(label="Who's notes do you want?", label_visibility="hidden")
    st.session_state.recieveTopicEntry = st.text_input(label="What subject?", label_visibility="hidden")

    st.session_state.recieveNextButton = st.button("Next >>")

    if st.session_state.recieveNextButton:
        st.session_state.currentScreen = "receive2"
        print("receive2")
        st.experimental_rerun()

elif st.session_state.currentScreen == "receive2":
    if st.session_state.recieveNameEntry is None or st.session_state.recieveTopicEntry is None:
        st.session_state.currentScreen = "get"
        print("select file")
    else:
        st.title("Receive Notes")
        try:
            objects = client.list_objects(st.session_state.bucketName,
                                          prefix=f"{st.session_state.recieveNameEntry}'s {st.session_state.recieveTopicEntry}")

            for obj in objects:
                if obj.object_name == f"{st.session_state.recieveNameEntry}'s {st.session_state.recieveTopicEntry}":
                    st.session_state.found_file = obj.object_name
                    break

            if st.session_state.found_file:
                st.session_state.fileToDownload = client.get_object(st.session_state.bucketName,
                                                                    st.session_state.found_file)

                fileData = BytesIO(st.session_state.fileToDownload.read())

                st.session_state.downloadButton = st.download_button(label="Download File", data=fileData,
                                                                     file_name=st.session_state.found_file)

                if st.session_state.downloadButton:
                    print("successfully downloaded")

                else:
                    print("didnt work...")

            else:
                st.warning("No file found with the provided name and topic.")
        except S3Error as e:
            print(f"Error occurred: {e}")