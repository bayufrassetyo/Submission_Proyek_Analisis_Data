import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob

# ---- MEMUAT DATA ----
@st.cache_data
def load_data():
    # Load dataset
    orders_df = pd.read_csv("order_payments.csv")
    reviews_df = pd.read_csv("order_reviews.csv")
    customers_df = pd.read_csv("customers.csv")

    # Konversi kolom tanggal
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    reviews_df['review_creation_date'] = pd.to_datetime(reviews_df['review_creation_date'])

    return orders_df, reviews_df, customers_df

orders_df, reviews_df, customers_df = load_data()

# ---- SIDEBAR FILTER ----
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(orders_df['order_purchase_timestamp'].dt.year.unique()))

# Filter berdasarkan tahun
filtered_orders = orders_df[orders_df['order_purchase_timestamp'].dt.year == selected_year]

# ---- DASHBOARD UTAMA ----
st.title("📊 E-Commerce Dashboard")

# ---- RINGKASAN STATISTIK ----
st.subheader("📌 Ringkasan Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transaksi", f"{len(filtered_orders):,}")
col2.metric("Total Pendapatan", f"${filtered_orders['payment_value'].sum():,.2f}")
col3.metric("Rata-rata Rating", f"{reviews_df['review_score'].mean():.2f}")

# ---- VISUALISASI 1: Tren Penjualan ----
st.subheader("📈 Tren Pendapatan Bulanan")
monthly_revenue = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.to_period("M"))['payment_value'].sum()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=monthly_revenue.index.astype(str), y=monthly_revenue.values, marker="o", ax=ax)
ax.set_xticklabels(monthly_revenue.index.astype(str), rotation=45)
ax.set_ylabel("Pendapatan")
st.pyplot(fig)

# ---- VISUALISASI 2: Distribusi Ulasan Pelanggan ----
st.subheader("🌟 Distribusi Ulasan Pelanggan")
review_counts = reviews_df['review_score'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=review_counts.index, y=review_counts.values, palette="viridis", ax=ax)
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

# ---- VISUALISASI 3: Word Cloud Ulasan ----
st.subheader("💬 Kata-kata yang Sering Muncul dalam Ulasan")
all_reviews = " ".join(reviews_df['review_comment_message'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_reviews)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# ---- VISUALISASI 4: Analisis Sentimen ----
st.subheader("😊 Analisis Sentimen Ulasan")
def get_sentiment(text):
    if pd.isna(text):
        return "Neutral"
    analysis = TextBlob(text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

reviews_df["sentiment"] = reviews_df["review_comment_message"].apply(get_sentiment)
sentiment_counts = reviews_df["sentiment"].value_counts()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette=["green", "gray", "red"], ax=ax)
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

# ---- VISUALISASI 5: Distribusi Demografi Pelanggan ----
st.subheader("📍 Distribusi Pelanggan Berdasarkan Lokasi")
customer_counts = customers_df["customer_state"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=customer_counts.index, y=customer_counts.values, palette="coolwarm", ax=ax)
ax.set_ylabel("Jumlah Pelanggan")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# ---- MENJALANKAN STREAMLIT ----
# Simpan kode ini dalam file `dashboard.py` lalu jalankan:
# streamlit run dashboard.py