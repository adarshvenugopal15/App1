import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from yfinance.exceptions import YFRateLimitError

st.set_page_config(
    page_title="Global Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f4f8fb;
}
.title {
    font-size:40px;
    font-weight:bold;
    color:#1565C0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">📈 Global Stock Market Dashboard</p>', unsafe_allow_html=True)
st.write("Search any stock listed on Yahoo Finance and visualize its performance.")

stocks = {
    "Apple":"AAPL",
    "Microsoft":"MSFT",
    "Google":"GOOGL",
    "Amazon":"AMZN",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",
    "Meta":"META",
    "Netflix":"NFLX",
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "HDFC Bank":"HDFCBANK.NS",
    "ICICI Bank":"ICICIBANK.NS",
    "Toyota":"7203.T",
    "Sony":"6758.T",
    "Samsung":"005930.KS",
    "Alibaba":"9988.HK",
    "Tencent":"0700.HK"
}

col1, col2 = st.columns([2,1])

with col1:
    symbol = st.text_input("Enter Stock Symbol", "AAPL")

with col2:
    suggestion = st.selectbox("Popular Stocks", ["None"] + list(stocks.keys()))

if suggestion != "None":
    symbol = stocks[suggestion]

period = st.selectbox(
    "Select Time Period",
    ["5d","1mo","3mo","6mo","1y","2y","5y","max"]
)

@st.cache_data(ttl=600)
def load_stock(symbol, period):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period)
    return data

if st.button("Fetch Stock Data"):

    try:
        data = load_stock(symbol, period)

        if data.empty:
            st.error("Invalid Stock Symbol")
            st.stop()

        current = data["Close"].iloc[-1]

        if len(data) > 1:
            previous = data["Close"].iloc[-2]
        else:
            previous = current

        change = current - previous
        percent = (change / previous) * 100 if previous != 0 else 0

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Price",
            f"${current:.2f}",
            f"{percent:.2f}%"
        )

        c2.metric(
            "Highest",
            f"${data['High'].max():.2f}"
        )

        c3.metric(
            "Lowest",
            f"${data['Low'].min():.2f}"
        )

        c4.metric(
            "Latest Volume",
            f"{int(data['Volume'].iloc[-1]):,}"
        )

        st.subheader("Closing Price")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            line=dict(color="#1565C0", width=3),
            name="Close Price"
        ))

        fig.update_layout(
            template="plotly_white",
            height=500,
            xaxis_title="Date",
            yaxis_title="Price"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trading Volume")

        fig2 = go.Figure()

        fig2.add_trace(go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume"
        ))

        fig2.update_layout(
            template="plotly_white",
            height=400,
            xaxis_title="Date",
            yaxis_title="Volume"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Recent Stock Data")

        st.dataframe(data.tail(10), use_container_width=True)

        csv = data.to_csv().encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            csv,
            file_name=f"{symbol}.csv",
            mime="text/csv"
        )

    except YFRateLimitError:
        st.error("Yahoo Finance rate limit exceeded. Please wait a few minutes and try again.")

    except Exception as e:
        st.error(f"Error: {e}")
