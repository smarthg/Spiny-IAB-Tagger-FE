import streamlit as st
import requests

# FastAPI Backend URL
backend_url = "https://classify-service-xzcxv4vana-ue.a.run.app/classify"

st.title("Text Classification App")

# Text input area
text_input = st.text_area("Enter your text:", height=200)

# Submit button
if st.button("Classify Text"):
    if text_input:
        # Call the FastAPI backend to classify text
        payload = {"text": text_input}
        response = requests.post(backend_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # Display the categories
            st.subheader("Categories:")
            for category in result[0]["categories"]:
                st.write(f"- **{category['name']}** (Similarity: {category['similarity']:.2f})")
        else:
            st.error("Error occurred while classifying text.")
    else:
        st.error("Please enter some text to classify.")

