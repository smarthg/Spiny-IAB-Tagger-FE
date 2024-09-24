import streamlit as st
import requests
import pandas as pd

# FastAPI Backend URL
backend_url = "https://classify-service-xzcxv4vana-ue.a.run.app//classify"

st.title("Spiny IAB Tagger")

# Load IAB Mapping CSV
iab_mapping = pd.read_csv("iab_mapping.csv")

# Text input area
text_input = st.text_area("Enter your text:", height=200)

# Submit button
if st.button("Tag Article"):
    if text_input:
        # Call the FastAPI backend to classify text
        payload = {"text": text_input}
        response = requests.post(backend_url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            # Display the categories
            st.subheader("Categories:")
            for category in result[0]["categories"][:4]:
                category_name = category['name']
                similarity = category['similarity']
                
                # Find the corresponding IAB category
                iab_category = iab_mapping[iab_mapping['IAB'] == category_name]
                
                if not iab_category.empty:
                    iab_info = iab_category.iloc[0]
                    iab_display = f"""
                    **Unique ID:** {iab_info['Unique ID']}  
                    **Parent:** {iab_info['Parent']}  
                    **Name:** {iab_info['Name']}  
                    **Tier 1:** <span style="background-color: #ffcccb; padding: 5px; border-radius: 5px;">{iab_info['Tier 1']}</span>  
                    """
                    if pd.notna(iab_info['Tier 2']):
                        iab_display += f"**Tier 2:** <span style='background-color: #add8e6; padding: 5px; border-radius: 5px;'>{iab_info['Tier 2']}</span>  \n"
                    if pd.notna(iab_info['Tier 3']):
                        iab_display += f"**Tier 3:** <span style='background-color: #90ee90; padding: 5px; border-radius: 5px;'>{iab_info['Tier 3']}</span>  \n"
                    if pd.notna(iab_info['Tier 4']):
                        iab_display += f"**Tier 4:** <span style='background-color: #ffb6c1; padding: 5px; border-radius: 5px;'>{iab_info['Tier 4']}</span>  \n"
                else:
                    iab_display = "IAB category not found"
                
                # Display the category with rich UI
                st.markdown(f"**{category_name}** (Similarity: {similarity:.2f})")
                st.markdown(iab_display, unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.error("Error occurred while classifying text.")
    else:
        st.error("Please enter some text to classify.")
