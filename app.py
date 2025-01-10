import requests
import streamlit as st

# Custom CSS for pills, examples, and footer
st.markdown(
    """
    <style>
    .pill {
        display: inline-block;
        padding: 0.4em 0.8em;
        margin: 0.2em;
        background-color: #e1f5fe;
        color: #0277bd;
        border-radius: 50px;
        font-size: 0.9em;
        font-weight: bold;
        box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    .example {
        color: #ff5722;
        font-style: italic;
        margin-left: 1em;
    }
    footer {
        text-align: center;
        margin-top: 2em;
        font-size: 0.9em;
        color: #888;
    }
    footer a {
        color: #0277bd;
        text-decoration: none;
        font-weight: bold;
    }
    footer a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to fetch word data
def fetch_word_data(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to display data
def display_word_data(word_data):
    for entry in word_data:
        st.markdown(f"## 🚀 {entry.get('word', 'Unknown Word')}")
        
        # Phonetics Section
        if "phonetics" in entry:
            st.markdown("### 🔊 Phonetics")
            col1, col2 = st.columns([1, 3], border=False)
            with col1:
                for phonetic in entry["phonetics"]:
                    if "text" in phonetic:
                        st.write(f"**Phonetic:** {phonetic['text']}")
            with col2:
                for phonetic in entry["phonetics"]:
                    if "audio" in phonetic and phonetic["audio"]:
                        st.audio(phonetic["audio"])
        
        # Origin Section
        if "origin" in entry:
            st.markdown("### 📜 Origin")
            st.write(entry["origin"])
        
        # Meanings Section
        if "meanings" in entry:
            st.markdown("### 📖 Meanings")
            for meaning in entry["meanings"]:
                st.subheader(f"**{meaning['partOfSpeech']}**")
                for definition in meaning["definitions"]:
                    st.markdown(f"🔹 {definition['definition']}")
                    
                    # Example with expander
                    if "example" in definition:
                        with st.expander("📜 Example"):
                            st.markdown(f"<span class='example'>{definition['example']}</span>", unsafe_allow_html=True)
                    
                    # Synonyms as pills
                    if definition.get("synonyms"):
                        st.markdown("#### ✨ Synonyms")
                        synonym_pills = "".join(
                            f"<span class='pill'>{synonym}</span>" for synonym in definition["synonyms"]
                        )
                        st.markdown(synonym_pills, unsafe_allow_html=True)

# Streamlit App
st.title("📚 **Dictionary App**")
st.write("Enter a word to get its definition, phonetics, origin, and more!")

# Input word
word = st.text_input("🔍 **Search Word**", "")

if word:
    word_data = fetch_word_data(word)
    if word_data:
        display_word_data(word_data)
    else:
        st.error("Word not found or error fetching data.")

# Footer
st.markdown(
    """
    <footer>
        Made with 💖 by <a href="https://linkedin.com/in/ian-wanjala-ke" target="_blank">Ian</a>.
    </footer>
    """,
    unsafe_allow_html=True,
)
