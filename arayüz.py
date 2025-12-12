import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Kitap & Yazar Öneri Sistemi", layout="wide", initial_sidebar_state="collapsed")

# --- 2. TASARIM VE RENKLER (CSS) ---
st.markdown("""
<style>
    /* Sekme Tasarımı */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; padding-bottom: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff; color: #4a4a4a; border: 1px solid #e0e0e0;
        border-radius: 8px 8px 0px 0px; padding: 10px 20px; font-weight: 600; transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #3b82f6; background-color: #f0f9ff; border-color: #3b82f6; }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important; color: #ffffff !important;
        border: none; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricValue"] { font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. VERİ YÜKLEME ---
@st.cache_data
def veri_yukle():
    try:
        authors = pd.read_csv('authors.csv')
        books = pd.read_csv('book_rating.csv')
        
        authors['biography'] = authors['biography'].fillna('')
        books['average_rating'] = pd.to_numeric(books['average_rating'], errors='coerce')
        books = books[(books['average_rating'] >= 0) & (books['average_rating'] <= 5)]
        books = books.dropna(subset=['average_rating', 'five_star_count'])
        books['name'] = books['name'].fillna('').astype(str)
        
        return authors, books
    except FileNotFoundError:
        return None, None

df_authors, df_books = veri_yukle()

# --- 4. FONKSİYONLAR ---

def get_author_recommendations(author_name, df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['biography'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    indices = pd.Series(df.index, index=df['name']).drop_duplicates()
    if author_name not in indices: return []

    idx = indices[author_name]
    if isinstance(idx, pd.Series): idx = idx.iloc[0]
        
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    author_indices = [i[0] for i in sim_scores]
    return df['name'].iloc[author_indices].tolist()

def get_top_books(df):
    C = df['average_rating'].mean()
    m = df['five_star_count'].quantile(0.70)
    q_books = df.copy().loc[df['five_star_count'] >= m]
    
    def weighted_rating(x, m=m, C=C):
        v = x['one_star_count'] + x['two_star_count'] + x['three_star_count'] + x['four_star_count'] + x['five_star_count']
        R = x['average_rating']
        return (v/(v+m) * R) + (m/(v+m) * C)
    
    q_books['score'] = q_books.apply(weighted_rating, axis=1)
    return q_books.sort_values('score', ascending=False).head(21)

def get_book_recommendations_by_title(book_title, df):
    try:
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['name'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        indices = pd.Series(df.index, index=df['name']).drop_duplicates()
        if book_title not in indices: return []
        
        idx = indices[book_title]
        if isinstance(idx, pd.Series): idx = idx.iloc[0]
            
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        book_indices = [i[0] for i in sim_scores]
        return df.iloc[book_indices][['name', 'average_rating']]
    except:
        return []

# --- 5. ARAYÜZ ---

if df_authors is None:
    st.error("❌ Dosyalar bulunamadı! Lütfen 'authors.csv' ve 'book_rating.csv' dosyalarını kontrol edin.")
else:
    tab_home, tab_author, tab_top = st.tabs(["🏠 Anasayfa", "✍️ Yazar Öneri Sistemi", "🏆 Kitaplar & Arama"])

    # --- SEKME 1: ANASAYFA ---
    with tab_home:
        st.title("📚 Kitap ve Yazar Öneri Sistemi")
        col1, col2 = st.columns([1, 1.5]) 
        with col1:
            st.image("https://images.unsplash.com/photo-1512820790803-83ca734da794", use_container_width=True)
            st.info("**Geliştiriciler:**\n\n👩‍💻 Semanur YILDIRIM\n\n👩‍💻 İlayda ÖZTÜRK")
        with col2:
            st.markdown("""
            ### 🚀 Proje Hakkında
            Bu proje, **Makine Öğrenmesi (Machine Learning)** dersi kapsamında geliştirdiğimiz, Doğal Dil İşleme (NLP) ve İstatistiksel Sıralama algoritmalarını kullanan kapsamlı bir öneri sistemidir.
            
            Amacımız, standart "en çok okunanlar" listelerinin ötesine geçerek, kullanıcının zevkine matematiksel olarak en yakın içerikleri sunmaktır.
            
            #### 🛠️ Kullandığımız Teknikler ve Algoritmalar
            
            **1. İçerik Tabanlı Filtreleme (Content-Based Filtering):**
            * Yazar öneri modülümüzde, yazarların biyografileri **TF-IDF (Term Frequency-Inverse Document Frequency)** yöntemiyle vektörize edilmiştir.
            * Ardından **Kosinüs Benzerliği (Cosine Similarity)** kullanılarak, seçtiğiniz yazarın üslubuna, türüne ve edebi kişiliğine en yakın diğer yazarlar hesaplanır.
            
            **2. Ağırlıklı Puanlama (Weighted Rating):**
            * Kitap sıralamalarında, sadece puana bakmak yanıltıcı olabilir (1 kişinin 5 verdiği kitap ile 1000 kişinin 4.5 verdiği kitap bir değildir).
            * Bu yüzden **IMDB'nin Top 250** listesinde kullandığı Bayesyen Formül kullanılarak hem oy sayısı hem de puan ağırlıklandırılmış, en güvenilir liste oluşturulmuştur.
            """)
            
        st.write("---")
        # Grafik Kısmı
        st.subheader("📊 Veri Seti İstatistikleri ve Analizi")
        try:
            fig = px.histogram(df_books, x="average_rating", nbins=20, 
                               title="Kitap Puanlarının Dağılımı (Histogram)",
                               labels={'average_rating':'Ortalama Puan (1-5)', 'count':'Kitap Sayısı'},
                               color_discrete_sequence=['#3b82f6'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.warning("""
            **📈 Grafik Analizi ve Çıkarımlar:**
            
            * **Negatif Çarpıklık (Negative Skewness):** Grafiğin sola yatık olması, veri setindeki puanların büyük çoğunluğunun yüksek değerlerde (3.5 - 4.5 arası) toplandığını gösterir.
            * **Kullanıcı Davranışı:** Bu durum, okuyucuların genellikle beğendikleri veya sevdikleri türdeki kitapları okuyup oylama eğiliminde olduklarını, beğenmedikleri kitaplara zaman harcamadıklarını kanıtlar.
            * **Veri Dağılımı:** 2.0 puanın altındaki kitap sayısı ihmal edilecek kadar azdır, bu da veri setinin popüler ve nitelikli kitaplardan oluştuğunu gösterir.
            """)
        except: pass

    # --- SEKME 2: YAZAR ÖNERİ ---
    with tab_author:
        st.header("✍️ Yazar Keşif Motoru")
        
        st.info("💡 **Bilgi:** Bu sistem sadece yazar isimlerine bakmaz. NLP algoritmamız, yazarların biyografilerini kelime kelime analiz ederek; **edebi tür, yazım üslubu, akım ve içerik** benzerliklerine göre en uygun eşleşmeleri yapar.")
        
        col_search, col_result = st.columns([1, 2])
        with col_search:
            with st.form("yazar_secim_formu"):
                yazar_listesi = df_authors['name'].sort_values().unique()
                secilen_yazar = st.selectbox("Yazar Seçin:", yazar_listesi)
                submit_btn = st.form_submit_button("Benzer Yazarları Getir", type="primary")
            
            if submit_btn:
                with st.spinner('Tür ve üslup analizi yapılıyor...'):
                    oneriler = get_author_recommendations(secilen_yazar, df_authors)
                with col_result:
                    if oneriler:
                        st.success(f"**{secilen_yazar}** ile tür ve üslup benzerliği taşıyan yazarlar:")
                        for yazar in oneriler:
                            st.markdown(f"- ✒️ **{yazar}**")
                    else:
                        st.warning("Veri bulunamadı.")
                
                st.write("---")
                st.subheader(f"📝 {secilen_yazar} Hakkında")
                bio = df_authors[df_authors['name'] == secilen_yazar]['biography'].iloc[0]
                if bio: st.info(bio)
                else: st.warning("Biyografi bulunamadı.")

    # --- SEKME 3: KİTAPLAR & ARAMA ---
    with tab_top:
        st.header("🏆 Kitap Dünyası ve Akıllı Arama")
        
        arama = st.text_input("🔍 Veritabanında Kitap Ara", placeholder="Kitap adı giriniz (Örn: Sefiller)...")
        
        if arama:
            sonuclar = df_books[df_books['name'].str.contains(arama, case=False, na=False)]
            
            if not sonuclar.empty:
                st.success(f"'{arama}' için **{len(sonuclar)}** kitap bulundu.")
                
                # --- BURADAKİ KISITLAMA KALDIRILDI (.head(10) SİLİNDİ) ---
                # Artık kaç kitap varsa hepsini gösterir
                gosterilecek_tablo = sonuclar[['name', 'average_rating', 'five_star_count']].reset_index(drop=True)
                gosterilecek_tablo.columns = ['Kitap Adı', 'Ortalama Puan', 'Oy Sayısı']
                st.dataframe(gosterilecek_tablo, use_container_width=True)
                
                st.write("---")
                st.markdown("### 📚 Benzer Kitap Önerileri")
                st.info("Bulunan kitaplardan birini seçerek, isim ve içerik olarak benzeyen diğer kitapları görebilirsiniz.")
                
                # Seçim kutusu için ilk 50 sonucu getirelim ki liste çok şişmesin (ama yukarıdaki tablo hepsini gösterir)
                secilen_kitap = st.selectbox("Benzerini bulmak istediğiniz kitabı seçin:", sonuclar['name'].head(50).unique())
                
                if st.button("Seçilen Kitabın Benzerlerini Göster", type="primary"):
                    with st.spinner(f"'{secilen_kitap}' için benzer kitaplar taranıyor..."):
                        benzer_kitaplar = get_book_recommendations_by_title(secilen_kitap, df_books)
                        
                        if len(benzer_kitaplar) > 0:
                            st.write(f"**{secilen_kitap}** kitabına benzer bulunanlar:")
                            cols = st.columns(len(benzer_kitaplar))
                            for idx, (i, row) in enumerate(benzer_kitaplar.iterrows()):
                                if idx < 5:
                                    with cols[idx]:
                                        with st.container(border=True):
                                            st.markdown(f"**{row['name']}**")
                                            st.caption(f"⭐ {row['average_rating']}")
                        else:
                            st.warning("Benzer kitap bulunamadı.")
            else:
                st.warning("Aradığınız kriterlere uygun kitap bulunamadı.")
        else:
            st.markdown("### 🔥 En Yüksek Skorlu Kitaplar")
            st.caption("Aşağıdaki liste, Weighted Rating (Ağırlıklı Puan) algoritması ile hesaplanmıştır.")
            top_books = get_top_books(df_books)
            cols = st.columns(3)
            for i, row in top_books.iterrows():
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(f"#{i+1} {row['name']}")
                        c1, c2 = st.columns(2)
                        c1.metric("Puan", f"{row['average_rating']:.1f}")
                        c2.metric("Skor", f"{row['score']:.2f}")
                        with st.expander("İstatistikler"):
                            val = min(max(row['average_rating']/5, 0.0), 1.0)
                            st.progress(val)
                            st.write(f"**Toplam Oy:** {int(row['five_star_count'])}")