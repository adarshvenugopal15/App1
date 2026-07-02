import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.main{
    background-color:#f4f8fb;
}
.big-font{
    font-size:35px;
    font-weight:bold;
    color:#0d47a1;
}
.stock-box{
    background:#ffffff;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}
.metric{
    text-align:center;
    font-size:22px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">📈 Global Stock Market Dashboard</p>', unsafe_allow_html=True)

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

col1,col2=st.columns([2,1])

with col1:
    symbol=st.text_input("Enter Stock Symbol","AAPL")

with col2:
    suggestion=st.selectbox(
        "Popular Stocks",
        ["None"]+list(stocks.keys())
    )

if suggestion!="None":
    symbol=stocks[suggestion]

period=st.selectbox(
    "Select Time Period",
    ["5d","1mo","3mo","6mo","1y","2y","5y","max"]
)

if st.button("Fetch Stock Data"):

    stock=yf.Ticker(symbol)

    data=stock.history(period=period)

    if data.empty:
        st.error("Invalid Stock Symbol")
    else:

        info=stock.info

        current=data["Close"].iloc[-1]

        previous=data["Close"].iloc[-2]

        change=current-previous

        percent=(change/previous)*100

        st.markdown("---")

        c1,c2,c3=st.columns(3)

        c1.metric(
            "Current Price",
            f"${current:.2f}",
            f"{percent:.2f}%"
        )

        c2.metric(
            "High",
            f"${data['High'].max():.2f}"
        )

        c3.metric(
            "Low",
            f"${data['Low'].min():.2f}"
        )

        st.markdown("## Company Information")

        st.write("**Company Name:**",info.get("longName","N/A"))
        st.write("**Sector:**",info.get("sector","N/A"))
        st.write("**Industry:**",info.get("industry","N/A"))
        st.write("**Country:**",info.get("country","N/A"))

        fig=go.Figure()

        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            line=dict(color="#1976D2",width=3),
            name="Closing Price"
        ))

        fig.update_layout(
            title="Closing Price",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig,use_container_width=True)

        volume=go.Figure()

        volume.add_trace(go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume"
        ))

        volume.update_layout(
            title="Trading Volume",
            template="plotly_white",
            height=400
        )

        st.plotly_chart(volume,use_container_width=True)

        st.dataframe(data.tail(10))
