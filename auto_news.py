import streamlit as st
import requests
import json
import os

st.title("Parafrase Berita dengan Gaya Non Formal")

st.markdown("Aplikasi ini menggunakan API dari News API untuk mengambil berita terbaru di Indonesia dan WebPilot API untuk melakukan parafrase dalam gaya non formal.")

def fetch_news():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=id&'
           'apiKey={}'.format(st.secrets['api_key']))
    response_news = requests.get(url)
    return response_news.json()['articles']

def paraphrase_article(article_url):
    endpoint = "https://preview.webpilotai.com/api/v1/watt"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(st.secrets['token'])
    }
    data = {
        "content": """Parafrase dengan gaya non formal berita ini dalam 1000 kata atau lebih: {}. Buat menjadi beberapa paragraf.""".format(article_url)
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    return response.json().get("content")

if st.button("Start Generating News"):
    st.markdown("### Mengambil Berita...")
    articles = fetch_news()
    article_titles = [article['title'] for article in articles]
    selected_title = st.selectbox("Pilih Judul Berita yang Ingin Diparafrase:", article_titles)
    selected_article = next((article for article in articles if article['title'] == selected_title), None)

    if selected_article:
        st.header("Judul Berita Terpilih:")
        st.write(selected_article['title'])
        st.image(selected_article['urlToImage'], caption=selected_article['title'])
        st.markdown("[Baca berita asli]({})".format(selected_article['url']))

        st.header("Parafrase dalam Gaya Non Formal:")
        paraphrased_content = paraphrase_article(selected_article['url'])
        st.write(paraphrased_content)
else:
    st.markdown("Tekan tombol di atas untuk mulai menghasilkan berita.")
