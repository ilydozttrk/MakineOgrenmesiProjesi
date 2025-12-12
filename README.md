# 📚 Kitap Veri Analizi ve Görselleştirme Projesi

Bu proje, kitap puanlarını, oy sayılarını ve yazar verilerini analiz ederek okuyucu eğilimlerini görselleştirmek amacıyla geliştirilmiştir. Ham veriler temizlenmiş, hatalı kayıtlar (NaN, metin içeren sayılar) düzeltilmiş ve anlamlı grafiklere dönüştürülmüştür.

## 🚀 Projenin Amacı
* Büyük veri setleri üzerinde **Veri Temizliği (Data Cleaning)** pratikleri yapmak.
* Kitapların oy dağılımlarını ve popülerlik seviyelerini analiz etmek.
* Python kütüphanelerini (Pandas, Matplotlib, Seaborn) kullanarak görselleştirme yeteneklerini geliştirmek.

## 📊 Kullanılan Teknolojiler
* **Python 3**
* **Pandas:** Veri manipülasyonu ve CSV okuma işlemleri için.
* **Matplotlib & Seaborn:** Veri görselleştirme ve grafik çizimi için.
* **Jupyter Notebook:** Kodları interaktif olarak çalıştırmak için.

## 📂 Veri Seti Hakkında
Projede iki ana veri seti kullanılmıştır:
* `book_rating.csv`: Kitapların puan ve oy sayısı bilgilerini içerir.
* `authors.csv`: Yazar bilgilerini içerir.

*Not: Verilerde bulunan "1,000" gibi virgüllü sayılar ve hatalı karakterler proje kapsamında temizlenmiştir.*

## 📈 Örnek Görselleştirme
Proje sonucunda elde edilen **Oy Sayısı Dağılımı** grafiği aşağıdadır:

![Oy Dağılımı Grafiği](buraya_grafigin_resim_yolunu_yaz.png)
*(Buraya kodun kaydettiği .png dosyasının adını yazarsan grafik GitHub'da görünür)*

## ⚙️ Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza klonlayın veya indirin.
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install pandas matplotlib seaborn
