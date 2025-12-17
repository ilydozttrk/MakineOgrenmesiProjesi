# 📚 Kitap ve Yazar Öneri Sistemi (Book Recommendation & Popularity Analysis)

**Durum:** Tamamlandı ✅
**Dil:** Python 3.13.5
**Geliştirme Ortamı:** Jupyter Notebook
**Kütüphaneler:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn

Bu proje, üçüncü sınıf **Makine Öğrenmesi** dersi dönem sonu çalışması kapsamında geliştirilmiş olup, kitaplara ait puanlama ve etkileşim verilerini kullanarak **kitap popülerliği tahmini** yapan ve bu tahmin üzerinden **öneri sistemlerine altyapı oluşturmayı** amaçlayan bir makine öğrenmesi projesidir.

---

## 🎯 Projenin Amacı

Projenin temel amacı:

* Kitaplara ait **puan (rating)** ve **oy dağılımlarını** analiz etmek,
* Kitapların **popüler** veya **standart** olarak sınıflandırılmasını sağlamak,
* Bu sınıflandırma yaklaşımını kullanarak **content-based öneri sistemlerine temel oluşturmak**tır.

Problem, bir **ikili sınıflandırma (binary classification)** problemi olarak ele alınmıştır.

---

## 🧠 Kullanılan Yaklaşım

Proje uçtan uca bir makine öğrenmesi süreci içermektedir:

1. Veri temizleme ve ön işleme (Preprocessing)
2. Özellik mühendisliği (Feature Engineering)
3. Model eğitimi
4. Hiperparametre optimizasyonu
5. Model karşılaştırması
6. Ensemble (Voting Classifier) denemesi
7. Performans değerlendirmesi

---

## 📂 Veri Setleri

Projede birden fazla veri kaynağı kullanılmıştır. Bu veri setleri farklı amaçlara hizmet ederek modelin daha anlamlı sonuçlar üretmesini sağlamıştır:

### 1️⃣ book_rating.csv

Bu veri seti, model eğitiminin ana omurgasını oluşturmaktadır.

**İçerik:**

* Kitap adı (name)
* Ortalama puan (rating / average_rating)
* 1–5 yıldız arası oy sayıları

Yıldız bazlı oy sayıları birleştirilerek **toplam oy sayısı (vote_count)** özelliği üretilmiştir.

```python
vote_cols = ['one_star_count', 'two_star_count', 'three_star_count', 'four_star_count', 'five_star_count']
df['vote_count'] = df[vote_cols].sum(axis=1)
```

---

### 2️⃣ authors.csv

Bu veri seti, projede yazar bilgilerini tanımlamak ve veri kümesinin bağlamsal (contextual) değerini artırmak amacıyla kullanılmıştır.

**İçerik:**

* Yazar adı
* Biyografik ve tanımlayıcı bilgiler

> Not: Bu veri seti doğrudan model eğitiminde kullanılmamış; ancak veri setlerinin kapsamını genişletmek ve ileride yapılabilecek içerik tabanlı öneri sistemleri için altyapı oluşturmak amacıyla projeye dahil edilmiştir.

---

### 3️⃣ Turkish_Book_Dataset_Kaggle_V2.csv

Bu veri seti, Türkçe kitaplar özelinde yapılan analizlerde ve veri çeşitliliğini artırmak amacıyla kullanılmıştır.

**Amaç:**

* Türkçe kitaplara ait kayıtları incelemek
* Veri setinin yerel (lokal) bağlamda genişletilmesi

> Bu veri seti, doğrudan sınıflandırma modelinde kullanılmamış; ancak proje kapsamında veri çeşitliliğini artıran destekleyici bir kaynak olarak değerlendirilmiştir.

> Not: Tüm veri setleri ham (raw) formatta olduğu için analiz öncesinde kapsamlı ön işleme adımları uygulanmıştır.

⚠️ Uyarı: Bu veri seti GitHub'a atılamayacak kadar büyük olduğu için yükleme yapılamamıştır. Lütfen Kaggle Turkish Book Dataset (https://www.kaggle.com/datasets/ardaakdere16/turkish-book-dataset) 'e giderek verisetini indiriniz!

---

## 🧹 Veri Ön İşleme (Data Preprocessing)

Uygulanan temel adımlar:

* Sütun adlarının temizlenmesi
* Sayısal alanların `float/int` tipe dönüştürülmesi
* Eksik (NaN) kayıtların temizlenmesi
* Yıldız bazlı oyların birleştirilmesiyle `vote_count` özelliğinin üretilmesi

```python
vote_cols = ['one_star_count', 'two_star_count', 'three_star_count', 'four_star_count', 'five_star_count']
df['vote_count'] = df[vote_cols].sum(axis=1)
```

---

## 🏷️ Sınıf Tanımı (Labeling)

Kitaplar, toplam oy sayısına göre iki sınıfa ayrılmıştır:

* **0:** Standart kitap
* **1:** Popüler kitap

```python
limit = 500
df['category'] = df['vote_count'].apply(lambda x: 1 if x > limit else 0)
```

Bu eşik değeri deneysel olarak belirlenmiş olup popülerlik kavramını somut bir metrikle ifade etmektedir.

---

## 🧩 Özellik Mühendisliği (Feature Engineering)

Model performansını artırmak amacıyla kitap başlığından yeni özellikler türetilmiştir:

* **rating:** Ortalama kitap puanı
* **title_len:** Kitap adının karakter uzunluğu
* **word_count:** Kitap adındaki kelime sayısı
* **has_digit:** Kitap adında rakam bulunup bulunmadığı (seri kitapları yakalamak için)

```python
X = df[['rating', 'title_len', 'word_count', 'has_digit']]
```

---

## 🤖 Kullanılan Modeller

Projede aşağıdaki modeller eğitilmiş ve karşılaştırılmıştır:

### 1️⃣ Random Forest (GridSearch ile optimize edilmiş)

* Hiperparametre optimizasyonu yapılmıştır
* Dengesiz veri için `class_weight='balanced'` kullanılmıştır

### 2️⃣ Gradient Boosting

* Daha güçlü bir boosting yaklaşımı
* En yüksek doğruluk oranını sağlamıştır

### 3️⃣ Voting Classifier (Ensemble)

* Random Forest + Gradient Boosting
* Hard voting yöntemi kullanılmıştır

> Not: Ensemble model, tekil modellere kıyasla daha yüksek performans göstermemiştir. Bu durum, modellerin benzer yapıda (tree-based) olmasıyla açıklanabilir.

---

## 📊 Model Karşılaştırması (Özet)

| Model                      | Accuracy |
| -------------------------- | -------- |
| Random Forest (GridSearch) | ~0.80    |
| Gradient Boosting          | ~0.81    |
| Voting Classifier          | ~0.80    |

En iyi performans **Gradient Boosting** modeli tarafından elde edilmiştir.

---

## 📈 Değerlendirme Metrikleri

* Accuracy
* Precision, Recall, F1-score (Classification Report)
* Confusion Matrix (en iyi model için)

Confusion matrix analizi, modelin sınıflar üzerindeki başarısını detaylı olarak incelemek amacıyla kullanılmıştır.

---

## 🛠️ Kullanılan Teknolojiler

* **Python** – Ana programlama dili
* **Pandas & NumPy** – Veri işleme ve analiz
* **Scikit-learn** – Makine öğrenmesi modelleri
* **Matplotlib & Seaborn** – Veri görselleştirme
* **Jupyter Notebook** – Deneysel geliştirme ve dokümantasyon

---

## ⚠️ Karşılaşılan Zorluklar ve Çözümler

Bu proje geliştirilirken hem veri hem de modelleme aşamalarında çeşitli teknik zorluklarla karşılaşılmıştır. Bu zorluklar ve uygulanan çözümler aşağıda özetlenmiştir:

1️⃣ Kirli ve Tutarsız Veri Problemleri

* Sayısal olması gereken bazı sütunlar string (object) formatındaydı

* Eksik (NaN) değerler ve boş kayıtlar mevcuttu

* Çözüm:

   1. Tip dönüşümleri (to_numeric) uygulanmış

   2. Eksik kayıtlar analiz dışı bırakılmış

   3. Sütun adları ve formatlar standartlaştırılmıştır

2️⃣ Popülerlik Tanımının Belirlenmesi

* "Popüler kitap" kavramı için net bir etiket bulunmamaktaydı

* Uygun eşik değerinin belirlenmesi deneysel bir süreç gerektirdi

* Çözüm:

   1. Toplam oy sayısına dayalı bir popülerlik metriği tanımlandı

   2. Farklı eşik değerleri denenerek vote_count > 500 seçildi

3️⃣ Özellik Seçimi ve Sınırlı Feature Sayısı

* Veri setinde doğrudan kullanılabilecek anlamlı özellik sayısı sınırlıydı

* Çözüm:

   1. Kitap başlığından ek bilgiler çıkarılarak feature engineering uygulandı

   2. Başlık uzunluğu, kelime sayısı ve rakam içeriği gibi yeni değişkenler üretildi

4️⃣ Dengesiz Sınıf Dağılımı (Class Imbalance)

* Popüler ve standart kitap sınıfları arasında örnek sayısı farkı bulunmaktaydı

* Çözüm:

   1. Random Forest modelinde class_weight='balanced' parametresi kullanıldı

   2. F1-score metriği GridSearch sürecinde değerlendirme ölçütü olarak seçildi

5️⃣ Ensemble Modelin Beklenen Performansı Vermemesi

* Voting Classifier, tekil modellerden daha yüksek doğruluk sağlamadı

* Değerlendirme:

   1. Kullanılan modellerin benzer yapıda (tree-based) olması

   2. Özellik sayısının sınırlı olması

   3. Bu durum, ensemble yöntemlerinin her zaman performans artışı sağlamayabileceğini göstermektedir.

---

## 📌 Sonuç

Bu proje, gerçek bir veri seti üzerinde uçtan uca bir makine öğrenmesi süreci sunmakta olup; veri temizleme, özellik mühendisliği, model optimizasyonu ve sonuçların akademik olarak yorumlanması açısından kapsamlı bir dönem sonu çalışmasıdır.

Proje, öneri sistemlerine temel oluşturabilecek bir **popülerlik tahmin altyapısı** sağlamaktadır.

---


## 💻 Web Arayüzü ve Öneri Algoritmaları (UI & Recommendation Engine)

Veri temizleme aşamasından sonra, kullanıcıların verilerle etkileşime geçebilmesi ve kişiselleştirilmiş öneriler alabilmesi için **Streamlit** tabanlı interaktif bir web arayüzü geliştirilmiştir.

### 🚀 Arayüz Özellikleri
* **Dinamik Dashboard:** `Streamlit` ve `Plotly Express` kullanılarak veri dağılımı histogramları interaktif olarak sunulmuştur.
* **Çoklu Sekme Yapısı:** "Anasayfa", "Yazar Öneri Sistemi" ve "Kitaplar & Arama" olmak üzere modüler bir yapı kurulmuştur.
* **Özelleştirilmiş CSS:** Kullanıcı deneyimini artırmak için arayüz elementleri (sekmeler, metrikler) özel CSS kodları ile modernize edilmiştir.

### 🧠 Kullanılan Algoritmalar

Projenin arayüz katmanında çalışan öneri motoru, 3 temel matematiksel yaklaşımı kullanmaktadır:

#### 1. TF-IDF ve Kosinüs Benzerliği (Content-Based Filtering)
Kullanıcı bir yazar seçtiğinde, sistem yazarın biyografisini analiz eder. `scikit-learn` kütüphanesi kullanılarak metinler vektörize edilir ve matematiksel benzerlik hesaplanır.

```python
# Biyografileri sayısal vektörlere dönüştürme
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['biography'])

# Yazarlar arası açıyı (benzerliği) hesaplama
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
```

#### 2. Weighted Rating (Ağırlıklı Puanlama - IMDB Formülü)
Basit ortalama puan yanıltıcı olabileceğinden (az oylu yüksek puanlar vs.), "En İyiler" listesi oluşturulurken IMDB'nin kullandığı **Bayesyen Ağırlıklı Puanlama** formülü sisteme entegre edilmiştir.

$$
\text{Weighted Rating (WR)} = \left( \frac{v}{v+m} \cdot R \right) + \left( \frac{m}{v+m} \cdot C \right)
$$

* **v:** Oy sayısı
* **m:** Listeye girmek için gereken minimum oy eşiği
* **R:** Kitabın ortalama puanı
* **C:** Tüm veri setinin ortalama puanı

#### 3. Bulanık Arama ve Filtreleme
Kullanıcı kitap ararken tam ismi hatırlamak zorunda değildir. String eşleşme algoritmaları ile anahtar kelime içeren tüm sonuçlar filtrelenir ve anında listelenir.

```python
# Büyük/küçük harf duyarsız arama (Case insensitive search)
sonuclar = df_books[df_books['name'].str.contains(arama, case=False, na=False)]
```

## 🚀 Projeyi Çalıştırma 

Gerekli kütüphanelerin yüklü olduğundan emin olduktan sonra, terminal veya komut satırında (CMD) proje klasörüne gelerek aşağıdaki komutu çalıştırınız:

```bash
streamlit run arayüz.py
