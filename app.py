import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from datetime import datetime

# ══════════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════
# 2. NEO GLASS ANALYTICS THEME (CLEAN CSS)
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-deep: #020617;
    --bg-card: #0F172A;
    --bg-elevated: #1E293B;
    --border-subtle: rgba(255,255,255,0.08);
    --border-medium: rgba(255,255,255,0.12);
    --border-strong: rgba(255,255,255,0.18);
    --primary: #3B82F6;
    --primary-soft: rgba(59,130,246,0.12);
    --secondary: #14B8A6;
    --secondary-soft: rgba(20,184,166,0.12);
    --purple: #8B5CF6;
    --purple-soft: rgba(139,92,246,0.12);
    --success: #22C55E;
    --success-soft: rgba(34,197,94,0.12);
    --warning: #F59E0B;
    --warning-soft: rgba(245,158,11,0.12);
    --danger: #EF4444;
    --danger-soft: rgba(239,68,68,0.12);
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --text-dim: #64748B;
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
    --shadow-soft: 0 1px 2px rgba(0,0,0,0.3), 0 4px 16px rgba(0,0,0,0.2);
    --shadow-glow: 0 0 40px rgba(59,130,246,0.15);
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 120% 80% at 10% -10%, rgba(59,130,246,0.08), transparent 50%),
        radial-gradient(ellipse 100% 60% at 100% 110%, rgba(139,92,246,0.06), transparent 50%),
        var(--bg-deep);
    background-attachment: fixed;
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { padding: 1.5rem 2rem 3rem 2rem; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060B1A 0%, #0A1124 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
    backdrop-filter: blur(20px);
}

.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(20,184,166,0.04));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    margin-bottom: 1.2rem;
}
.sidebar-brand-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3);
}
.sidebar-brand-text {
    font-size: 13px; font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.sidebar-brand-sub {
    font-size: 10px; font-weight: 500;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}

.sidebar-section {
    font-size: 10px; font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    padding: 0 4px;
    margin: 1.2rem 0 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sidebar-section::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, var(--border-subtle), transparent);
}

.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
    margin: 1rem 0;
}

.glass-panel {
    background: rgba(15,23,42,0.5);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 14px;
    backdrop-filter: blur(12px);
    margin-top: 8px;
}
.glass-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    line-height: 1.4;
}
.glass-row:last-child { margin-bottom: 0; }
.glass-row-icon {
    width: 24px; height: 24px;
    background: var(--primary-soft);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
}

.stat-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 600;
    background: var(--success-soft);
    color: var(--success);
    border: 1px solid rgba(34,197,94,0.2);
}
.stat-badge .dot {
    width: 6px; height: 6px;
    background: var(--success);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--success);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%,100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}

[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
.stMultiSelect [data-baseweb="tag"] {
    background: var(--primary-soft) !important;
    border: 1px solid rgba(59,130,246,0.25) !important;
    border-radius: 6px !important;
}
.stMultiSelect [data-baseweb="tag"] span { color: var(--text-primary) !important; font-size: 12px !important; }
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    border: 2px solid #fff !important;
    box-shadow: 0 0 0 3px var(--primary-soft) !important;
}

.stExpander {
    background: rgba(15,23,42,0.4) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    margin-bottom: 10px !important;
}
.stExpander summary {
    padding: 12px 14px !important;
    color: var(--text-primary) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

.risk-pill {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
}
.risk-high { background: var(--danger-soft); color: var(--danger); border: 1px solid rgba(239,68,68,0.25); }
.risk-low { background: var(--success-soft); color: var(--success); border: 1px solid rgba(34,197,94,0.25); }

.stButton > button {
    background: linear-gradient(135deg, var(--primary), #2563EB) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.25) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(59,130,246,0.35) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, var(--secondary), #0D9488) !important;
    color: #fff !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 12px rgba(20,184,166,0.25) !important;
}

.stNumberInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-medium) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

.exec-header {
    background: linear-gradient(135deg, rgba(15,23,42,0.8), rgba(2,6,23,0.9));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px 28px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow-soft);
    position: relative;
    overflow: hidden;
}
.exec-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,0.4), transparent);
}
.exec-header-left { flex: 1; }
.exec-header-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 10px;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 6px;
}
.exec-header-eyebrow .dot {
    width: 6px; height: 6px;
    background: var(--success);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--success);
    animation: pulse-dot 2s infinite;
}
.exec-header-title {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.exec-header-sub {
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 4px;
    font-weight: 400;
}
.exec-header-right {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: flex-end;
}
.exec-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 50px;
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}
.exec-pill strong { color: var(--text-primary); font-weight: 600; }

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 2rem;
}
@media (max-width: 1200px) { .kpi-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .kpi-grid { grid-template-columns: 1fr; } }

.kpi-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.7), rgba(2,6,23,0.8));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-soft);
}
.kpi-card:hover {
    transform: translateY(-3px);
    border-color: var(--border-strong);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4), var(--shadow-glow);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
    opacity: 0.7;
}
.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
}
.kpi-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.kpi-icon.blue { background: var(--primary-soft); color: var(--primary); }
.kpi-icon.cyan { background: var(--secondary-soft); color: var(--secondary); }
.kpi-icon.purple { background: var(--purple-soft); color: var(--purple); }
.kpi-icon.green { background: var(--success-soft); color: var(--success); }
.kpi-icon.amber { background: var(--warning-soft); color: var(--warning); }

.kpi-trend {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 50px;
    letter-spacing: 0.02em;
}
.trend-up { background: var(--success-soft); color: var(--success); }
.trend-down { background: var(--danger-soft); color: var(--danger); }
.trend-neutral { background: rgba(100,116,139,0.15); color: var(--text-dim); }
.trend-warn { background: var(--warning-soft); color: var(--warning); }

.kpi-label {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    color: var(--text-primary);
    margin-bottom: 4px;
    font-variant-numeric: tabular-nums;
}
.kpi-sub {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 500;
    margin-bottom: 10px;
}
.kpi-spark {
    height: 24px;
    display: flex;
    align-items: flex-end;
    gap: 2px;
}
.kpi-spark-bar {
    flex: 1;
    border-radius: 2px 2px 0 0;
    transition: height 0.6s ease;
    min-height: 2px;
}

.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 2.5rem 0 1.5rem 0;
}
.section-divider-num {
    font-size: 11px;
    font-weight: 800;
    color: var(--primary);
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.05em;
}
.section-divider-title {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.15em;
    white-space: nowrap;
}
.section-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-medium), transparent);
}

.chart-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.6), rgba(2,6,23,0.7));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 22px 22px 18px 22px;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow-soft);
    transition: all 0.3s ease;
    margin-bottom: 14px;
    height: 100%;
}
.chart-card:hover {
    border-color: var(--border-strong);
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.35);
}
.chart-card-head {
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border-subtle);
}
.chart-card-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 3px 0;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
}
.chart-card-title .ico {
    font-size: 14px;
    opacity: 0.9;
}
.chart-card-desc {
    font-size: 12px;
    color: var(--text-dim);
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
}

.insight-box {
    background: linear-gradient(135deg, var(--primary-soft), rgba(20,184,166,0.06));
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
    margin-top: 14px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 12px;
    color: var(--text-secondary);
    line-height: 1.6;
}
.insight-box-icon {
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 1px;
}
.insight-box strong { color: var(--primary); font-weight: 600; }

.exec-insights {
    background: linear-gradient(135deg, rgba(139,92,246,0.06), rgba(59,130,246,0.04));
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
}
.exec-insights-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-subtle);
}
.exec-insights-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--purple), var(--primary));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(139,92,246,0.3);
}
.exec-insights-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.01em;
}
.exec-insights-sub {
    font-size: 11px;
    color: var(--text-dim);
    margin: 2px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.insights-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}
@media (max-width: 768px) { .insights-grid { grid-template-columns: 1fr; } }

.insight-item {
    background: rgba(2,6,23,0.4);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    transition: all 0.2s ease;
}
.insight-item:hover {
    background: rgba(59,130,246,0.05);
    border-color: rgba(59,130,246,0.25);
    transform: translateY(-1px);
}
.insight-item-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}
.insight-item-icon {
    font-size: 14px;
}
.insight-item-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.insight-item-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.55;
}
.insight-item-text strong { color: var(--text-primary); font-weight: 600; }

.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.5) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 5px !important;
    gap: 3px !important;
    backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    padding: 9px 18px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"] p {
    color: var(--text-dim) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    margin: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover { background: rgba(59,130,246,0.08) !important; }
.stTabs [data-baseweb="tab"]:hover p { color: var(--text-primary) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary-soft), var(--secondary-soft)) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] p {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

.grid-2-1 {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 14px;
    margin-bottom: 14px;
}
.grid-1-2 {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 14px;
    margin-bottom: 14px;
}
.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 14px;
}
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin-bottom: 14px;
}
@media (max-width: 900px) {
    .grid-2-1, .grid-1-2, .grid-3, .grid-2 { grid-template-columns: 1fr; }
}

.mc-status-bar {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 16px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 14px;
}
.mc-idle { background: rgba(100,116,139,0.12); color: var(--text-dim); border: 1px solid rgba(100,116,139,0.25); }
.mc-ready { background: var(--primary-soft); color: var(--primary); border: 1px solid rgba(59,130,246,0.3); }
.mc-running { background: var(--warning-soft); color: var(--warning); border: 1px solid rgba(245,158,11,0.3); }
.mc-done { background: var(--success-soft); color: var(--success); border: 1px solid rgba(34,197,94,0.3); }
.mc-dot-anim {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: currentColor;
    animation: blink 1.2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.mc-metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0;
}
@media (max-width: 768px) { .mc-metrics { grid-template-columns: repeat(2, 1fr); } }
.mc-metric {
    background: rgba(2,6,23,0.5);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 16px;
    text-align: center;
}
.mc-metric-val {
    font-size: 22px;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 6px;
    font-variant-numeric: tabular-nums;
}
.mc-metric-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.model-info {
    padding: 14px 16px;
    background: rgba(59,130,246,0.05);
    border: 1px solid rgba(59,130,246,0.15);
    border-radius: var(--radius-sm);
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.7;
    margin-top: 14px;
}
.model-info strong { color: var(--primary); font-weight: 700; }

.mc-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    background: rgba(2,6,23,0.5);
    border: 1px dashed var(--border-medium);
    border-radius: var(--radius-md);
    text-align: center;
}
.mc-placeholder-ico { font-size: 48px; opacity: 0.4; margin-bottom: 12px; }
.mc-placeholder-text { color: var(--text-dim); font-size: 13px; font-weight: 500; }
.mc-placeholder-sub { color: var(--text-dim); font-size: 12px; margin-top: 6px; }

.final-rec {
    background: linear-gradient(135deg, rgba(34,197,94,0.05), rgba(20,184,166,0.04));
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: var(--radius-lg);
    padding: 24px 28px;
    margin-top: 14px;
}
.rec-item {
    display: flex;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border-subtle);
}
.rec-item:last-child { border-bottom: none; padding-bottom: 0; }
.rec-item:first-child { padding-top: 0; }
.rec-item-num {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px;
    font-weight: 800;
    color: white;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3);
}
.rec-item-content { flex: 1; }
.rec-item-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px 0;
}
.rec-item-desc {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
}

.dq-panel {
    background: linear-gradient(135deg, rgba(15,23,42,0.5), rgba(2,6,23,0.6));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px 24px;
    margin-bottom: 2rem;
    backdrop-filter: blur(12px);
}
.dq-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border-subtle);
}
.dq-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--secondary), var(--primary));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(20,184,166,0.3);
}
.dq-title {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.01em;
}
.dq-sub {
    font-size: 11px;
    color: var(--text-dim);
    margin: 2px 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.dq-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 10px;
}
.dq-item {
    background: rgba(2,6,23,0.5);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 12px 14px;
}
.dq-label {
    font-size: 10px;
    font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
.dq-value {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    font-variant-numeric: tabular-nums;
}
.semester-badge {
    display: inline-block;
    margin-top: 6px;
    padding: 2px 8px;
    border-radius: 50px;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.semester-badge.included { background: var(--primary-soft); color: var(--primary); }
.semester-badge.missing { background: var(--warning-soft); color: var(--warning); }

.heatmap-interp {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
}
.heatmap-interp.strong-pos { background: var(--success-soft); color: var(--success); }
.heatmap-interp.weak-neg { background: var(--danger-soft); color: var(--danger); }
.heatmap-interp.neutral { background: rgba(100,116,139,0.12); color: var(--text-dim); }

.dashboard-footer {
    margin-top: 3rem;
    padding: 24px 28px;
    background: linear-gradient(135deg, rgba(15,23,42,0.5), rgba(2,6,23,0.7));
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    backdrop-filter: blur(12px);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}
.footer-brand {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    margin-bottom: 4px;
}
.footer-brand span {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.footer-meta {
    font-size: 11px;
    color: var(--text-dim);
    line-height: 1.6;
}
.footer-tech {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
}
.tech-badge {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-subtle);
    border-radius: 50px;
    padding: 4px 11px;
    font-size: 11px;
    color: var(--text-dim);
    font-weight: 500;
}

p, h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
label { color: var(--text-secondary) !important; }
.stMarkdown { color: var(--text-primary); }

div[data-testid="stMetricValue"] { color: var(--primary) !important; font-weight: 800 !important; font-size: 26px !important; }
div[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.08em !important; }
div[data-testid="stMetricDelta"] { font-size: 12px !important; font-weight: 600 !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-medium); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: transparent !important;
    border-color: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 3. DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════
SOFT_COLORS = {
    'primary': '#3B82F6',
    'secondary': '#14B8A6',
    'success': '#22C55E',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'purple': '#8B5CF6',
    'muted': '#64748B',
}
PLOTLY_TEMPLATE = 'plotly_dark'

# ══════════════════════════════════════════════════════════════════
# 4. HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════
def dark_layout(fig, height=360):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#CBD5E1', size=12),
        height=height,
        margin=dict(t=10, b=10, l=0, r=0),
        legend=dict(
            bgcolor='rgba(15,23,42,0.6)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(color='#94A3B8', size=11)
        ),
    )
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.04)',
        zerolinecolor='rgba(255,255,255,0.06)',
        tickfont=dict(color='#64748B', size=11),
        title_font=dict(color='#94A3B8', size=12, family='Inter')
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.04)',
        zerolinecolor='rgba(255,255,255,0.06)',
        tickfont=dict(color='#64748B', size=11),
        title_font=dict(color='#94A3B8', size=12, family='Inter')
    )
    return fig

def chart_card(title, desc, icon="📊"):
    st.markdown(f"""
    <div class="chart-card-head">
        <p class="chart-card-title"><span class="ico">{icon}</span>{title}</p>
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

def section_divider(num, title):
    st.markdown(f"""
    <div class="section-divider">
        <span class="section-divider-num">{num}</span>
        <span class="section-divider-title">{title}</span>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(icon, label, value, sub, trend_text, trend_class, spark_data=None, icon_class="blue"):
    spark_html = ""
    if spark_data:
        bars = "".join([f'<div class="kpi-spark-bar" style="height:{h}%; background: {c};"></div>' for h, c in spark_data])
        spark_html = f'<div class="kpi-spark">{bars}</div>'
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-icon {icon_class}">{icon}</div>
            <span class="kpi-trend {trend_class}">{trend_text}</span>
        </div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
        {spark_html}
    </div>
    """, unsafe_allow_html=True)

def render_data_quality(df):
    if len(df) == 0:
        return
    missing = df.isnull().sum().sum()
    total = df.shape[0] * df.shape[1]
    missing_pct = (missing / total * 100) if total > 0 else 0
    date_min = str(df['Date_Parsed'].min())[:10] if 'Date_Parsed' in df.columns else 'N/A'
    date_max = str(df['Date_Parsed'].max())[:10] if 'Date_Parsed' in df.columns else 'N/A'
    
    if 'Semester' in df.columns:
        try:
            sem_list = sorted([int(s) for s in df['Semester'].dropna().unique().tolist()])
            sem_display = ', '.join(str(s) for s in sem_list)
            sem_count = len(sem_list)
            has_4 = 4 in sem_list
            badge = '<span class="semester-badge included">✓ SMT 4</span>' if has_4 else '<span class="semester-badge missing">⚠ No SMT 4</span>'
            sem_val = f"{sem_count} ({sem_display})"
        except Exception:
            sem_val = str(df['Semester'].nunique())
            badge = ''
    else:
        sem_val = '0'
        badge = ''
    
    prodi_count = df['Prodi'].nunique() if 'Prodi' in df.columns else 0
    
    # FIXED: Variables hardcoded to 13 (core dataset columns only)
    core_variables = 13
    
    st.markdown(f"""
    <div class="dq-panel">
        <div class="dq-head">
            <div class="dq-icon">📊</div>
            <div>
                <p class="dq-title">Data Quality Overview</p>
                <p class="dq-sub">Dataset integrity metrics</p>
            </div>
            <div style="margin-left: auto;"><span class="stat-badge"><span class="dot"></span>Verified</span></div>
        </div>
        <div class="dq-grid">
            <div class="dq-item"><div class="dq-label">Total Records</div><div class="dq-value">{len(df):,}</div></div>
            <div class="dq-item"><div class="dq-label">Missing Values</div><div class="dq-value">{missing} ({missing_pct:.2f}%)</div></div>
            <div class="dq-item"><div class="dq-label">Program Studi</div><div class="dq-value">{prodi_count}</div></div>
            <div class="dq-item"><div class="dq-label">Semester</div><div class="dq-value" style="font-size:13px;">{sem_val}</div>{badge}</div>
            <div class="dq-item"><div class="dq-label">Variables</div><div class="dq-value">{core_variables}</div></div>
            <div class="dq-item"><div class="dq-label">Date Range</div><div class="dq-value" style="font-size:12px;">{date_min} → {date_max}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 5. LOAD DATA
# ══════════════════════════════════════════════════════════════════
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
    except Exception:
        df['Date_Parsed'] = df['Timestamp']
    return df

df_raw = load_data()

# ══════════════════════════════════════════════════════════════════
# 6. SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🎓</div>
        <div>
            <div class="sidebar-brand-text">AI Learning Impact</div>
            <div class="sidebar-brand-sub">Analytics Workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">Filters</div>', unsafe_allow_html=True)
    
    with st.expander("🎯 Program Studi & Semester", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist()
        filter_prodi = st.multiselect("Program Studi", options=prodi_list, default=prodi_list, label_visibility="collapsed")
        semester_list = sorted(df_raw['Semester'].unique().tolist())
        filter_semester = st.multiselect("Semester", options=semester_list, default=semester_list, label_visibility="collapsed")
    
    st.markdown('<div class="sidebar-section">Simulation</div>', unsafe_allow_html=True)
    
    with st.expander("🔮 Personal Risk Profiler", expanded=True):
        sim_tugas = st.slider("Porsi Bantuan AI (dari 10 tugas):", 0, 10, 6)
        if sim_tugas > 5:
            st.markdown('<div class="risk-pill risk-high">⚠️ High Dependency Risk</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-pill risk-low">✓ Safe Usage Range</div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">Dataset Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-panel">
        <div class="glass-row"><div class="glass-row-icon">📊</div><span><strong style="color:#F8FAFC;">{len(df_raw):,}</strong> Total Records</span></div>
        <div class="glass-row"><div class="glass-row-icon">🎓</div><span><strong style="color:#F8FAFC;">{df_raw['Prodi'].nunique()}</strong> Programs</span></div>
        <div class="glass-row"><div class="glass-row-icon">📚</div><span><strong style="color:#F8FAFC;">{df_raw['Semester'].nunique()}</strong> Semesters</span></div>
        <div class="glass-row"><div class="glass-row-icon">📋</div><span><strong style="color:#F8FAFC;">13</strong> Variables</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-section">Research Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-panel">
        <div class="glass-row"><div class="glass-row-icon">👨‍💻</div><span>Ahmad Rizza Pahlevi</span></div>
        <div class="glass-row"><div class="glass-row-icon">🏛️</div><span>UIN K.H. Abdurrahman Wahid</span></div>
        <div class="glass-row"><div class="glass-row-icon">📅</div><span>Updated: Juni 2026</span></div>
        <div class="glass-row"><div class="glass-row-icon">🎯</div><span>Skripsi Research 2026</span></div>
    </div>
    """, unsafe_allow_html=True)

# Apply filter
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ══════════════════════════════════════════════════════════════════
# 7. EXECUTIVE HEADER
# ══════════════════════════════════════════════════════════════════
n_resp = len(df)
setiap_hari_pct = len(df[df['Frekuensi_Penggunaan'] == 'Setiap hari']) / max(len(df), 1) * 100
avg_jam = df['Jam_per_Hari'].mean() if len(df) > 0 else 0
avg_tugas = df['Porsi_Tugas_AI'].mean() if len(df) > 0 else 0
avg_skor = df['Skor_Efektivitas'].mean() if len(df) > 0 else 0
ketergantungan_pct = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5 Tugas)']) / max(len(df), 1) * 100

st.markdown(f"""
<div class="exec-header">
    <div class="exec-header-left">
        <div class="exec-header-eyebrow"><span class="dot"></span>Live · Research Analytics Dashboard</div>
        <h1 class="exec-header-title">AI Learning Impact Analytics</h1>
        <p class="exec-header-sub">Executive analytics for understanding AI integration in academic ecosystems</p>
    </div>
    <div class="exec-header-right">
        <div class="exec-pill"><span>📊</span><strong>{n_resp:,}</strong> Responden</div>
        <div class="exec-pill"><span>🎓</span><strong>{df['Prodi'].nunique()}</strong> Prodi</div>
        <div class="exec-pill"><span>📅</span>Juni 2026</div>
        <div class="exec-pill"><span>👨‍💻</span>Ahmad R. P.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 8. KPI CARDS
# ══════════════════════════════════════════════════════════════════
section_divider("01", "Key Performance Indicators")

def make_spark(series, color='#3B82F6', bins=8):
    if len(series) == 0:
        return None
    try:
        counts, _ = np.histogram(series, bins=bins)
        max_c = counts.max() if counts.max() > 0 else 1
        return [(int(c / max_c * 100), color) for c in counts]
    except Exception:
        return None

st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
with st.container():
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("👥", "Total Responden", f"{n_resp:,}", "Filtered dataset", "ACTIVE", "trend-neutral", icon_class="blue")
    with c2:
        spark2 = make_spark(df['Jam_per_Hari'], '#14B8A6')
        t_class = "trend-warn" if avg_jam >= 3 else "trend-up"
        t_txt = "HIGH" if avg_jam >= 3 else "NORMAL"
        kpi_card("⏱️", "Avg Durasi", f"{avg_jam:.1f}h", "Per hari", t_txt, t_class, spark2, "cyan")
    with c3:
        spark3 = make_spark(df['Porsi_Tugas_AI'], '#8B5CF6')
        t_class3 = "trend-down" if avg_tugas > 5 else "trend-up"
        t_txt3 = "HIGH" if avg_tugas > 5 else "SAFE"
        kpi_card("📝", "Porsi Tugas AI", f"{avg_tugas:.1f}/10", "Ketergantungan", t_txt3, t_class3, spark3, "purple")
    with c4:
        spark4 = make_spark(df['Skor_Efektivitas'], '#22C55E')
        t_class4 = "trend-up" if avg_skor >= 3.5 else "trend-warn"
        t_txt4 = "GOOD" if avg_skor >= 3.5 else "MODERATE"
        kpi_card("⭐", "Efektivitas", f"{avg_skor:.2f}", "Skor 1-5", t_txt4, t_class4, spark4, "green")
    with c5:
        t_class5 = "trend-warn" if ketergantungan_pct > 50 else "trend-up"
        t_txt5 = "RISK" if ketergantungan_pct > 50 else "OK"
        kpi_card("⚠️", "High Dep.", f"{ketergantungan_pct:.0f}%", "Ketergantungan", t_txt5, t_class5, icon_class="amber")
st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 9. DATA QUALITY PANEL
# ══════════════════════════════════════════════════════════════════
render_data_quality(df)

# ══════════════════════════════════════════════════════════════════
# 10. EXECUTIVE INSIGHTS
# ══════════════════════════════════════════════════════════════════
section_divider("02", "Executive Insights")

try:
    corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
    corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
except Exception:
    corr_val = 0.0

max_jam = df['Jam_per_Hari'].max() if len(df) > 0 else 0

st.markdown(f"""
<div class="exec-insights">
    <div class="exec-insights-head">
        <div class="exec-insights-icon">🧠</div>
        <div>
            <p class="exec-insights-title">AI-Generated Executive Summary</p>
            <p class="exec-insights-sub">Automated Research Intelligence</p>
        </div>
    </div>
    <div class="insights-grid">
        <div class="insight-item">
            <div class="insight-item-head">
                <span class="insight-item-icon">🤖</span>
                <span class="insight-item-label">Adoption Rate</span>
            </div>
            <p class="insight-item-text"><strong>{setiap_hari_pct:.0f}%</strong> of students use AI daily, indicating deep integration into academic workflows and strong technology adoption.</p>
        </div>
        <div class="insight-item">
            <div class="insight-item-head">
                <span class="insight-item-icon">⚠️</span>
                <span class="insight-item-label">Risk Assessment</span>
            </div>
            <p class="insight-item-text"><strong>{ketergantungan_pct:.0f}%</strong> show high dependency (>5 tasks), posing cognitive independence risks that require pedagogical intervention.</p>
        </div>
        <div class="insight-item">
            <div class="insight-item-head">
                <span class="insight-item-icon">📊</span>
                <span class="insight-item-label">Correlation Insight</span>
            </div>
            <p class="insight-item-text">Pearson correlation of <strong>r = {corr_val:.2f}</strong> between AI usage and effectiveness shows quantity alone doesn't guarantee learning quality.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 11. TABS
# ══════════════════════════════════════════════════════════════════
section_divider("03", "Analytical Modules")

tab1, tab2, tab3 = st.tabs([
    "📊 Descriptive Analytics",
    "🔗 Correlation Analysis",
    "🎲 Monte Carlo Simulation"
])

# ══════════════════════════════════════════════════════════════════
# TAB 1: DESCRIPTIVE
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="grid-2-1">', unsafe_allow_html=True)
    c_a, c_b = st.columns([2, 1])
    
    with c_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Tren Frekuensi Penggunaan AI", "Distribusi intensitas penggunaan AI per kategori frekuensi", "📈")
        trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
        trend_data.columns = ['Frekuensi', 'Jumlah']
        fig_hero = px.bar(trend_data, x='Frekuensi', y='Jumlah', text='Jumlah', color='Frekuensi',
            color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple'], SOFT_COLORS['muted']],
            template=PLOTLY_TEMPLATE)
        fig_hero.update_traces(textposition='outside', marker_line_width=0)
        fig_hero.update_layout(showlegend=False)
        st.plotly_chart(dark_layout(fig_hero, 360), use_container_width=True)
        if len(trend_data) > 0:
            top = trend_data.iloc[0]
            insight_box(f"Kategori <strong>{top['Frekuensi']}</strong> mendominasi dengan <strong>{top['Jumlah']} mahasiswa</strong>, menunjukkan adopsi AI yang tinggi dalam rutinitas akademik.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Intensitas Ketergantungan", "Proporsi ketergantungan AI", "🍩")
        fig_pie = px.pie(df, names='Is_Ketergantungan_Tinggi', hole=0.6,
            color='Is_Ketergantungan_Tinggi',
            color_discrete_map={'Tinggi (>5 Tugas)': SOFT_COLORS['danger'], 'Rendah (<=5 Tugas)': SOFT_COLORS['secondary']},
            template=PLOTLY_TEMPLATE)
        fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
        fig_pie.update_layout(showlegend=False)
        st.plotly_chart(dark_layout(fig_pie, 360), use_container_width=True)
        insight_box(f"<strong>{ketergantungan_pct:.0f}%</strong> mahasiswa memiliki ketergantungan tinggi terhadap AI.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="grid-3">', unsafe_allow_html=True)
    cc1, cc2, cc3 = st.columns(3)
    
    with cc1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Distribusi Porsi Tugas", "Jumlah tugas dibantu AI", "📊")
        fig_porsi = px.histogram(df, x='Porsi_Tugas_AI', text_auto=True,
            color_discrete_sequence=[SOFT_COLORS['primary']], template=PLOTLY_TEMPLATE)
        fig_porsi.update_traces(marker_line_width=0)
        fig_porsi.update_layout(xaxis_title="Jumlah Tugas", yaxis_title="Mahasiswa", showlegend=False)
        st.plotly_chart(dark_layout(fig_porsi, 300), use_container_width=True)
        insight_box(f"Rata-rata <strong>{avg_tugas:.1f}/10</strong> tugas dibantu AI.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cc2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Durasi Pemakaian Harian", "Histogram dengan boxplot marginal", "⏳")
        fig_hist = px.histogram(df, x='Jam_per_Hari', nbins=8, marginal="box",
            color_discrete_sequence=[SOFT_COLORS['secondary']], template=PLOTLY_TEMPLATE)
        fig_hist.update_traces(marker_line_width=0)
        st.plotly_chart(dark_layout(fig_hist, 300), use_container_width=True)
        insight_box(f"Rata-rata <strong>{avg_jam:.1f} jam/hari</strong>, max <strong>{max_jam}</strong> jam.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cc3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Skor Efektivitas Belajar", "Persepsi efektivitas (1-5)", "⭐")
        fig_skor = px.histogram(df, x='Skor_Efektivitas', text_auto=True,
            color_discrete_sequence=[SOFT_COLORS['success']], template=PLOTLY_TEMPLATE)
        fig_skor.update_traces(marker_line_width=0)
        fig_skor.update_layout(xaxis_title="Skor (1-5)", showlegend=False)
        st.plotly_chart(dark_layout(fig_skor, 300), use_container_width=True)
        insight_box(f"Rata-rata <strong>{avg_skor:.2f}/5</strong> - persepsi {'positif' if avg_skor >= 3.5 else 'moderat'}.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card("Persepsi Peningkatan Nilai Akademik", "Distribusi persepsi mahasiswa terhadap dampak AI pada nilai", "📈")
    fig_nilai = px.histogram(df, x='Peningkatan_Nilai', text_auto=True, color='Peningkatan_Nilai',
        color_discrete_sequence=[SOFT_COLORS['success'], SOFT_COLORS['warning'], SOFT_COLORS['muted']],
        template=PLOTLY_TEMPLATE)
    fig_nilai.update_traces(marker_line_width=0)
    fig_nilai.update_layout(xaxis_title="Persepsi Nilai", showlegend=False)
    st.plotly_chart(dark_layout(fig_nilai, 320), use_container_width=True)
    insight_box("Persepsi peningkatan nilai bervariasi - pengguna terstruktur cenderung melaporkan peningkatan yang lebih konsisten.")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2: CORRELATION
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="grid-1-2">', unsafe_allow_html=True)
    ca1, ca2 = st.columns([1, 2])
    
    with ca1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Probabilitas Kesulitan", "Kesulitan belajar tanpa AI", "⚠️")
        prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
        prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
        fig_prob = px.bar(prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
            barmode='stack', text_auto='.1f',
            color_discrete_map={'Ya': SOFT_COLORS['danger'], 'Tidak': SOFT_COLORS['secondary']},
            template=PLOTLY_TEMPLATE)
        fig_prob.update_traces(marker_line_width=0)
        st.plotly_chart(dark_layout(fig_prob, 400), use_container_width=True)
        insight_box("Ketergantungan tinggi berkorelasi dengan <strong>probabilitas kesulitan belajar mandiri</strong> yang signifikan.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with ca2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Heatmap Korelasi Pearson", "Matriks korelasi dengan skala diverging RdBu", "🔗")
        corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        fig_heat = px.imshow(corr_matrix, text_auto=".3f", aspect="auto",
            color_continuous_scale="RdBu_r", zmin=-1, zmax=1, origin="lower", template=PLOTLY_TEMPLATE)
        fig_heat.update_coloraxes(colorbar=dict(
            tickfont=dict(color='#64748B', size=10),
            title=dict(text='r', font=dict(color='#64748B'))
        ))
        st.plotly_chart(dark_layout(fig_heat, 400), use_container_width=True)
        
        try:
            cv = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
        except Exception:
            cv = 0.0
        
        if cv > 0.5:
            interp_cls, interp_txt = "strong-pos", "Strong Positive"
        elif cv < -0.5:
            interp_cls, interp_txt = "weak-neg", "Strong Negative"
        else:
            interp_cls, interp_txt = "neutral", "Weak"
        
        st.markdown(f'<div class="heatmap-interp {interp_cls}"><span>Correlation: {cv:.2f}</span><span>•</span><span>{interp_txt}</span></div>', unsafe_allow_html=True)
        insight_box(f"Korelasi Porsi Tugas ↔ Efektivitas <strong>r = {cv:.3f}</strong> - kuantitas tidak otomatis meningkatkan kualitas.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="grid-2">', unsafe_allow_html=True)
    cb1, cb2 = st.columns(2)
    
    with cb1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Efektivitas vs Porsi Tugas AI", "Scatter plot dengan trendline regresi linear", "📉")
        z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
        p = np.poly1d(z)
        df_sorted = df.sort_values('Porsi_Tugas_AI')
        fig_scat = px.scatter(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', opacity=0.75, template=PLOTLY_TEMPLATE)
        fig_scat.update_traces(marker=dict(size=10, color=SOFT_COLORS['secondary'], line=dict(width=0)))
        fig_scat.add_trace(go.Scatter(x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
            mode='lines', name='Trendline', line=dict(color=SOFT_COLORS['danger'], width=2.5, dash='dot')))
        r_squared = np.corrcoef(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'])[0, 1] ** 2
        eq = f"y = {z[0]:.3f}x + {z[1]:.3f}"
        fig_scat.update_layout(showlegend=False,
            annotations=[dict(x=0.02, y=0.98, xref='paper', yref='paper',
                text=f"{eq}<br>R² = {r_squared:.3f}", showarrow=False,
                font=dict(size=11, color='#E2E8F0'),
                bgcolor='rgba(15,23,42,0.9)', bordercolor='rgba(59,130,246,0.3)',
                borderwidth=1, borderpad=8, align='left')])
        st.plotly_chart(dark_layout(fig_scat, 360), use_container_width=True)
        direction = "negatif" if z[0] < 0 else "positif"
        insight_box(f"Trendline menunjukkan slope <strong>{direction}</strong> (slope ≈ {z[0]:.3f}) - penggunaan AI lebih banyak tidak otomatis meningkatkan efektivitas.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with cb2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        chart_card("Boxplot Efektivitas per Porsi", "Sebaran & outlier skor efektivitas", "📦")
        fig_box = px.box(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
            color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple']],
            template=PLOTLY_TEMPLATE)
        fig_box.update_layout(xaxis_title="Porsi Tugas (0-10)", showlegend=False)
        st.plotly_chart(dark_layout(fig_box, 360), use_container_width=True)
        insight_box("Variasi (IQR) yang lebar pada level tinggi menunjukkan hasil yang <strong>tidak konsisten</strong> antar individu.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card("Rata-rata Copy-Paste per Porsi Tugas", "Korelasi ketergantungan AI dengan perilaku copy-paste", "📑")
    cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
    fig_cp = px.bar(cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste',
        text_auto='.2f', color='Tingkat_Copy_Paste',
        color_continuous_scale=[[0, '#14B8A6'], [0.5, '#8B5CF6'], [1, '#EF4444']],
        template=PLOTLY_TEMPLATE)
    fig_cp.update_traces(textposition='outside', marker_line_width=0)
    fig_cp.update_layout(xaxis_title="Porsi Tugas AI (0-10)", yaxis_title="Skor Copy-Paste (1-5)")
    st.plotly_chart(dark_layout(fig_cp, 320), use_container_width=True)
    insight_box("Tren positif antara porsi tugas AI dan copy-paste mengonfirmasi risiko <strong>surface learning</strong> pada pengguna berat AI.")
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3: MONTE CARLO
# ══════════════════════════════════════════════════════════════════
with tab3:
    section_divider("04", "Stochastic Simulation Engine")
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    chart_card("Monte Carlo Simulation", "Proyeksi stokastik stabilitas skor efektivitas pada kelas berskala besar (n=100)", "🎲")
    
    mc_current = st.session_state.get('run_mc', False)
    status_cls = "mc-done" if mc_current else "mc-ready"
    status_txt = "COMPLETED" if mc_current else "READY"
    st.markdown(f'<div class="mc-status-bar {status_cls}"><span class="mc-dot-anim"></span>{status_txt}</div>', unsafe_allow_html=True)
    
    mc1, mc2 = st.columns([1, 3])
    
    with mc1:
        iterations = st.number_input("Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000)
        run_btn = st.button("🚀 Jalankan Simulasi", use_container_width=True)
        if run_btn:
            st.session_state['run_mc'] = True
            st.toast("Menjalankan model stokastik...", icon="⚙️")
        
        st.markdown("""
        <div class="model-info">
            <strong>Model Configuration</strong><br>
            • Distribution: Normal<br>
            • Sample/iter: 100 students<br>
            • Confidence: 95% (Percentile)<br>
            • Clip range: [1, 5]<br>
            • Engine: NumPy Stochastic
        </div>
        """, unsafe_allow_html=True)
    
    with mc2:
        if st.session_state.get('run_mc', False):
            if len(df) == 0:
                st.warning("Tidak ada data untuk disimulasikan. Silakan sesuaikan filter.")
            else:
                with st.spinner(f"Memproses {iterations:,} komputasi stokastik..."):
                    time.sleep(0.8)
                    p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                    cats, weights = p_dist.index.values, p_dist.values
                    stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())
                    hasil = []
                    for _ in range(iterations):
                        sim_tugas_mc = np.random.choice(cats, size=100, p=weights)
                        skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas_mc]
                        hasil.append(np.mean(skor))
                    mean_mc = np.mean(hasil)
                    ci_low = np.percentile(hasil, 2.5)
                    ci_high = np.percentile(hasil, 97.5)
                    ci_width = ci_high - ci_low
                    running_mean = np.cumsum(hasil) / np.arange(1, iterations + 1)
                
                st.markdown('<div class="mc-metrics">', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.markdown(f'<div class="mc-metric"><div class="mc-metric-val">{iterations:,}</div><div class="mc-metric-label">Total Iterasi</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="mc-metric"><div class="mc-metric-val">{mean_mc:.3f}</div><div class="mc-metric-label">Mean Ekspektasi</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="mc-metric"><div class="mc-metric-val">{ci_low:.3f}–{ci_high:.3f}</div><div class="mc-metric-label">95% CI</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="mc-metric"><div class="mc-metric-val">{ci_width:.3f}</div><div class="mc-metric-label">CI Width</div></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
                chart_card("Kurva Konvergensi Running Mean", "Stabilitas estimasi mean seiring iterasi bertambah", "📉")
                n_pts = min(iterations, 5000)
                step = max(1, iterations // n_pts)
                xs = np.arange(1, iterations + 1)[::step]
                ys = running_mean[::step]
                fig_run = go.Figure()
                fig_run.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='Running Mean',
                    line=dict(color=SOFT_COLORS['primary'], width=2.5), fill='none'))
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=SOFT_COLORS['danger'], line_width=1.5,
                    annotation_text=f"Converge: {mean_mc:.3f}", annotation_font_color='#EF4444', annotation_font_size=11)
                fig_run.add_hrect(y0=ci_low, y1=ci_high, fillcolor='rgba(59,130,246,0.07)',
                    line=dict(color='rgba(59,130,246,0.2)', width=1, dash='dot'),
                    annotation_text="95% CI", annotation_font_color='#3B82F6', annotation_font_size=10, annotation_position="right")
                fig_run.update_layout(xaxis_title="Iterasi", yaxis_title="Running Mean", template=PLOTLY_TEMPLATE, showlegend=False)
                st.plotly_chart(dark_layout(fig_run, 300), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div style="margin-top:16px;">', unsafe_allow_html=True)
                chart_card("Distribusi Hasil Simulasi", "Histogram skor efektivitas dari seluruh iterasi", "📊")
                fig_dist = px.histogram(x=hasil, nbins=50, color_discrete_sequence=[SOFT_COLORS['purple']], template=PLOTLY_TEMPLATE)
                fig_dist.update_traces(marker_line_width=0)
                fig_dist.update_layout(xaxis_title="Skor Efektivitas", yaxis_title="Frekuensi")
                st.plotly_chart(dark_layout(fig_dist, 300), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                stability = "stabil" if ci_width < 0.1 else "cukup stabil"
                insight_box(f"Model konvergen pada <strong>{mean_mc:.3f}</strong> dengan 95% CI [{ci_low:.3f}, {ci_high:.3f}]. Lebar CI {ci_width:.3f} menunjukkan model yang <strong>{stability}</strong> untuk proyeksi skala besar.")
        else:
            st.markdown("""
            <div class="mc-placeholder">
                <div class="mc-placeholder-ico">🎲</div>
                <div class="mc-placeholder-text">Stochastic engine ready</div>
                <div class="mc-placeholder-sub">Set iterations and click <strong style="color:#3B82F6;">Jalankan Simulasi</strong> to begin</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 12. RECOMMENDATIONS + DOCX DOWNLOAD
# ══════════════════════════════════════════════════════════════════
section_divider("05", "Strategic Recommendations")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
chart_card("Research Highlights & Policy Recommendations", "Temuan kunci dan rekomendasi untuk kebijakan akademik", "💡")

if len(df) > 0:
    st.markdown(f"""
    <div class="final-rec">
        <div class="rec-item">
            <div class="rec-item-num">1</div>
            <div class="rec-item-content">
                <p class="rec-item-title">🎯 High Adoption Rate</p>
                <p class="rec-item-desc"><strong>{setiap_hari_pct:.0f}%</strong> mahasiswa menggunakan AI setiap hari. Institusi perlu mengembangkan <strong>AI Literacy Framework</strong> untuk memaksimalkan manfaat dan meminimalkan risiko.</p>
            </div>
        </div>
        <div class="rec-item">
            <div class="rec-item-num">2</div>
            <div class="rec-item-content">
                <p class="rec-item-title">⚠️ Dependency Risk Mitigation</p>
                <p class="rec-item-desc"><strong>{ketergantungan_pct:.0f}%</strong> responden menunjukkan ketergantungan tinggi. Rekomendasi: batas maksimal 50% porsi tugas menggunakan AI untuk menjaga kemandirian kognitif.</p>
            </div>
        </div>
        <div class="rec-item">
            <div class="rec-item-num">3</div>
            <div class="rec-item-content">
                <p class="rec-item-title">📊 Quality Over Quantity</p>
                <p class="rec-item-desc">Korelasi lemah (<strong>r = {corr_val:.2f}</strong>) membuktikan bahwa kuantitas penggunaan AI tidak menjamin efektivitas. Fokus pada <strong>metode penggunaan</strong>, bukan frekuensi.</p>
            </div>
        </div>
        <div class="rec-item">
            <div class="rec-item-num">4</div>
            <div class="rec-item-content">
                <p class="rec-item-title">🎓 Pedagogical Intervention</p>
                <p class="rec-item-desc">Durasi rata-rata <strong>{avg_jam:.1f} jam/hari</strong> (max {max_jam} jam) memerlukan panduan waktu penggunaan yang sehat dan terstruktur untuk keseimbangan akademik.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ── DOCX DOWNLOAD BUTTON ──────────────────────────────────────
    docx_path = "Laporan_Analisis_AI_Efektivitas_Belajar.docx"
    
    col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
    with col_dl2:
        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                docx_bytes = f.read()
            
            st.download_button(
                label="📄 Download Laporan Lengkap (DOCX)",
                data=docx_bytes,
                file_name="Laporan_Analisis_AI_Efektivitas_Belajar.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        else:
            st.warning(
                f"⚠️ File `{docx_path}` tidak ditemukan. "
                "Pastikan file berada di folder yang sama dengan `app.py`."
            )
else:
    st.info("Pilih data pada filter sidebar untuk melihat rekomendasi.")

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# 13. FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dashboard-footer">
    <div>
        <div class="footer-brand">AI Learning Impact <span>Analytics</span></div>
        <div class="footer-meta">Research Analytics Dashboard · Skripsi 2026 · Enterprise Edition v3.0</div>
    </div>
    <div>
        <div class="footer-meta">👨‍💻 Ahmad Rizza Pahlevi · 🏛️ UIN K.H. Abdurrahman Wahid · 📅 Juni 2026</div>
    </div>
    <div class="footer-tech">
        <span class="tech-badge">🐍 Python</span>
        <span class="tech-badge">⚡ Streamlit</span>
        <span class="tech-badge">📊 Plotly</span>
        <span class="tech-badge">🔢 NumPy</span>
        <span class="tech-badge">🐼 Pandas</span>
    </div>
</div>
""", unsafe_allow_html=True)
