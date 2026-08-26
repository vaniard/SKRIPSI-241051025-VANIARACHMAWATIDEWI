import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
import re
import requests
import csv
from io import StringIO
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import os
from datetime import datetime

# --- SETUP DASHBOARD ---
st.set_page_config(page_title="Dashboard Sentimen Ulasan Gojek", page_icon="🛵", layout="wide")

# --- WATERMARK KUSTOM MENGGUNAKAN CSS ---
watermark_html = """
<style>
.watermark {
    position: fixed;
    bottom: 15px;
    right: 20px;
    opacity: 0.7;
    font-family: 'Arial', sans-serif;
    font-size: 13px;
    color: #666;
    background-color: rgba(255, 255, 255, 0.5);
    padding: 5px 10px;
    border-radius: 10px;
    z-index: 100;
    pointer-events: none;
    user-select: none;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
<div class="watermark">✨ Crafted by Vania | AI & Data Scientist</div>
"""
st.markdown(watermark_html, unsafe_allow_html=True)

# Menentukan nama file penyimpanan feedback menggunakan tanda hubung
FEEDBACK_FILE = "feedback-pengguna.csv"

# Membersihkan file lama jika struktur kolomnya berbeda dari versi sebelumnya
if os.path.exists(FEEDBACK_FILE):
    try:
        df_check = pd.read_csv(FEEDBACK_FILE)
        if "Nama" not in df_check.columns:
            os.remove(FEEDBACK_FILE)
    except:
        pass

# --- 1. LOAD DATA & LEXICON (Dengan Cache) ---
@st.cache_data
def load_lexicons():
    lexicon_pos = dict()
    lexicon_neg = dict()
    
    url_pos = 'https://raw.githubusercontent.com/fajri91/InSet/master/positive.tsv'
    resp_pos = requests.get(url_pos)
    if resp_pos.status_code == 200:
        reader = csv.reader(StringIO(resp_pos.text), delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                try: lexicon_pos[row[0]] = int(row[1])
                except ValueError: continue
                
    url_neg = 'https://raw.githubusercontent.com/fajri91/InSet/master/negative.tsv'
    resp_neg = requests.get(url_neg)
    if resp_neg.status_code == 200:
        reader = csv.reader(StringIO(resp_neg.text), delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                try: lexicon_neg[row[0]] = int(row[1])
                except ValueError: continue
                
    return lexicon_pos, lexicon_neg

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("clean-data-ulasan-gojek-baru.csv") 
    except FileNotFoundError:
        df = pd.read_csv("clean_data_ulasan_gojek_baru.csv")
    df = df.dropna(subset=['text_final'])
    return df

@st.cache_data
def calculate_polarity(df, lex_pos, lex_neg):
    def get_sentiment(text):
        score = 0
        if isinstance(text, str):
            for word in text.split():
                if word in lex_pos: score += lex_pos[word]
                elif word in lex_neg: score += lex_neg[word]
        
        if score > 0: return score, 'positive'
        elif score < 0: return score, 'negative'
        else: return score, 'neutral'
        
    results = df['text_final'].apply(get_sentiment)
    df['polarity_score'] = [r[0] for r in results]
    df['polarity'] = [r[1] for r in results]
    return df

with st.spinner("Memuat Data dan Leksikon..."):
    lexicon_pos, lexicon_neg = load_lexicons()
    df_raw = load_data()
    df_clean = calculate_polarity(df_raw, lexicon_pos, lexicon_neg)

# --- 2. TRAINING MODEL UNTUK PREDIKSI INPUT ---
@st.cache_resource
def train_model(df):
    vectorizer = TfidfVectorizer(max_features=2000)
    X = vectorizer.fit_transform(df['text_final'])
    y = df['polarity']
    
    selector = SelectKBest(chi2, k=1000)
    X_selected = selector.fit_transform(X, y)
    
    rf_model = RandomForestClassifier(n_estimators=50, random_state=42)
    rf_model.fit(X_selected, y)
    
    return vectorizer, selector, rf_model

with st.spinner("Menyiapkan Model Machine Learning..."):
    vectorizer, selector, model = train_model(df_clean)

# --- 3. NLP PREPROCESSING UNTUK TEKS BARU ---
@st.cache_resource
def get_nlp_tools():
    stemmer = StemmerFactory().create_stemmer()
    stopword = StopWordRemoverFactory().create_stop_word_remover()
    return stemmer, stopword

stemmer, stopword_remover = get_nlp_tools()

def preprocess_text(text):
    text = text.lower() 
    text = re.sub(r'[^a-z\s]', '', text) 
    text = stopword_remover.remove(text) 
    text = stemmer.stem(text) 
    return text

# --- 4. SIDEBAR NAVIGASI & LOGO ---
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <div style='font-size: 60px;'>🛵📊</div>
    <b style='font-size: 22px; color: #00AA13; font-family: sans-serif;'>Go-Sentimen</b>
    <p style='font-size: 12px; color: gray; margin-top: 5px;'>By Vania</p>
</div>
<hr>
""", unsafe_allow_html=True)

st.sidebar.markdown("**Pilih fitur yang ingin diakses:**")
menu = st.sidebar.radio(
    "", 
    [
        "Halaman Utama",
        "Visualisasi Data", 
        "Data Ulasan Berdasarkan Sentimen", 
        "Uji Prediksi Sentimen", 
        "Penilaian Pengguna (Feedback)"
    ]
)

# --- 5. LOGIKA HALAMAN BERDASARKAN MENU ---

# ----------------- HALAMAN UTAMA -----------------
if menu == "Halaman Utama":
    st.markdown("<br><br><br>", unsafe_allow_html=True) 
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>Dashboard Analisis Sentimen<br>Ulasan Pengguna Gojek</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; color: gray;'>Gunakan panel navigasi di sebelah kiri untuk mengeksplorasi visualisasi data, menguji model prediksi, dan melihat ulasan pengguna.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='width: 50%; margin: auto;'>", unsafe_allow_html=True)

# ----------------- VISUALISASI DATA -----------------
elif menu == "Visualisasi Data":
    st.title("📈 Visualisasi Data Sentimen Gojek")
    st.markdown("Gunakan filter di bawah ini untuk melihat grafik berdasarkan kategori sentimen secara spesifik.")
    
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        filter_sentimen = st.selectbox(
            "Filter Kategori Sentimen:", 
            ["Semua Sentimen", "Positive", "Negative", "Neutral"]
        )
    with col_filter2:
        jenis_grafik = st.selectbox(
            "Pilih Grafik:", 
            [
                "Pie Chart Sentimen", 
                "Bar Chart Sentimen", 
                "Distribusi Panjang Teks", 
                "Top 20 Words", 
                "Word Cloud"
            ]
        )
        
    st.divider()
    
    if filter_sentimen == "Semua Sentimen":
        df_vis = df_clean.copy()
    else:
        df_vis = df_clean[df_clean['polarity'] == filter_sentimen.lower()].copy()

    color_map = {'positive': '#99ff99', 'negative': '#ff9999', 'neutral': '#66b3ff'}

    if jenis_grafik == "Pie Chart Sentimen":
        st.subheader("Pie Chart Polarity (Keseluruhan Data)")
        
        sizes = df_clean['polarity'].value_counts()
        labels = [str(idx).capitalize() for idx in sizes.index]
        colors = [color_map.get(idx, '#cccccc') for idx in sizes.index]
        explode = [0.1] + [0] * (len(sizes) - 1)
        
        # Penyesuaian Ukuran Pie Chart
        col1, col2, col3 = st.columns([1, 1.5, 1]) 
        with col2:
            fig1, ax1 = plt.subplots(figsize=(4, 4)) 
            fig1.patch.set_facecolor('white')
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode, textprops={'fontsize': 10}, shadow=True, colors=colors)
            st.pyplot(fig1)

    elif len(df_vis) == 0:
        st.warning(f"⚠️ Tidak ada data untuk kategori sentimen '{filter_sentimen}'.")

    elif jenis_grafik == "Bar Chart Sentimen":
        st.subheader(f"Bar Chart Distribusi ({filter_sentimen})")
        
        sizes = df_vis['polarity'].value_counts()
        labels = [str(idx).capitalize() for idx in sizes.index]
        colors = [color_map.get(idx, '#cccccc') for idx in sizes.index]
        
        # Penyesuaian Ukuran Bar Chart
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            fig2, ax2 = plt.subplots(figsize=(5, 3.5)) 
            fig2.patch.set_facecolor('white')
            sns.barplot(x=sizes.index, y=sizes.values, palette=colors, ax=ax2)
            for p in ax2.patches:
                ax2.annotate(format(p.get_height(), '.0f'), 
                             (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha='center', va='center', xytext=(0, 6), textcoords='offset points', fontsize=10)
            ax2.set_xticklabels(labels, fontsize=10)
            ax2.set_xlabel('Polarity', fontsize=11)
            ax2.set_ylabel('Jumlah', fontsize=11)
            st.pyplot(fig2)

    else:
        if jenis_grafik == "Distribusi Panjang Teks":
            st.subheader(f"Distribusi Panjang Teks ({filter_sentimen})")
            df_vis['text_length'] = df_vis['text_final'].apply(lambda x: len(str(x).split()))
            
            # --- PENYESUAIAN BARU: Dibungkus dengan kolom agar ukurannya di tengah dan proporsional ---
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                fig3, ax3 = plt.subplots(figsize=(6, 4)) 
                fig3.patch.set_facecolor('white')
                sns.histplot(df_vis['text_length'], bins=30, kde=True, color='teal', ax=ax3)
                ax3.set_xlabel('Panjang Kata', fontsize=10)
                ax3.set_ylabel('Frekuensi', fontsize=10)
                st.pyplot(fig3)

        elif jenis_grafik == "Top 20 Words":
            st.subheader(f"Top 20 Words berdasarkan TF-IDF ({filter_sentimen})")
            @st.cache_data
            def get_tfidf_top(data_text):
                vec = TfidfVectorizer()
                x = vec.fit_transform(data_text.astype(str))
                df_tfidf = pd.DataFrame(x.toarray(), columns=vec.get_feature_names_out())
                df_sum = df_tfidf.sum().reset_index(name='result')
                return df_sum.sort_values('result', ascending=False).head(15) 
            
            top_words = get_tfidf_top(df_vis['text_final'])
            
            # Penyesuaian Ukuran TF-IDF Chart
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                fig4, ax4 = plt.subplots(figsize=(6, 4)) 
                fig4.patch.set_facecolor('white')
                sns.barplot(x='result', y='index', data=top_words, palette='magma', ax=ax4)
                ax4.set_xlabel('Score TF-IDF', fontsize=10)
                ax4.set_ylabel('Words', fontsize=10)
                st.pyplot(fig4)

        elif jenis_grafik == "Word Cloud":
            # Penyesuaian Ukuran Asli WordCloud
            def plot_wordcloud(text, title):
                wc = WordCloud(width=400, height=250, background_color='white', stopwords=STOPWORDS).generate(text)
                fig, ax = plt.subplots(figsize=(4, 2.5)) 
                fig.patch.set_facecolor('white')
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                ax.set_title(title, pad=10, fontsize=12)
                return fig

            if filter_sentimen == "Semua Sentimen":
                st.subheader("Word Cloud Semua Kelas")
                col_wc1, col_wc2, col_wc3 = st.columns(3)
                
                pos_text = ' '.join(df_vis[df_vis['polarity'] == 'positive']['text_final'].astype(str))
                neg_text = ' '.join(df_vis[df_vis['polarity'] == 'negative']['text_final'].astype(str))
                neu_text = ' '.join(df_vis[df_vis['polarity'] == 'neutral']['text_final'].astype(str))
                
                if pos_text.strip():
                    with col_wc1: st.pyplot(plot_wordcloud(pos_text, "Positive Words"))
                if neg_text.strip():
                    with col_wc2: st.pyplot(plot_wordcloud(neg_text, "Negative Words"))
                if neu_text.strip():
                    with col_wc3: st.pyplot(plot_wordcloud(neu_text, "Neutral Words"))
            else:
                st.subheader(f"Word Cloud - {filter_sentimen}")
                kumpulan_teks = ' '.join(df_vis['text_final'].astype(str))
                
                # Pembungkus kolom untuk tampilan satu kelas
                col1, col2, col3 = st.columns([1, 1.5, 1])
                with col2:
                    if kumpulan_teks.strip():
                        st.pyplot(plot_wordcloud(kumpulan_teks, f"{filter_sentimen} Words"))
                    else:
                        st.info("Tidak ada kata yang cukup untuk ditampilkan di Word Cloud.")

# ----------------- MELIHAT DATA BERDASARKAN SENTIMEN -----------------
elif menu == "Data Ulasan Berdasarkan Sentimen":
    st.title("📂 Lihat Data Ulasan Pengguna")
    st.markdown("Gunakan fitur *dropdown* di bawah ini untuk memfilter teks ulasan (*review*) asli dari pengguna berdasarkan kategori sentimennya.")
    
    filter_data = st.selectbox(
        "Pilih Kategori Sentimen:", 
        ["Semua Sentimen", "Positive", "Negative", "Neutral"],
        key='data_filter'
    )
    
    if filter_data == "Semua Sentimen":
        df_tampil = df_clean[['Review', 'polarity', 'polarity_score']]
    else:
        df_tampil = df_clean[df_clean['polarity'] == filter_data.lower()][['Review', 'polarity', 'polarity_score']]
        
    st.write(f"Menampilkan **{len(df_tampil)}** baris ulasan dengan sentimen: **{filter_data}**")
    st.dataframe(df_tampil, use_container_width=True, height=500)

# ----------------- UJI PREDIKSI -----------------
elif menu == "Uji Prediksi Sentimen":
    st.title("📝 Uji Prediksi Sentimen")
    st.markdown("Masukkan kalimat baru untuk diprediksi menggunakan model Random Forest.")
    
    user_input = st.text_input("Masukkan kalimat baru: ")
    
    if st.button("Prediksi", type="primary"):
        if user_input.strip() == "":
            st.warning("Silakan masukkan teks terlebih dahulu!")
        else:
            with st.spinner('Memproses teks...'):
                cleaned_text = preprocess_text(user_input)
                
                X_new_kalimat = vectorizer.transform([cleaned_text])
                X_new_kalimat_df = pd.DataFrame(X_new_kalimat.toarray(), columns=vectorizer.get_feature_names_out())
                new_array = np.array(X_new_kalimat_df)
                
                selector_new = selector.transform(new_array)
                new_prediksi = model.predict(selector_new)[0]
                
                st.subheader("Hasil:")
                if new_prediksi == 'positive':
                    st.success("Sentimen kalimat baru adalah POSITIVE.")
                elif new_prediksi == 'neutral':
                    st.info("Sentimen kalimat baru adalah NEUTRAL.")
                else:
                    st.error("Sentimen kalimat baru adalah NEGATIVE.")

# ----------------- PENILAIAN + FITUR UNDUH DATA -----------------
elif menu == "Penilaian Pengguna (Feedback)":
    st.title("⭐ Penilaian Dashboard")
    st.markdown("Bagaimana pengalaman Anda menggunakan dashboard ini? Berikan *rating* dan komentar Anda!")

    # Menginisialisasi CSV dengan struktur kolom baru (menyertakan "Nama")
    if not os.path.exists(FEEDBACK_FILE):
        df_feedback_init = pd.DataFrame(columns=["Waktu", "Nama", "Rating", "Komentar"])
        df_feedback_init.to_csv(FEEDBACK_FILE, index=False)

    with st.form("feedback_form", clear_on_submit=True):
        input_nama = st.text_input("Masukkan Nama Anda:", placeholder="Ketik nama Anda di sini (opsional)...")
        
        rating = st.slider("Pilih Rating Bintang", min_value=1, max_value=5, value=5, step=1, format="%d ⭐")
        komentar = st.text_area("Masukkan komentar atau masukan Anda:")
        submitted = st.form_submit_button("Kirim Penilaian")
        
        if submitted:
            waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nama_bersih = input_nama.strip() if input_nama.strip() else "Anonim"
            komentar_bersih = komentar if komentar.strip() else "Tidak ada komentar."
            
            # Menyimpan data penilaian baru ke CSV
            new_data = pd.DataFrame([{"Waktu": waktu_sekarang, "Nama": nama_bersih, "Rating": rating, "Komentar": komentar_bersih}])
            new_data.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
            
            st.success("Terima kasih atas penilaian Anda! Feedback telah tersimpan secara permanen.")

    st.divider()
    st.subheader("Daftar Feedback Pengguna")
    
    try:
        df_tampil_fb = pd.read_csv(FEEDBACK_FILE)
        if len(df_tampil_fb) == 0:
            st.info("Belum ada feedback yang masuk. Jadilah yang pertama!")
        else:
            # 📥 KODE BARU: Fitur Tombol Unduh Data Penilaian Langsung dari Web Browser
            csv_data = df_tampil_fb.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Unduh Seluruh Data Feedback (CSV)",
                data=csv_data,
                file_name="feedback-pengguna-unduh.csv",
                mime="text/csv",
                type="secondary"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Mengurutkan dari input penilai paling baru
            df_tampil_fb = df_tampil_fb.sort_values(by="Waktu", ascending=False)
            
            for index, row in df_tampil_fb.iterrows():
                bintang = '⭐' * int(row['Rating'])
                st.write(f"👤 **{row['Nama']}** ({row['Waktu']}) | Rating: {bintang}")
                st.write(f"💬: *\"{row['Komentar']}\"*")
                st.markdown("---")
    except Exception as e:
        st.error(f"Gagal memuat data feedback: {e}")