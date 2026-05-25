import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="众安保险 · 2024组织感知调研报告", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans SC', sans-serif; }
    .report-title { font-family: 'Noto Serif SC', serif; font-size: 2.4rem; font-weight: 700; color: #0E5C4F; letter-spacing: -0.5px; margin-bottom: 0.2rem; }
    .report-subtitle { color: #7A7E7C; font-size: 1rem; font-weight: 400; margin-bottom: 1.5rem; }
    .brand-badge { display: inline-block; background: linear-gradient(135deg, #0E5C4F 0%, #1a7a6a 100%); color: white; padding: 4px 16px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; margin-bottom: 0.5rem; }
    .kpi-container { background: white; border-radius: 16px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .kpi-container:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.1); }
    .kpi-value { font-family: 'Noto Serif SC', serif; font-size: 2.2rem; font-weight: 700; color: #0A0A0A; line-height: 1; }
    .kpi-label { font-size: 0.8rem; color: #7A7E7C; font-weight: 500; margin-top: 8px; letter-spacing: 1px; text-transform: uppercase; }
    .kpi-delta-positive { color: #0E5C4F; font-weight: 600; font-size: 0.85rem; }
    .kpi-delta-negative { color: #DC2626; font-weight: 600; font-size: 0.85rem; }
    .quad-card { border-radius: 12px; padding: 20px; border-left: 4px solid; background: white; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
    .section-divider { height: 1px; background: linear-gradient(90deg, transparent, #ddd, transparent); margin: 2rem 0; border: none; }
    .insight-box { background: linear-gradient(135deg, #F4F8F7 0%, #ffffff 100%); border-radius: 12px; padding: 20px 24px; border: 1px solid #e8edeb; margin-bottom: 16px; }
    .insight-title { color: #0E5C4F; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; }
    .insight-text { color: #3A3D3C; font-size: 0.88rem; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('survey_data.csv', encoding='utf-8-sig')
    df['年份'] = df['年份'].astype(str)
    return df

df = load_data()
ALL_DEPTS = sorted(df['部门'].unique().tolist())
YEAR_COLORS = {'2024': '#0E5C4F', '2023': '#5A8A82', '2022': '#A0B5B0'}

GLOBAL_AE = df['敬业度'].mean()
GLOBAL_AS = df['满意度'].mean()
YEARLY_AVG = df.groupby('年份').agg({'敬业度':'mean','满意度':'mean','领导力':'mean'}).to_dict('index')

with st.sidebar:
    st.markdown("### 🔧 筛选条件")
    selected_years = st.multiselect("📅 年份", options=['2022', '2023', '2024'], default=['2022', '2023', '2024'])
    selected_depts = st.multiselect("🏢 部门", options=ALL_DEPTS, default=ALL_DEPTS, max_selections=None)
    selected_quads = st.multiselect("📍 象限", options=['① 高敬业·高满意', '② 高敬业·低满意', '③ 低敬业·高满意', '④ 低敬业·低满意'], default=['① 高敬业·高满意', '② 高敬业·低满意', '③ 低敬业·高满意', '④ 低敬业·低满意'])
    st.markdown("---")
    st.caption("💡 悬停图表查看详情")

filtered_df = df[(df['年份'].isin(selected_years)) & (df['部门'].isin(selected_depts))].copy()

def get_quadrant(row):
    ref_e = YEARLY_AVG[row['年份']]['敬业度'] if len(selected_years) == 1 else GLOBAL_AE
    ref_s = YEARLY_AVG[row['年份']]['满意度'] if len(selected_years) == 1 else GLOBAL_AS
    high_e = row['敬业度'] >= ref_e
    high_s = row['满意度'] >= ref_s
    if high_e and high_s: return '① 高敬业·高满意'
    elif high_e and not high_s: return '② 高敬业·低满意'
    elif not high_e and high_s: return '③ 低敬业·高满意'
    else: return '④ 低敬业·低满意'

filtered_df['象限'] = filtered_df.apply(get_quadrant, axis=1)
filtered_df = filtered_df[filtered_df['象限'].isin(selected_quads)]

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="brand-badge">众安保险 ZHONGAN</div>', unsafe_allow_html=True)
    st.markdown('<div class="report-title">2024年度组织感知调研报告</div>', unsafe_allow_html=True)
    st.markdown('<div class="report-subtitle">2022 - 2024 三年回顾 · 数据驱动组织优化</div>', unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div style="text-align:right; padding-top:20px;">
        <div style="color:#7A7E7C; font-size:0.8rem;">数据更新时间</div>
        <div style="color:#0A0A0A; font-size:1rem; font-weight:600;">2026/05/22</div>
        <div style="color:#0E5C4F; font-size:0.75rem; margin-top:4px;">组织发展部</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("### 💡 关键发现")
latest_year = max(selected_years) if selected_years else '2024'
latest_df = df[df['年份'] == latest_year]
prev_year = str(int(latest_year) - 1) if str(int(latest_year) - 1) in selected_years else None

insight_cols = st.columns(2)
with insight_cols[0]:
    if prev_year and len(selected_years) >= 2:
        prev_df = df[df['年份'] == prev_year]
        merged = latest_df.merge(prev_df, on='部门', suffixes=('_今', '_去'))
        merged['敬业度变化'] = merged['敬业度_今'] - merged['敬业度_去']
        worst = merged.nsmallest(3, '敬业度变化')
        worst_text = "、".join([f"{r['部门']}(-{abs(r['敬业度变化']):.1f}pp)" for _, r in worst.iterrows()])
        st.markdown(f'<div class="insight-box"><div class="insight-title">⚠️ 敬业度下滑最严重的部门（{latest_year} vs {prev_year}）</div><div class="insight-text">{worst_text}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-box"><div class="insight-title">📊 {latest_year}年平均敬业度</div><div class="insight-text">{latest_year}年整体敬业度为 <b>{latest_df["敬业度"].mean():.1f}%</b>，最高为 {latest_df.nlargest(1, "敬业度").iloc[0]["部门"]} ({latest_df["敬业度"].max():.1f}%)，最低为 {latest_df.nsmallest(1, "敬业度").iloc[0]["部门"]} ({latest_df["敬业度"].min():.1f}%)</div></div>', unsafe_allow_html=True)

with insight_cols[1]:
    if len(latest_df) > 0:
        latest_df['敬满差'] = latest_df['敬业度'] - latest_df['满意度']
        gap = latest_df.nlargest(3, '敬满差')
        gap_text = "、".join([f"{r['部门']}({r['敬满差']:.1f}pp)" for _, r in gap.iterrows()])
        st.markdown(f'<div class="insight-box"><div class="insight-title">🔍 敬业度远高于满意度的部门（{latest_year}）</div><div class="insight-text">{gap_text}<br><span style="color:#7A7E7C;font-size:0.8rem;">这些部门员工虽然敬业但满意度低，存在"高敬业不可持续"风险，建议重点改善满意度驱动因素。</span></div></div>', unsafe_allow_html=True)

if len(filtered_df) > 0:
    total_hc = int(filtered_df['人数'].sum())
    avg_e = filtered_df['敬业度'].mean()
    avg_s = filtered_df['满意度'].mean()
    avg_l = filtered_df['领导力'].mean()
    unique_depts = filtered_df['部门'].nunique()

    if len(selected_years) >= 2:
        years_sorted = sorted(selected_years)
        latest_y = years_sorted[-1]
        prev_y = years_sorted[-2]
        latest_f = filtered_df[filtered_df['年份'] == latest_y]
        prev_f = filtered_df[filtered_df['年份'] == prev_y]
        if len(latest_f) > 0 and len(prev_f) > 0:
            e_delta = latest_f['敬业度'].mean() - prev_f['敬业度'].mean()
            s_delta = latest_f['满意度'].mean() - prev_f['满意度'].mean()
        else:
            e_delta, s_delta = 0, 0
    else:
        e_delta, s_delta = 0, 0

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f'<div class="kpi-container"><div class="kpi-value">{unique_depts}</div><div class="kpi-label">部门数</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="kpi-container"><div class="kpi-value">{total_hc:,}</div><div class="kpi-label">总人数</div></div>', unsafe_allow_html=True)
    with kpi3:
        dc = "kpi-delta-positive" if e_delta >= 0 else "kpi-delta-negative"
        da = "↑" if e_delta >= 0 else "↓"
        st.markdown(f'<div class="kpi-container"><div class="kpi-value">{avg_e:.1f}<span style="font-size:1rem;color:#7A7E7C;">%</span></div><div class="kpi-label">平均敬业度</div><div class="{dc}">{da} {abs(e_delta):.1f}pp</div></div>', unsafe_allow_html=True)
    with kpi4:
        dc = "kpi-delta-positive" if s_delta >= 0 else "kpi-delta-negative"
        da = "↑" if s_delta >= 0 else "↓"
        st.markdown(f'<div class="kpi-container"><div class="kpi-value">{avg_s:.1f}<span style="font-size:1rem;color:#7A7E7C;">%</span></div><div class="kpi-label">平均满意度</div><div class="{dc}">{da} {abs(s_delta):.1f}pp</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown(f'<div class="kpi-container"><div class="kpi-value">{avg_l:.1f}<span style="font-size:1rem;color:#7A7E7C;">%</span></div><div class="kpi-label">平均领导力</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("### 📊 四象限定义")
q1, q2, q3, q4 = st.columns(4)
quad_styles = {
    '① 高敬业·高满意': ('#0E5C4F', '#E8F4F1', '可结合绩效情况进行判断'),
    '② 高敬业·低满意': ('#D97706', '#FEF6E7', '低满意带来的高敬业不可持续，需着力改善'),
    '③ 低敬业·高满意': ('#CA8A04', '#FEF9E7', '其敬业表现需要进一步激发'),
    '④ 低敬业·低满意': ('#DC2626', '#FEE2E2', '风险较大，需要特别关注')
}
for col, quad_name in zip([q1, q2, q3, q4], ['① 高敬业·高满意', '② 高敬业·低满意', '③ 低敬业·高满意', '④ 低敬业·低满意']):
    color, bg, desc = quad_styles[quad_name]
    with col:
        st.markdown(f'<div class="quad-card" style="border-left-color: {color}; background: {bg};"><h4 style="color: {color}; margin:0 0 6px 0; font-size:1rem;">{quad_name}</h4><p style="margin:0; font-size:0.85rem; color:#5a5a5a; line-height:1.5;">{desc}</p></div>', unsafe_allow_html=True)

st.markdown("### 🎯 敬业度 vs 满意度 散点分析")

if len(filtered_df) > 0:
    ref_e = filtered_df['敬业度'].mean()
    ref_s = filtered_df['满意度'].mean()

    fig = go.Figure()
    fig.add_vrect(x0=ref_e, x1=105, y0=ref_s, y1=105, fillcolor="rgba(14,92,79,0.07)", line_width=0, layer="below")
    fig.add_vrect(x0=60, x1=ref_e, y0=ref_s, y1=105, fillcolor="rgba(202,138,4,0.07)", line_width=0, layer="below")
    fig.add_vrect(x0=60, x1=ref_e, y0=50, y1=ref_s, fillcolor="rgba(220,38,38,0.08)", line_width=0, layer="below")
    fig.add_vrect(x0=ref_e, x1=105, y0=50, y1=ref_s, fillcolor="rgba(217,119,6,0.07)", line_width=0, layer="below")

    for year in sorted(selected_years):
        year_df = filtered_df[filtered_df['年份'] == year]
        if len(year_df) == 0: continue
        fig.add_trace(go.Scatter(
            x=year_df['敬业度'], y=year_df['满意度'], mode='markers+text', name=f'{year}年',
            text=year_df['部门'], textposition="top center",
            textfont=dict(size=9, color=YEAR_COLORS[year]),
            marker=dict(size=year_df['人数'].apply(lambda x: max(8, min(20, x/15))), color=YEAR_COLORS[year], line=dict(width=1.5, color='white'), opacity=0.85),
            hovertemplate="<b>%{text}</b><br>年份: " + year + "<br>敬业度: %{x:.1f}%<br>满意度: %{y:.1f}%<br>人数: %{customdata}<extra></extra>",
            customdata=year_df['人数']
        ))

    fig.add_vline(x=ref_e, line_dash="dash", line_color="#DC2626", line_width=2, annotation_text=f"均值 {ref_e:.1f}%", annotation_position="top")
    fig.add_hline(y=ref_s, line_dash="dash", line_color="#DC2626", line_width=2, annotation_text=f"均值 {ref_s:.1f}%", annotation_position="right")

    fig.update_layout(
        xaxis_title="敬业度 (%)", yaxis_title="满意度 (%)",
        xaxis=dict(range=[60, 105], gridcolor='rgba(0,0,0,0.05)', showgrid=True),
        yaxis=dict(range=[50, 105], gridcolor='rgba(0,0,0,0.05)', showgrid=True),
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(family="Noto Sans SC, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=40, t=80, b=60), height=650, hovermode='closest'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("请调整筛选条件以显示数据")

st.markdown("### 📈 三年趋势对比")

if len(filtered_df) > 0:
    trend_df = filtered_df.groupby('年份').agg({'敬业度':'mean','满意度':'mean','领导力':'mean'}).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=trend_df['年份'], y=trend_df['敬业度'], mode='lines+markers', name='敬业度', line=dict(color='#0E5C4F', width=3), marker=dict(size=10)))
    fig2.add_trace(go.Scatter(x=trend_df['年份'], y=trend_df['满意度'], mode='lines+markers', name='满意度', line=dict(color='#5A8A82', width=3), marker=dict(size=10)))
    fig2.add_trace(go.Scatter(x=trend_df['年份'], y=trend_df['领导力'], mode='lines+markers', name='领导力', line=dict(color='#A0B5B0', width=3), marker=dict(size=10)))
    fig2.update_layout(xaxis_title="年份", yaxis_title="得分 (%)", yaxis=dict(range=[70, 100]), plot_bgcolor='white', paper_bgcolor='white', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5), margin=dict(l=60, r=40, t=60, b=60), height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 🏆 部门排名（按最新年份敬业度）")

if len(filtered_df) > 0:
    latest_y = max(selected_years)
    rank_df = filtered_df[filtered_df['年份'] == latest_y].sort_values('敬业度', ascending=False)
    fig3 = go.Figure()
    colors = ['#0E5C4F' if v >= rank_df['敬业度'].mean() else '#DC2626' for v in rank_df['敬业度']]
    fig3.add_trace(go.Bar(y=rank_df['部门'], x=rank_df['敬业度'], orientation='h', marker_color=colors, text=[f'{v:.1f}%' for v in rank_df['敬业度']], textposition='outside', hovertemplate="%{y}<br>敬业度: %{x:.1f}%<br>人数: %{customdata}<extra></extra>", customdata=rank_df['人数']))
    fig3.add_vline(x=rank_df['敬业度'].mean(), line_dash="dash", line_color="#999", line_width=1.5, annotation_text=f"均值 {rank_df['敬业度'].mean():.1f}%")
    fig3.update_layout(xaxis_title="敬业度 (%)", yaxis=dict(categoryorder='total ascending'), plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=120, r=60, t=40, b=60), height=max(400, len(rank_df)*28))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 📋 部门年度对比")

if len(filtered_df) > 0:
    pivot = filtered_df.pivot_table(index='部门', columns='年份', values=['敬业度','满意度','领导力','人数'], aggfunc='first').round(1)
    pivot.columns = [f"{col[0]}_{col[1]}" for col in pivot.columns]
    pivot = pivot.reset_index()

    def style_table(df):
        num_cols = [c for c in df.columns if '敬业度_' in c or '满意度_' in c or '领导力_' in c]
        return df.style.background_gradient(cmap='RdYlGn', subset=num_cols, axis=1).format({c: '{:.1f}%' for c in df.columns if '敬业度_' in c or '满意度_' in c or '领导力_' in c}).format({c: '{:.0f}' for c in df.columns if '人数_' in c}).set_properties(**{'text-align': 'center', 'font-size': '13px'})

    st.dataframe(style_table(pivot), use_container_width=True, height=500)

    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="⬇️ 下载筛选数据 (CSV)", data=csv, file_name='组织感知调研数据.csv', mime='text/csv')

st.markdown("---")
st.caption("📅 数据来源：2022-2024年度组织感知调研 | 众安保险 · 组织发展部")
