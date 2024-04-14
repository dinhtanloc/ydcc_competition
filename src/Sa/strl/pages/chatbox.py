# Contents of ~/my_app/pages/page_3.py


import streamlit as st
import openai
import cv2
# Load model directly
from transformers import AutoImageProcessor, AutoModelForImageClassification, ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import numpy as np

processor = AutoImageProcessor.from_pretrained("prithivMLmods/Deep-Fake-Detector-Model")
model = AutoModelForImageClassification.from_pretrained("prithivMLmods/Deep-Fake-Detector-Model")

# Load pre-trained GPT-2 model and tokenizer
feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')

def predict(model,image):
    # y_pred=model.predict(img)
    # predicted_label = np.argmax(y_pred, axis=1)
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    return model.config.id2label[predicted_class_idx]
    # return predicted_label






# App title
st.set_page_config(page_title="ChatBox")
st.markdown("# ChatBox")
st.sidebar.markdown("# ChatBox")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
openai.api_key = "Your API Key"

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
      model="ft:gpt-3.5-turbo-0125:ueh::9DUn0U80",  
      messages=[{"role": "system", "content": "You are cybersecurity specialist. Please answer any question concern about security problem!"}, {"role": "user", "content": prompt}],
      max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def display_chat_message(role, content):
    st.write(content)

for message in st.session_state.messages:
    display_chat_message(message["role"], message["content"])
def is_string_empty(input_string):
    return not input_string.strip()


# User-provided prompt
prompt = st.text_area("Type here:")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

   
if st.button("Send"):
    if uploaded_file is not None and  not is_string_empty(prompt):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        st.session_state.messages.append({"role": "user", "content": f'User: {prompt}'})
        st.session_state.messages.append({"role": "assistant", "content": f'Safefriend: This pirture is {predict(model,image)} because we determine the features in the picture like eys, face,emotion,...'})

    elif  is_string_empty(prompt):
        st.session_state.messages.append({"role": "assistant", "content": 'What do you need'})

    else:
        if prompt:
            st.session_state.messages.append({"role": "user", "content": f'User: {prompt}'})
            response = get_gpt_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": f'Safefriend: {response}'})
        else:
            st.warning("Please enter a prompt!")
