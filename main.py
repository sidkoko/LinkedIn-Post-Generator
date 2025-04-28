import streamlit as st
from post_generator import generate_post
from few_shot import FewShotPosts

# Constants
LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]


# Main App
def main():
    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="📝", layout="centered")

    st.title("📝 LinkedIn Post Generator")
    st.markdown("Generate engaging LinkedIn posts effortlessly!")

    fs = FewShotPosts()

    # Input Section
    with st.form("post_generator_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_tag = st.selectbox("Select a Title", options=fs.get_tags())

        with col2:
            selected_length = st.selectbox("Select Length", options=LENGTH_OPTIONS)

        with col3:
            selected_language = st.selectbox("Select Language", options=LANGUAGE_OPTIONS)

        generate_clicked = st.form_submit_button("🚀 Generate Post")

    # Output Section
    if generate_clicked:
        with st.spinner("Generating your post..."):
            post = generate_post(selected_length, selected_language, selected_tag)
            st.success("Here's your LinkedIn post!")
            st.write(post)


if __name__ == "__main__":
    main()
