import streamlit as st
import time
from agents import (
    DraftingAgent, ComplianceAgent, 
    LocalizationAgent, DistributionAgent, IntelligenceAgent
)
from orchestrator import ContentOrchestrator

st.set_page_config(
    page_title="AI Content Operations | Enterprise Suite",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PREMIUM CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Header */
    .hero-section {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        padding: 2.5rem 2rem;
        border-radius: 28px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 35px -12px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(56,189,248,0.15) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #a5f3fc 50%, #7dd3fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.75rem;
    }
    
    .hero-badge {
        background: rgba(165, 243, 252, 0.15);
        padding: 0.35rem 1rem;
        border-radius: 40px;
        font-size: 0.75rem;
        color: #a5f3fc;
        display: inline-block;
        margin-right: 0.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(165, 243, 252, 0.3);
    }
    
    /* Sidebar Premium */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fefefe 100%);
        border-right: 1px solid #e2e8f0;
        padding: 1.5rem 1rem;
    }
    
    [data-testid="stSidebar"] h3 {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        padding: 0.6rem 1rem;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0f172a;
        box-shadow: 0 0 0 2px rgba(15,23,42,0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 12px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.2rem;
        border-radius: 14px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        width: 100%;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(15,23,42,0.25);
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px -12px rgba(0,0,0,0.15);
        border-color: #cbd5e1;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Human Review Card */
    .human-review-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef9e6 100%);
        border: 1px solid #fde047;
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px -8px rgba(250,204,21,0.2);
    }
    
    .compliance-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 40px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .compliance-high {
        background: #dcfce7;
        color: #166534;
    }
    
    .compliance-mid {
        background: #fef9c3;
        color: #854d0e;
    }
    
    .compliance-low {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Content Card */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 60px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.85rem;
        color: #64748b;
        border-radius: 40px;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    
    /* Audit Trail */
    .audit-entry {
        padding: 0.6rem;
        border-left: 3px solid #0f172a;
        margin-bottom: 0.6rem;
        background: #f8fafc;
        border-radius: 10px;
        font-size: 0.75rem;
        font-family: monospace;
    }
    
    /* Progress Animation */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 0%, #e0e0e0 50%, #f0f0f0 100%);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
        border-radius: 12px;
        height: 4px;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
    }
    
    /* Welcome Section */
    .welcome-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .welcome-card {
        background: white;
        padding: 1.2rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .welcome-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px -12px rgba(0,0,0,0.1);
    }
    
    .welcome-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .welcome-title {
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    
    .welcome-desc {
        font-size: 0.7rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HERO SECTION
# ============================================================================
st.markdown("""
<div class="hero-section">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <div class="hero-title">🤖 AI Content Operations</div>
            <div class="hero-subtitle">Enterprise-grade multi-agent content automation with human oversight</div>
            <div style="margin-top: 1rem;">
                <span class="hero-badge">⚡ 5 Specialized Agents</span>
                <span class="hero-badge">👤 Human-in-the-Loop</span>
                <span class="hero-badge">🔒 Compliance Guardrails</span>
                <span class="hero-badge">🌍 Multi-Region</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: #a5f3fc; font-size: 0.7rem;">Powered by</div>
            <div style="color: white; font-weight: 600;">Groq Llama 3.3</div>
            <div style="color: #94a3b8; font-size: 0.7rem;">70B Parameters</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'workflow_step' not in st.session_state:
    st.session_state.workflow_step = 'input'
if 'pending_result' not in st.session_state:
    st.session_state.pending_result = None
if 'final_result' not in st.session_state:
    st.session_state.final_result = None
if 'brief' not in st.session_state:
    st.session_state.brief = None
if 'regions' not in st.session_state:
    st.session_state.regions = None
if 'channels' not in st.session_state:
    st.session_state.channels = None
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None

# ============================================================================
# SIDEBAR - PREMIUM INPUT
# ============================================================================
with st.sidebar:
    st.markdown("### ✍️ Content Brief")
    st.markdown("Define your content parameters")
    st.markdown("---")
    
    topic = st.text_input(
        "📌 Topic",
        "AI Revolution in Enterprise",
        placeholder="Enter content topic..."
    )
    
    audience = st.selectbox(
        "👥 Target Audience",
        ["CTOs", "Marketing Leaders", "IT Directors", "Business Executives", "CFOs"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        format_type = st.selectbox("📄 Format", ["Blog Post", "Whitepaper", "Case Study", "Newsletter"])
    with col2:
        tone = st.selectbox("🎭 Tone", ["Professional", "Educational", "Persuasive", "Technical"])
    
    word_count = st.slider("📏 Target Word Count", 300, 2000, 600)
    
    st.markdown("---")
    st.markdown("### 🌍 Distribution")
    
    regions = st.multiselect(
        "Target Regions",
        ["US", "India", "UK", "Singapore", "Canada", "Australia"],
        default=["US", "India"]
    )
    
    channels = st.multiselect(
        "Publish Channels",
        ["LinkedIn", "Twitter", "Website", "Newsletter", "Medium"],
        default=["LinkedIn", "Website"]
    )
    
    st.markdown("---")
    
    generate_btn = st.button("🚀 Start Pipeline", type="primary", use_container_width=True)
    
    if generate_btn:
        st.session_state.workflow_step = 'input'
        st.session_state.pending_result = None
        st.session_state.final_result = None
        st.session_state.brief = {
            "topic": topic,
            "audience": audience,
            "format": format_type,
            "tone": tone,
            "word_count": word_count
        }
        st.session_state.regions = regions
        st.session_state.channels = channels
        st.rerun()

# ============================================================================
# STEP 1: GENERATE CONTENT
# ============================================================================
if st.session_state.workflow_step == 'input' and st.session_state.brief:
    
    st.markdown("### 🤖 AI Agents Processing")
    st.markdown("---")
    
    # Create columns for agent status
    col_status1, col_status2, col_status3, col_status4, col_status5 = st.columns(5)
    
    with col_status1:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">📝</span>
            <div style="font-size: 0.7rem;">Drafting</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status2:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">🔍</span>
            <div style="font-size: 0.7rem;">Compliance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status3:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">🌍</span>
            <div style="font-size: 0.7rem;">Localization</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status4:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">📤</span>
            <div style="font-size: 0.7rem;">Distribution</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_status5:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="font-size: 1.5rem;">📊</span>
            <div style="font-size: 0.7rem;">Intelligence</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="loading-shimmer"></div>', unsafe_allow_html=True)
    
    with st.spinner("Processing..."):
        drafting = DraftingAgent()
        compliance = ComplianceAgent()
        localization = LocalizationAgent()
        distribution = DistributionAgent()
        intelligence = IntelligenceAgent()
        
        orchestrator = ContentOrchestrator(
            drafting, compliance, localization, distribution, intelligence
        )
        st.session_state.orchestrator = orchestrator
        
        result = orchestrator.run_workflow(
            st.session_state.brief,
            st.session_state.regions,
            st.session_state.channels,
            human_approved=None,
            human_feedback=None
        )
        
        st.session_state.pending_result = result
    
    if result.get("status") == "pending_human_approval":
        st.session_state.workflow_step = 'review'
    else:
        st.session_state.final_result = result
        st.session_state.workflow_step = 'results'
    
    st.rerun()

# ============================================================================
# STEP 2: HUMAN-IN-THE-LOOP REVIEW
# ============================================================================
if st.session_state.workflow_step == 'review':
    result = st.session_state.pending_result
    comp = result.get("compliance", {})
    score = comp.get("score", 0)
    
    st.markdown("""
    <div class="human-review-card">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">👤</span>
            <h3 style="margin: 0; color: #854d0e;">Human-in-the-Loop Review</h3>
        </div>
        <p style="color: #854d0e; margin-top: 0.5rem;">Review the content before it proceeds to distribution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compliance Badge
    badge_class = "compliance-high" if score >= 85 else "compliance-mid" if score >= 70 else "compliance-low"
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
        <span style="font-weight: 600;">Compliance Score</span>
        <span class="compliance-badge {badge_class}">{score}/100</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(score/100)
    st.caption(comp.get("message", ""))
    
    if comp.get("issues"):
        st.warning("⚠️ Issues Identified:")
        for issue in comp.get("issues", []):
            st.markdown(f"• {issue}")
    
    st.markdown("---")
    
    col_content, col_approval = st.columns([2, 1])
    
    with col_content:
        st.markdown("### 📄 Content Preview")
        draft = result.get("draft", {})
        st.markdown(f"**Topic:** {st.session_state.brief['topic']}")
        st.markdown(f"**Audience:** {st.session_state.brief['audience']}")
        st.markdown("---")
        
        content_text = draft.get("draft", "No content")
        st.markdown(content_text[:2500])
        if len(content_text) > 2500:
            st.caption(f"... (showing first 2500 of {len(content_text)} characters)")
    
    with col_approval:
        st.markdown("### ✅ Decision")
        
        feedback = st.text_area(
            "📝 Feedback (for revisions)",
            placeholder="E.g., Make tone more professional, add more data...",
            height=100
        )
        
        st.markdown("---")
        
        if st.button("✅ Approve & Continue", type="primary", use_container_width=True):
            with st.spinner("Continuing with approval..."):
                final = st.session_state.orchestrator.run_workflow(
                    st.session_state.brief,
                    st.session_state.regions,
                    st.session_state.channels,
                    human_approved=True,
                    human_feedback=feedback if feedback else "Approved"
                )
                st.session_state.final_result = final
                st.session_state.workflow_step = 'results'
            st.rerun()
        
        if st.button("✏️ Request Revisions", use_container_width=True):
            if not feedback:
                st.error("Please provide feedback")
            else:
                with st.spinner("Revising..."):
                    revised = st.session_state.orchestrator.run_workflow(
                        st.session_state.brief,
                        st.session_state.regions,
                        st.session_state.channels,
                        human_approved=False,
                        human_feedback=feedback
                    )
                    if revised.get("status") == "pending_human_approval":
                        st.session_state.pending_result = revised
                    else:
                        st.session_state.final_result = revised
                        st.session_state.workflow_step = 'results'
                st.rerun()
    
    st.stop()

# ============================================================================
# STEP 3: RESULTS
# ============================================================================
if st.session_state.workflow_step == 'results' and st.session_state.final_result:
    result = st.session_state.final_result
    
    if result.get("status") == "completed":
        st.balloons()
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); padding: 1rem; border-radius: 16px; margin: 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">✅</span>
                <div>
                    <strong style="color: #166534;">Pipeline Complete</strong>
                    <p style="color: #166534; margin: 0;">Content generated with human approval</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{result['total_time_minutes']*60:.0f}s</div>
                <div class="metric-label">Processing Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">-{result['impact']['saved_minutes']:.0f} min</div>
                <div class="metric-label">Time Saved</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{result['compliance']['score']}/100</div>
                <div class="metric-label">Compliance Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(result['distribution']['published'])}</div>
                <div class="metric-label">Channels</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Content", "🔍 Compliance", "🌍 Localization", "📊 Insights"])
        
        with tab1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(result['draft']['draft'])
            with st.expander("🎯 Suggested Headlines"):
                for h in result['draft']['headlines']:
                    st.markdown(f"• {h}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.progress(result['compliance']['score']/100)
            st.markdown(f"**Score:** {result['compliance']['score']}/100")
            st.markdown(f"**Status:** {result['compliance']['status'].upper()}")
            st.markdown(f"**Message:** {result['compliance']['message']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            for region, content in result['localized']['versions'].items():
                with st.expander(f"🌐 {region}"):
                    st.markdown(content)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown(f"**{result['insights']['analysis']}**")
            st.markdown("#### 💡 Key Insights")
            for insight in result['insights']['insights']:
                st.markdown(f"• {insight}")
            st.markdown("#### 🎯 Recommendations")
            for rec in result['insights']['recommendations']:
                st.markdown(f"• {rec}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Audit Trail
        with st.expander("📋 Audit Trail", expanded=False):
            for log in result['audit_log']:
                st.markdown(f"""
                <div class="audit-entry">
                    <strong>{log['timestamp'][:19]}</strong> | 
                    <span style="color: #0f172a;">{log['stage'].upper()}</span> | 
                    {log['action']}
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("🔄 Create New Content", use_container_width=True):
            st.session_state.workflow_step = 'input'
            st.session_state.pending_result = None
            st.session_state.final_result = None
            st.session_state.brief = None
            st.rerun()

# ============================================================================
# WELCOME SCREEN
# ============================================================================
# CLEAN WELCOME SCREEN - NO REDUNDANCY
# ============================================================================
if st.session_state.workflow_step == 'input' and not st.session_state.brief:
    
    # ============================================================
    # MAIN HIGHLIGHT: HUMAN-IN-THE-LOOP CARD (Hero Feature)
    # ============================================================
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                border: 2px solid #f59e0b; 
                border-radius: 24px; 
                padding: 1.8rem; 
                margin-bottom: 2rem;
                box-shadow: 0 8px 20px -8px rgba(245,158,11,0.3);">
        <div style="display: flex; align-items: center; gap: 1.2rem; flex-wrap: wrap;">
            <div style="background: #f59e0b; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 2rem;">👤</span>
            </div>
            <div style="flex: 1;">
                <h2 style="margin: 0; color: #92400e;">Human-in-the-Loop Approval Gate</h2>
                <p style="margin: 0.25rem 0 0 0; color: #b45309; font-size: 1rem;">Enterprise-grade governance • Human oversight before publishing • Complete audit trail</p>
            </div>
            <div style="background: white; padding: 0.5rem 1rem; border-radius: 40px;">
                <span style="color: #92400e; font-weight: 700;">⭐ Key Differentiator</span>
            </div>
        </div>
        <div style="display: flex; gap: 1rem; margin-top: 1.2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.8); border-radius: 12px; padding: 0.5rem 1rem;">
                <span>✅ Human Review Required</span>
            </div>
            <div style="background: rgba(255,255,255,0.8); border-radius: 12px; padding: 0.5rem 1rem;">
                <span>✏️ Revision Feedback Loop</span>
            </div>
            <div style="background: rgba(255,255,255,0.8); border-radius: 12px; padding: 0.5rem 1rem;">
                <span>📋 Complete Audit Trail</span>
            </div>
            <div style="background: rgba(255,255,255,0.8); border-radius: 12px; padding: 0.5rem 1rem;">
                <span>🔒 Compliance Enforcement</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # THE 5 AGENTS - ONE CLEAN GRID
    # ============================================================
    st.markdown("""
    <div style="background: white; border-radius: 24px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #e2e8f0;">
        <h3 style="margin: 0 0 1rem 0; color: #0f172a; text-align: center;">🤖 The 5 Specialized AI Agents</h3>
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem;">
            <div style="text-align: center;">
                <div style="background: #f8fafc; border-radius: 16px; padding: 1rem;">
                    <span style="font-size: 2rem;">📝</span>
                    <div style="font-weight: 700; margin-top: 0.5rem;">Drafting</div>
                    <div style="font-size: 0.7rem; color: #64748b;">Content Creation</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #f8fafc; border-radius: 16px; padding: 1rem;">
                    <span style="font-size: 2rem;">🔍</span>
                    <div style="font-weight: 700; margin-top: 0.5rem;">Compliance</div>
                    <div style="font-size: 0.7rem; color: #64748b;">Brand Guidelines</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #fef3c7; border-radius: 16px; padding: 1rem; border: 2px solid #f59e0b;">
                    <span style="font-size: 2rem;">👤</span>
                    <div style="font-weight: 700; margin-top: 0.5rem; color: #92400e;">Human Review</div>
                    <div style="font-size: 0.7rem; color: #b45309;">Approval Gate</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #f8fafc; border-radius: 16px; padding: 1rem;">
                    <span style="font-size: 2rem;">🌍</span>
                    <div style="font-weight: 700; margin-top: 0.5rem;">Localization</div>
                    <div style="font-size: 0.7rem; color: #64748b;">Multi-Region</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="background: #f8fafc; border-radius: 16px; padding: 1rem;">
                    <span style="font-size: 2rem;">📊</span>
                    <div style="font-weight: 700; margin-top: 0.5rem;">Intelligence</div>
                    <div style="font-size: 0.7rem; color: #64748b;">Insights</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # HOW IT WORKS - SIMPLE FLOW
    # ============================================================
    st.markdown("""
    <div style="background: #f1f5f9; border-radius: 20px; padding: 1.5rem; margin: 1rem 0;">
        <h4 style="margin: 0 0 1rem 0; color: #0f172a;">⚡ How It Works</h4>
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
            <div style="text-align: center; flex: 1;">
                <div style="background: white; border-radius: 12px; padding: 0.5rem;">
                    <span>📝</span>
                    <div style="font-size: 0.7rem;">Draft</div>
                </div>
            </div>
            <div style="color: #64748b;">→</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: white; border-radius: 12px; padding: 0.5rem;">
                    <span>🔍</span>
                    <div style="font-size: 0.7rem;">Compliance</div>
                </div>
            </div>
            <div style="color: #64748b;">→</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: #fef3c7; border-radius: 12px; padding: 0.5rem; border: 1px solid #f59e0b;">
                    <span>👤</span>
                    <div style="font-size: 0.7rem; font-weight: 600;">HUMAN REVIEW</div>
                </div>
            </div>
            <div style="color: #64748b;">→</div>
            <div style="text-align: center; flex: 1;">
                <div style="background: white; border-radius: 12px; padding: 0.5rem;">
                    <span>🌍📤📊</span>
                    <div style="font-size: 0.7rem;">Publish</div>
                </div>
            </div>
        </div>
        <p style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 1rem;">
            ⏱️ 4.5 hours manual → 6 seconds automated • 97% time reduction
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================================
    # CALL TO ACTION
    # ============================================================
    st.markdown("""
    <div style="text-align: center; margin-top: 1.5rem;">
        <p style="color: #64748b; font-size: 1rem;">👈 <strong>Ready to experience enterprise content automation?</strong><br>Fill in the content brief in the sidebar and watch the 5 agents work</p>
        <p style="color: #94a3b8; font-size: 0.7rem; margin-top: 0.5rem;">
            ⚡ Groq Llama 3.3 70B • 5 Specialized Agents • Human-in-the-Loop • Compliance Guardrails • Audit Trail
        </p>
    </div>
    """, unsafe_allow_html=True)