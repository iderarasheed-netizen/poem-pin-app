# 🔐 Poem PIN Steganography App

An interactive text-based steganography web application built with **Python** and **Streamlit**. This app allows users to hide secret numeric PIN codes within ordinary poetry or extract hidden keys out of text files using structural character counts.

## 🚀 Live Demo
Once deployed, add your public Streamlit URL link here! 
*(e.g., https://streamlit.app)*

---

## ✨ Features
* **🕵️ PIN Extraction:** Scan custom poems or text files to retrieve secret numeric codes instantly.
* **🛠️ Custom PIN Encoding:** Input your own custom numeric key and structural template text to generate a brand new hidden-code poem.
* **📁 File Handling:** Drag-and-drop support to directly upload `.txt` files for fast extraction or encoding.
* **📥 Instant Download:** Export your newly generated secret poems back to your machine with a single click.

---

## 🛠️ How It Works (The Logic)
The tool works by checking word counts line-by-line using its matching line index position:
1. **Line 0** checks the character length of **Word 0**.
2. **Line 1** checks the character length of **Word 1**.
3. **Line 2** checks the character length of **Word 2**, and so on.
4. If a text line contains fewer words than its line number index, the app automatically scales or inserts default placeholder values (`0` or padding text) to maintain code integrity.

---

## 💻 Local Setup Instructions

If you want to run this project on your local machine, follow these steps:

### 1. Clone or Download the Files
Make sure you have `app.py` and `requirements.txt` in the same project directory.

### 2. Install Dependencies
Open your Terminal or Command Prompt in that directory and run:
```bash
pip install -r requirements.txt
```

### 3. Launch the Web Application
```bash
streamlit run app.py
```
Your default browser will automatically launch and display the interface at `http://localhost:8501`.

---

## 📦 Technologies Used
* **Python 3** - Core application programming language
* **Streamlit** - Rapid UI deployment framework for script rendering
