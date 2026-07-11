import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. Advanced Page & Theme Configuration
st.set_page_config(page_title="Next-Gen E-Commerce Analytics Suite", layout="wide")
st.title("🌌 Next-Gen E-Commerce Analytics Suite")
st.markdown("A premium, high-fidelity data experience optimized for modern enterprise intelligence.")

# Custom CSS injected for minimalist design & premium font scaling
st.markdown("""
    <style>
    .stMetric { background-color: #111217; padding: 15px; border-radius: 12px; border: 1px solid #23262f; }
    div[data-testid="stNotification"] { border-radius: 12px; background-color: #171923; border: 1px solid #2d3748; }
    </style>
""", unsafe_allow_html=True)

# Set Global Matplotlib style to Dark/Premium Aesthetic
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#0e1117'
plt.rcParams['axes.edgecolor'] = '#23262f'
plt.rcParams['grid.color'] = '#1b1d26'

# 2. Dataset Simulation
@st.cache_data
def load_enterprise_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-06-30", freq="D")
    categories = ['Electronics', 'Clothing', 'Home Decor', 'Books', 'Beauty']
    products = ['Smartphone', 'Laptop', 'T-Shirt', 'Jeans', 'Sofa', 'Wall Clock', 'Fiction Book', 'Notebook', 'Lipstick', 'Sunscreen']
    states = ['Kerala', 'Tamil Nadu', 'Karnataka', 'Maharashtra', 'Delhi', 'Telangana']
    status_options = ['Delivered', 'In Transit', 'Returned', 'Cancelled']
    
    data = {
        'OrderID': [f"ORD{1000+i}" for i in range(2000)],
        'CustomerID': [f"CUST{np.random.randint(100, 500)}" for _ in range(2000)],
        'Date': np.random.choice(dates, size=2000),
        'Category': np.random.choice(categories, size=2000),
        'Product': np.random.choice(products, size=2000),
        'Sales_Amount': np.random.uniform(500, 45000, size=2000).round(2),
        'Quantity': np.random.randint(1, 6, size=2000),
        'Payment_Method': np.random.choice(['UPI', 'Credit Card', 'Debit Card', 'COD'], size=2000),
        'State': np.random.choice(states, size=2000),
        'Order_Status': np.random.choice(status_options, p=[0.75, 0.15, 0.07, 0.03], size=2000)
    }
    df = pd.DataFrame(data)
    df['Profit'] = (df['Sales_Amount'] * np.random.uniform(0.15, 0.38, size=2000)).round(2)
    return df.sort_values('Date')

with st.spinner('Synchronizing Data Matrix...'):
    df = load_enterprise_data()

# 3. Sidebar Configuration
st.sidebar.header("🕹️ Operations Control")

selected_category = st.sidebar.multiselect("Categories", options=df['Category'].unique(), default=df['Category'].unique())
selected_state = st.sidebar.multiselect("Regions/States", options=df['State'].unique(), default=df['State'].unique())

min_date, max_date = df['Date'].min().to_pydatetime(), df['Date'].max().to_pydatetime()
start_date, end_date = st.sidebar.date_input("Timeline Window", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered_df = df[
    (df['Category'].isin(selected_category)) & 
    (df['State'].isin(selected_state)) &
    (df['Date'] >= pd.to_datetime(start_date)) & 
    (df['Date'] <= pd.to_datetime(end_date))
]

# 4. Premium KPI Performance Matrix
total_sales = filtered_df['Sales_Amount'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df.shape[0]
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gross Revenue", f"₹{total_sales:,.2f}", delta="+12.4% vs Last Month")
col2.metric("Net Margin Generated", f"₹{total_profit:,.2f}", delta="+8.2% Growth")
col3.metric("Fulfillment Velocity", f"{total_orders:,} Orders", delta="+14.1% Scale")
col4.metric("Avg Basket Value (AOV)", f"₹{avg_order_value:,.2f}", delta="-1.5% Dev", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# Executive Summary Insights
if not filtered_df.empty:
    top_product = filtered_df.groupby('Product')['Sales_Amount'].sum().idxmax()
    top_state = filtered_df.groupby('State')['Sales_Amount'].sum().idxmax()
    top_payment = filtered_df['Payment_Method'].mode()[0]
    
    st.info(f"⚡ **Automated Intel Summary:** Key driver identified in product vertical **{top_product}**. Regional focus points heavily towards **{top_state}**. Payment velocity spikes around **{top_payment}** integration paths.")

st.markdown("---")

# 5. Core Insights (Cyberpunk Teal & Purple Accents)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Revenue Trajectory Over Time")
    trend_df = filtered_df.groupby('Date')['Sales_Amount'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.lineplot(data=trend_df, x='Date', y='Sales_Amount', ax=ax, color='#00f2fe', linewidth=2.5)
    ax.fill_between(trend_df['Date'], trend_df['Sales_Amount'], color='#00f2fe', alpha=0.08)
    plt.xticks(rotation=45)
    ax.set_ylabel("Revenue (₹)")
    ax.grid(True, linestyle=':', alpha=0.3)
    st.pyplot(fig)

with chart_col2:
    st.subheader("🗺️ Market Valuation (State-wise Volume)")
    state_df = filtered_df.groupby('State')['Sales_Amount'].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    # Using modern single color tone gradient rather than distracting rainbows
    sns.barplot(data=state_df, x='Sales_Amount', y='State', ax=ax, palette="flare_r")
    ax.set_xlabel("Gross Volume (₹)")
    ax.grid(True, axis='x', linestyle=':', alpha=0.3)
    st.pyplot(fig)

st.markdown("---")

# 6. Behavioral Matrix (Neon Accents)
st.header("🎯 Customer Profile Analytics")
prof_col1, prof_col2 = st.columns(2)

with prof_col1:
    st.subheader("👥 Elite Customer Cohorts (Top 10 Spenders)")
    customer_df = filtered_df.groupby('CustomerID').agg({'Sales_Amount': 'sum'}).rename(columns={'Sales_Amount': 'Total_Spent'}).sort_values('Total_Spent', ascending=False).head(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=customer_df, x='Total_Spent', y='CustomerID', ax=ax, palette="cool")
    ax.set_xlabel("Capital Spent (₹)")
    st.pyplot(fig)

with prof_col2:
    st.subheader("🛒 Spending Tier Segmentation (Donut Chart Style)")
    def segment_customer(price):
        if price > 30000: return 'Premium Cluster'
        elif price > 15000: return 'Mid-Tier Segment'
        else: return 'Budget Cohort'
        
    filtered_df['Customer_Segment'] = filtered_df['Sales_Amount'].apply(segment_customer)
    segment_counts = filtered_df['Customer_Segment'].value_counts().reset_index()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    # Wedgeprops makes it a minimalist Donut Chart
    ax.pie(segment_counts['count'], labels=segment_counts['Customer_Segment'], autopct='%1.1f%%', 
           startangle=90, colors=['#4facfe', '#00f2fe', '#f35588'], wedgeprops=dict(width=0.4, edgecolor='#0e1117', linewidth=3))
    st.pyplot(fig)

st.markdown("---")

# 7. Logistics & Velocity Analytics
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("📦 Supply Chain & Order Status Distribution")
    status_df = filtered_df['Order_Status'].value_counts().reset_index()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(status_df['count'], labels=status_df['Order_Status'], autopct='%1.1f%%', startangle=140, 
           colors=['#00e676', '#ffea00', '#ff1744', '#7c4dff'], wedgeprops=dict(width=0.4, edgecolor='#0e1117', linewidth=3))
    st.pyplot(fig)

with chart_col4:
    st.subheader("💎 Asset Viability Matrix (Volume vs Margin)")
    prod_df = filtered_df.groupby('Product').agg({'Quantity':'sum', 'Profit':'sum', 'Sales_Amount':'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.scatterplot(data=prod_df, x='Quantity', y='Profit', size='Sales_Amount', hue='Product', sizes=(200, 1200), ax=ax, palette="rainbow")
    ax.set_xlabel("Velocity (Units Sold)")
    ax.set_ylabel("Yield Margin (₹)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)
    ax.grid(True, linestyle=':', alpha=0.3)
    st.pyplot(fig)

st.markdown("---")

# 8. Data Extraction Terminal
st.subheader("📥 Data Governance Protocol")
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⚡ Secure Stream Download (CSV Format)",
    data=csv_data,
    file_name=f'enterprise_filtered_data_{datetime.now().strftime("%Y%m%d")}.csv',
    mime='text/csv',
)

st.dataframe(filtered_df.tail(15), use_container_width=True)

# 9. Signed Footnote Integration
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #4e5569; font-size: 14px; font-family: sans-serif; letter-spacing: 0.5px;'>
        Engineered with ❤️ by <strong>Munawir MT</strong> (<a href='mailto:munawirmt002@gmail.com' style='color: #00f2fe; text-decoration: none;'>munawirmt002@gmail.com</a>) | © 2026 Analytics Architecture
    </div>
    """, 
    unsafe_allow_html=True
)
