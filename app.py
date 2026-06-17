import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ─── GLOBAL RESET ─── */
    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Inter', sans-serif !important;
        color: #F8FAFC;
    }

    /* ─── MAIN BACKGROUND: deep gradient, no grid ─── */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0F172A 0%, #0D1526 40%, #111827 70%, #0F172A 100%) !important;
        min-height: 100vh;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* ─── SIDEBAR ─── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1117 0%, #0F172A 100%) !important;
        border-right: 1px solid rgba(59, 130, 246, 0.15) !important;
    }

    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* ─── SIDEBAR BRAND ─── */
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 16px;
        background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(6,182,212,0.08));
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 14px;
        margin-bottom: 1.5rem;
    }
    .sidebar-brand-icon {
        font-size: 28px;
        line-height: 1;
    }
    .sidebar-brand-text {
        font-size: 13px;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.3;
        letter-spacing: 0.02em;
    }
    .sidebar-brand-sub {
        font-size: 10px;
        font-weight: 400;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ─── SIDEBAR SECTION LABELS ─── */
    .sidebar-section-label {
        font-size: 10px;
        font-weight: 700;
        color: #3B82F6;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        padding: 0 4px;
        margin-bottom: 0.5rem;
        margin-top: 1rem;
        display: block;
    }

    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.3), transparent);
        margin: 1rem 0;
        border: none;
    }

    /* ─── SIDEBAR INPUTS ─── */
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label {
        color: #94A3B8 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }

    /* ─── SIDEBAR RISK BOX ─── */
    .risk-box {
        padding: 10px 14px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .risk-high {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.3);
        color: #EF4444;
    }
    .risk-low {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.3);
        color: #22C55E;
    }

    /* ─── SIDEBAR META ─── */
    .sidebar-meta {
        background: rgba(30,41,59,0.6);
        border: 1px solid rgba(51,65,85,0.5);
        border-radius: 10px;
        padding: 12px 14px;
        margin-top: 0.5rem;
    }
    .sidebar-meta-row {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        color: #64748B;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .sidebar-meta-row:last-child { margin-bottom: 0; }
    .sidebar-meta-row span { color: #94A3B8; }

    /* ─── HERO SECTION ─── */
    .hero-section {
        background: linear-gradient(135deg,
            rgba(59,130,246,0.18) 0%,
            rgba(6,182,212,0.10) 40%,
            rgba(15,23,42,0.95) 100%);
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-section::after {
        content: '';
        position: absolute;
        bottom: -40px; left: 30%;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-eyebrow {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #3B82F6;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .hero-eyebrow::after {
        content: '';
        flex: 1;
        max-width: 40px;
        height: 1px;
        background: linear-gradient(90deg, #3B82F6, transparent);
    }
    .hero-title {
        font-size: 34px;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0 0 8px 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .hero-title span {
        background: linear-gradient(90deg, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #94A3B8;
        font-weight: 400;
        margin: 0 0 24px 0;
        max-width: 560px;
        line-height: 1.6;
    }
    .hero-meta-bar {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        align-items: center;
    }
    .hero-meta-pill {
        display: flex;
        align-items: center;
        gap: 7px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 50px;
        padding: 5px 14px;
        font-size: 12px;
        color: #CBD5E1;
        font-weight: 500;
        backdrop-filter: blur(4px);
    }
    .hero-meta-pill .pill-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #22C55E;
        box-shadow: 0 0 6px #22C55E;
        animation: pulse-green 2s infinite;
    }
    @keyframes pulse-green {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(0.85); }
    }

    /* ─── SECTION DIVIDER ─── */
    .section-divider {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 2rem 0 1.5rem 0;
    }
    .section-divider-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #475569;
        white-space: nowrap;
    }
    .section-divider-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(51,65,85,0.8), transparent);
    }
    .section-divider-line.left {
        background: linear-gradient(90deg, transparent, rgba(51,65,85,0.8));
        flex: 0.15;
    }

    /* ─── KPI CARDS ─── */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
        border: 1px solid rgba(51,65,85,0.6);
        border-radius: 18px;
        padding: 22px 24px;
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        cursor: default;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    }
    .kpi-card.blue:hover { border-color: rgba(59,130,246,0.5); box-shadow: 0 12px 40px rgba(59,130,246,0.15); }
    .kpi-card.cyan:hover { border-color: rgba(6,182,212,0.5); box-shadow: 0 12px 40px rgba(6,182,212,0.15); }
    .kpi-card.amber:hover { border-color: rgba(245,158,11,0.5); box-shadow: 0 12px 40px rgba(245,158,11,0.15); }
    .kpi-card.green:hover { border-color: rgba(34,197,94,0.5); box-shadow: 0 12px 40px rgba(34,197,94,0.15); }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        border-radius: 18px 18px 0 0;
    }
    .kpi-card.blue::before  { background: linear-gradient(90deg, #3B82F6, #06B6D4); }
    .kpi-card.cyan::before  { background: linear-gradient(90deg, #06B6D4, #3B82F6); }
    .kpi-card.amber::before { background: linear-gradient(90deg, #F59E0B, #EF4444); }
    .kpi-card.green::before { background: linear-gradient(90deg, #22C55E, #06B6D4); }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 14px;
    }
    .kpi-icon-wrap {
        width: 40px; height: 40px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    .kpi-card.blue  .kpi-icon-wrap { background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.2); }
    .kpi-card.cyan  .kpi-icon-wrap { background: rgba(6,182,212,0.15);  border: 1px solid rgba(6,182,212,0.2); }
    .kpi-card.amber .kpi-icon-wrap { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.2); }
    .kpi-card.green .kpi-icon-wrap { background: rgba(34,197,94,0.15);  border: 1px solid rgba(34,197,94,0.2); }

    .kpi-badge {
        font-size: 10px;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 50px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .badge-neutral  { background: rgba(100,116,139,0.2); color: #64748B; border: 1px solid rgba(100,116,139,0.2); }
    .badge-up       { background: rgba(34,197,94,0.12);  color: #22C55E; border: 1px solid rgba(34,197,94,0.25); }
    .badge-warn     { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.25); }
    .badge-down     { background: rgba(239,68,68,0.12);  color: #EF4444; border: 1px solid rgba(239,68,68,0.25); }

    .kpi-value {
        font-size: 30px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 4px;
        letter-spacing: -0.02em;
    }
    .kpi-card.blue  .kpi-value { color: #60A5FA; }
    .kpi-card.cyan  .kpi-value { color: #22D3EE; }
    .kpi-card.amber .kpi-value { color: #FCD34D; }
    .kpi-card.green .kpi-value { color: #4ADE80; }

    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        color: #64748B;
        letter-spacing: 0.01em;
    }
    .kpi-bar-track {
        height: 4px;
        background: rgba(51,65,85,0.6);
        border-radius: 99px;
        margin-top: 14px;
        overflow: hidden;
    }
    .kpi-bar-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.8s ease;
    }
    .kpi-card.blue  .kpi-bar-fill { background: linear-gradient(90deg, #3B82F6, #06B6D4); }
    .kpi-card.cyan  .kpi-bar-fill { background: linear-gradient(90deg, #06B6D4, #22D3EE); }
    .kpi-card.amber .kpi-bar-fill { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .kpi-card.green .kpi-bar-fill { background: linear-gradient(90deg, #22C55E, #4ADE80); }

    /* ─── EXECUTIVE SUMMARY ─── */
    .exec-summary {
        background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
        border: 1px solid rgba(59,130,246,0.15);
        border-radius: 18px;
        padding: 24px 28px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        backdrop-filter: blur(8px);
    }
    .exec-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #3B82F6;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .exec-title::before {
        content: '';
        width: 20px; height: 2px;
        background: #3B82F6;
        border-radius: 99px;
    }
    .exec-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
    }
    @media (max-width: 768px) { .exec-grid { grid-template-columns: 1fr; } }
    .exec-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(51,65,85,0.4);
        border-radius: 12px;
        padding: 14px 16px;
        transition: background 0.2s, border-color 0.2s;
    }
    .exec-item:hover {
        background: rgba(59,130,246,0.06);
        border-color: rgba(59,130,246,0.2);
    }
    .exec-item-icon { font-size: 16px; margin-bottom: 6px; }
    .exec-item-text {
        font-size: 13px;
        color: #CBD5E1;
        line-height: 1.5;
        font-weight: 400;
    }
    .exec-item-text strong { color: #F8FAFC; font-weight: 600; }

    /* ─── CHART CARD ─── */
    .chart-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.85), rgba(15,23,42,0.9));
        border: 1px solid rgba(51,65,85,0.5);
        border-radius: 18px;
        padding: 22px 22px 14px 22px;
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.22);
        backdrop-filter: blur(8px);
        margin-bottom: 0;
    }
    .chart-card:hover {
        transform: translateY(-3px);
        border-color: rgba(59,130,246,0.25);
        box-shadow: 0 10px 36px rgba(0,0,0,0.32), 0 0 0 1px rgba(59,130,246,0.08);
    }
    .chart-card-header {
        margin-bottom: 4px;
    }
    .chart-card-title {
        font-size: 15px;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0 0 3px 0;
        letter-spacing: -0.01em;
    }
    .chart-card-desc {
        font-size: 12px;
        color: #64748B;
        margin: 0 0 12px 0;
        font-weight: 400;
    }

    /* ─── INSIGHT BOX ─── */
    .insight-box {
        background: rgba(59,130,246,0.07);
        border: 1px solid rgba(59,130,246,0.18);
        border-radius: 10px;
        padding: 11px 15px;
        margin-top: 12px;
        display: flex;
        align-items: flex-start;
        gap: 10px;
        font-size: 12px;
        color: #94A3B8;
        line-height: 1.5;
        transition: background 0.2s;
    }
    .insight-box:hover {
        background: rgba(59,130,246,0.10);
    }
    .insight-box-icon {
        font-size: 14px;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .insight-box strong { color: #93C5FD; }

    /* ─── TAB NAV ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,23,42,0.6) !important;
        border: 1px solid rgba(51,65,85,0.5) !important;
        border-radius: 14px !important;
        padding: 5px !important;
        gap: 4px !important;
        backdrop-filter: blur(8px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        padding: 8px 20px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(59,130,246,0.18) !important;
        border: 1px solid rgba(59,130,246,0.3) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #93C5FD !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ─── SLIDER ─── */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #3B82F6 !important;
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.2) !important;
    }

    /* ─── BUTTON ─── */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        border: none !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.01em !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        box-shadow: 0 6px 18px rgba(59,130,246,0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* ─── MULTISELECT ─── */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(59,130,246,0.2) !important;
        border: 1px solid rgba(59,130,246,0.35) !important;
        border-radius: 6px !important;
    }
    .stMultiSelect [data-baseweb="tag"] span { color: #93C5FD !important; }

    /* ─── NUMBER INPUT ─── */
    .stNumberInput input {
        background: rgba(30,41,59,0.8) !important;
        border: 1px solid rgba(51,65,85,0.7) !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    .stNumberInput input:focus {
        border-color: rgba(59,130,246,0.5) !important;
        box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
    }

    /* ─── METRICS ─── */
    div[data-testid="stMetricValue"] { color: #60A5FA !important; font-weight: 800 !important; font-size: 28px !important; }
    div[data-testid="stMetricLabel"] { color: #64748B !important; font-size: 12px !important; font-weight: 500 !important; }
    div[data-testid="stMetricDelta"] { font-size: 12px !important; }

    /* ─── EXPANDER ─── */
    .stExpander details {
        background: rgba(30,41,59,0.5) !important;
        border: 1px solid rgba(51,65,85,0.5) !important;
        border-radius: 12px !important;
        padding: 2px !important;
    }
    .stExpander details summary {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
    }

    /* ─── SELECTBOX / DROPDOWN ─── */
    .stSelectbox > div > div {
        background: rgba(30,41,59,0.8) !important;
        border-color: rgba(51,65,85,0.7) !important;
        border-radius: 8px !important;
    }

    /* ─── SCROLLBAR ─── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(51,65,85,0.7); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(59,130,246,0.5); }

    /* ─── REMOVE STREAMLIT ARTIFACTS ─── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: transparent !important;
        border-color: transparent !important;
        border-radius: 0px !important;
        box-shadow: none !important;
    }

    /* ─── TEXT OVERRIDE ─── */
    p, h1, h2, h3, h4, h5, h6 { color: #F8FAFC !important; }
    label { color: #94A3B8 !important; }

    /* ─── MONTE CARLO CARD ─── */
    .mc-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 5px 14px;
        border-radius: 50px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .mc-status-idle {
        background: rgba(100,116,139,0.15);
        border: 1px solid rgba(100,116,139,0.3);
        color: #64748B;
    }
    .mc-status-running {
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.3);
        color: #F59E0B;
    }
    .mc-status-done {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.3);
        color: #22C55E;
    }
    .mc-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: currentColor;
        animation: blink 1.2s infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    .mc-metric-card {
        background: rgba(30,41,59,0.8);
        border: 1px solid rgba(51,65,85,0.5);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        transition: border-color 0.2s, transform 0.2s;
    }
    .mc-metric-card:hover {
        border-color: rgba(59,130,246,0.3);
        transform: translateY(-2px);
    }
    .mc-metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #60A5FA;
        letter-spacing: -0.02em;
        line-height: 1;
        margin-bottom: 5px;
    }
    .mc-metric-label {
        font-size: 11px;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ─── FOOTER ─── */
    .dashboard-footer {
        margin-top: 3rem;
        padding: 24px 32px;
        background: linear-gradient(135deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8));
        border: 1px solid rgba(51,65,85,0.4);
        border-radius: 18px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        backdrop-filter: blur(8px);
    }
    .footer-brand {
        font-size: 13px;
        font-weight: 700;
        color: #F8FAFC;
    }
    .footer-brand span {
        background: linear-gradient(90deg, #3B82F6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .footer-meta { font-size: 11px; color: #475569; line-height: 1.6; }
    .footer-tech {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        align-items: center;
    }
    .tech-badge {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 50px;
        padding: 4px 11px;
        font-size: 11px;
        color: #64748B;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ─── COLOR PALETTE ───────────────────────────────────────────────────────────
SOFT_COLORS = {
    'primary':   '#3B82F6',
    'secondary': '#06B6D4',
    'success':   '#22C55E',
    'danger':    '#EF4444',
    'warning':   '#F59E0B',
    'purple':    '#A78BFA',
    'muted':     '#64748B',
}

PLOTLY_TEMPLATE = 'plotly_dark'

CHART_PAPER_BG = 'rgba(0,0,0,0)'
CHART_PLOT_BG  = 'rgba(0,0,0,0)'

# ==========================================
# 2. MEMUAT & PRE-PROCESSING DATA
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
    df['Is_Ketergantungan_Tinggi'] = np.where(
        df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)'
    )
    try:
        df['Date_Parsed'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
    except:
        df['Date_Parsed'] = df['Timestamp']
    return df

df_raw = load_data()

# ==========================================
# 3. SIDEBAR: FILTER & NAVIGASI
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🎓</div>
            <div>
                <div class="sidebar-brand-text">AI Learning Impact</div>
                <div class="sidebar-brand-sub">Analytics Dashboard</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">📁 Filter Dataset</span>', unsafe_allow_html=True)

    with st.expander("Program Studi & Semester", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist()
        filter_prodi = st.multiselect(
            "Program Studi", options=prodi_list, default=prodi_list,
            label_visibility="collapsed",
            placeholder="Pilih Program Studi..."
        )
        semester_list = sorted(df_raw['Semester'].unique().tolist())
        filter_semester = st.multiselect(
            "Semester", options=semester_list, default=semester_list,
            label_visibility="collapsed",
            placeholder="Pilih Semester..."
        )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-section-label">🔮 Profil Simulator</span>', unsafe_allow_html=True)

    with st.expander("Pengaturan Simulasi Pribadi", expanded=True):
        sim_tugas = st.slider("Porsi Bantuan AI (dari 10 tugas):", 0, 10, 6)
        if sim_tugas > 5:
            st.markdown(
                '<div class="risk-box risk-high">⚠️ Risiko Ketergantungan Tinggi</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="risk-box risk-low">✅ Penggunaan Dalam Batas Aman</div>',
                unsafe_allow_html=True
            )

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-meta">
            <div class="sidebar-meta-row">👨‍💻 <span>Ahmad Rizza Pahlevi</span></div>
            <div class="sidebar-meta-row">🏛️ <span>UIN K.H. Abdurrahman Wahid</span></div>
            <div class="sidebar-meta-row">📅 <span>Update: Juni 2026</span></div>
        </div>
    """, unsafe_allow_html=True)


# ─── APPLY FILTER ────────────────────────────────────────────────────────────
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ─── HELPER ──────────────────────────────────────────────────────────────────
def update_dark_layout(fig, height=350):
    fig.update_layout(
        paper_bgcolor=CHART_PAPER_BG,
        plot_bgcolor=CHART_PLOT_BG,
        font=dict(family='Inter, sans-serif', color='#CBD5E1', size=12),
        height=height,
        margin=dict(t=10, b=10, l=0, r=0),
        legend=dict(
            bgcolor='rgba(15,23,42,0.8)',
            bordercolor='rgba(51,65,85,0.5)',
            borderwidth=1,
            font=dict(color='#94A3B8', size=11)
        ),
    )
    fig.update_xaxes(
        gridcolor='rgba(51,65,85,0.3)',
        zerolinecolor='rgba(51,65,85,0.4)',
        tickfont=dict(color='#64748B', size=11),
        title_font=dict(color='#94A3B8', size=12)
    )
    fig.update_yaxes(
        gridcolor='rgba(51,65,85,0.3)',
        zerolinecolor='rgba(51,65,85,0.4)',
        tickfont=dict(color='#64748B', size=11),
        title_font=dict(color='#94A3B8', size=12)
    )
    return fig

def chart_card(title, desc):
    st.markdown(f"""
        <div class="chart-card-header">
            <p class="chart-card-title">{title}</p>
            <p class="chart-card-desc">{desc}</p>
        </div>
    """, unsafe_allow_html=True)

def insight_box(text):
    st.markdown(f"""
        <div class="insight-box">
            <span class="insight-box-icon">💡</span>
            <span>{text}</span>
        </div>
    """, unsafe_allow_html=True)

def section_divider(label):
    st.markdown(f"""
        <div class="section-divider">
            <div class="section-divider-line left"></div>
            <span class="section-divider-label">{label}</span>
            <div class="section-divider-line"></div>
        </div>
    """, unsafe_allow_html=True)


# ==========================================
# 4. HERO SECTION
# ==========================================
n_responden = len(df)
setiap_hari_pct = len(df[df['Frekuensi_Penggunaan'] == 'Setiap hari']) / max(len(df), 1) * 100

st.markdown(f"""
    <div class="hero-section">
        <div class="hero-eyebrow">Research Analytics Dashboard</div>
        <h1 class="hero-title">AI Learning Impact <span>Analytics</span></h1>
        <p class="hero-subtitle">
            Monitoring komprehensif perilaku penggunaan Artificial Intelligence
            pada ekosistem akademik mahasiswa perguruan tinggi.
        </p>
        <div class="hero-meta-bar">
            <div class="hero-meta-pill">
                <span class="pill-dot"></span>
                Live · {n_responden} Responden Aktif
            </div>
            <div class="hero-meta-pill">📅 Update: Juni 2026</div>
            <div class="hero-meta-pill">👨‍💻 Ahmad Rizza Pahlevi</div>
            <div class="hero-meta-pill">🏛️ UIN K.H. Abdurrahman Wahid</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. KPI CARDS
# ==========================================
section_divider("Key Performance Indicators")

avg_jam   = df['Jam_per_Hari'].mean() if len(df) > 0 else 0
avg_tugas = df['Porsi_Tugas_AI'].mean() if len(df) > 0 else 0
avg_skor  = df['Skor_Efektivitas'].mean() if len(df) > 0 else 0

bar_jam   = min(avg_jam / 10.0, 1.0) * 100
bar_tugas = avg_tugas / 10.0 * 100
bar_skor  = avg_skor / 5.0 * 100

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class="kpi-card blue">
            <div class="kpi-header">
                <div class="kpi-icon-wrap">👥</div>
                <span class="kpi-badge badge-neutral">Dataset</span>
            </div>
            <div class="kpi-value">{n_responden}</div>
            <div class="kpi-label">Total Mahasiswa Terfilter</div>
            <div class="kpi-bar-track"><div class="kpi-bar-fill" style="width:100%"></div></div>
        </div>
    """, unsafe_allow_html=True)

with k2:
    delta_cls = "badge-warn" if avg_jam >= 3 else "badge-up"
    st.markdown(f"""
        <div class="kpi-card cyan">
            <div class="kpi-header">
                <div class="kpi-icon-wrap">⏱️</div>
                <span class="kpi-badge {delta_cls}">{'⬆ Tinggi' if avg_jam >= 3 else '✓ Normal'}</span>
            </div>
            <div class="kpi-value">{avg_jam:.1f} Jam</div>
            <div class="kpi-label">Durasi Penggunaan AI / Hari</div>
            <div class="kpi-bar-track"><div class="kpi-bar-fill" style="width:{bar_jam:.0f}%"></div></div>
        </div>
    """, unsafe_allow_html=True)

with k3:
    dep_cls = "badge-down" if avg_tugas > 5 else "badge-up"
    dep_lbl = "⚠ Ketergantungan" if avg_tugas > 5 else "✓ Aman"
    st.markdown(f"""
        <div class="kpi-card amber">
            <div class="kpi-header">
                <div class="kpi-icon-wrap">📝</div>
                <span class="kpi-badge {dep_cls}">{dep_lbl}</span>
            </div>
            <div class="kpi-value">{avg_tugas:.1f}/10</div>
            <div class="kpi-label">Rata-rata Porsi Tugas Dibantu AI</div>
            <div class="kpi-bar-track"><div class="kpi-bar-fill" style="width:{bar_tugas:.0f}%"></div></div>
        </div>
    """, unsafe_allow_html=True)

with k4:
    eff_cls = "badge-up" if avg_skor >= 3.5 else "badge-warn"
    eff_lbl = "⭐ Efektif" if avg_skor >= 3.5 else "⚠ Perlu Perhatian"
    st.markdown(f"""
        <div class="kpi-card green">
            <div class="kpi-header">
                <div class="kpi-icon-wrap">⭐</div>
                <span class="kpi-badge {eff_cls}">{eff_lbl}</span>
            </div>
            <div class="kpi-value">{avg_skor:.2f}/5</div>
            <div class="kpi-label">Skor Efektivitas Belajar</div>
            <div class="kpi-bar-track"><div class="kpi-bar-fill" style="width:{bar_skor:.0f}%"></div></div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. EXECUTIVE SUMMARY
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

ketergantungan_pct = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5 Tugas)']) / max(len(df), 1) * 100

st.markdown(f"""
    <div class="exec-summary">
        <div class="exec-title">Executive Summary</div>
        <div class="exec-grid">
            <div class="exec-item">
                <div class="exec-item-icon">🤖</div>
                <div class="exec-item-text">
                    <strong>{setiap_hari_pct:.0f}% mahasiswa</strong> menggunakan AI setiap hari,
                    menunjukkan integrasi teknologi yang sangat dalam pada proses belajar.
                </div>
            </div>
            <div class="exec-item">
                <div class="exec-item-icon">⚠️</div>
                <div class="exec-item-text">
                    <strong>{ketergantungan_pct:.0f}% responden</strong> memiliki tingkat ketergantungan tinggi (>5 tugas dibantu AI),
                    berisiko pada kemandirian kognitif.
                </div>
            </div>
            <div class="exec-item">
                <div class="exec-item-icon">📊</div>
                <div class="exec-item-text">
                    Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong> mengindikasikan manfaat yang masih belum optimal
                    dari penggunaan AI dalam pembelajaran.
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 7. TABS NAVIGASI
# ==========================================
section_divider("Analisis Data")

tab1, tab2, tab3 = st.tabs([
    "📊  Eksplorasi Deskriptif",
    "🔗  Hubungan & Probabilitas",
    "🎲  Monte Carlo Simulation"
])

# ==========================================
# TAB 1: EKSPLORASI DESKRIPTIF
# ==========================================
with tab1:

    # ── CHART 1: Tren Frekuensi ──────────────────────────────────────────────
    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "📈 Tren Frekuensi Penggunaan AI",
            "Distribusi intensitas penggunaan AI per kategori frekuensi"
        )
        trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
        trend_data.columns = ['Frekuensi', 'Jumlah']

        fig_hero = px.bar(
            trend_data, x='Frekuensi', y='Jumlah',
            text='Jumlah', color='Frekuensi',
            color_discrete_sequence=[
                SOFT_COLORS['primary'], SOFT_COLORS['secondary'],
                SOFT_COLORS['purple'], SOFT_COLORS['muted']
            ],
            template=PLOTLY_TEMPLATE
        )
        fig_hero.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(update_dark_layout(fig_hero, 340), use_container_width=True)

        top_freq = trend_data.iloc[0]['Frekuensi'] if len(trend_data) > 0 else '-'
        top_n    = trend_data.iloc[0]['Jumlah']    if len(trend_data) > 0 else 0
        insight_box(
            f"Kategori frekuensi terbanyak adalah <strong>{top_freq}</strong> dengan "
            f"<strong>{top_n} mahasiswa</strong>. Pola ini menunjukkan adopsi AI yang tinggi "
            f"dalam rutinitas akademik harian."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # ── CHART 2: Donut ───────────────────────────────────────────────────────
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "🍩 Distribusi Intensitas Ketergantungan",
            "Proporsi mahasiswa berdasarkan tingkat ketergantungan AI"
        )
        fig_pie = px.pie(
            df, names='Is_Ketergantungan_Tinggi', hole=0.55,
            color='Is_Ketergantungan_Tinggi',
            color_discrete_map={
                'Tinggi (>5 Tugas)': SOFT_COLORS['danger'],
                'Rendah (<=5 Tugas)': SOFT_COLORS['secondary']
            },
            template=PLOTLY_TEMPLATE
        )
        fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(update_dark_layout(fig_pie, 340), use_container_width=True)
        insight_box(
            f"<strong>{ketergantungan_pct:.0f}% mahasiswa</strong> menunjukkan pola ketergantungan "
            f"tinggi terhadap AI. Perlu intervensi literasi digital yang lebih baik."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHART 3: Histogram Porsi ─────────────────────────────────────────────
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "📊 Distribusi Porsi Tugas Dibantu AI",
            "Sebaran jumlah tugas yang diselesaikan dengan bantuan AI"
        )
        fig_porsi = px.histogram(
            df, x='Porsi_Tugas_AI', text_auto=True,
            color_discrete_sequence=[SOFT_COLORS['primary']],
            template=PLOTLY_TEMPLATE
        )
        fig_porsi.update_traces(marker_line_width=0)
        fig_porsi.update_layout(xaxis_title="Jumlah Tugas (0–10)", yaxis_title="Mahasiswa", showlegend=False)
        st.plotly_chart(update_dark_layout(fig_porsi, 340), use_container_width=True)
        insight_box(
            f"Rata-rata porsi tugas dibantu AI adalah <strong>{avg_tugas:.1f}/10</strong>. "
            f"Distribusi cenderung condong ke nilai tinggi, mengindikasikan ketergantungan substansial."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    # ── CHART 4: Durasi ──────────────────────────────────────────────────────
    with col3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "⏳ Histogram Durasi Pemakaian Harian",
            "Sebaran waktu penggunaan AI per hari (jam)"
        )
        fig_hist = px.histogram(
            df, x='Jam_per_Hari', nbins=8, marginal="box",
            color_discrete_sequence=[SOFT_COLORS['secondary']],
            template=PLOTLY_TEMPLATE
        )
        fig_hist.update_traces(marker_line_width=0)
        st.plotly_chart(update_dark_layout(fig_hist, 340), use_container_width=True)
        max_jam = df['Jam_per_Hari'].max() if len(df) > 0 else 0
        insight_box(
            f"Durasi rata-rata <strong>{avg_jam:.1f} jam/hari</strong>, dengan maksimum mencapai "
            f"<strong>{max_jam} jam/hari</strong>. Mahasiswa dengan durasi >4 jam perlu pemantauan khusus."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHART 5: Skor Efektivitas ────────────────────────────────────────────
    with col4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "⭐ Distribusi Skor Efektivitas Belajar",
            "Persepsi mahasiswa terhadap efektivitas belajar menggunakan AI"
        )
        fig_skor = px.histogram(
            df, x='Skor_Efektivitas', text_auto=True,
            color_discrete_sequence=[SOFT_COLORS['success']],
            template=PLOTLY_TEMPLATE
        )
        fig_skor.update_traces(marker_line_width=0)
        fig_skor.update_layout(xaxis_title="Skor Efektivitas (1–5)", showlegend=False)
        st.plotly_chart(update_dark_layout(fig_skor, 340), use_container_width=True)
        insight_box(
            f"Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong>. "
            f"Nilai ini menunjukkan persepsi yang {'positif' if avg_skor >= 3.5 else 'moderat'} "
            f"terhadap manfaat AI, namun belum mencapai potensi maksimal."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # ── CHART 6: Peningkatan Nilai ───────────────────────────────────────────
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card(
        "📈 Persepsi Peningkatan Nilai Akademik",
        "Distribusi persepsi mahasiswa terhadap dampak AI pada nilai mereka"
    )
    fig_nilai = px.histogram(
        df, x='Peningkatan_Nilai', text_auto=True,
        color='Peningkatan_Nilai',
        color_discrete_sequence=[
            SOFT_COLORS['success'], SOFT_COLORS['warning'], SOFT_COLORS['muted']
        ],
        template=PLOTLY_TEMPLATE
    )
    fig_nilai.update_layout(showlegend=False)
    st.plotly_chart(update_dark_layout(fig_nilai, 320), use_container_width=True)
    insight_box(
        "Persepsi peningkatan nilai bervariasi. Mahasiswa dengan intensitas penggunaan AI terstruktur "
        "cenderung melaporkan peningkatan nilai yang lebih konsisten dibandingkan pengguna sporadis."
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# TAB 2: HUBUNGAN & PROBABILITAS
# ==========================================
with tab2:

    col5, col6 = st.columns(2)

    # ── CHART 7: Probabilitas ────────────────────────────────────────────────
    with col5:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "⚠️ Probabilitas Kesulitan Belajar Mandiri",
            "Persentase kesulitan belajar tanpa AI berdasarkan tingkat ketergantungan"
        )
        prob_df = pd.crosstab(
            df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index'
        ) * 100
        prob_df = prob_df.reset_index().melt(
            id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase'
        )
        fig_prob = px.bar(
            prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
            barmode='stack', text_auto='.1f',
            color_discrete_map={
                'Ya': SOFT_COLORS['danger'],
                'Tidak': SOFT_COLORS['secondary']
            },
            template=PLOTLY_TEMPLATE
        )
        fig_prob.update_traces(marker_line_width=0)
        st.plotly_chart(update_dark_layout(fig_prob, 380), use_container_width=True)
        insight_box(
            "Mahasiswa dengan <strong>ketergantungan tinggi (>5 tugas)</strong> memiliki probabilitas "
            "kesulitan belajar mandiri yang jauh lebih besar. Ini mengindikasikan risiko akademik "
            "jangka panjang yang signifikan."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHART 8: Heatmap Korelasi ────────────────────────────────────────────
    with col6:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "🔗 Heatmap Korelasi Pearson",
            "Matriks korelasi antar variabel numerik utama (diverging scale)"
        )
        corr_matrix = df[[
            'Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas'
        ]].corr()
        fig_heat = px.imshow(
            corr_matrix, text_auto=".3f", aspect="auto",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            origin="lower",
            template=PLOTLY_TEMPLATE
        )
        fig_heat.update_coloraxes(
            colorbar=dict(
                tickfont=dict(color='#64748B', size=10),
                title=dict(text='r', font=dict(color='#64748B'))
            )
        )
        st.plotly_chart(update_dark_layout(fig_heat, 380), use_container_width=True)
        try:
            corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
            corr_txt = f"Korelasi Porsi Tugas ↔ Efektivitas: <strong>r = {corr_val:.3f}</strong> (lemah)"
        except:
            corr_txt = "Skema diverging memudahkan identifikasi korelasi positif (biru) dan negatif (merah)."
        insight_box(corr_txt + " — Warna merah menandakan korelasi negatif, biru korelasi positif.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col7, col8 = st.columns(2)

    # ── CHART 9: Scatter + Trendline ─────────────────────────────────────────
    with col7:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "📉 Tren Efektivitas vs Porsi Tugas AI",
            "Scatter plot dengan regresi linear — semakin banyak bantuan AI, seberapa efektif?"
        )
        z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
        p = np.poly1d(z)
        df_sorted = df.sort_values('Porsi_Tugas_AI')
        fig_scatter = px.scatter(
            df, x='Porsi_Tugas_AI', y='Skor_Efektivitas',
            opacity=0.75, template=PLOTLY_TEMPLATE
        )
        fig_scatter.update_traces(marker=dict(size=10, color=SOFT_COLORS['secondary']))
        fig_scatter.add_trace(go.Scatter(
            x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
            mode='lines', name='Trendline',
            line=dict(color=SOFT_COLORS['danger'], width=2.5, dash='dot')
        ))
        fig_scatter.update_layout(showlegend=False)
        st.plotly_chart(update_dark_layout(fig_scatter, 340), use_container_width=True)
        slope_dir = "negatif" if z[0] < 0 else "positif"
        insight_box(
            f"Trendline menunjukkan kemiringan <strong>{slope_dir}</strong> "
            f"(slope ≈ {z[0]:.3f}), mengindikasikan bahwa peningkatan porsi bantuan AI "
            f"{'tidak mendorong' if z[0] < 0 else 'sedikit mendorong'} efektivitas belajar."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CHART 10: Boxplot ────────────────────────────────────────────────────
    with col8:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card(
            "📦 Boxplot Efektivitas per Porsi Tugas",
            "Sebaran & outlier skor efektivitas di setiap level porsi tugas AI"
        )
        fig_box = px.box(
            df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
            color_discrete_sequence=[
                SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple']
            ],
            template=PLOTLY_TEMPLATE
        )
        fig_box.update_layout(
            xaxis_title="Porsi Tugas (0–10)", showlegend=False
        )
        st.plotly_chart(update_dark_layout(fig_box, 340), use_container_width=True)
        insight_box(
            "Variasi (IQR) yang lebar pada level tugas tinggi mengindikasikan hasil yang tidak konsisten "
            "— sebagian mahasiswa tetap efektif, namun sebagian lainnya mengalami penurunan pemahaman."
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHART 11: Copy-Paste Bar ─────────────────────────────────────────────
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card(
        "📑 Rata-rata Tingkat Copy-Paste per Porsi Tugas",
        "Korelasi antara ketergantungan AI dan perilaku copy-paste tanpa pemrosesan mandiri"
    )
    cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
    fig_cp = px.bar(
        cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste',
        text_auto='.2f', color='Tingkat_Copy_Paste',
        color_continuous_scale=[
            [0, '#06B6D4'], [0.5, '#8B5CF6'], [1, '#EF4444']
        ],
        template=PLOTLY_TEMPLATE
    )
    fig_cp.update_traces(textposition='outside', marker_line_width=0)
    fig_cp.update_layout(
        xaxis_title="Porsi Tugas AI (0–10)",
        yaxis_title="Skor Copy-Paste (1–5)"
    )
    st.plotly_chart(update_dark_layout(fig_cp, 320), use_container_width=True)
    insight_box(
        "Terlihat tren positif antara porsi tugas AI dan tingkat copy-paste, "
        "mengonfirmasi bahwa penggunaan AI yang berlebihan mendorong perilaku "
        "<strong>surface learning</strong> daripada pemahaman mendalam."
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 8. MONTE CARLO SIMULATION
# ==========================================
with tab3:

    # ── Header Monte Carlo ────────────────────────────────────────────────────
    mc_header_col, mc_status_col = st.columns([3, 1])
    with mc_header_col:
        section_divider("Stochastic Simulation Engine")
    with mc_status_col:
        mc_current_state = st.session_state.get('run_mc', False)
        status_class = "mc-status-done" if mc_current_state else "mc-status-idle"
        status_text  = "Completed" if mc_current_state else "Idle"
        status_dot   = '<span class="mc-dot"></span>' if not mc_current_state else '●'
        st.markdown(f"""
            <div style="margin-top:1.8rem; text-align:right;">
                <span class="mc-status-pill {status_class}">{status_dot} {status_text}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card(
        "🎲 Monte Carlo Simulation",
        "Proyeksi stokastik stabilitas skor efektivitas belajar pada kelas berskala besar (n=100)"
    )

    mc_c1, mc_c2 = st.columns([1, 3])

    with mc_c1:
        st.markdown("<br>", unsafe_allow_html=True)
        iterations = st.number_input(
            "Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000
        )
        run_btn = st.button("🚀 Jalankan Simulasi", use_container_width=True)
        if run_btn:
            st.session_state['run_mc'] = True
            st.toast("Menyiapkan model stokastik...", icon="⚙️")
        else:
            st.session_state['run_mc'] = st.session_state.get('run_mc', False)

        st.markdown("""
            <div style="margin-top:16px; padding:12px 14px;
                background:rgba(59,130,246,0.07);
                border:1px solid rgba(59,130,246,0.18);
                border-radius:10px; font-size:11px; color:#64748B; line-height:1.6;">
                <strong style="color:#93C5FD;">Model Info</strong><br>
                • Distribusi: Normal<br>
                • Sample / iterasi: 100<br>
                • CI: 95% (Percentile)<br>
                • Clip: [1, 5]
            </div>
        """, unsafe_allow_html=True)

    with mc_c2:
        if st.session_state.get('run_mc', False):
            with st.spinner(f"Memproses {iterations:,} komputasi stokastik..."):
                time.sleep(1)

                p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                cats, weights = p_dist.index.values, p_dist.values
                stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(
                    ['mean', 'std']
                ).fillna(df['Skor_Efektivitas'].std())

                hasil = []
                for i in range(iterations):
                    sim_tugas_mc = np.random.choice(cats, size=100, p=weights)
                    skor = [
                        np.clip(
                            np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']),
                            1, 5
                        )
                        for p in sim_tugas_mc
                    ]
                    hasil.append(np.mean(skor))

                mean_mc    = np.mean(hasil)
                ci_low     = np.percentile(hasil, 2.5)
                ci_high    = np.percentile(hasil, 97.5)
                ci_width   = ci_high - ci_low
                running_mean = np.cumsum(hasil) / np.arange(1, iterations + 1)

                st.balloons()

            # ── Metrics ─────────────────────────────────────────────────────
            mc_m1, mc_m2, mc_m3, mc_m4 = st.columns(4)
            with mc_m1:
                st.markdown(f"""
                    <div class="mc-metric-card">
                        <div class="mc-metric-value">{iterations:,}</div>
                        <div class="mc-metric-label">Total Iterasi</div>
                    </div>
                """, unsafe_allow_html=True)
            with mc_m2:
                st.markdown(f"""
                    <div class="mc-metric-card">
                        <div class="mc-metric-value">{mean_mc:.3f}</div>
                        <div class="mc-metric-label">Mean Ekspektasi</div>
                    </div>
                """, unsafe_allow_html=True)
            with mc_m3:
                st.markdown(f"""
                    <div class="mc-metric-card">
                        <div class="mc-metric-value">{ci_low:.3f}–{ci_high:.3f}</div>
                        <div class="mc-metric-label">95% Confidence Interval</div>
                    </div>
                """, unsafe_allow_html=True)
            with mc_m4:
                st.markdown(f"""
                    <div class="mc-metric-card">
                        <div class="mc-metric-value">{ci_width:.3f}</div>
                        <div class="mc-metric-label">Lebar CI</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Convergence Chart ────────────────────────────────────────────
            st.markdown('<div class="chart-card" style="margin-top:0">', unsafe_allow_html=True)
            chart_card(
                "📉 Kurva Konvergensi Running Mean",
                "Stabilitas estimasi mean skor efektivitas seiring bertambahnya iterasi"
            )

            # CI band
            n_pts = min(iterations, 5000)
            step  = max(1, iterations // n_pts)
            xs    = np.arange(1, iterations + 1)[::step]
            ys    = running_mean[::step]

            fig_run = go.Figure()
            fig_run.add_trace(go.Scatter(
                x=xs, y=ys,
                mode='lines', name='Running Mean',
                line=dict(color=SOFT_COLORS['primary'], width=2),
                fill='none'
            ))
            fig_run.add_hline(
                y=mean_mc, line_dash="dash",
                line_color=SOFT_COLORS['danger'], line_width=1.5,
                annotation_text=f"Konvergen: {mean_mc:.3f}",
                annotation_font_color='#EF4444',
                annotation_font_size=11
            )
            fig_run.add_hrect(
                y0=ci_low, y1=ci_high,
                fillcolor='rgba(59,130,246,0.07)',
                line=dict(color='rgba(59,130,246,0.2)', width=1, dash='dot'),
                annotation_text="95% CI",
                annotation_font_color='#3B82F6',
                annotation_font_size=10,
                annotation_position="right"
            )
            fig_run.update_layout(
                xaxis_title="Iterasi", yaxis_title="Running Mean",
                template=PLOTLY_TEMPLATE, showlegend=False
            )
            st.plotly_chart(update_dark_layout(fig_run, 300), use_container_width=True)

            insight_box(
                f"Model konvergen pada nilai <strong>{mean_mc:.3f}</strong> dengan interval kepercayaan 95% "
                f"antara <strong>{ci_low:.3f}</strong> dan <strong>{ci_high:.3f}</strong>. "
                f"Lebar CI sebesar {ci_width:.3f} menunjukkan model yang {'stabil' if ci_width < 0.1 else 'cukup stabil'}."
            )
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
                <div style="
                    display:flex; flex-direction:column; align-items:center; justify-content:center;
                    padding: 60px 20px; gap: 16px;
                    background: rgba(15,23,42,0.4);
                    border: 1px dashed rgba(51,65,85,0.5);
                    border-radius: 14px; margin-top: 8px;
                ">
                    <span style="font-size:48px; opacity:0.4;">🎲</span>
                    <p style="color:#475569; font-size:14px; text-align:center; margin:0; font-weight:500;">
                        Model stokastik siap dijalankan.<br>
                        <span style="color:#64748B; font-size:12px;">
                        Atur jumlah iterasi dan klik <strong style="color:#3B82F6">Jalankan Simulasi</strong> untuk memulai.
                        </span>
                    </p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close chart-card


# ==========================================
# 9. KEY INSIGHTS SECTION
# ==========================================
section_divider("Key Insights & Temuan Utama")

with st.container():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card(
        "💡 Ringkasan Temuan Analitik",
        "Interpretasi otomatis berdasarkan data yang sedang ditampilkan"
    )

    if len(df) > 0:
        try:
            corr_matrix_ins = df[[
                'Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas'
            ]].corr()
            corr_val = corr_matrix_ins.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
        except:
            corr_val = 0.0

        max_jam = df['Jam_per_Hari'].max()

        ins_col1, ins_col2 = st.columns(2)
        with ins_col1:
            st.markdown(f"""
                <div class="exec-item" style="margin-bottom:10px;">
                    <div class="exec-item-icon">🤖</div>
                    <div class="exec-item-text">
                        <strong>{setiap_hari_pct:.0f}% mahasiswa</strong> menggunakan AI setiap hari
                        untuk keperluan akademik — adopsi teknologi yang masif di lingkungan kampus.
                    </div>
                </div>
                <div class="exec-item">
                    <div class="exec-item-icon">⏱️</div>
                    <div class="exec-item-text">
                        Durasi penggunaan rata-rata <strong>{avg_jam:.1f} jam/hari</strong>,
                        dengan rekor maksimal <strong>{max_jam} jam/hari</strong>.
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with ins_col2:
            st.markdown(f"""
                <div class="exec-item" style="margin-bottom:10px;">
                    <div class="exec-item-icon">⚠️</div>
                    <div class="exec-item-text">
                        Mahasiswa dengan porsi bantuan AI tinggi (>5 tugas) memiliki probabilitas
                        kesulitan belajar mandiri yang sangat besar — <strong>risiko ketergantungan kritis</strong>.
                    </div>
                </div>
                <div class="exec-item">
                    <div class="exec-item-icon">📊</div>
                    <div class="exec-item-text">
                        Korelasi Pearson yang lemah (<strong>r = {corr_val:.2f}</strong>) membuktikan
                        bahwa bergantung pada AI <strong>tidak menjamin</strong> efektivitas pemahaman meningkat.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown(
            '<p style="color:#475569; font-size:13px; padding:16px 0;">Pilih data pada filter sidebar untuk melihat insight.</p>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 10. FOOTER
# ==========================================
st.markdown("""
    <div class="dashboard-footer">
        <div>
            <div class="footer-brand">AI Learning Impact <span>Analytics</span></div>
            <div class="footer-meta">
                Penelitian Ilmiah · Data Science Portfolio · Sidang Skripsi 2026
            </div>
        </div>
        <div>
            <div class="footer-meta" style="margin-bottom:6px;">👨‍💻 Ahmad Rizza Pahlevi &nbsp;|&nbsp; 🏛️ UIN K.H. Abdurrahman Wahid &nbsp;|&nbsp; 📅 Juni 2026</div>
        </div>
        <div class="footer-tech">
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">⚡ Streamlit</span>
            <span class="tech-badge">📊 Plotly</span>
            <span class="tech-badge">🔢 NumPy / Pandas</span>
        </div>
    </div>
""", unsafe_allow_html=True)
