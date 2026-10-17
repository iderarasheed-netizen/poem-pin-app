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

# --- NEW FUNCTION: Extract Text Using a PIN Map ---
def extract_text_with_pin(poem, pin):
    secret_words = []
    lines = poem.strip().split('\n')
    
    # Loop through each digit in the PIN
    for line_index, digit_char in enumerate(pin):
        # Safety check if poem has fewer lines than the PIN length
        if line_index >= len(lines):
            break
            
        words = lines[line_index].split()
        word_index = int(digit_char) # Convert pin digit to numerical index
        
        # If the line has enough words, grab the secret word
        if word_index < len(words):
            secret_words.append(words[word_index])
        else:
            secret_words.append("[missing]")
            
    return " ".join(secret_words)

# --- Streamlit UI App Setup ---
st.set_page_config(page_title="Poem PIN Steganography", page_icon="🔐")
st.title("🔐 Poem PIN Steganography App")
st.write("Hide secret PIN codes inside text, or decode hidden messages.")

# Added a 3rd Tab for Text Decoding
tab1, tab2, tab3 = st.tabs(["🕵️ Extract a PIN", "🛠️ Encode a PIN", "🔓 Reveal Hidden Text"])

with tab1:
    st.header("Extract Hidden PIN")
    uploaded_file = st.file_uploader("Upload an encoded poem (.txt file)", type=["txt"], key="extractor_file")
    if uploaded_file is not None:
        user_poem = uploaded_file.read().decode("utf-8")
    else:
        user_poem = st.text_area("Or paste your poem manually here:", height=150, value="Stars and the moon\nshine in the sky\nwhite and\nuntil the end of the night")
    if st.button("Extract Code", type="primary"):
        extracted_pin = pin_extractor(user_poem)
        st.success(f"The extracted secret key is: **{extracted_pin}**")

with tab2:
    st.header("Encode Custom PIN")
    template_file = st.file_uploader("Upload a template poem (.txt file)", type=["txt"], key="encoder_file")
    if template_file is not None:
        base_text = template_file.read().decode("utf-8")
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
            st.download_button(label="📥 Download Encoded Poem as .txt", data=result_poem, file_name="secret_poem.txt", mime="text/plain")

# --- NEW TAB INTERFACE ---
with tab3:
    st.header("🔓 Reveal Hidden Text via PIN Map")
    st.write("Provide an encoded text block and a numeric PIN key to extract the hidden phrase.")
    
    decode_poem = st.text_area(
        "Paste the poem/text block:",
        height=150,
        value="The secret agent arrived early\nHe looked around the busy station\nTrying to spot the contact person\nBefore the train departed fast"
    )
    decode_pin = st.text_input("Enter the Numeric PIN Key (e.g., 1321):", value="1321")
    
    if st.button("Decode Secret Message", type="secondary"):
        if not decode_pin.isdigit():
            st.error("The PIN key must contain numbers only.")
        else:
            hidden_message = extract_text_with_pin(decode_poem, decode_pin)
            st.success(f"🔓 The hidden text message is: **{hidden_message}**")
