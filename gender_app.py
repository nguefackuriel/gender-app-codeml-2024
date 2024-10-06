import streamlit as st
import pandas as pd
import openai

df = pd.read_csv('data_gender.csv')

# OpenAI API Key 
openai.api_key = "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"#st.secrets["OPENAI_API_KEY"]


# Function to modify the sentence based on gender choice using the dataframe as support
def preprocess_sentence(input_text, gender):
    words = input_text.split()
    processed_sentence = []
    
    for word in words:
        row = df[df['Key Term'].str.lower() == word.lower()]
        if not row.empty:
            if gender == 'Male':
                replacement = row['Gendered Translation (Male)'].values[0]
            elif gender == 'Female':
                replacement = row['Gendered Translation (Female)'].values[0]
            else:
                replacement = row['Neutral Translation'].values[0]
            processed_sentence.append(replacement)
        else:
            processed_sentence.append(word)
    
    return ' '.join(processed_sentence)


    

# Function to get translation using OpenAI API
def translate_with_openai(input_text, gender):
    prompt = f"Translate the following English sentence into French considering {gender} gender sensitivity: '{input_text}'"

    system_content = prompt
    user_content = input_text
    chat_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ]
        )


    return chat_response.choices[0].message.content.strip()#response.choices[0].text.strip()




st.title("Gender-Sensitive Translation App")

st.write("""
This app allows you to translate English sentences into French with gender-sensitive options.
Choose a sentence and select the gender for the translation.
""")

# Text input for the user
input_text = st.text_input("Enter the sentence you want to translate:")

# Dropdown for gender selection
gender = st.selectbox("Select Gender for Translation", ["Male", "Female", "Neutral"])


if st.button("Translate"):
    # Preprocess the input sentence to apply contextual, gender-based changes
    preprocessed_text = preprocess_sentence(input_text, gender)
    
    # Translation
    translation = translate_with_openai(preprocessed_text, gender)
    
    st.markdown(f"Translation: {translation}")
