"""
src/ui.py
---------
Reusable Tailwind CSS UI components for the Monthly Revenue Trend Analysis Streamlit application.
Renders responsive headers, executive KPI cards, and alert banners via st.components.v1.html
using the official Tailwind CSS CDN.
"""

import streamlit as st
import streamlit.components.v1 as components

TAILWIND_CDN = '<script src="https://cdn.tailwindcss.com"></script>'

def render_header(title: str, subtitle: str, badge: str = "Novatech Analytics") -> None:
    """
    Renders an enterprise header with title, subtitle, and branded badge.
    """
    html_code = f"""
    {TAILWIND_CDN}
    <div class="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 p-6 rounded-2xl shadow-md border border-slate-800 text-white font-sans mb-4">
        <div class="flex items-center justify-between mb-2">
            <span class="bg-blue-600/30 text-blue-300 border border-blue-500/40 text-xs font-semibold px-3 py-1 rounded-full uppercase tracking-wider">
                {badge}
            </span>
            <span class="text-xs text-slate-400">
                FY2024–FY2025 | Production Architecture
            </span>
        </div>
        <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight text-white mb-1">
            {title}
        </h1>
        <p class="text-sm md:text-base text-slate-300 font-normal">
            {subtitle}
        </p>
    </div>
    """
    components.html(html_code, height=135, scrolling=False)


def render_kpi_card(title: str, value: str, delta_text: str = "", is_positive: bool = True, icon: str = "📈") -> str:
    """
    Helper generating HTML snippet for a single Tailwind KPI card.
    """
    delta_color = "text-emerald-600 bg-emerald-50 border-emerald-200" if is_positive else "text-rose-600 bg-rose-50 border-rose-200"
    arrow = "▲" if is_positive else "▼"
    
    delta_badge = ""
    if delta_text:
        delta_badge = f"""
        <span class="inline-flex items-center gap-1 text-xs font-bold px-2 py-0.5 rounded-full border {delta_color}">
            <span>{arrow}</span>
            <span>{delta_text}</span>
        </span>
        """
        
    return f"""
    <div class="bg-white rounded-xl p-5 shadow-sm border border-slate-200 hover:shadow-md transition-shadow duration-200 font-sans">
        <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold tracking-wider text-slate-500 uppercase">{title}</span>
            <span class="text-lg">{icon}</span>
        </div>
        <div class="text-2xl md:text-3xl font-black text-slate-900 mb-2 tracking-tight">
            {value}
        </div>
        <div class="flex items-center">
            {delta_badge}
        </div>
    </div>
    """


def render_kpi_grid(cards_data: list) -> None:
    """
    Renders a responsive 4-column KPI card grid.
    cards_data: list of dicts with keys: title, value, delta_text, is_positive, icon
    """
    cards_html = "".join([
        render_kpi_card(
            title=c.get("title", ""),
            value=c.get("value", ""),
            delta_text=c.get("delta_text", ""),
            is_positive=c.get("is_positive", True),
            icon=c.get("icon", "📊")
        ) for c in cards_data
    ])
    
    html_code = f"""
    {TAILWIND_CDN}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-sans mb-4">
        {cards_html}
    </div>
    """
    components.html(html_code, height=130, scrolling=False)


def render_alert_banner(message: str, level: str = "warning") -> None:
    """
    Renders a Tailwind notification or high-concentration alert banner.
    level: 'warning', 'danger', 'info', 'success'
    """
    colors = {
        "warning": "bg-amber-50 border-amber-300 text-amber-900",
        "danger": "bg-rose-50 border-rose-300 text-rose-900",
        "info": "bg-blue-50 border-blue-300 text-blue-900",
        "success": "bg-emerald-50 border-emerald-300 text-emerald-900"
    }
    icons = {
        "warning": "⚠️",
        "danger": "🚨",
        "info": "ℹ️",
        "success": "✅"
    }
    
    theme_cls = colors.get(level, colors["warning"])
    icon_str = icons.get(level, "⚠️")
    
    html_code = f"""
    {TAILWIND_CDN}
    <div class="{theme_cls} border px-4 py-3 rounded-xl shadow-sm flex items-center gap-3 font-sans mb-3 text-sm font-medium">
        <span class="text-xl">{icon_str}</span>
        <div>{message}</div>
    </div>
    """
    components.html(html_code, height=65, scrolling=False)
