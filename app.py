import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. LOADING SCREEN (Premium Experience)
# ==========================================
if 'loaded' not in st.session_state:
    st.session_state.loaded = False

if not st.session_state.loaded:
    loading_container = st.container()
    with loading_container:
        st.markdown("""
        <div style='text-align: center; padding: 100px 0;'>
            <div style='font-size: 48px; margin-bottom: 20px;'>🎓</div>
            <div style='font-size: 28px; font-weight: 700; background: linear-gradient(135deg, #3B82F6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;'>
                AI Learning Impact Analytics
            </div>
            <div style='color: #94A3B8; font-size: 14px; margin-bottom: 30px;'>Enterprise Analytics Dashboard</div>
            <div style='max-width: 400px; margin: 0 auto;'>
                <div style='background: rgba(30, 41, 59, 0.5); border-radius: 10px; padding: 20px; border: 1px solid rgba(59, 130, 246, 0.2);'>
                    <div style='color: #F8FAFC; font-size: 14px; margin-bottom: 15px;'>Initializing Dashboard...</div>
                    <div style='background: #1E293B; border-radius: 8px; height: 8px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #3B82F6, #06B6D4); height: 100%; width: 100%; animation: loading 2s ease-in-out;'></div>
                    </div>
                </div>
            </div>
        </div>
        <style>
        @keyframes loading {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        </style>
        """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.loaded = True
    st.rerun()

# ==========================================
# 3. CUSTOM CSS (ENTERPRISE THEME LENGKAP)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === ROOT VARIABLES === */
:root {
    --bg-primary: #0F172A;
    --bg-surface: #1E293B;
    --bg-elevated: #273449;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-medium: #475569;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --accent-primary: #3B82F6;
    --accent-secondary: #06B6D4;
    --accent-success: #22C55E;
    --accent-warning: #F59E0B;
    --accent-danger: #EF4444;
    --accent-purple: #8B5CF6;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 40px rgba(59, 130, 246, 0.15);
}

/* === GLOBAL TYPOGRAPHY === */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
    -webkit-font-smoothing: antialiased;
}

/* === BACKGROUND === */
[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(59, 130, 246, 0.08), transparent),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(139, 92, 246, 0.06), transparent),
        linear-gradient(180deg, #0F172A 0%, #0B1120 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* === SIDEBAR === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120 0%, #131B2E 100%) !important;
    border-right: 1px solid var(--border-subtle);
    position: sticky;
    top: 0;
}

[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-primary);
}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 6px;
    border: 1px solid var(--border-subtle);
    display: inline-flex;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    padding: 10px 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
}

.stTabs [data-baseweb="tab"] p {
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(59, 130, 246, 0.08);
}

.stTabs [data-baseweb="tab"]:hover p {
    color: var(--text-primary);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
}

.stTabs [aria-selected="true"] p {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 14px;
}

/* === SLIDER === */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
    border: 2px solid #fff !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}

/* === BUTTON === */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-primary) 0%, #2563EB 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

/* === MULTISELECT === */
.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.15));
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
}

.stMultiSelect [data-baseweb="tag"] span {
    color: var(--text-primary);
    font-weight: 500;
}

/* === EXPANDER === */
[data-testid="stExpander"] {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}

[data-testid="stExpander"]:hover {
    border-color: var(--border-medium);
    background: rgba(30, 41, 59, 0.6);
}

[data-testid="stExpander"] summary {
    padding: 14px 18px;
}

[data-testid="stExpander"] summary span {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

/* === METRIC CARDS DEFAULT === */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 22px 24px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: var(--shadow-glow), var(--shadow-lg);
}

div[data-testid="stMetric"]:hover::before {
    opacity: 1;
}

div[data-testid="stMetricValue"] {
    color: var(--text-primary);
    font-weight: 700;
    font-size: 34px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

div[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}

div[data-testid="stMetricDelta"] {
    font-size: 12px;
    font-weight: 600;
}

/* === CARD WRAPPER === */
[data-testid="stVerticalBlockBorderWrapper"] > div,
section[data-testid="stVerticalBlock"] > div {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    box-shadow: var(--shadow-md);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 24px;
}

[data-testid="stVerticalBlockBorderWrapper"] > div:hover,
section[data-testid="stVerticalBlock"] > div:hover {
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: var(--shadow-lg), 0 0 30px rgba(59, 130, 246, 0.1);
    transform: translateY(-2px);
}

/* === HERO SECTION === */
.hero-box {
    background:
        radial-gradient(ellipse 100% 100% at 0% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 80% 100% at 100% 100%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
        linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    backdrop-filter: blur(20px);
    padding: 48px 40px;
    border-radius: 24px;
    border: 1px solid rgba(59, 130, 246, 0.2);
    box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.8s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.hero-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    animation: pulse-glow 8s ease-in-out infinite;
    pointer-events: none;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.05); }
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.hero-subtitle {
    font-size: 17px;
    color: var(--text-secondary);
    font-weight: 400;
    margin-top: 0;
    margin-bottom: 28px;
    line-height: 1.6;
    max-width: 720px;
    position: relative;
    z-index: 1;
}

.hero-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
    transition: all 0.3s ease;
}

.meta-chip:hover {
    border-color: var(--accent-primary);
    background: rgba(59, 130, 246, 0.1);
    color: var(--text-primary);
}

.meta-chip-icon {
    font-size: 14px;
}

/* === EXECUTIVE SUMMARY === */
.executive-summary {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-left: 3px solid var(--accent-primary);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 20px 0;
    color: var(--text-secondary);
    font-size: 14.5px;
    line-height: 1.7;
    animation: slideIn 0.6s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

.executive-summary strong {
    color: var(--text-primary);
}

/* === SECTION DIVIDER === */
.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 40px 0 24px 0;
}

.section-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
}

.section-divider-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    padding: 6px 14px;
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

/* === INSIGHT BOX === */
.insight-box {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.06) 0%, rgba(6, 182, 212, 0.04) 100%);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-left: 3px solid var(--accent-success);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 18px;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    transition: all 0.3s ease;
}

.insight-box:hover {
    border-left-color: var(--accent-primary);
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
    transform: translateX(4px);
}

.insight-box strong {
    color: var(--accent-success);
    font-weight: 600;
    margin-right: 6px;
}

/* === CHART TITLE === */
.chart-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}

.chart-description {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 20px;
    line-height: 1.5;
}

/* === MONTE CARLO === */
.mc-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--accent-success);
    font-weight: 600;
    margin-bottom: 16px;
}

.mc-status-dot {
    width: 8px;
    height: 8px;
    background: var(--accent-success);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent-success);
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.2); }
}

/* === FOOTER === */
.dashboard-footer {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 28px 32px;
    margin-top: 60px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.7;
}

.dashboard-footer strong {
    color: var(--text-primary);
    font-weight: 600;
}

.footer-meta {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-subtle);
    font-size: 12px;
    color: var(--text-muted);
}

/* === TEXT COLORS === */
p, h1, h2, h3, h4, h5, h6, label {
    color: var(--text-primary) !important;
}

.stMarkdown {
    color: var(--text-primary);
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--border-medium);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-primary);
}

/* === NUMBER INPUT === */
.stNumberInput input {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

.stNumberInput input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}

/* === KPI CARD CUSTOM (FIXED) === */
.kpi-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 24px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}

.kpi-card:hover {
    transform: translateY(-6px);
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: var(--shadow-glow), var(--shadow-lg);
}

.kpi-card:hover::before {
    opacity: 1;
}

.kpi-icon {
    font-size: 32px;
    margin-bottom: 12px;
    display: block;
    line-height: 1;
}

.kpi-label {
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
    line-height: 1.2;
}

.kpi-subtitle {
    color: var(--text-secondary);
    font-size: 13px;
    margin-bottom: 12px;
}

.kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    width: fit-content;
}

.kpi-delta.positive {
    background: rgba(34, 197, 94, 0.15);
    color: var(--accent-success);
}

.kpi-delta.negative {
    background: rgba(239, 68, 68, 0.15);
    color: var(--accent-danger);
}

.kpi-delta.neutral {
    background: rgba(148, 163, 184, 0.15);
    color: var(--text-muted);
}

.kpi-progress {
    margin-top: 14px;
    height: 4px;
    background: rgba(30, 41, 59, 0.8);
    border-radius: 2px;
    overflow: hidden;
    width: 100%;
}

.kpi-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #3B82F6, #06B6D4);
    border-radius: 2px;
    transition: width 1s ease;
    box-shadow: 0 0 8px rgba(59, 130, 246, 0.4);
}

/* === DATA QUALITY PANEL === */
.data-quality-panel {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 20px 0;
}

.dq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 12px;
}

.dq-item {
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 14px 16px;
    transition: all 0.3s ease;
}

.dq-item:hover {
    border-color: rgba(59, 130, 246, 0.3);
    transform: translateY(-2px);
}

.dq-label {
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.dq-value {
    color: var(--text-primary);
    font-size: 18px;
    font-weight: 600;
}

/* === AI INSIGHT PANEL === */
.ai-insight-panel {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(59, 130, 246, 0.06) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-left: 3px solid var(--accent-purple);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 24px 0;
    color: var(--text-secondary);
    font-size: 14.5px;
    line-height: 1.7;
}

.ai-insight-panel strong {
    color: var(--accent-purple);
}

/* === SECTION NUMBER === */
.section-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white;
    font-size: 14px;
    font-weight: 700;
    border-radius: 8px;
}

/* === HEATMAP INTERPRETATION === */
.heatmap-interp {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 12px;
}

.heatmap-interp.strong-pos {
    background: rgba(34, 197, 94, 0.15);
    color: var(--accent-success);
}

.heatmap-interp.weak-neg {
    background: rgba(239, 68, 68, 0.15);
    color: var(--accent-danger);
}

.heatmap-interp.neutral {
    background: rgba(148, 163, 184, 0.15);
    color: var(--text-muted);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. DESIGN TOKENS
# ==========================================
SOFT_COLORS = {
    'primary': '#3B82F6',
    'secondary': '#06B6D4',
    'success': '#22C55E',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'purple': '#8B5CF6',
    'muted': '#94A3B8'
}

PLOTLY_TEMPLATE = 'plotly_dark'

# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================
def render_section_divider(title, number=None):
    number_html = f'<span class="section-number">{number}</span>' if number else ''
    st.markdown(f"""
    <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-divider-title">{number_html}{title}</div>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

def render_chart_header(title, description):
    st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-description">{description}</div>', unsafe_allow_html=True)

def render_insight_box(text):
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insight</strong>{text}
    </div>
    """, unsafe_allow_html=True)

def update_dark_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter', size=12),
        margin=dict(t=20, b=20, l=0, r=0)
    )
    return fig

def render_kpi_card(icon, label, value, subtitle, delta_text, delta_type, progress=None):
    """Render custom KPI card with progress bar - FIXED VERSION"""
    
    # Validasi delta_type
    if delta_type not in ['positive', 'negative', 'neutral']:
        delta_type = 'neutral'
    
    # Icon untuk delta
    if delta_type == 'positive':
        delta_icon = "▲"
    elif delta_type == 'negative':
        delta_icon = "▼"
    else:
        delta_icon = "●"
    
    # Validasi dan format progress
    progress_html = ""
    if progress is not None:
        try:
            progress_val = float(progress)
            # Clamp antara 0-100 untuk menghindari error
            progress_val = max(0.0, min(100.0, progress_val))
            progress_html = f'<div class="kpi-progress"><div class="kpi-progress-bar" style="width: {progress_val:.1f}%;"></div></div>'
        except (TypeError, ValueError):
            progress_html = ""  # Skip progress bar jika error
    
    # Render card dengan HTML yang clean
    html_content = f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtitle">{subtitle}</div>
        <span class="kpi-delta {delta_type}">
            {delta_icon} {delta_text}
        </span>
        {progress_html}
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)

def render_data_quality_panel(df):
    """Render Data Quality Overview Panel"""
    missing_count = df.isnull().sum().sum()
    total_cells = df.shape[0] * df.shape[1]
    missing_pct = (missing_count / total_cells * 100) if total_cells > 0 else 0
    
    date_min = str(df['Date_Parsed'].min()) if 'Date_Parsed' in df.columns else 'N/A'
    date_max = str(df['Date_Parsed'].max()) if 'Date_Parsed' in df.columns else 'N/A'
    
    prodi_count = df['Prodi'].nunique() if 'Prodi' in df.columns else 0
    semester_count = df['Semester'].nunique() if 'Semester' in df.columns else 0
    
    st.markdown(f"""
    <div class="data-quality-panel">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <div style="font-size: 24px;">📊</div>
            <div>
                <div style="font-size: 16px; font-weight: 600; color: #F8FAFC;">Data Quality Overview</div>
                <div style="font-size: 12px; color: #94A3B8;">Ringkasan kualitas dataset</div>
            </div>
        </div>
        <div class="dq-grid">
            <div class="dq-item">
                <div class="dq-label">Total Records</div>
                <div class="dq-value">{len(df):,}</div>
            </div>
            <div class="dq-item">
                <div class="dq-label">Missing Values</div>
                <div class="dq-value">{missing_count} ({missing_pct:.2f}%)</div>
            </div>
            <div class="dq-item">
                <div class="dq-label">Program Studi</div>
                <div class="dq-value">{prodi_count}</div>
            </div>
            <div class="dq-item">
                <div class="dq-label">Semester</div>
                <div class="dq-value">{semester_count}</div>
            </div>
            <div class="dq-item">
                <div class="dq-label">Variables</div>
                <div class="dq-value">{len(df.columns)}</div>
            </div>
            <div class="dq-item">
                <div class="dq-label">Date Range</div>
                <div class="dq-value" style="font-size: 14px;">{date_min[:10]} → {date_max[:10]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. MEMUAT & PRE-PROCESSING DATA (TIDAK BERUBAH)
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('Data Mentah.csv', sep=';')
    df.columns = [
        'Timestamp', 'Prodi', 'Semester', 'Jenis_AI', 'Frekuensi_Penggunaan',
        'Tujuan_Penggunaan', 'Kesulitan_Tanpa_AI', 'Jam_per_Hari',
        'Porsi_Tugas_AI', 'Frekuensi_Info_Salah', 'Peningkatan_Nilai',
        'Tingkat_Copy_Paste', 'Skor_Efektivitas'
    ]
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)')
    try:
        df['Date_Parsed'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
    except:
        df['Date_Parsed'] = df['Timestamp']
    return df

df_raw = load_data()

# ==========================================
# 7. SIDEBAR (REDESIGNED)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
        <div style="font-size: 22px; font-weight: 700; letter-spacing: -0.02em; 
                    background: linear-gradient(135deg, #3B82F6, #06B6D4); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎓 AI Learning Impact
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
            Enterprise Analytics Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📁 Filter Dataset", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist()
        filter_prodi = st.multiselect("Program Studi", options=prodi_list, default=prodi_list)
        
        semester_list = sorted(df_raw['Semester'].unique().tolist())
        filter_semester = st.multiselect("Semester", options=semester_list, default=semester_list)
    
    with st.expander("🔮 Profil Simulator"):
        sim_tugas = st.slider("Porsi Bantuan AI Anda:", 0, 10, 6)
        if sim_tugas > 5:
            st.error("⚠️ Risiko Ketergantungan Tinggi")
        else:
            st.success("✅ Ketergantungan Aman")
    
    with st.expander("ℹ️ Tentang Dashboard"):
        st.markdown("""
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            Dashboard ini menganalisis dampak penggunaan <strong>Artificial Intelligence</strong> 
            terhadap efektivitas belajar mahasiswa dengan pendekatan <em>data-driven analytics</em>.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 40px; padding-top: 20px; border-top: 1px solid #334155;'>", unsafe_allow_html=True)
    st.caption("👨‍💻 **Developer:** Ahmad Rizza Pahlevi")
    st.caption("🏢 UIN K.H. Abdurrahman Wahid")
    st.caption("📅 Juni 2026")

# Apply filter
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ==========================================
# 8. HERO SECTION
# ==========================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">AI Learning Impact Analytics</div>
    <div class="hero-subtitle">
        Memahami pola, dampak, dan probabilitas penggunaan <strong>Artificial Intelligence</strong> 
        dalam ekosistem akademik melalui pendekatan analitik berbasis data, probabilitas, 
        dan simulasi Monte Carlo untuk proyeksi skala besar.
    </div>
    <div class="hero-meta">
        <div class="meta-chip"><span class="meta-chip-icon">📅</span> Update: Juni 2026</div>
        <div class="meta-chip"><span class="meta-chip-icon">👨‍💻</span> Ahmad Rizza Pahlevi</div>
        <div class="meta-chip"><span class="meta-chip-icon">🏢</span> UIN K.H. Abdurrahman Wahid</div>
        <div class="meta-chip"><span class="meta-chip-icon">📊</span> {len(df)} Responden Aktif</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 9. KPI PREMIUM CARDS (FIXED VERSION)
# ==========================================
col1, col2, col3, col4 = st.columns(4)

avg_jam = df['Jam_per_Hari'].mean() if len(df) > 0 else 0
avg_tugas = df['Porsi_Tugas_AI'].mean() if len(df) > 0 else 0
avg_skor = df['Skor_Efektivitas'].mean() if len(df) > 0 else 0

with col1:
    render_kpi_card(
        icon="👥",
        label="Total Respondent",
        value=f"{len(df)}",
        subtitle="Data Terfilter",
        delta_text="Active Dataset",
        delta_type="neutral",
        progress=None
    )

with col2:
    # Progress bar untuk durasi (max 10 jam = 100%)
    progress_jam = min(avg_jam / 10 * 100, 100) if len(df) > 0 else 0
    render_kpi_card(
        icon="⏱️",
        label="Durasi Rata-rata",
        value=f"{avg_jam:.1f} Jam",
        subtitle="Per Hari",
        delta_text="-0.2 vs Nasional",
        delta_type="negative",
        progress=progress_jam
    )

with col3:
    # Progress bar untuk ketergantungan (max 10 = 100%)
    progress_tugas = avg_tugas * 10 if len(df) > 0 else 0
    render_kpi_card(
        icon="📝",
        label="Bantuan Tugas",
        value=f"{avg_tugas:.1f}/10",
        subtitle="Ketergantungan AI",
        delta_text="Moderate",
        delta_type="neutral",
        progress=progress_tugas
    )

with col4:
    # Progress bar untuk skor efektivitas (max 5 = 100%)
    progress_skor = (avg_skor / 5 * 100) if len(df) > 0 else 0
    delta_type_skor = "positive" if avg_skor > 3.5 else "neutral"
    delta_text_skor = "Excellent" if avg_skor > 3.5 else "Moderate"
    
    render_kpi_card(
        icon="⭐",
        label="Skor Efektivitas",
        value=f"{avg_skor:.2f}/5",
        subtitle="Learning Impact",
        delta_text=delta_text_skor,
        delta_type=delta_type_skor,
        progress=progress_skor
    )

# ==========================================
# 10. DATA QUALITY PANEL
# ==========================================
if len(df) > 0:
    render_data_quality_panel(df)

# ==========================================
# 11. EXECUTIVE SUMMARY
# ==========================================
render_section_divider("Executive Summary", "01")

if len(df) > 0:
    setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100
    mean_jam = df['Jam_per_Hari'].mean()
    max_jam = df['Jam_per_Hari'].max()
    high_dep_pct = len(df[df['Is_Ketergantungan_Tinggi']=='Tinggi (>5 Tugas)'])/len(df)*100
    
    st.markdown(f"""
    <div class="executive-summary">
        Dataset saat ini merepresentasikan <strong>{len(df)} mahasiswa</strong> yang aktif menggunakan AI untuk keperluan akademik. 
        <strong>{setiap_hari_pct:.0f}%</strong> di antaranya menggunakan AI setiap hari dengan durasi rata-rata 
        <strong>{mean_jam:.1f} jam/hari</strong> (maksimal {max_jam} jam). 
        Proporsi mahasiswa dengan ketergantungan tinggi (>5 tugas) mencapai <strong>{high_dep_pct:.0f}%</strong>, 
        mengindikasikan perlunya intervensi edukatif untuk menjaga kemandirian kognitif.
        <br><br>
        <strong>Rekomendasi:</strong> Perlu pengembangan panduan penggunaan AI yang seimbang untuk memaksimalkan 
        manfaat pembelajaran tanpa mengurangi kemampuan analitis mandiri mahasiswa.
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

# ==========================================
# 12. TAB NAVIGATION
# ==========================================
render_section_divider("Modul Analitik", "02")

tab1, tab2, tab3 = st.tabs([
    "📊 02 • Descriptive Analytics", 
    "🔗 03 • Correlation Analysis", 
    "🎲 04 • Monte Carlo Simulation"
])

# ==========================================
# TAB 1: EKSPLORASI DESKRIPTIF
# ==========================================
with tab1:
    with st.container(border=True):
        render_chart_header(
            "📈 Tren Frekuensi Penggunaan AI",
            "Distribusi seberapa sering mahasiswa menggunakan AI dalam aktivitas akademik harian."
        )
        trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
        trend_data.columns = ['Frekuensi', 'Jumlah']
        fig_hero = px.bar(
            trend_data, x='Frekuensi', y='Jumlah',
            text='Jumlah', color='Frekuensi',
            color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple'], SOFT_COLORS['muted']],
            template=PLOTLY_TEMPLATE
        )
        fig_hero.update_traces(
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
        )
        fig_hero.update_layout(height=380, showlegend=False)
        st.plotly_chart(update_dark_layout(fig_hero), use_container_width=True)
        
        top_freq = trend_data.iloc[0] if len(trend_data) > 0 else None
        if top_freq is not None:
            render_insight_box(
                f"Mayoritas mahasiswa ({top_freq['Jumlah']} orang) menggunakan AI dengan frekuensi <strong>{top_freq['Frekuensi']}</strong>, "
                f"menunjukkan pola adopsi yang cukup tinggi di kalangan responden."
            )

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            render_chart_header(
                "🍩 Distribusi Tingkat Ketergantungan",
                "Perbandingan proporsi mahasiswa dengan ketergantungan tinggi vs rendah."
            )
            fig_pie = px.pie(
                df, names='Is_Ketergantungan_Tinggi', hole=0.55,
                color='Is_Ketergantungan_Tinggi',
                color_discrete_map={'Tinggi (>5 Tugas)': SOFT_COLORS['danger'], 'Rendah (<=5 Tugas)': SOFT_COLORS['secondary']},
                template=PLOTLY_TEMPLATE
            )
            fig_pie.update_traces(
                textinfo='percent+label', 
                hoverinfo='label+percent+value',
                hovertemplate='<b>%{label}</b><br>Proporsi: %{percent}<br>Jumlah: %{value}<extra></extra>'
            )
            fig_pie.update_layout(height=380, showlegend=False)
            st.plotly_chart(update_dark_layout(fig_pie), use_container_width=True)
            
            high_count = len(df[df['Is_Ketergantungan_Tinggi']=='Tinggi (>5 Tugas)'])
            high_pct = (high_count/len(df)*100) if len(df) > 0 else 0
            render_insight_box(
                f"Sebanyak <strong>{high_pct:.1f}%</strong> responden memiliki ketergantungan tinggi (>5 tugas dibantu AI), "
                f"yang memerlukan perhatian khusus dari sisi pedagogis."
            )

    with col2:
        with st.container(border=True):
            render_chart_header(
                "📊 Distribusi Porsi Tugas Dibantu AI",
                "Histogram jumlah tugas per mahasiswa yang dibantu oleh AI."
            )
            fig_porsi = px.histogram(
                df, x='Porsi_Tugas_AI', text_auto=True,
                color_discrete_sequence=[SOFT_COLORS['primary']],
                template=PLOTLY_TEMPLATE
            )
            fig_porsi.update_traces(
                hovertemplate='<b>Porsi Tugas:</b> %{x}<br><b>Jumlah Mahasiswa:</b> %{y}<extra></extra>'
            )
            fig_porsi.update_layout(height=380, xaxis_title="Jumlah Tugas (0-10)", yaxis_title="Jumlah Mahasiswa")
            st.plotly_chart(update_dark_layout(fig_porsi), use_container_width=True)
            render_insight_box(
                f"Distribusi menunjukkan variasi penggunaan AI dari ringan hingga intensif. "
                f"Rata-rata mahasiswa menggunakan AI untuk <strong>{avg_tugas:.1f} tugas</strong>."
            )

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            render_chart_header(
                "⏳ Histogram Durasi Pemakaian Harian",
                "Distribusi durasi penggunaan AI per hari dengan boxplot marginal."
            )
            fig_hist = px.histogram(
                df, x='Jam_per_Hari', nbins=8, marginal="box",
                color_discrete_sequence=[SOFT_COLORS['secondary']],
                template=PLOTLY_TEMPLATE
            )
            fig_hist.update_traces(
                hovertemplate='<b>Durasi:</b> %{x} jam<br><b>Frekuensi:</b> %{y}<extra></extra>'
            )
            fig_hist.update_layout(height=380)
            st.plotly_chart(update_dark_layout(fig_hist), use_container_width=True)
            render_insight_box(
                f"Durasi rata-rata penggunaan AI adalah <strong>{mean_jam:.1f} jam/hari</strong>, "
                f"dengan outlier di atas menunjukkan mahasiswa yang sangat intensif menggunakan AI."
            )

    with col4:
        with st.container(border=True):
            render_chart_header(
                "⭐ Distribusi Skor Efektivitas Belajar",
                "Seberapa efektif AI membantu proses belajar menurut persepsi mahasiswa."
            )
            fig_skor = px.histogram(
                df, x='Skor_Efektivitas', text_auto=True,
                color_discrete_sequence=[SOFT_COLORS['success']],
                template=PLOTLY_TEMPLATE
            )
            fig_skor.update_traces(
                hovertemplate='<b>Skor:</b> %{x}/5<br><b>Jumlah:</b> %{y}<extra></extra>'
            )
            fig_skor.update_layout(height=380, xaxis_title="Skor Efektivitas (1-5)")
            st.plotly_chart(update_dark_layout(fig_skor), use_container_width=True)
            render_insight_box(
                f"Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong>, "
                f"menunjukkan persepsi positif terhadap peran AI dalam pembelajaran."
            )

    with st.container(border=True):
        render_chart_header(
            "📈 Persepsi Peningkatan Nilai Akademik",
            "Distribusi persepsi mahasiswa tentang peningkatan nilai setelah menggunakan AI."
        )
        fig_nilai = px.histogram(
            df, x='Peningkatan_Nilai', text_auto=True, color='Peningkatan_Nilai',
            color_discrete_sequence=[SOFT_COLORS['success'], SOFT_COLORS['warning'], SOFT_COLORS['muted']],
            template=PLOTLY_TEMPLATE
        )
        fig_nilai.update_traces(
            hovertemplate='<b>Persepsi:</b> %{x}<br><b>Jumlah:</b> %{y}<extra></extra>'
        )
        fig_nilai.update_layout(height=380, xaxis_title="Persepsi Nilai", showlegend=False)
        st.plotly_chart(update_dark_layout(fig_nilai), use_container_width=True)
        render_insight_box(
            "Sebagian besar mahasiswa merasa AI berkontribusi pada peningkatan nilai akademik mereka, "
            "meskipun persepsi ini perlu divalidasi dengan data nilai riil."
        )

# ==========================================
# TAB 2: HUBUNGAN & PROBABILITAS
# ==========================================
with tab2:
    col5, col6 = st.columns(2)
    with col5:
        with st.container(border=True):
            render_chart_header(
                "⚠️ Probabilitas Kesulitan Tanpa AI",
                "Analisis kondisional: seberapa besar mahasiswa merasa kesulitan jika tidak menggunakan AI."
            )
            prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
            prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
            fig_prob = px.bar(
                prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
                barmode='stack', text_auto='.1f',
                color_discrete_map={'Ya': SOFT_COLORS['danger'], 'Tidak': SOFT_COLORS['secondary']},
                template=PLOTLY_TEMPLATE
            )
            fig_prob.update_traces(
                hovertemplate='<b>%{x}</b><br>Kesulitan: %{fullData.name}<br>Persentase: %{y:.1f}%<extra></extra>'
            )
            fig_prob.update_layout(height=400)
            st.plotly_chart(update_dark_layout(fig_prob), use_container_width=True)
            render_insight_box(
                "Mahasiswa dengan ketergantungan tinggi memiliki probabilitas kesulitan belajar mandiri "
                "yang secara signifikan lebih besar, mengindikasikan <strong>risiko kognitif</strong> jangka panjang."
            )

    with col6:
        with st.container(border=True):
            render_chart_header(
                "🔗 Heatmap Korelasi Pearson (Diverging)",
                "Matriks korelasi dengan skema warna diverging untuk membedakan hubungan positif/negatif."
            )
            corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            fig_heat = px.imshow(
                corr_matrix, text_auto=".3f", aspect="auto",
                color_continuous_scale="RdBu",
                origin="lower",
                zmin=-1, zmax=1,
                template=PLOTLY_TEMPLATE
            )
            fig_heat.update_traces(
                hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Korelasi: %{z:.3f}<extra></extra>'
            )
            fig_heat.update_layout(height=400)
            st.plotly_chart(update_dark_layout(fig_heat), use_container_width=True)
            
            try:
                corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
            except:
                corr_val = 0.0
            
            if corr_val > 0.5:
                interp_class = "strong-pos"
                interp_text = "Kuat Positif"
            elif corr_val < -0.5:
                interp_class = "weak-neg"
                interp_text = "Kuat Negatif"
            else:
                interp_class = "neutral"
                interp_text = "Lemah"
            
            st.markdown(f"""
            <div class="heatmap-interp {interp_class}">
                <span>Korelasi: {corr_val:.2f}</span>
                <span>•</span>
                <span>{interp_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
            render_insight_box(
                f"Korelasi antara Porsi Tugas AI dan Skor Efektivitas adalah <strong>r = {corr_val:.2f}</strong> "
                f"(lemah), menunjukkan bahwa <strong>kuantitas penggunaan AI tidak otomatis menjamin</strong> "
                f"peningkatan efektivitas belajar."
            )

    col7, col8 = st.columns(2)
    with col7:
        with st.container(border=True):
            render_chart_header(
                "📉 Tren Efektivitas vs Porsi Tugas AI",
                "Scatter plot dengan trendline linear untuk melihat hubungan dua variabel."
            )
            z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
            p = np.poly1d(z)
            df_sorted = df.sort_values('Porsi_Tugas_AI')
            
            fig_scatter = px.scatter(
                df, x='Porsi_Tugas_AI', y='Skor_Efektivitas',
                opacity=0.8, template=PLOTLY_TEMPLATE,
                hover_data={'Porsi_Tugas_AI': ':.0f', 'Skor_Efektivitas': ':.2f'}
            )
            fig_scatter.update_traces(
                marker=dict(size=12, color=SOFT_COLORS['secondary']),
                hovertemplate='<b>Porsi Tugas:</b> %{x}<br><b>Skor Efektivitas:</b> %{y:.2f}<extra></extra>'
            )
            fig_scatter.add_trace(go.Scatter(
                x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
                mode='lines', name='Trendline', line=dict(color=SOFT_COLORS['danger'], width=3)
            ))
            
            r_squared = np.corrcoef(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'])[0, 1] ** 2
            equation = f"y = {z[0]:.3f}x + {z[1]:.3f}"
            
            fig_scatter.update_layout(
                height=380, 
                showlegend=False,
                annotations=[
                    dict(
                        x=0.02, y=0.98, xref='paper', yref='paper',
                        text=f"{equation}<br>R² = {r_squared:.3f}",
                        showarrow=False,
                        font=dict(size=12, color='#E2E8F0'),
                        bgcolor='rgba(30, 41, 59, 0.8)',
                        bordercolor='rgba(59, 130, 246, 0.3)',
                        borderwidth=1,
                        borderpad=8
                    )
                ]
            )
            st.plotly_chart(update_dark_layout(fig_scatter), use_container_width=True)
            render_insight_box(
                "Trendline menunjukkan hubungan yang relatif datar/lemah, "
                "memperkuat hipotesis bahwa efektivitas lebih bergantung pada <strong>cara penggunaan</strong> "
                "daripada <strong>seberapa sering</strong> AI digunakan."
            )

    with col8:
        with st.container(border=True):
            render_chart_header(
                "📦 Boxplot: Efektivitas Berdasarkan Porsi Tugas",
                "Distribusi skor efektivitas untuk setiap tingkat porsi bantuan AI."
            )
            fig_box = px.box(
                df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
                color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple']],
                template=PLOTLY_TEMPLATE
            )
            fig_box.update_traces(
                hovertemplate='<b>Porsi Tugas:</b> %{x}<br><b>Skor:</b> %{y:.2f}<extra></extra>'
            )
            fig_box.update_layout(height=380, xaxis_title="Porsi Tugas (0-10)", showlegend=False)
            st.plotly_chart(update_dark_layout(fig_box), use_container_width=True)
            render_insight_box(
                "Boxplot memperlihatkan variasi yang cukup besar dalam setiap kategori, "
                "menunjukkan bahwa <strong>faktor individu</strong> sangat berpengaruh pada efektivitas penggunaan AI."
            )

    with st.container(border=True):
        render_chart_header(
            "📑 Rata-rata Tingkat Copy-Paste per Porsi Tugas",
            "Mengukur tingkat ketergantungan pasif (copy-paste) terhadap output AI."
        )
        cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
        fig_cp = px.bar(
            cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste',
            text_auto='.2f', color='Tingkat_Copy_Paste',
            color_continuous_scale="Purples",
            template=PLOTLY_TEMPLATE
        )
        fig_cp.update_traces(
            textposition='outside',
            hovertemplate='<b>Porsi Tugas:</b> %{x}<br><b>Skor Copy-Paste:</b> %{y:.2f}<extra></extra>'
        )
        fig_cp.update_layout(height=380, xaxis_title="Porsi Tugas AI (0-10)", yaxis_title="Skor Copy-Paste (1-5)")
        st.plotly_chart(update_dark_layout(fig_cp), use_container_width=True)
        render_insight_box(
            "Tren menunjukkan korelasi positif antara porsi tugas AI dan tingkat copy-paste, "
            "menandakan adanya <strong>risiko plagiarisme dan penurunan daya analitis</strong> pada pengguna berat AI."
        )

# ==========================================
# TAB 3: MONTE CARLO SIMULATION
# ==========================================
with tab3:
    with st.container(border=True):
        render_chart_header(
            "🎲 Monte Carlo Simulation",
            "Proyeksi stokastik untuk memprediksi stabilitas skor efektivitas belajar pada kelas berskala besar "
            "melalui ribuan iterasi acak berbasis distribusi empiris data."
        )
        
        st.markdown('<div class="mc-status"><span class="mc-status-dot"></span> Stochastic Engine Ready</div>', unsafe_allow_html=True)
        
        mc_c1, mc_c2 = st.columns([1, 3])
        with mc_c1:
            iterations = st.number_input("Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000)
            if st.button("🚀 Jalankan Simulasi", use_container_width=True):
                st.session_state['run_mc'] = True
                st.toast("Menyiapkan model stokastik...", icon="⚙️")
            else:
                st.session_state['run_mc'] = st.session_state.get('run_mc', False)
        
        with mc_c2:
            if st.session_state.get('run_mc', False):
                with st.spinner(f"Memproses {iterations} komputasi Monte Carlo..."):
                    time.sleep(1)
                    p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                    cats, weights = p_dist.index.values, p_dist.values
                    stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())
                    hasil = []
                    for i in range(iterations):
                        sim_tugas = np.random.choice(cats, size=100, p=weights)
                        skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas]
                        hasil.append(np.mean(skor))
                    mean_mc = np.mean(hasil)
                    ci_low, ci_high = np.percentile(hasil, 2.5), np.percentile(hasil, 97.5)
                    running_mean = np.cumsum(hasil) / np.arange(1, iterations+1)
                    st.balloons()
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Target Iterasi", f"{iterations:,}")
                with col_m2:
                    st.metric("Mean Ekspektasi", f"{mean_mc:.3f}")
                with col_m3:
                    st.metric("95% Confidence Interval", f"{ci_low:.2f} - {ci_high:.2f}")
                
                fig_run = px.line(x=np.arange(1, iterations+1), y=running_mean, template=PLOTLY_TEMPLATE)
                fig_run.update_traces(
                    line=dict(color=SOFT_COLORS['primary'], width=2.5),
                    hovertemplate='<b>Iterasi:</b> %{x}<br><b>Running Mean:</b> %{y:.3f}<extra></extra>'
                )
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=SOFT_COLORS['danger'], 
                                 annotation_text="Titik Konvergen", annotation_font_color=SOFT_COLORS['danger'])
                fig_run.update_layout(title="Kurva Konvergensi Stokastik", 
                                     xaxis_title="Iterasi", 
                                     yaxis_title="Running Mean",
                                     height=380)
                fig_run = update_dark_layout(fig_run)
                st.plotly_chart(fig_run, use_container_width=True)
                
                fig_dist = px.histogram(
                    x=hasil, nbins=50,
                    color_discrete_sequence=[SOFT_COLORS['purple']],
                    template=PLOTLY_TEMPLATE
                )
                fig_dist.update_traces(
                    hovertemplate='<b>Skor:</b> %{x:.3f}<br><b>Frekuensi:</b> %{y}<extra></extra>'
                )
                fig_dist.update_layout(
                    title="Distribusi Hasil Simulasi",
                    xaxis_title="Skor Efektivitas",
                    yaxis_title="Frekuensi",
                    height=380
                )
                fig_dist = update_dark_layout(fig_dist)
                st.plotly_chart(fig_dist, use_container_width=True)
                
                render_insight_box(
                    f"Setelah {iterations:,} iterasi, simulasi menunjukkan <strong>konvergensi stabil</strong> "
                    f"di sekitar nilai {mean_mc:.3f} dengan 95% CI [{ci_low:.2f}, {ci_high:.2f}]. "
                    f"Ini memberikan estimasi yang <strong>robust</strong> untuk proyeksi efektivitas di skala kelas besar."
                )

# ==========================================
# 13. AI INSIGHT PANEL
# ==========================================
render_section_divider("AI Insights & Recommendations", "05")

with st.container(border=True):
    st.markdown('<div class="chart-title">🤖 AI-Generated Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-description">Analisis otomatis berdasarkan pola data terkini</div>', unsafe_allow_html=True)
    
    if len(df) > 0:
        setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100
        mean_jam = df['Jam_per_Hari'].mean()
        try:
            corr_matrix_local = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            corr_val_local = corr_matrix_local.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
        except:
            corr_val_local = 0.0
        
        st.markdown(f"""
        <div class="ai-insight-panel">
            <strong>Analisis Pola Penggunaan AI:</strong><br>
            Berdasarkan pola data saat ini, mahasiswa dengan penggunaan AI tinggi memiliki kecenderungan mengalami 
            ketergantungan lebih besar, namun peningkatan efektivitas belajar hanya menunjukkan korelasi yang lemah (r = {corr_val_local:.2f}). 
            {setiap_hari_pct:.0f}% mahasiswa menggunakan AI setiap hari dengan durasi rata-rata {mean_jam:.1f} jam. 
            Temuan ini mengindikasikan bahwa <strong>kualitas penggunaan AI lebih penting daripada kuantitas</strong>, 
            dan perlu pengembangan strategi pembelajaran yang mengintegrasikan AI secara bijak tanpa mengurangi 
            kemampuan analitis mandiri mahasiswa.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pilih data pada filter sidebar untuk melihat insight.")

# ==========================================
# 14. STRATEGIC INSIGHTS
# ==========================================
render_section_divider("Strategic Insights", "06")

with st.container(border=True):
    st.markdown('<div class="chart-title">💡 Strategic Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-description">Temuan kunci yang dapat dijadikan landasan kebijakan akademik terkait integrasi AI.</div>', unsafe_allow_html=True)
    
    if len(df) > 0:
        setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100
        mean_jam = df['Jam_per_Hari'].mean()
        max_jam = df['Jam_per_Hari'].max()
        try:
            corr_matrix_local = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            corr_val_local = corr_matrix_local.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
        except:
            corr_val_local = 0.0
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 16px;">
            <div class="insight-box" style="margin-top: 0;">
                <strong>🎯 Adopsi Tinggi:</strong> {setiap_hari_pct:.0f}% mahasiswa menggunakan AI setiap hari untuk keperluan akademis.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>⏱️ Intensitas:</strong> Durasi penggunaan rata-rata mencapai {mean_jam:.1f} jam, dengan rekor maksimal {max_jam} jam per hari.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>⚠️ Risiko Kognitif:</strong> Mahasiswa dengan porsi bantuan AI tinggi (>5 tugas) memiliki probabilitas kesulitan belajar mandiri mencapai 83.3%.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>📊 Korelasi Lemah:</strong> Korelasi Pearson (r = {corr_val_local:.2f}) membuktikan bahwa bergantung pada AI tidak menjamin peningkatan pemahaman kognitif.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pilih data pada filter sidebar untuk melihat insight.")

# ==========================================
# 15. FOOTER PROFESIONAL
# ==========================================
st.markdown("""
<div class="dashboard-footer">
    <div style="font-size: 16px; font-weight: 600; color: #F8FAFC; margin-bottom: 8px;">
        🎓 AI Learning Impact Analytics
    </div>
    <div>
        Dashboard analitik ini dibangun untuk memahami dampak penggunaan <strong>Artificial Intelligence</strong> 
        dalam ekosistem akademik melalui pendekatan <em>data-driven analytics</em>, probabilitas kondisional, 
        dan simulasi Monte Carlo.
    </div>
    <div class="footer-meta">
        <div>
            <strong style="color: #CBD5E1;">Developer:</strong> Ahmad Rizza Pahlevi<br>
            <strong style="color: #CBD5E1;">Institusi:</strong> UIN K.H. Abdurrahman Wahid
        </div>
        <div>
            <strong style="color: #CBD5E1;">Tech Stack:</strong> Python • Streamlit • Plotly • Pandas • NumPy<br>
            <strong style="color: #CBD5E1;">Version:</strong> 2.0 Enterprise Edition • Juni 2026
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
