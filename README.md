# Kişisel Günlük Uygulaması

Streamlit ile geliştirilmiş, kullanıcı girişi olan kişisel günlük (dijital jurnal)
uygulaması. Kullanıcılar günlük yazabilir, ruh hallerini takip edebilir ve
istatistiklerini grafiklerle görebilir.

## Özellikler

- **Kullanıcı sistemi**: Kayıt olma ve giriş yapma (şifreler SHA-256 ile hashlenerek saklanır)
- **Günlük yönetimi**: Başlık, içerik ve ruh hali ile günlük ekleme, düzenleme, silme
- **Ruh hali istatistikleri**: Mutlu / üzgün / yorgun / heyecanlı / normal dağılımının
  bar grafiği ve zaman içindeki günlük sayısının çizgi grafiği
- **Filtreleme ve arama**: Tarihe, ruh haline veya metin içeriğine göre filtreleme
- **Dışa aktarma**: Günlükleri CSV veya TXT olarak indirme

## Proje Yapısı

```
app.py       # Streamlit arayüzü ve sayfa akışı
auth.py       # Kayıt / giriş formları
db.py          # SQLite veritabanı işlemleri (kullanıcılar ve günlükler)
```

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Çalıştırma

```bash
streamlit run app.py
```

Uygulama ilk çalıştırıldığında `gunluk.db` adında bir SQLite veritabanı
otomatik olarak oluşturulur.

## Kullanılan Teknolojiler

- Python
- Streamlit — web arayüzü
- SQLite — veri depolama
- pandas — veri işleme ve grafikler
