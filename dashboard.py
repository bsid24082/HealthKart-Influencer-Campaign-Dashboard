import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set up the page layout with a dark theme and wider view
st.set_page_config(
    page_title="Influencer Campaign Dashboard 🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Influencer Campaign Analytics 📊")
st.markdown("A deep-dive into campaign performance, influencer insights, and key metrics for HealthKart.")
st.write("---")

# --- 1. Data Ingestion ---
try:
    influencers_df = pd.read_csv('influencers.csv')
    posts_df = pd.read_csv('posts.csv')
    tracking_df = pd.read_csv('tracking_data.csv')
    payouts_df = pd.read_csv('payouts.csv')
except FileNotFoundError:
    st.error("CSV files not found. Please run the data generation script first.")
    st.stop()

# --- Data Merging and Pre-processing ---
campaign_data = pd.merge(tracking_df, influencers_df, left_on='influencer_id', right_on='ID', how='left')
campaign_data = pd.merge(campaign_data, payouts_df, on='influencer_id', how='left')

# Additional data cleaning and filling NaNs
campaign_data['category'].fillna('Organic', inplace=True)
campaign_data['platform'].fillna('Organic', inplace=True)
campaign_data['total_payout'].fillna(0, inplace=True)
campaign_data['revenue'].fillna(0, inplace=True)
campaign_data['date'] = pd.to_datetime(campaign_data['date'])


# --- 2. Interactive Filters ---
st.sidebar.header("Filter Campaigns ⚙️")
with st.sidebar:
    # Date range filter
    min_date = campaign_data['date'].min()
    max_date = campaign_data['date'].max()
    date_range = st.date_input("Select Date Range:", value=(min_date, max_date))

    # Multi-select for categories
    unique_categories = ['All'] + list(influencers_df['category'].unique())
    selected_categories = st.multiselect(
        "Select Influencer Categories:",
        options=unique_categories,
        default='All'
    )

    # Multi-select for platforms
    unique_platforms = ['All'] + list(influencers_df['platform'].unique())
    selected_platforms = st.multiselect(
        "Select Platforms:",
        options=unique_platforms,
        default='All'
    )
    
# Apply all filters
filtered_df = campaign_data.copy()
if 'All' not in selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]
if 'All' not in selected_platforms:
    filtered_df = filtered_df[filtered_df['platform'].isin(selected_platforms)]
if date_range:
    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df['date'] >= pd.Timestamp(start_date)) & (filtered_df['date'] <= pd.Timestamp(end_date))]

# --- 3. Key Performance Indicators (KPIs) ---
st.header("Campaign Overview 📈")
total_revenue = filtered_df['revenue'].sum()
total_payout = filtered_df['total_payout'].sum()
organic_revenue_baseline = tracking_df[tracking_df['source'] == 'organic']['revenue'].sum()
influencer_revenue = filtered_df[filtered_df['source'] == 'influencer']['revenue'].sum()

# Calculations
roi = (total_revenue - total_payout) / total_payout if total_payout > 0 else 0
incremental_roas = (influencer_revenue - organic_revenue_baseline) / total_payout if total_payout > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💸 Total Revenue", f"₹{total_revenue:,.2f}")
with col2:
    st.metric("💰 Total Payouts", f"₹{total_payout:,.2f}")
with col3:
    st.metric("📈 ROI", f"{roi:.2%}")
with col4:
    st.metric("🚀 Incremental ROAS", f"{incremental_roas:.2f}")
st.write("---")

# --- 4. Detailed Performance and Insights ---
st.header("Detailed Performance 🔍")

# Revenue trend over time
st.subheader("Revenue & Payouts Over Time")
time_series_data = filtered_df.groupby(filtered_df['date'].dt.date).agg(
    total_revenue=('revenue', 'sum'),
    total_payout=('total_payout', 'sum')
).reset_index()
fig_time = px.line(
    time_series_data,
    x='date',
    y=['total_revenue', 'total_payout'],
    labels={'value': 'Amount (₹)', 'variable': 'Metric'},
    title='Daily Revenue vs. Payouts',
    template='plotly_dark'
)
st.plotly_chart(fig_time, use_container_width=True)

# Performance by platform and category
col_chart1, col_chart2 = st.columns(2)
with col_chart1:
    st.subheader("Revenue by Platform")
    platform_revenue = filtered_df.groupby('platform')['revenue'].sum().reset_index()
    fig_platform = px.bar(
        platform_revenue,
        x='platform',
        y='revenue',
        title="Total Revenue by Platform",
        color='platform',
        template='plotly_dark'
    )
    st.plotly_chart(fig_platform, use_container_width=True)

with col_chart2:
    st.subheader("Performance by Category")
    category_revenue = filtered_df.groupby('category').agg(
        total_revenue=('revenue', 'sum'),
        total_payout=('total_payout', 'sum')
    ).reset_index()
    category_revenue['ROI'] = (category_revenue['total_revenue'] - category_revenue['total_payout']) / category_revenue['total_payout']
    fig_category = px.bar(
        category_revenue,
        x='category',
        y='ROI',
        title="ROI by Influencer Category",
        color='category',
        template='plotly_dark'
    )
    st.plotly_chart(fig_category, use_container_width=True)

# Top and Poor Performing Influencers
st.subheader("Influencer Leaderboard 🏆")
influencer_performance = filtered_df.groupby('ID').agg(
    total_revenue=('revenue', 'sum'),
    total_payout=('total_payout', 'sum')
).reset_index()
influencer_performance['ROI'] = (influencer_performance['total_revenue'] - influencer_performance['total_payout']) / influencer_performance['total_payout']
influencer_performance.replace([np.inf, -np.inf], np.nan, inplace=True)
influencer_performance.fillna(0, inplace=True) # Fill NaNs (for influencers with no payout) with 0

# Merge with influencer details for name and platform
influencer_performance = pd.merge(influencer_performance, influencers_df[['ID', 'name', 'category', 'platform']], on='ID')
influencer_performance = influencer_performance.sort_values(by='ROI', ascending=False)

# Display top and poor performers in two columns
col_top, col_poor = st.columns(2)
with col_top:
    st.markdown("#### Top 10 Influencers by ROI")
    st.dataframe(
        influencer_performance.head(10)[['name', 'platform', 'category', 'ROI', 'total_revenue', 'total_payout']].rename(
            columns={'name': 'Influencer', 'platform': 'Platform', 'category': 'Category'}
        ).style.format({'ROI': '{:.2%}'}),
        use_container_width=True
    )

with col_poor:
    st.markdown("#### Poor Performing Influencers")
    st.dataframe(
        influencer_performance.tail(10)[['name', 'platform', 'category', 'ROI', 'total_revenue', 'total_payout']].rename(
            columns={'name': 'Influencer', 'platform': 'Platform', 'category': 'Category'}
        ).style.format({'ROI': '{:.2%}'}),
        use_container_width=True
    )
st.write("---")

# --- 5. Optional: Post Performance ---
st.header("Post-Level Performance 📝")
post_performance = pd.merge(posts_df, influencers_df[['ID', 'name', 'platform']], left_on='influencer_id', right_on='ID', how='left')
st.dataframe(
    post_performance[['name', 'platform_x', 'date', 'reach', 'likes', 'comments']].rename(
        columns={'name': 'Influencer', 'platform_x': 'Platform', 'date': 'Date'}
    ),
    use_container_width=True,
    hide_index=True
)

# --- 6. Generate Detailed Insight Report ---
st.header("Generate Detailed Insight Report 📄")

def generate_detailed_report(filtered_df, influencers_df):
    report = "### Detailed Campaign Insights Report\n\n"
    report += "This report provides a comprehensive, plain-language summary of the campaign's performance, key influencers, and trends.\n\n"
    
    # 1. Overall Summary
    total_revenue_val = filtered_df['revenue'].sum()
    total_payout_val = filtered_df['total_payout'].sum()
    roi_val = (total_revenue_val - total_payout_val) / total_payout_val if total_payout_val > 0 else 0
    incremental_roas_val = ((filtered_df[filtered_df['source'] == 'influencer']['revenue'].sum() - filtered_df[filtered_df['source'] == 'organic']['revenue'].sum()) / total_payout_val) if total_payout_val > 0 else 0
    
    report += "#### 🚀 Overall Campaign Summary\n"
    report += f"- **Total Revenue:** The campaign generated a total of ₹{total_revenue_val:,.2f}.\n"
    report += f"- **Total Payouts:** The total cost for all influencer activities was ₹{total_payout_val:,.2f}.\n"
    report += f"- **ROI:** The campaign achieved an outstanding ROI of **{roi_val:.2%}**, meaning for every rupee spent, we gained a return of {roi_val:.2%} in revenue.\n"
    report += f"- **Incremental ROAS:** The incremental ROAS was **{incremental_roas_val:.2f}**, indicating that for every rupee spent, we generated ₹{incremental_roas_val:.2f} in *new* revenue that we wouldn't have earned otherwise.\n\n"
    
    # 2. Performance by Category & Platform
    category_performance = filtered_df.groupby('category').agg(
        total_revenue=('revenue', 'sum'),
        total_payout=('total_payout', 'sum')
    ).reset_index()
    category_performance['ROI'] = (category_performance['total_revenue'] - category_performance['total_payout']) / category_performance['total_payout']
    category_performance.replace([np.inf, -np.inf], np.nan, inplace=True)
    category_performance.fillna(0, inplace=True)
    top_categories = category_performance.sort_values(by='ROI', ascending=False).head(3)
    
    platform_performance = filtered_df.groupby('platform').agg(
        total_revenue=('revenue', 'sum'),
        total_payout=('total_payout', 'sum')
    ).reset_index()
    platform_performance['ROI'] = (platform_performance['total_revenue'] - platform_performance['total_payout']) / platform_performance['total_payout']
    platform_performance.replace([np.inf, -np.inf], np.nan, inplace=True)
    platform_performance.fillna(0, inplace=True)
    top_platforms = platform_performance.sort_values(by='ROI', ascending=False).head(3)
    
    report += "#### 📊 Performance Breakdown\n"
    report += "##### Top Performing Categories:\n"
    for _, row in top_categories.iterrows():
        if row['category'] != 'Organic':
            report += f"- The **{row['category']}** category achieved an impressive ROI of **{row['ROI']:.2%}** with a total revenue of ₹{row['total_revenue']:,.2f}.\n"
    report += "\n##### Top Performing Platforms:\n"
    for _, row in top_platforms.iterrows():
        if row['platform'] != 'Organic':
            report += f"- **{row['platform']}** was the most effective platform, with an ROI of **{row['ROI']:.2%}** and generating ₹{row['total_revenue']:,.2f} in revenue.\n"
    report += "\n"
    
    # 3. Influencer Performance
    influencer_performance = filtered_df.groupby('ID').agg(
        total_revenue=('revenue', 'sum'),
        total_payout=('total_payout', 'sum')
    ).reset_index()
    influencer_performance['ROI'] = (influencer_performance['total_revenue'] - influencer_performance['total_payout']) / influencer_performance['total_payout']
    influencer_performance.replace([np.inf, -np.inf], np.nan, inplace=True)
    influencer_performance.fillna(0, inplace=True)
    influencer_performance = pd.merge(influencer_performance, influencers_df[['ID', 'name', 'category', 'platform']], on='ID')
    
    top_influencers = influencer_performance.sort_values(by='ROI', ascending=False).head(3)
    poor_influencers = influencer_performance.sort_values(by='ROI', ascending=True).head(3)
    
    report += "#### 🏆 Key Influencer Analysis\n"
    report += "##### Top Performers:\n"
    for _, row in top_influencers.iterrows():
        report += f"- **{row['name']}** ({row['category']}): A standout performer, generating an ROI of **{row['ROI']:.2%}** from a total revenue of ₹{row['total_revenue']:,.2f}.\n"
    report += "\n##### Underperformers:\n"
    for _, row in poor_influencers.iterrows():
        report += f"- **{row['name']}** ({row['category']}): Had a low ROI of {row['ROI']:.2%} and generated a total revenue of only ₹{row['total_revenue']:,.2f}. This influencer may need to be reevaluated for future campaigns.\n"
    report += "\n"
    
    return report

if st.button("Generate Detailed Report"):
    report_text = generate_detailed_report(filtered_df, influencers_df)
    st.markdown(report_text)
    
    # Add a download button for the generated report
    st.download_button(
        label="Download Report as Text",
        data=report_text,
        file_name='influencer_campaign_report.txt',
        mime='text/plain',
    )






