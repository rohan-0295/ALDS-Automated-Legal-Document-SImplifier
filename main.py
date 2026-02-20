import os
from dotenv import load_dotenv,dotenv_values
from groq import Groq
import streamlit as st
from pypdf import PdfReader
import pdfplumber

load_dotenv()

#print(os.getenv('GROQ_API_KEY'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))
st.title("LEGALEASE : Automated Legal Document SImplifier")
st.write("Turn complex legalese into plain English instantly.")
raw_text = ""

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1048/1048953.png", width=100) # Optional Icon
    st.title("Settings")

    model_choice = st.segmented_control(
        "Select AI Model",
        options= ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"],
        default="llama-3.3-70b-versatile",
        help="70B is more accurate; 8B is faster."
    )

    tone = st.radio(
        "Simplification Tone",
        ["Plain English", "For a 5-year-old", "Action Items Only"],
        index=0
    )
    st.divider()
    st.write("Developed by **Rohan Shaw**")



uploaded_file = st.file_uploader("Upload a Legal PDF", type="pdf")

@st.cache_data
def extracted_text_from_pdf(uploaded_file):
    extracted_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_content = page.extract_text() 
            if page_content:
                extracted_text += page_content + "\n"
        return extracted_text


def Simplify(raw_text,models,selected_tone):
    response = client.chat.completions.create(
        model=models,
        messages=[
            {'role':'system',"content":f"You are a legal document expert. Rewrite the text in {selected_tone} for a student. Use bullet points."},
            {"role": "user", "content": f"Simplify this: {raw_text}"}
        ]
    )
    return response.choices[0].message.content

if uploaded_file is not None:
    raw_text = extracted_text_from_pdf(uploaded_file)
    st.info("Pdf extracted succesfully")
else:
    raw_text = st.text_area("OR Paste your Legal Clause Here", height=200)



    # reader = PdfReader(uploaded_file)
    # raw_text = reader.pages[0].extract_text()
    # st.info("Pdf succesfully extracted")






if st.button("Simplify Now",type="primary"):
    if raw_text:
        with st.spinner("Processing..."):
            result = Simplify(raw_text,model_choice,tone)
            st.divider()

            col1,col2 = st.columns(2)
            with col1:
                st.subheader("Orginal Text")
                st.text_area("Legal Text",raw_text,height=300,disabled=True)

            with col2:
                st.subheader("Simplified Version")
                with st.container(height=400):
        # We put the success message inside the scrollable container
                    st.success("Simplification Complete!")
                    st.markdown(result)
            
        st.download_button(
        label="📥 Download Summary",
        data=result,
        file_name="legal_summary.txt",
        mime="text/plain",
        use_container_width=True
    )



            
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

