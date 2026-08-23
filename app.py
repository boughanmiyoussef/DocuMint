import streamlit as st
import os
import tempfile
from populate_database import ingest_file, clear_database
from query_data import query_rag

# Professional page config
st.set_page_config(
    page_title="DocuMint - Intelligent Document Q&A",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global styling - adapts to theme */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 900px;
    }
    
    /* Title styling */
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        font-size: 1rem;
        color: var(--text-color-secondary);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Chat container */
    .chat-container {
        background: var(--background-color);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: var(--shadow);
        min-height: 400px;
        max-height: 550px;
        overflow-y: auto;
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 85%;
        word-wrap: break-word;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    
    .assistant-message {
        background: var(--message-bg);
        color: var(--text-color);
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border-left: 4px solid #667eea;
    }
    
    .message-role {
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.7;
        margin-bottom: 0.2rem;
    }
    
    .user-message .message-role {
        color: rgba(255,255,255,0.8);
    }
    
    .assistant-message .message-role {
        color: var(--text-color-secondary);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border: 2px solid var(--border-color);
        border-radius: 25px;
        padding: 0.7rem 1.5rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background-color: var(--input-bg);
        color: var(--text-color);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background-color: var(--input-bg);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-color-secondary);
        opacity: 0.7;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Secondary button */
    .stButton > button[data-baseweb="button"]:not(.st-emotion-cache-1r6slb0) {
        background: transparent !important;
        color: #667eea !important;
        border: 2px solid #667eea;
    }
    
    /* Upload section */
    .upload-section {
        background: var(--upload-bg);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed var(--border-color);
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #667eea;
    }
    
    .upload-section h4 {
        color: var(--text-color);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .upload-section p {
        color: var(--text-color-secondary);
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--sidebar-bg);
    }
    
    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    
    .sidebar-section {
        margin-bottom: 1.5rem;
    }
    
    .sidebar-section h4 {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-color-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    /* Status indicator */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        background: #28a745;
        color: white;
        margin-top: 0.5rem;
    }
    
    /* Separator */
    .custom-divider {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #667eea, transparent);
        margin: 1.5rem 0;
    }
    
    /* Conversation header */
    .conversation-header {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .conversation-header span {
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 3rem 0;
        color: var(--text-color-secondary);
    }
    
    .empty-state h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        font-size: 0.95rem;
        opacity: 0.8;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        font-size: 0.8rem;
        color: var(--text-color-secondary);
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border-color);
        opacity: 0.7;
    }
    
    /* Scrollbar styling */
    .chat-container::-webkit-scrollbar {
        width: 4px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: var(--scrollbar-track);
        border-radius: 10px;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    /* Theme variables - Light mode (default) */
    :root {
        --text-color: #1a1a2e;
        --text-color-secondary: #6c757d;
        --background-color: #ffffff;
        --sidebar-bg: #f8f9fa;
        --message-bg: #f1f3f5;
        --input-bg: #f8f9fa;
        --upload-bg: #f8f9fa;
        --border-color: #e9ecef;
        --shadow: 0 2px 8px rgba(0,0,0,0.05);
        --scrollbar-track: #f1f1f1;
    }
    
    /* Dark mode overrides */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #e9ecef;
            --text-color-secondary: #adb5bd;
            --background-color: #1a1a2e;
            --sidebar-bg: #16213e;
            --message-bg: #2d2d44;
            --input-bg: #2d2d44;
            --upload-bg: #2d2d44;
            --border-color: #3d3d5c;
            --shadow: 0 2px 8px rgba(0,0,0,0.3);
            --scrollbar-track: #2d2d44;
        }
        
        .stApp {
            background: #1a1a2e;
        }
        
        .stSidebar {
            background: #16213e !important;
        }
        
        .stSelectbox > div > div {
            background: #2d2d44 !important;
            color: #e9ecef !important;
        }
        
        .stSelectbox label {
            color: #e9ecef !important;
        }
        
        .css-1d391kg .stMarkdown {
            color: #e9ecef !important;
        }
        
        .stSidebar .stMarkdown p {
            color: #e9ecef !important;
        }
        
        .stSidebar .stMarkdown h1,
        .stSidebar .stMarkdown h2,
        .stSidebar .stMarkdown h3,
        .stSidebar .stMarkdown h4 {
            color: #e9ecef !important;
        }
        
        .stSelectbox > div > div > div {
            background-color: #2d2d44 !important;
            color: #e9ecef !important;
        }
        
        .stFileUploader > div > div {
            background: #2d2d44 !important;
        }
        
        .stFileUploader label {
            color: #e9ecef !important;
        }
        
        .stAlert {
            background: #2d2d44 !important;
        }
        
        .stAlert p {
            color: #e9ecef !important;
        }
        
        .stSpinner > div {
            color: #e9ecef !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #2d2d44 !important;
            color: #e9ecef !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #adb5bd !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'show_upload' not in st.session_state:
    st.session_state['show_upload'] = False

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧠 DocuMint</div>', unsafe_allow_html=True)
    
    # Model Selection
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h4>🧠 Model Selection</h4>', unsafe_allow_html=True)
    
    model_options = ["phi3:mini", "tinyllama"]
    selected_model = st.selectbox(
        "Choose LLM Model",
        model_options,
        index=0,
        help="Select which Ollama model to use for answering questions"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h4>📤 Document Management</h4>', unsafe_allow_html=True)
    
    if st.button("📄 " + ("Hide Upload" if st.session_state['show_upload'] else "Add Document"), 
                 use_container_width=True, type="secondary"):
        st.session_state['show_upload'] = not st.session_state['show_upload']
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h4>⚙️ Settings</h4>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state['chat_history'] = []
        st.rerun()
    
    if st.button("🧹 Clear Database", use_container_width=True, type="secondary"):
        with st.spinner("Clearing database..."):
            clear_database()
            st.session_state['chat_history'] = []
        st.success("✅ Database cleared!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System status
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<h4>📊 System Status</h4>', unsafe_allow_html=True)
    st.markdown('<span class="status-badge">● Online</span>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.8rem;color:var(--text-color-secondary);margin-top:0.5rem;">🧠 Model: {selected_model}<br>📚 Documents: Ready</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:0.7rem;color:var(--text-color-secondary);opacity:0.7;">DocuMint v1.0<br>Powered by RAG</p>', unsafe_allow_html=True)

# ============================================
# MAIN AREA
# ============================================

# Title
st.markdown('<div class="app-title">🧠 DocuMint</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Intelligent Document Q&A · Powered by RAG</div>', unsafe_allow_html=True)

# Upload section
if st.session_state['show_upload']:
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown('<h4>📄 Upload PDF Document</h4>', unsafe_allow_html=True)
        st.markdown('<p>Drag and drop or browse to upload</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("🔄 Processing document..."):
                result = ingest_file(file_path)
            st.success(f"✅ {uploaded_file.name} added successfully")
            st.session_state['show_upload'] = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state['chat_history']:
    st.markdown('<div class="conversation-header"><span>💬</span> Conversation</div>', unsafe_allow_html=True)
    
    for i, (question, answer) in enumerate(reversed(st.session_state['chat_history'])):
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-role">You</div>
            {question}
        </div>
        """, unsafe_allow_html=True)
        
        # Assistant message
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <div class="message-role">Assistant</div>
            {answer}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div style="font-size:3rem;margin-bottom:1rem;">🧠</div>
        <h3>Ask me anything about your documents</h3>
        <p>Upload a PDF and start asking questions</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
with st.container():
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("", placeholder="Ask a question about your documents...", label_visibility="collapsed")
        with col2:
            submit_button = st.form_submit_button("Send", use_container_width=True)
    
    if submit_button and user_input:
        with st.spinner("🧠 Thinking..."):
            try:
                answer = query_rag(user_input, model_name=selected_model)
            except Exception as e:
                answer = f"I encountered an error: {str(e)}"
        
        st.session_state['chat_history'].append((user_input, answer))
        st.rerun()

# Footer
st.markdown('<div class="app-footer">🔒 All processing is local · Your data never leaves your computer</div>', unsafe_allow_html=True)