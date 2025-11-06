# 🤖 Portföy Botu (Portfolio Discord Bot)

![Discord Logo](https://cdn-icons-png.flaticon.com/512/5968/5968756.png)

## 🧠 Proje Hakkında
Bu proje, kullanıcıların **Discord** üzerinden kendi **projelerini kaydedebileceği, beceriler ekleyebileceği ve güncelleyebileceği** bir **Portföy Yönetim Botu**dur!  
Kısaca: Herkesin kendi projelerini takip edebileceği küçük ama akıllı bir asistan 💼✨

## 🚀 Özellikler
- 🆕 **Yeni proje ekleme:** `!new_project` komutuyla kolayca proje ekleyebilirsin.  
- 📋 **Proje listesi görüntüleme:** `!projects`  
- 🔧 **Proje güncelleme:** `!update_projects`  
- 💪 **Beceri ekleme:** `!skills`  
- ❌ **Proje silme:** `!delete`  
- ℹ️ **Yardım menüsü:** `!info`

Tüm bilgiler, yerel bir **SQLite veritabanında (`portfolio.db`)** güvenli şekilde saklanır.

---

## 🧩 Kullanılan Teknolojiler
| Teknoloji | Açıklama |
|------------|-----------|
| 🐍 Python | Ana programlama dili |
| 💬 Discord.py | Discord bot altyapısı |
| 🗃️ SQLite | Veritabanı yönetimi |
| ⚙️ Flask (Opsiyonel) | Web arayüzü entegrasyonu için kullanılabilir |

---


---

## 🧠 Veritabanı Yapısı
| Tablo | Açıklama |
|--------|-----------|
| `projects` | Proje bilgilerini tutar |
| `skills` | Becerileri listeler |
| `project_skills` | Proje-beceri bağlantısını oluşturur |
| `status` | Proje durumlarını saklar |

---

## ⚙️ Kurulum
1. Bu projeyi klonla:
   ```bash
   git clone https://github.com/arialperen456-dotcom/simbulamadm.git


👤 Geliştirici

Alperen Arı
💬 Discord: thedoctoralp
📧 Mail: ari.alperen@hotmail.com

🏁 Lisans

Bu proje, kişisel ve eğitim amaçlı olarak paylaşılmıştır.
Kodunuzu geliştirip paylaşmaktan çekinmeyin! 💖
