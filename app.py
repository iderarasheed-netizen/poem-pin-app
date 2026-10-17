import streamlit as st

# --- Core Logic Functions ---
def pin_extractor(poem):
    secret_code = ''
    lines = poem.split('\n')
    for line_index, line in enumerate(lines):
        words = line.split()
        if len(words) > line_index:
            secret_code += str(len(words[line_index]))
        else:
            secret_code += '0'
    return secret_code

def pin_encoder(base_poem, target_pin):
    lines = base_poem.strip().split('\n')
    encoded_lines = []
    for line_index, line in enumerate(lines):
        words = line.split()
        if line_index < len(target_pin):
            target_length = int(target_pin[line_index])
            while len(words) <= line_index:
                words.append("text")
            words[line_index] = "x" * target_length 
        encoded_lines.append(" ".join(words))
    return "\n".join(encoded_lines)

# --- Streamlit UI App Setup ---
st.set_page_config(page_title="Poem PIN Steganography", page_icon="🔐")
st.title("🔐 Poem PIN Steganography App")
st.write("Hide secret PIN codes inside text, or extract keys from encoded poems.")

tab1, tab2 = st.tabs(["🕵️ Extract a PIN", "🛠 Encode a PIN"])

with tab1:
    st.header("Extract Hidden PIN")
    
    # File Uploader component
    uploaded_file = st.file_uploader("Upload an encoded poem (.txt file)", type=["txt"], key="extractor_file")
    
    # Use uploaded text if available, otherwise use text area
    if uploaded_file is not None:
        user_poem = uploaded_file.read().decode("utf-8")
        st.info("File uploaded successfully! Preview:")
        st.text_area("File Content Preview", user_poem, height=100, disabled=True)
    else:
        user_poem = st.text_area("Or paste your poem manually here:", height=150, value="Stars and the moon\nshine in the sky\nwhite and\nuntil the end of the night")
        
    if st.button("Extract Code", type="primary"):
        extracted_pin = pin_extractor(user_poem)
        st.success(f"The extracted secret key is: **{extracted_pin}**")

with tab2:
    st.header("Encode Custom PIN")
    
    # File Uploader for template
    template_file = st.file_uploader("Upload a template poem (.txt file)", type=["txt"], key="encoder_file")
    
    if template_file is not None:
        base_text = template_file.read().decode("utf-8")
        st.info("Template file uploaded successfully!")
    else:
        base_text = st.text_area("Or enter a template text/poem manually:", height=150, value="Birds fly high\nup in air\nclouds are passing\nlate at night")
        
    custom_pin = st.text_input("Enter your secret numeric PIN (e.g., 4263):", value="4263")
    
    if st.button("Generate Encoded Poem"):
        if not custom_pin.isdigit():
            st.error("Please enter numbers only for the PIN.")
        elif len(custom_pin) > len(base_text.split('\n')):
            st.warning("Your template poem needs more lines to accommodate this PIN length!")
        else:
            result_poem = pin_encoder(base_text, custom_pin)
            st.subheader("Your Encoded Poem:")
            st.code(result_poem, language="text")
            
            # Allow user to download the generated file directly
            st.download_button(
                label="📥 Download Encoded Poem as .txt",
                data=result_poem,
                file_name="secret_poem.txt",
                mime="text/plain"
            )
