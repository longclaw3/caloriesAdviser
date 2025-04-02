import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini AI response
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')  # ✅ Updated to latest model
    response = model.generate_content([input_prompt, image])  # ✅ Pass actual image, not dict
    return response.text

# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)  # ✅ Convert file to PIL Image
        return image  # ✅ Return the actual PIL image
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI setup
st.set_page_config(page_title="Calories Advisor App")
st.header("Calories Advisor APP")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image.", use_column_width=True)

# Define input prompt
input_prompt = """
You are an expert nutritionist. Analyze the food items from the image, 
calculate the total calories, and provide a breakdown as follows:

1. Item 1 - No of calories
2. Item 2 - No of calories
---
Finally, indicate whether the food is healthy or not. Also, provide a percentage 
split of carbohydrates, fats, fibers, sugar, and other essential nutrients.
"""

submit = st.button('Tell me about the total calories')

if submit:
    if uploaded_file:
        try:
            image_data = input_image_setup(uploaded_file)  # ✅ Now returns a PIL image
            response = get_gemini_response(input_prompt, image_data)  # ✅ Correct format
            st.header("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please upload an image first.")
