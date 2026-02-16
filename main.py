import os
from dotenv import load_dotenv,dotenv_values
from groq import Groq
import streamlit as st

load_dotenv()

#print(os.getenv('GROQ_API_KEY'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
st.title("LEGALEASE : Automated Legal Document SImplifier")
st.write("Turn complex legalese into plain English instantly.")

def Simplify(raw_text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {'role':'system',"content":"You are a legal document expert. Rewrite the text in Plain English for a student. Use bullet points."},
            {"role": "user", "content": f"Simplify this: {raw_text}"}
        ]
    )
    return response.choices[0].message.content


raw_text = st.text_area("Paste your Legal Clause Here",height=200)

if st.button("Simplify Now"):
    if raw_text:
        with st.spinner("Processing..."):
            result = Simplify(raw_text)
            st.subheader("Simplified Version")
            st.success(result)

            
    else:
        st.warning("Please paste some text first!")



complex_legalese = """
The Lessee shall be entitled at any time during the said term to install, erect, 
fix and set up such internal partitions, walls and electrical and sanitary 
and other fixtures and fittings, counters, vaults, lockers, cabinets, doors, 
gates, air-conditioning plants in the demised premises and every part thereof 
as shall be required by the Lessee and the same shall remain the property of 
the Lessee and the Lessee shall be entitled to remove the same at any time.
"""



# def test_brain():
#     print("Sending complex Indian Lease Clause to Groq...")
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": "You are a legal document expert. Rewrite the text in Plain English for a student. Use bullet points."},
#             {"role": "user", "content": f"Simplify this: {complex_legalese}"}
#         ]
#     )
#     return response.choices[0].message.content
    
#     print("\n--- LegalEase Simplified Test Result ---")
#     print(response.choices[0].message.content)

