# 📚 Kitap Veri Analizi ve Görselleştirme (Book Data Analysis Project)

**Durum:** Tamamlandı ✅
**Dil:** Python 3.13.5
**Kütüphaneler:** Pandas, Matplotlib, Seaborn
Bu proje, geniş kapsamlı kitap ve yazar veri setlerini kullanarak okuyucu davranışlarını, oy dağılımlarını ve popülerlik metriklerini analiz eden bir **Veri Bilimi (Data Science)** çalışmasıdır. 

Proje kapsamında; ham verilerin işlenmesi (preprocessing), tip dönüşümleri (type casting), veri temizliği ve istatistiksel görselleştirme aşamaları Python kullanılarak gerçekleştirilmiştir.

## 🎯 Projenin Amacı ve Kapsamı
Bu projenin temel amacı, kitaplara verilen puanlar ve oy sayıları arasındaki ilişkiyi incelemektir ve aynı zamanda kullanıcılara bir öneri sistemi sunmaktır. Ancak bu süreçte aşağıdaki teknik problemlerin çözümü hedeflenmiştir:

1.  **Kirli Veri Yönetimi:** Sayısal olması gereken sütunlardaki metin ifadelerinin (örn: "Bilinmiyor", "Hata") tespit edilip temizlenmesi.
2.  **Format Düzeltme:** Binlik ayracı olarak kullanılan virgüllerin (örn: "1,000") kaldırılarak verinin işlenebilir `integer/float` formatına dönüştürülmesi.
3.  **Veri Görselleştirme:** Temizlenen verinin dağılımını `Seaborn` ve `Matplotlib` kullanarak histogram ve yoğunluk grafikleriyle sunmak.

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

* **Python:** Ana programlama dili.
* **Pandas:** Veri manipülasyonu, CSV okuma ve `DataFrame` yönetimi için.
* **Seaborn:** İstatistiksel veri görselleştirme ve estetik grafikler için.
* **Matplotlib:** Grafiklerin eksen ayarları ve özelleştirilmesi için.
* **Jupyter Notebook:** Kodun interaktif geliştirilmesi ve dokümantasyonu için.

## 📂 Veri Seti Yapısı

Proje iki ana veri kaynağı kullanmaktadır:

* `book_rating.csv`: Kitapların ID'leri, aldığı puanlar ve oy sayıları (`vote_count`) verilerini içerir.
* `authors.csv`: Yazar isimleri ve biyografik bilgileri içerir.

> **Not:** Veri setleri ham (raw) formatta olduğu için, analiz öncesinde ön işleme adımları uygulanmıştır.

## ⚙️ Teknik Zorluklar ve Çözümler (Key Features)

Bu projede karşılaşılan **"Vote Count Type Error"** sorunu şu adımlarla çözülmüştür:

### 1. String Manipülasyonu
Veri setinde sayısal değerler `object` (string) olarak saklanmış ve "1,250" şeklinde virgül içermekteydi. Bu durum matematiksel işlemleri engelliyordu.
```python
# Virgülleri silme ve string temizliği
df['vote_count'] = df['vote_count'].astype(str).str.replace(',', '', regex=False)
```
#💻 Web Arayüzü ve Öneri Algoritmaları (UI & Recommendation Engine)

Veri temizleme aşamasından sonra, kullanıcıların verilerle etkileşime geçebilmesi ve kişiselleştirilmiş öneriler alabilmesi için Streamlit tabanlı interaktif bir web arayüzü geliştirilmiştir.🚀 Arayüz ÖzellikleriDinamik Dashboard: Streamlit ve Plotly Express kullanılarak veri dağılımı histogramları interaktif olarak sunulmuştur.Çoklu Sekme Yapısı: "Anasayfa", "Yazar Öneri Sistemi" ve "Kitaplar & Arama" olmak üzere modüler bir yapı kurulmuştur.Özelleştirilmiş CSS: Kullanıcı deneyimini artırmak için arayüz elementleri (sekmeler, metrikler) özel CSS kodları ile modernize edilmiştir.🧠 Kullanılan AlgoritmalarProjenin arayüz katmanında çalışan öneri motoru, 3 temel matematiksel yaklaşımı kullanmaktadır:1. TF-IDF ve Kosinüs Benzerliği (Content-Based Filtering)Kullanıcı bir yazar seçtiğinde, sistem yazarın biyografisini analiz eder. scikit-learn kütüphanesi kullanılarak metinler vektörize edilir ve matematiksel benzerlik hesaplanır.Python# Biyografileri sayısal vektörlere dönüştürme
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['biography'])

# Yazarlar arası açıyı (benzerliği) hesaplama
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
2. Weighted Rating (Ağırlıklı Puanlama - IMDB Formülü)Basit ortalama puan yanıltıcı olabileceğinden (az oylu yüksek puanlar vs.), "En İyiler" listesi oluşturulurken IMDB'nin kullandığı Bayesyen Ağırlıklı Puanlama formülü sisteme entegre edilmiştir.$$\text{Weighted Rating (WR)} = \left( \frac{v}{v+m} \cdot R \right) + \left( \frac{m}{v+m} \cdot C \right)$$v: Oy sayısım: Listeye girmek için gereken minimum oy eşiğiR: Kitabın ortalama puanıC: Tüm veri setinin ortalama puanı3. Bulanık Arama ve FiltrelemeKullanıcı kitap ararken tam ismi hatırlamak zorunda değildir. String eşleşme algoritmaları ile anahtar kelime içeren tüm sonuçlar filtrelenir ve anında listelenir.

