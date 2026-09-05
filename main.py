import streamlit as st
from post_generator import generate_post
from few_shot import FewShotPosts

# Constants
LENGTH_OPTIONS = ["Short", "Medium", "Long"]
LANGUAGE_OPTIONS = ["English", "Hinglish"]

def main():
    st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS for UI/UX improvements
    st.markdown("""
    <style>
    /* Modern, clean background mimicking LinkedIn feed */
    .stApp {
        background-color: #f3f2ef;
    }
    
    /* Header styling */
    .hero-container {
        text-align: center;
        padding: 3rem 0 1rem 0;
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .hero-title {
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #000000;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #555555;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        margin-bottom: 2rem;
    }

    /* LinkedIn Post Mockup Card */
    .linkedin-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 0 0 1px rgba(0,0,0,0.08), 0 2px 3px rgba(0,0,0,0.1);
        margin: 20px auto;
        max-width: 600px; 
    }
    .linkedin-header {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
    }
    .profile-pic {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background-color: #e9e9df;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        margin-right: 12px;
    }
    .profile-info {
        display: flex;
        flex-direction: column;
    }
    .profile-name {
        font-weight: 600;
        color: #000000;
        font-size: 14px;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .profile-headline {
        color: #666666;
        font-size: 12px;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .linkedin-content {
        color: #000000;
        font-size: 14px;
        line-height: 1.5;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        white-space: pre-wrap;
    }

    /* Primary Button Styling */
    div.stButton > button {
        background-color: #0a66c2;
        color: white;
        border-radius: 24px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        border: none;
        width: 100%;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #004182;
        color: white;
    }
    div.stButton > button:active {
        background-color: #004182;
        color: white;
    }
    div.stButton > button:focus {
        box-shadow: none;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    fs = FewShotPosts()

    # Sidebar Configuration
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", width=60)
    st.sidebar.title("Post Settings")
    st.sidebar.markdown("Configure your post parameters below.")
    st.sidebar.divider()

    selected_tag = st.sidebar.selectbox("🎯 Select a Topic", options=fs.get_tags())
    selected_length = st.sidebar.selectbox("📏 Select Length", options=LENGTH_OPTIONS)
    selected_language = st.sidebar.selectbox("🌐 Select Language", options=LANGUAGE_OPTIONS)

    st.sidebar.divider()
    generate_clicked = st.sidebar.button("🚀 Generate Post")

    # Main Hero Section
    st.markdown(
        '''
        <div class="hero-container">
            <div class="hero-title">LinkedIn Post Generator</div>
            <div class="hero-subtitle">Craft professional, engaging, and high-converting LinkedIn posts in seconds with AI.</div>
        </div>
        ''', unsafe_allow_html=True
    )

    # Output Section
    if generate_clicked:
        # Loading State with engaging messages
        with st.status("Crafting your perfect post...", expanded=True) as status:
            st.write("🔍 Analyzing the topic...")
            st.write("✨ Applying LinkedIn best practices...")
            post = generate_post(selected_length, selected_language, selected_tag)
            status.update(label="Post Generated Successfully!", state="complete", expanded=False)
            
        st.toast("Your LinkedIn post is ready! 🎉")
        
        # Format the post content to handle HTML newlines just in case
        post_html = post.replace('<', '&lt;').replace('>', '&gt;')

        # Display the Mockup
        st.markdown(f'''
        <div class="linkedin-card">
            <div class="linkedin-header">
                <div class="profile-pic">👤</div>
                <div class="profile-info">
                    <span class="profile-name">Your Name</span>
                    <span class="profile-headline">LinkedIn Top Voice | Industry Expert</span>
                </div>
            </div>
            <div class="linkedin-content">{post_html}</div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Raw Output for Easy Copying
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            with st.expander("📝 Show raw text (Easy to copy)", expanded=False):
                st.code(post, language="text")

if __name__ == "__main__":
    main()
