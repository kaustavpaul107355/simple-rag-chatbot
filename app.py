"""
Databricks RAG Chat Application
===============================

A modern, responsive Streamlit application that provides an intuitive chat interface 
for querying SharePoint data using Databricks' Retrieval-Augmented Generation (RAG) capabilities.

Features:
- Modern glassmorphism UI design with light theme
- Interactive chat interface with enhanced visual effects
- Clickable question suggestions for easy interaction
- Real-time chat with Databricks model serving endpoints
- Responsive design with professional styling
- Session management and user authentication
- Clean sidebar with system information and help

Author: Kaustav Paul
Version: 2.0
Last Updated: 2024
"""

import logging
import os
import streamlit as st
from model_serving_utils import query_endpoint

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

def setup_page_config():
    """Configure Streamlit page settings and logging."""
    st.set_page_config(
        page_title="Databricks RAG Assistant",
        page_icon="🤖",
        layout='wide',
        initial_sidebar_state="expanded"
    )
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

def validate_environment():
    """Validate required environment variables."""
    serving_endpoint = os.getenv('SERVING_ENDPOINT')
    if not serving_endpoint:
        st.error("⚠️ SERVING_ENDPOINT environment variable is not set. Please set it in app.yaml.")
        st.stop()
    return serving_endpoint

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_user_info():
    """
    Retrieve user information from request headers.
    
    Returns:
        dict: User information including email address
    """
    try:
        headers = getattr(st.context, 'headers', {}) or {}
        return {
            'user_email': headers.get("X-Forwarded-Email", "Not available")
        }
    except Exception as e:
        logging.warning(f"Error getting user info: {e}")
        return {
            'user_email': "Not available"
        }

def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

# ============================================================================
# MODERN UI STYLING SYSTEM
# ============================================================================

def apply_modern_styling():
    """
    Apply comprehensive modern styling with glassmorphism design system.
    
    This function includes:
    - CSS custom properties for consistent theming
    - Modern light theme with vibrant gradients
    - Enhanced component styling
    - Responsive design patterns
    - Interactive hover effects and animations
    """
    st.markdown("""
    <style>
    /* ========================================================================
       DESIGN SYSTEM - CSS CUSTOM PROPERTIES
       ======================================================================== */
    
    :root {
        /* Vibrant Gradient System */
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --accent-gradient: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        --success-gradient: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        --warning-gradient: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        --error-gradient: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        
        /* Modern Light Theme Colors */
        --background-color: #fafbfc;
        --surface-primary: #ffffff;
        --surface-secondary: #f8fafc;
        --surface-tertiary: #f1f5f9;
        --surface-hover: #f8fafc;
        
        /* Typography Scale */
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --text-inverse: #ffffff;
        
        /* Border System */
        --border-light: #e2e8f0;
        --border-medium: #cbd5e1;
        --border-strong: #94a3b8;
        --border-accent: #3b82f6;
        
        /* Elevation System - Shadows */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        
        /* Semantic Color System */
        --primary-50: #eff6ff;
        --primary-100: #dbeafe;
        --primary-500: #3b82f6;
        --primary-600: #2563eb;
        --primary-700: #1d4ed8;
        
        --success-50: #f0fdf4;
        --success-500: #22c55e;
        --success-600: #16a34a;
        
        --warning-50: #fffbeb;
        --warning-500: #f59e0b;
        --warning-600: #d97706;
        
        --error-50: #fef2f2;
        --error-500: #ef4444;
        --error-600: #dc2626;
        
        /* Interactive States */
        --focus-ring: 0 0 0 3px rgba(59, 130, 246, 0.1);
        --focus-ring-success: 0 0 0 3px rgba(34, 197, 94, 0.1);
        --focus-ring-warning: 0 0 0 3px rgba(245, 158, 11, 0.1);
        --focus-ring-error: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }

    /* ========================================================================
       GLOBAL STYLES & LAYOUT
       ======================================================================== */

    * {
        box-sizing: border-box;
    }

    .stApp {
        background: var(--background-color) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        min-height: 100vh;
        line-height: 1.6;
    }

    /* Subtle background pattern for visual interest */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(250, 112, 154, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(168, 237, 234, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }

    .main .block-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 2rem 1rem !important;
    }

    /* ========================================================================
       TYPOGRAPHY SYSTEM
       ======================================================================== */

    h1 {
        background: var(--primary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 900 !important;
        font-size: 3rem !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.03em !important;
        position: relative !important;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
    }

    h1::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 120px;
        height: 4px;
        background: var(--secondary-gradient);
        border-radius: 4px;
        box-shadow: var(--shadow-md);
    }

    h3 {
        background: var(--secondary-gradient) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.75rem !important;
        letter-spacing: -0.01em !important;
    }

    /* ========================================================================
       LAYOUT COMPONENTS
       ======================================================================== */

    .stColumns {
        gap: 2.5rem !important;
        margin-top: 3rem !important;
    }

    /* Enhanced column containers with gradient accents */
    div[data-testid="column"]:nth-of-type(1) {
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        box-shadow: var(--shadow-xl) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    div[data-testid="column"]:nth-of-type(1)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 24px 24px 0 0;
    }

    div[data-testid="column"]:nth-of-type(1):hover {
        transform: translateY(-8px) !important;
        box-shadow: var(--shadow-2xl) !important;
        border-color: var(--border-accent) !important;
    }

    div[data-testid="column"]:nth-of-type(2) {
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 24px !important;
        padding: 2.5rem !important;
        min-height: 750px !important;
        box-shadow: var(--shadow-xl) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    div[data-testid="column"]:nth-of-type(2)::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--secondary-gradient);
        border-radius: 24px 24px 0 0;
    }

    div[data-testid="column"]:nth-of-type(2):hover {
        border-color: var(--border-accent) !important;
        box-shadow: var(--shadow-2xl) !important;
    }

    /* ========================================================================
       INTERACTIVE ELEMENTS
       ======================================================================== */

    /* Enhanced link styling */
    a {
        color: var(--primary-600) !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        border-bottom: 2px solid transparent !important;
        font-weight: 500 !important;
        padding: 0.25rem 0 !important;
    }

    a:hover {
        color: var(--primary-700) !important;
        border-bottom-color: var(--primary-600) !important;
        transform: translateY(-1px) !important;
    }

    /* Modern code block styling */
    .stCodeBlock {
        background: var(--surface-secondary) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 0.9rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stCodeBlock::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 16px 16px 0 0;
    }

    .stCodeBlock:hover {
        border-color: var(--border-accent) !important;
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    /* ========================================================================
       CHAT INTERFACE COMPONENTS
       ======================================================================== */

    /* Enhanced chat input with modern styling */
    .stChatInput {
        background: var(--surface-primary) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 20px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    .stChatInput:focus-within {
        border-color: var(--primary-500) !important;
        box-shadow: var(--focus-ring), var(--shadow-md) !important;
        transform: translateY(-2px) !important;
    }

    /* Enhanced Default Chat Message Styling - Compact Design */
    [data-testid="stChatMessage"] {
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        margin: 0.5rem 0 !important;
        padding: 1rem !important;
        box-shadow: 
            0 2px 6px rgba(0, 0, 0, 0.05),
            0 1px 3px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="stChatMessage"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent-gradient);
        border-radius: 12px 12px 0 0;
        z-index: 1;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 6px 15px rgba(0, 0, 0, 0.1),
            0 3px 8px rgba(0, 0, 0, 0.06) !important;
        border-color: var(--border-accent) !important;
    }

    /* User Messages - Questions (More Indented) */
    [data-testid="stChatMessage"]:has(svg[data-testid="icon-user"]) {
        background: linear-gradient(135deg, var(--surface-secondary) 0%, var(--surface-primary) 100%) !important;
        border-color: var(--border-medium) !important;
        margin-left: 4rem !important;
        margin-right: 1rem !important;
        box-shadow: 
            0 2px 8px rgba(250, 112, 154, 0.08),
            0 1px 4px rgba(250, 112, 154, 0.05) !important;
    }

    [data-testid="stChatMessage"]:has(svg[data-testid="icon-user"])::before {
        background: var(--secondary-gradient) !important;
    }

    [data-testid="stChatMessage"]:has(svg[data-testid="icon-user"]):hover {
        border-color: #fa709a !important;
        box-shadow: 
            0 8px 20px rgba(250, 112, 154, 0.15),
            0 4px 10px rgba(250, 112, 154, 0.08) !important;
    }

    /* Assistant Messages - Answers (Less Indented) */
    [data-testid="stChatMessage"]:has(svg[data-testid="icon-bot"]) {
        background: linear-gradient(135deg, var(--primary-50) 0%, var(--surface-primary) 100%) !important;
        border-color: var(--primary-200) !important;
        margin-left: 1rem !important;
        margin-right: 2rem !important;
        box-shadow: 
            0 2px 8px rgba(59, 130, 246, 0.08),
            0 1px 4px rgba(59, 130, 246, 0.05) !important;
    }

    [data-testid="stChatMessage"]:has(svg[data-testid="icon-bot"])::before {
        background: var(--primary-gradient) !important;
    }

    [data-testid="stChatMessage"]:has(svg[data-testid="icon-bot"]):hover {
        border-color: var(--primary-500) !important;
        box-shadow: 
            0 8px 20px rgba(59, 130, 246, 0.15),
            0 4px 10px rgba(59, 130, 246, 0.08) !important;
    }

    /* Chat Message Content Styling */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        font-size: 1rem !important;
        line-height: 1.6 !important;
        color: var(--text-primary) !important;
    }

    /* Chat Message Icons */
    [data-testid="stChatMessage"] svg {
        width: 1.5rem !important;
        height: 1.5rem !important;
        margin-right: 0.75rem !important;
    }

    /* Chat Message Avatar Background */
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background: var(--primary-gradient) !important;
        border-radius: 50% !important;
        padding: 0.5rem !important;
        color: white !important;
    }

    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background: var(--secondary-gradient) !important;
        border-radius: 50% !important;
        padding: 0.5rem !important;
        color: white !important;
    }

    /* ========================================================================
       BUTTON COMPONENTS
       ======================================================================== */

    /* Enhanced reset button with shimmer effect */
    .stButton > button {
        background: var(--error-gradient) !important;
        color: var(--text-inverse) !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-lg) !important;
        margin-bottom: 2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-2xl) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* Question suggestion buttons */
    .stButton[data-testid="baseButton-secondary"] button {
        background: var(--surface-secondary) !important;
        border: 2px solid var(--border-light) !important;
        border-radius: 16px !important;
        padding: 1rem 1.5rem !important;
        margin: 0.5rem 0 !important;
        width: 100% !important;
        text-align: left !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton[data-testid="baseButton-secondary"] button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
        border-radius: 16px 16px 0 0;
    }

    .stButton[data-testid="baseButton-secondary"] button:hover {
        background: var(--surface-hover) !important;
        border-color: var(--border-accent) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
        color: var(--text-primary) !important;
    }

    /* Chat History Control Buttons */
    .stButton button[data-testid*="expand_messages"],
    .stButton button[data-testid*="collapse_messages"] {
        background: var(--primary-gradient) !important;
        color: var(--text-inverse) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-sm) !important;
        white-space: nowrap !important;
    }

    .stButton button[data-testid*="expand_messages"]:hover,
    .stButton button[data-testid*="collapse_messages"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
        filter: brightness(1.1) !important;
    }

    /* Scrollable Chat Container Styling */
    .chat-history-scroll {
        scrollbar-width: thin;
        scrollbar-color: var(--border-medium) var(--surface-secondary);
    }

    .chat-history-scroll::-webkit-scrollbar {
        width: 8px;
    }

    .chat-history-scroll::-webkit-scrollbar-track {
        background: var(--surface-secondary);
        border-radius: 4px;
        margin: 8px 0;
    }

    .chat-history-scroll::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 4px;
        border: 1px solid var(--surface-secondary);
    }

    .chat-history-scroll::-webkit-scrollbar-thumb:hover {
        background: var(--border-strong);
    }

    /* ========================================================================
       SIDEBAR STYLING
       ======================================================================== */

    .stSidebar {
        background: var(--surface-primary) !important;
    }

    .stSidebar .sidebar-content {
        background: var(--surface-primary) !important;
        border-right: 1px solid var(--border-light) !important;
        padding: 1.5rem !important;
    }

    .stSidebar h2, .stSidebar h3 {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
    }

    .stSidebar h2 {
        font-size: 1.3rem !important;
    }

    .stSidebar h3 {
        font-size: 1.1rem !important;
        border-bottom: 2px solid var(--border-light) !important;
        padding-bottom: 0.5rem !important;
    }

    .stSidebar p {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
    }

    .stSidebar .stMetric {
        background: var(--surface-secondary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        margin: 0.5rem 0 !important;
    }

    .stSidebar .stInfo {
        border-radius: 12px !important;
        border: 1px solid var(--primary-100) !important;
        background: var(--primary-50) !important;
    }

    .stSidebar .stExpander {
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        background: var(--surface-secondary) !important;
    }

    /* ========================================================================
       SCROLLBAR STYLING
       ======================================================================== */

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: var(--surface-secondary);
        border-radius: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-medium);
        border-radius: 8px;
        border: 2px solid var(--surface-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--border-strong);
    }

    /* ========================================================================
       ANIMATIONS & TRANSITIONS
       ======================================================================== */

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .stChatMessage {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stChatMessage.user {
        animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ========================================================================
       RESPONSIVE DESIGN
       ======================================================================== */

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        h1 {
            font-size: 2.5rem !important;
        }
        
        .stColumns {
            gap: 1.5rem !important;
        }
        
        div[data-testid="column"] {
            padding: 2rem !important;
        }
    }

    /* ========================================================================
       COMPONENT STATES
       ======================================================================== */

    /* Loading states */
    .stSpinner {
        border: 3px solid var(--border-light) !important;
        border-top: 3px solid var(--primary-500) !important;
        border-radius: 50% !important;
        animation: spin 1s linear infinite !important;
    }

    /* Alert components */
    .stAlert {
        background: var(--error-50) !important;
        border: 2px solid var(--error-500) !important;
        border-radius: 16px !important;
        color: var(--error-600) !important;
        padding: 1rem !important;
        box-shadow: var(--shadow-md) !important;
    }

    .stSuccess {
        background: var(--success-50) !important;
        border: 2px solid var(--success-500) !important;
        border-radius: 16px !important;
        color: var(--success-600) !important;
        padding: 1rem !important;
        box-shadow: var(--shadow-md) !important;
    }

    /* Focus states for accessibility */
    *:focus {
        outline: none !important;
    }

    *:focus-visible {
        box-shadow: var(--focus-ring) !important;
        border-color: var(--primary-500) !important;
    }

    /* Fallback styles for chat messages - Compact Design */
    [data-testid="stChatMessage"] {
        background: var(--surface-primary) !important;
        border: 1px solid var(--border-light) !important;
        border-radius: 12px !important;
        margin-bottom: 0.5rem !important;
        padding: 1rem !important;
        box-shadow: 
            0 2px 6px rgba(0, 0, 0, 0.05),
            0 1px 3px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="stChatMessage"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent-gradient);
        border-radius: 12px 12px 0 0;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 
            0 6px 15px rgba(0, 0, 0, 0.1),
            0 3px 8px rgba(0, 0, 0, 0.06) !important;
        border-color: var(--border-accent) !important;
    }

    .stChatMessage.assistant, 
    [data-testid="stChatMessage"]:has(svg[data-testid="icon-bot"]) {
        background: linear-gradient(135deg, var(--primary-50) 0%, var(--surface-primary) 100%) !important;
        border-color: var(--primary-100) !important;
        margin-left: 1rem !important;
        margin-right: 2rem !important;
    }

    .stChatMessage.assistant::before {
        background: var(--primary-gradient) !important;
    }

    .stChatMessage.user {
        background: linear-gradient(135deg, var(--surface-secondary) 0%, var(--surface-primary) 100%) !important;
        border-color: var(--border-medium) !important;
        margin-left: 4rem !important;
        margin-right: 1rem !important;
    }

    .stChatMessage.user::before {
        background: var(--secondary-gradient) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# QUESTION MANAGEMENT
# ============================================================================

def get_suggested_questions():
    """
    Return a list of suggested questions for user interaction.
    
    Returns:
        list: Predefined questions about Databricks and Lakeflow
    """
    return [
        "What is Lakeflow and how does it work?",
        "How can I ingest data into Databricks using Lakeflow?",
        "What source systems are supported by Lakeflow?",
        "Explain the benefits of using Databricks for data processing"
    ]

def handle_question_selection():
    """
    Handle the selection and display of suggested questions.
    
    Returns:
        str or None: Selected question prompt or None
    """
    # Handle selected question display and confirmation
    if "selected_question" in st.session_state:
        st.info(f"📝 Selected question: {st.session_state.selected_question}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Use this question", key="use_question"):
                prompt = st.session_state.selected_question
                del st.session_state.selected_question
                return prompt
        
        with col2:
            if st.button("❌ Clear selection", key="clear_question"):
                del st.session_state.selected_question
                st.rerun()
        
        return None
    else:
        return st.chat_input("Ask me anything about your SharePoint data...")

# ============================================================================
# CHAT INTERFACE
# ============================================================================

def render_chat_interface(serving_endpoint, logger):
    """
    Render the enhanced chat interface with scrollable area and collapse/expand functionality.
    
    Args:
        serving_endpoint (str): Databricks serving endpoint
        logger: Logger instance for error handling
    """
    # Handle new message processing first
    prompt = handle_question_selection()
    
    if prompt:
        # Add user message to session
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate and display assistant response
        try:
            response = query_endpoint(
                endpoint_name=serving_endpoint,
                messages=st.session_state.messages,
                max_tokens=400,
            )
            assistant_response = response if isinstance(response, str) else response.get("content", "")
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.rerun()
        except Exception as e:
            error_message = f"Error getting response from endpoint: {str(e)}"
            logger.error(error_message)
            st.error(error_message)
    
    # Display chat messages with collapse/expand functionality
    if st.session_state.messages:
        # Determine how many messages to show
        total_messages = len(st.session_state.messages)
        show_all = st.session_state.get('show_all_messages', False)
        
        # Show collapse/expand controls if there are more than 6 messages (3 Q&A pairs)
        if total_messages > 6:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if show_all:
                    if st.button("📄 Show Recent Only", key="collapse_messages", help="Show only the latest 3 Q&A pairs"):
                        st.session_state.show_all_messages = False
                        st.rerun()
                else:
                    if st.button("📜 Show All History", key="expand_messages", help="Show complete conversation history"):
                        st.session_state.show_all_messages = True
                        st.rerun()
        
        # Determine which messages to display
        if show_all or total_messages <= 6:
            messages_to_show = st.session_state.messages
            if not show_all and total_messages > 6:
                st.info(f"Showing recent messages. Click 'Show All History' to see {total_messages - 6} earlier messages.")
        else:
            # Show only the latest 6 messages (3 Q&A pairs)
            messages_to_show = st.session_state.messages[-6:]
            st.info(f"Showing latest 3 Q&A pairs. Click 'Show All History' to see {total_messages - 6} earlier messages.")
        
        # Display the selected messages using native Streamlit components
        for message in messages_to_show:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        # Show placeholder when no messages
        st.info("💬 Start a conversation by selecting a question above or typing your own message below")

# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

def render_sidebar(serving_endpoint, user_info):
    """
    Render the application sidebar with system information and help.
    
    Args:
        serving_endpoint (str): Databricks serving endpoint
        user_info (dict): User information dictionary
    """
    with st.sidebar:
        # Application header
        st.markdown("## 🤖 RAG Assistant")
        st.success("🟢 Online & Ready")
        st.markdown("---")
        
        # Session statistics
        st.markdown("### 📊 Session Info")
        st.write(f"**Messages:** {len(st.session_state.messages)}")
        st.write("**Status:** Active")
        
        # User information
        st.markdown("### 👤 User")
        st.write(f"📧 {user_info['user_email']}")
        
        # System details (collapsible)
        with st.expander("🔧 System Details"):
            st.text(f"Endpoint: {serving_endpoint}")
            st.caption("Databricks Model Serving")
        
        # Help section
        st.markdown("### ❓ Help")
        st.markdown("""
        **Tips:**
        - Click any suggested question to use it
        - Use the reset button to clear chat history
        - Questions are processed using RAG on SharePoint data
        """)
        
        # Footer
        st.markdown("---")
        st.caption("💡 Powered by Lakeflow, Vector Search & Apps")

# ============================================================================
# MAIN APPLICATION LAYOUT
# ============================================================================

def render_main_content(serving_endpoint, logger):
    """
    Render the main application content with two-column layout.
    
    Args:
        serving_endpoint (str): Databricks serving endpoint
        logger: Logger instance
    """
    # Application header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🤖 Databricks RAG Assistant</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem; margin-top: 0.5rem;">
            Powered by Lakeflow, Vector Search and Apps
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Two-column layout
    left_col, right_col = st.columns([5, 7])

    # Left column: Information and question suggestions
    with left_col:
        # Quick resources section
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h3>📚 Quick Resources</h3>
            <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                <a href="https://docs.databricks.com" target="_blank">📖 Databricks Documentation</a>
                <a href="https://learn.microsoft.com/en-us/sharepoint/" target="_blank">📄 SharePoint Documentation</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggested questions section
        st.markdown("### 💡 Try These Questions")
        questions = get_suggested_questions()
        
        for i, question in enumerate(questions, 1):
            if st.button(f"💬 {question}", key=f"main_question_{i}", help="Click to use this question"):
                st.session_state.selected_question = question
                st.rerun()

        # Chat input section
        st.markdown("### 💬 Start a Conversation")

    # Right column: Chat interface
    with right_col:
        # Chat header with reset functionality
        st.markdown('<div style="margin-top: -2rem;">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown("### 🗨️ Chat History")
        
        with col2:
            if st.button("🔄 Reset", help="Clear all chat messages"):
                st.session_state.messages = []
                st.rerun()

        # Render the enhanced chat interface
        render_chat_interface(serving_endpoint, logger)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """
    Main application entry point.
    
    This function orchestrates the entire application flow:
    1. Sets up page configuration and logging
    2. Validates environment variables
    3. Initializes session state
    4. Applies modern styling
    5. Renders main content and sidebar
    """
    # Initialize application
    logger = setup_page_config()
    serving_endpoint = validate_environment()
    user_info = get_user_info()
    initialize_session_state()
    
    # Apply modern styling system
    apply_modern_styling()
    
    # Render application components
    render_main_content(serving_endpoint, logger)
    render_sidebar(serving_endpoint, user_info)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
