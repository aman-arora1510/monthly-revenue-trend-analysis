"""
src/visualizations.py
---------------------
Plotly Express & Graph Objects chart factory producing responsive,
enterprise-styled visual analytics for all 8 application screens.
"""

from src.config import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SUCCESS, COLOR_DANGER,
    COLOR_WARNING, COLOR_ACCENT
)

try:
    import plotly.graph_objects as go
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def create_revenue_area_chart(monthly_totals: list):
    """
    Renders 24-month revenue area trajectory chart.
    monthly_totals: list of dicts with 'billing_month' and 'billed_amount'
    """
    if not HAS_PLOTLY or not monthly_totals:
        return None

    months = [m["billing_month"] for m in monthly_totals]
    amounts = [m["billed_amount"] for m in monthly_totals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months,
        y=amounts,
        mode='lines+markers',
        name='Billed Revenue',
        line=dict(color=COLOR_PRIMARY, width=3),
        marker=dict(size=6, color=COLOR_SECONDARY),
        fill='tozeroy',
        fillcolor='rgba(31, 73, 125, 0.12)'
    ))
    fig.update_layout(
        title="24-Month Consolidated Revenue Trajectory (INR Lakhs)",
        xaxis_title="Billing Month",
        yaxis_title="Revenue (Lakhs)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    return fig

def create_multiline_trends_chart(practice_trends: dict):
    """
    Renders multi-line trajectory contrasting the 4 service lines.
    practice_trends: dict {practice_name: [(month, amount), ...]}
    """
    if not HAS_PLOTLY or not practice_trends:
        return None

    colors = [COLOR_PRIMARY, COLOR_SUCCESS, COLOR_SECONDARY, "#7C3AED"]
    fig = go.Figure()

    for idx, (practice, pts) in enumerate(practice_trends.items()):
        months = [p[0] for p in pts]
        revs = [p[1] for p in pts]
        fig.add_trace(go.Scatter(
            x=months,
            y=revs,
            mode='lines+markers',
            name=practice,
            line=dict(color=colors[idx % len(colors)], width=2.5),
            marker=dict(size=5)
        ))

    fig.update_layout(
        title="Service Line Monthly Growth Momentum",
        xaxis_title="Billing Month",
        yaxis_title="Revenue (Lakhs)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_regional_donut_chart(regional_shares: dict):
    """
    Renders regional revenue share donut chart.
    """
    if not HAS_PLOTLY or not regional_shares:
        return None

    labels = list(regional_shares.keys())
    values = list(regional_shares.values())
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.48,
        marker=dict(colors=colors)
    )])
    fig.update_layout(
        title="Geographic Territory Distribution",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

def create_waterfall_variance_chart(variance_steps: list):
    """
    Renders budget vs actual revenue variance waterfall chart.
    variance_steps: list of dicts with 'label', 'value', 'type' ('relative' or 'total')
    """
    if not HAS_PLOTLY or not variance_steps:
        return None

    x = [v["label"] for v in variance_steps]
    y = [v["value"] for v in variance_steps]
    measure = ["relative" if v.get("type") != "total" else "total" for v in variance_steps]

    fig = go.Figure(go.Waterfall(
        name="Budget Variance",
        orientation="v",
        measure=measure,
        x=x,
        y=y,
        connector=dict(line=dict(color="rgb(63, 63, 63)")),
        decreasing=dict(marker=dict(color=COLOR_DANGER)),
        increasing=dict(marker=dict(color=COLOR_SUCCESS)),
        totals=dict(marker=dict(color=COLOR_PRIMARY))
    ))
    fig.update_layout(
        title="Corporate Budget-to-Actual Variance Waterfall (INR Lakhs)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        height=400
    )
    return fig

def create_pareto_concentration_chart(client_revenues: list):
    """
    Renders dual-axis Pareto chart (Top 10 Client Bars + Cumulative % Line).
    """
    if not HAS_PLOTLY or not client_revenues:
        return None

    clients = [c["client_name"] for c in client_revenues]
    revenues = [c["billed_amount"] for c in client_revenues]
    cum_pcts = [c["cum_pct"] for c in client_revenues]

    fig = go.Figure()
    # Bar trace (Primary Y-axis)
    fig.add_trace(go.Bar(
        x=clients,
        y=revenues,
        name="Billed Revenue",
        marker=dict(color=COLOR_PRIMARY)
    ))
    # Cumulative % Line (Secondary Y-axis)
    fig.add_trace(go.Scatter(
        x=clients,
        y=cum_pcts,
        name="Cumulative Share %",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color=COLOR_DANGER, width=2.5),
        marker=dict(size=6)
    ))

    # Add 80% Pareto threshold line and 15% single-account threshold
    fig.update_layout(
        title="Client Portfolio Concentration & Pareto 80/20 Curve",
        xaxis=dict(tickangle=-25),
        yaxis=dict(title="Revenue (Lakhs)"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 105],
            showgrid=False
        ),
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=70),
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_forecast_ribbon_chart(
    historical_months: list,
    historical_rev: list,
    forecast_months: list,
    forecast_points: list,
    upper_band: list,
    lower_band: list
):
    """
    Renders historical actuals + 3-month forward projection with shaded confidence ribbon.
    """
    if not HAS_PLOTLY:
        return None

    fig = go.Figure()

    # Historical line
    fig.add_trace(go.Scatter(
        x=historical_months,
        y=historical_rev,
        mode="lines+markers",
        name="Historical Actuals",
        line=dict(color=COLOR_PRIMARY, width=2.5)
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=forecast_months,
        y=forecast_points,
        mode="lines+markers",
        name="3-Month Forward Forecast",
        line=dict(color=COLOR_SUCCESS, width=2.5, dash="dash")
    ))

    # Confidence ribbon (Upper bound)
    fig.add_trace(go.Scatter(
        x=forecast_months,
        y=upper_band,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Confidence ribbon (Lower bound + fill)
    fig.add_trace(go.Scatter(
        x=forecast_months,
        y=lower_band,
        mode="lines",
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.18)',
        name="95% Confidence Interval"
    ))

    fig.update_layout(
        title="3-Month Time-Series Forecast & Prediction Interval",
        xaxis_title="Billing Month",
        yaxis_title="Revenue (Lakhs)",
        template="plotly_white",
        margin=dict(l=40, r=40, t=50, b=40),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def create_aging_bar_chart(bucket_counts: dict):
    """
    Renders A/R Aging bucket distribution horizontal bar chart.
    """
    if not HAS_PLOTLY or not bucket_counts:
        return None

    buckets = list(bucket_counts.keys())
    counts = list(bucket_counts.values())
    colors = [COLOR_SUCCESS, COLOR_ACCENT, COLOR_WARNING, COLOR_DANGER]

    fig = go.Figure(go.Bar(
        x=counts,
        y=buckets,
        orientation='h',
        marker=dict(color=colors[:len(buckets)])
    ))
    fig.update_layout(
        title="Accounts Receivable Aging Bucket Distribution",
        xaxis_title="Invoice Count",
        yaxis_title="Aging Bucket",
        template="plotly_white",
        margin=dict(l=100, r=40, t=40, b=40),
        height=320
    )
    return fig
