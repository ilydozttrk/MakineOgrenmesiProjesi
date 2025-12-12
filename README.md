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
