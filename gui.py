from libraries import *
from preprocessing import *
from tests import (run_performance_test, run_guvenlik_test, run_functionality_test,
                   search_url, archive, interactive_ddos)
from gui_fonksiyonlar import (domain_sorgula, hosting_paketleri_getir, marka_sorgula,
                              web_paket_getir, e_posta_getir, sunucu_paket, yorumları_getir,
                              save_result, clear_results, baslik, add_radio_button, add_button,
                              kaydet_site, ozet_al, baslik_getir, paragraf_getir, link_getir)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("TürkTicaret.Bot")
root.geometry("800x800")
root.configure(bg="#1e1e2e")

# Ana çerçeve
result_frame = tk.Frame(root, bg="#1e1e2e")
result_frame.pack(fill="both", expand=True)

# Üst frame
upper_frame = tk.Frame(result_frame, bg="#3c3c5c", height=70)
upper_frame.pack(side="top", fill="x")
upper_frame.pack_propagate(False)

# Üçlü düzen için iç frame
header_frame = tk.Frame(upper_frame, bg="#3c3c5c")
header_frame.pack(expand=True)

# Sol yazı
left_label = baslik(
    header_frame, bg="#3c3c5c", fg="white", text="TürkTicaret.net",
    fw=15, side="left", px=10
)

# Logo
logo = tk.Label(header_frame, bg="#3c3c5c")
logo_image = tk.PhotoImage(file="logo.png")
logo.config(image=logo_image)
logo.image = logo_image
logo.pack(side="left", padx=20)

# Sağ yazı
right_label = baslik(
    header_frame, bg="#3c3c5c", fg="white", text="ChatBot",
    fw=15, side="right", px=10
)

# Orta frame
middle_frame = tk.Frame(result_frame, bg="#1e1e2e")
middle_frame.pack(fill="both", expand=True)
middle_frame.pack_propagate(False)

# İç frame
result_inner_frame = tk.Frame(middle_frame, bg="#1e1e2e")
result_inner_frame.place(
    relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85
)

# Dikey Scrollbar
vertical_scrollbar = tk.Scrollbar(
    result_inner_frame, orient=tk.VERTICAL, troughcolor="#1e1e2e",
    background="#1e1e2e", activebackground="#1e1e2e", highlightthickness=0
)
vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Yatay Scrollbar
horizontal_scrollbar = tk.Scrollbar(
    result_inner_frame, orient=tk.HORIZONTAL, troughcolor="#1e1e2e",
    background="#1e1e2e", activebackground="#1e1e2e", highlightthickness=0
)
horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Text widget
result_text = tk.Text(
    result_inner_frame, font=("Arial", 10),
    yscrollcommand=vertical_scrollbar.set,
    xscrollcommand=horizontal_scrollbar.set,
    wrap="none", bg="#2e2e3e", fg="white"
)
result_text.pack(side=tk.LEFT, fill="both", expand=True)

# Scrollbar'larla Text widget'ını bağlama
vertical_scrollbar.config(command=result_text.yview)
horizontal_scrollbar.config(command=result_text.xview)

# Result text için mesaj fonksiyonu
def log_callback(message):
    result_text.insert(tk.END, message + "\n")
    result_text.yview(tk.END)

# Kullanıcı için logo fonksiyonu
def load_user_logo():
    user_logo = tk.PhotoImage(file="user.png")
    user_logo = user_logo.subsample(6, 6)
    return user_logo

user_logo = load_user_logo()

# Mesaj gönderme butonu için fonksiyon
def send_message():
    mesaj_renk = "lightgreen"
    mesaj = message_entry.get()
    if mesaj.strip() != "":
        result_text.tag_configure(
            "user", justify="right", foreground=mesaj_renk,
            font=("Arial", 12, "bold")
        )
        result_text.insert(tk.END, mesaj, "user")
        result_text.insert(tk.END, " : ", "user")
        result_text.image_create(tk.END, image=user_logo)
        result_text.insert(tk.END, "\n")
        result_text.see(tk.END)

        message_entry.delete(0, tk.END)

        # Cevap için case if li fonksiyona mesajı aktarmalıyız
        cevap = handle_user_request(mesaj)

        if cevap:
            # Bot cevap rengi
            bot_text_color = "red"
            result_text.tag_configure(
                "bot", justify="left", foreground=bot_text_color,
                font=("Arial", 12)
            )
            result_text.image_create(tk.END, image=bot_logo)
            result_text.insert(tk.END, " : " + cevap + "\n", "bot")
            result_text.see(tk.END)

# URL kontrol fonksiyonu
def is_valid_url(url):
    regex = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(regex, url) is not None

# Kullanıcı girdisine göre yanıt işleme
def handle_user_request(text):
    cleaned_text = preprocess_text(text)
    sentence = cleaned_text.lower()
    words = text.split()

    # Hosting işlemleri için koşul
    if "hosting" in sentence:
        threading.Thread(
            target=hosting_paketleri_getir,
            args=(result_text, bot_logo), daemon=True
        ).start()
        return "Hosting paket bilgileri getiriliyor..."

    # E-posta işlemleri için koşul
    if "eposta" in sentence or "posta" in sentence:
        threading.Thread(
            target=e_posta_getir,
            args=(result_text, bot_logo), daemon=True
        ).start()
        return "Kurumsal e-posta paket bilgileri getiriliyor..."

    # Sunucu işlemleri için koşul
    if "sunucu" in sentence or "server" in sentence:
        threading.Thread(
            target=sunucu_paket,
            args=(result_text, bot_logo), daemon=True
        ).start()
        return "Sunucu paket bilgileri getiriliyor..."

    # Yorum işlemleri için koşul
    if "yorum" in sentence:
        threading.Thread(
            target=yorumları_getir,
            args=(result_text, bot_logo), daemon=True
        ).start()
        return "Müşteri yorumları getiriliyor..."

    # Hazır siteler için koşul
    if "hazır site" in sentence:
        threading.Thread(
            target=web_paket_getir,
            args=(result_text, bot_logo), daemon=True
        ).start()
        return "Hazır web sitesi paketleri getiriliyor..."

    # Marka/İsim sorgulama işlemleri için koşul
    if "isim" in sentence or "marka" in sentence:
        keyword = text.split()[0] if text.split() else "marka"
        threading.Thread(
            target=marka_sorgula,
            args=(keyword, result_text, bot_logo), daemon=True
        ).start()
        return f"'{keyword}' kelimesiyle marka sorgusu yapılıyor..."

    # Domain işlemleri için koşul
    if "domain" in sentence:
        keyword = text.split()[0] if text.split() else "turkticaret"
        threading.Thread(
            target=domain_sorgula,
            args=(keyword, result_text, bot_logo), daemon=True
        ).start()
        return f"'{keyword}' kelimesiyle domain sorgusu yapılıyor..."

    # Paragraf çekimi için koşul
    if "paragraf" in sentence:
        url = next((word for word in words if is_valid_url(word)), "https://www.turkticaret.net")
        threading.Thread(
            target=paragraf_getir,
            args=(url, result_text, bot_logo), daemon=True
        ).start()
        return f"'{url}' adresinden paragraflar getiriliyor..."

    # Link çekme işlemleri için koşul
    if "link" in sentence:
        url = next((word for word in words if is_valid_url(word)), "https://www.turkticaret.net")
        threading.Thread(
            target=link_getir,
            args=(url, result_text, bot_logo), daemon=True
        ).start()
        return f"'{url}' adresinden paragraflar getiriliyor..."

    # Site ve kelime arama için koşul
    if any(w in sentence for w in ["ara", "git", "siteye git"]):
        words_lower = [w.lower() for w in words]
        for i, word in enumerate(words_lower):
            if word in ["ara", "git"]:
                if i > 0:
                    # Tüm önceki kelimeleri al o kelimeleri keyword yap ve ara
                    query = ' '.join(words[:i])
                    break
        else:
            query = "turkticaret"

        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(tk.END, f" : '{query}' için arama yapılıyor...\n", "bot")
        result_text.see(tk.END)

        try:
            search_url(query, log_callback)
            return f"'{query}' için arama penceresi açılıyor..."
        except Exception as e:
            return f"[HATA] Arama başlatılamadı: {str(e)}"

    # Güvenlik testi işlemleri için koşul
    if "güvenlik" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Güvenlik Testi Başlıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        try:
            run_guvenlik_test(url, result_text)
            return "Güvenlik testi tamamlandı. Başka nasıl yardımcı olabilirim?"
        except Exception as e:
            return f"Güvenlik testi başlatılamadı. Hata: {str(e)}"

    # Performans testi için koşul
    if "performans" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Performans Testi Başlıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        try:
            run_performance_test(url, result_text)
            return "Performans testi tamamlandı. Başka nasıl yardımcı olabilirim?"
        except Exception as e:
            return f"Performans testi başlatılamadı. Hata: {str(e)}"

    # Fonksiyon testi için koşul
    if "fonksiyon" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Fonksiyon Testi Başlıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        try:
            run_functionality_test(url, result_text)
            return "Fonksiyon testi tamamlandı. Başka nasıl yardımcı olabilirim?"
        except Exception as e:
            return f"Fonksiyon testi başlatılamadı. Hata: {str(e)}"

    # Arşivleme işlemi için koşul
    if "arşivle" in sentence or "arşiv" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Arşivleme Başlıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        try:
            archive(url, log_callback)
            return "Arşivleme tamamlandı. Başka nasıl yardımcı olabilirim?"
        except Exception as e:
            return f"Arşivleme başlatılamadı. Hata: {str(e)}"

    # DDos saldırısı işlemleri için koşul
    if any(word in sentence for word in ["dos", "saldır", "atak"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Saldırı Başlıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        def start_ddos():
            try:
                interactive_ddos(url, result_text, bot_logo)
            except Exception as e:
                result_text.insert(
                    tk.END,
                    f" : Saldırı başlatılamadı. Hata: {str(e)}\n",
                    "bot"
                )
                result_text.see(tk.END)

        try:
            threading.Thread(target=start_ddos, daemon=True).start()
            return "Saldırı başlatıldı. Tarayıcıyı kapatınca sona erecek."
        except Exception as e:
            return f"Saldırı başlatılamadı. Hata: {str(e)}"

    # Bu işlem biraz kastırabilir bilgisayarı bu sebep dikkat edelim
    # Sitenin dosyalarını kaydetme koşulu
    if any(word in sentence for word in ["kaydet", "indir"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )

        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : Site dosyaları indirilmeye hazırlanıyor: {url}\n",
            "bot"
        )
        result_text.see(tk.END)

        def start_download():
            try:
                kaydet_site(url, result_text, bot_logo)
            except Exception as e:
                result_text.insert(
                    tk.END,
                    f" : Dosyalar kaydedilemedi. Hata: {str(e)}\n",
                    "bot"
                )
                result_text.see(tk.END)

        try:
            threading.Thread(target=start_download, daemon=True).start()
            return "İndirme işlemi başlatıldı. Tamamlandığında size bilgi vereceğim."
        except Exception as e:
            return f"İndirme işlemi başlatılamadı. Hata: {str(e)}"

    # Nasılsın cevapları işlemleri için koşul
    if any(word in sentence for word in ["nasılsın", "nasıl gidiyor", "naber", "ne var ne yok"]):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            " : İyiyim, teşekkür ederim! Size nasıl yardımcı olabilirim?\n",
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # Selamlaşma işlemleri için koşul
    if any(word in sentence for word in ["merhaba", "selam", "günaydın", "iyi akşamlar"]):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            " : Merhaba! Size nasıl yardımcı olabilirim?\n",
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # Teşekkür ifadeleri için koşul
    if any(
            word in sentence for word in [
                "teşekkür", "sağol", "çok teşekkür ederim"
            ]
    ):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            " : Rica ederim! Herhangi bir konuda yardımcı olabilir miyim?\n",
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # İyilik ifadeleri için koşul
    if any(
            word in sentence for word in [
                "iyiyim", "iyi"
            ]
    ):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            " : İyi olmana sevindim! Herhangi bir konuda yardımcı olabilir miyim?\n",
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # Yardım kelimeleri için koşul
    if any(
            word in sentence for word in [
                "yardım", "destek", "yardımcı olur musun", "yardım istiyorum", "Yardim"
            ]
    ):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            " : Elbette! Size nasıl yardımcı olabilirim?\n",
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # Yapılanları sıralama işlemleri için koşul
    if any(
            word in sentence for word in [
                "yapabildiklerin", "yaptıkların", "sırala", "ne yapıyorsun", "listele", "yap"
            ]
    ):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            (
                " : Size aşağıdaki hizmetlerde yardımcı olabilir ve yapabilirim:\n\n"
                "**GENEL HİZMETLER:**\n"
                "- Domain sorgulama\n"
                "- Marka / İsim hakkı sorgulama\n"
                "- Hosting paketlerini listeleme\n"
                "- Hazır web sitesi paketlerini gösterme\n"
                "- Kurumsal e-posta hizmetlerini sunma\n"
                "- Sunucu (server) paketlerini görüntüleme\n"
                "- Sitenin kodlarını ve dosyalarını kaydetme\n"
                "- Müşteri yorumlarını listeleme\n"
                "- Sitenin başlıklarını listeleme ve kaydetme\n"
                "- Paragrafları listeleme ve kaydetme\n"
                "- Linkleri listeleme ve kaydetme\n"
                "- Sitenin kodlarını ve dosyalarını kaydetme\n"
                "- Müşteri yorumlarını listeleme\n\n"
                "**TEST ARAÇLARI:**\n"
                "- Performans testi (site hızı, öğe sayısı, HTTP durumu)\n"
                "- Güvenlik testi (zararlı bağlantı analizi)\n"
                "- Fonksiyonellik testi (tüm linklerin çalışabilirlik kontrolü)\n"
                "- Arama (URL veya anahtar kelime ile web'de gez)\n"
                "- Arşivleme (sayfaları PDF olarak kaydetme)\n"
                "- Etkileşimli DDoS simülasyonu (gelişmiş yapı, test amaçlı)\n\n"
                "   Lütfen yapmak istediğiniz işlemi belirtin.\n"
            ),
            "bot"
        )
        result_text.see(tk.END)
        return ""

    # Site hakkında bilgi işlemleri için koşul
    if any(word in sentence for word in ["hakkında", "nedir", "hakkında bilgi", "özet"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )

        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : {url} adresindeki web sitesi analiz ediliyor...\n",
            "bot"
        )
        result_text.see(tk.END)

        def start_meta_analysis():
            try:
                ozet_al(url, result_text, bot_logo)
            except Exception as e:
                result_text.insert(
                    tk.END,
                    f" : Site bilgisi alınamadı. Hata: {str(e)}\n",
                    "bot"
                )
                result_text.see(tk.END)

        threading.Thread(target=start_meta_analysis, daemon=True).start()
        return ""

    # Başlıkları getirme işlemleri için koşul
    if any(word in sentence for word in ["başlık", "başlıkları getir"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )

        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            f" : {url} adresindeki başlıklar kontrol ediliyor...\n",
            "bot"
        )
        result_text.see(tk.END)

        def start_get_headers():
            try:
                baslik_getir(url, result_text, bot_logo)
            except Exception as e:
                result_text.insert(
                    tk.END,
                    f" : Başlıklar alınamadı. Hata: {str(e)}\n",
                    "bot"
                )
                result_text.see(tk.END)

        try:
            threading.Thread(target=start_get_headers, daemon=True).start()
            return ""
        except Exception as e:
            return f"Başlık alma işlemi başlatılamadı. Hata: {str(e)}"

    # Kim olduğunu söyleme koşulu
    if any(word in sentence for word in ["kimsin", "nesin", "kim"]):
        result_text.tag_configure(
            "bot", justify="left", foreground="red", font=("Arial", 12)
        )
        result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(
            tk.END,
            (
                " : Merhaba! Ben dijital dünyada size rehberlik eden bir asistanım.\n"
                "Yaratıcım Namıkcan GÖLOVA (NamKodX) tarafından geliştirildim.\n"
                "Amacım, dijital hizmetler ve web testleri konusunda size hızlı, akıllı ve etkili destek sunmak.\n\n"
                "**Sunabildiğim Hizmetler:**\n"
                "- Domain sorgulama\n"
                "- Marka / İsim hakkı sorgulama\n"
                "- Hosting ve sunucu paketlerini listeleme\n"
                "- Hazır web sitesi ve kurumsal e-posta çözümleri\n"
                "- Sitenin kodlarını ve dosyalarını kaydetme\n"
                "- Müşteri yorumlarını listeleme\n"
                "- Sitenin başlıklarını listeleme ve kaydetme\n"
                "- Paragrafları listeleme ve kaydetme\n"
                "- Linkleri listeleme ve kaydetme\n"
                "- Sitenin kodlarını ve dosyalarını kaydetme\n"
                "- Müşteri yorumlarını gösterme\n\n"
                "**Test Araçlarım:**\n"
                "- Performans testi (site hızı, öğe sayısı, HTTP durumu)\n"
                "- Güvenlik testi (zararlı bağlantı analizi)\n"
                "- Fonksiyonellik testi (link kontrolü)\n"
                "- Web arama ve URL tarayıcı\n"
                "- Arşivleme (PDF olarak sayfa kaydı)\n"
                "- Etkileşimli DDoS simülasyonu (test amaçlı)\n\n"
                "Sadece komut verin, gerekeni hemen yapayım! 😊\n"
            ),
            "bot"
        )
        result_text.see(tk.END)
        return ""

    return "Ne dediğinizi anlayamadım. Lütfen daha açık bir şekilde tekrar deneyin."

# Bot Logo Ayarlama
def load_bot_logo():
    bot_logo = tk.PhotoImage(file="logo.png")
    bot_logo = bot_logo.subsample(6, 6)
    return bot_logo

bot_logo = load_bot_logo()

# Bot cevap verme fonksiyonu
def bot_response(kullanici_mesaj):
    cevap = "Merhaba, nasıl yardımcı olabilirim?"

    result_text.tag_configure(
        "bot", justify="left", foreground="red", font=("Arial", 12)
    )
    result_text.image_create(tk.END, image=bot_logo)
    result_text.insert(tk.END, " : " + cevap + "\n", "bot")
    result_text.see(tk.END)
    result_text.image = bot_logo

# Sesle message_entry kısmına yazma
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            result_text.tag_configure(
                "user", justify="right", foreground="lightgreen",
                font=("Arial", 12, "bold")
            )
            result_text.insert(tk.END, "🎤 Dinleniyor...", "user")
            result_text.insert(tk.END, " : ", "user")
            result_text.image_create(tk.END, image=user_logo)
            result_text.insert(tk.END, "\n")
            result_text.see(tk.END)
            root.update()

            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language="tr-TR")

            message_entry.delete(0, tk.END)
            message_entry.insert(0, text)

        # Ses errorları için olan seyler
        except sr.UnknownValueError:
            result_text.insert(tk.END, "🎤 Ses anlaşılamadı, tekrar deneyin.\n", "user")
            result_text.see(tk.END)
        except sr.RequestError:
            result_text.insert(tk.END, "🎤 Bağlantı sorunu, tekrar deneyin.\n", "user")
            result_text.see(tk.END)
        except sr.WaitTimeoutError:
            result_text.insert(tk.END, "🎤 Zaman aşımı. Lütfen tekrar deneyin.\n", "user")
            result_text.see(tk.END)

# Send_message enter tıkladıgında da gitmesi icin fonksiyon
def enter_gonder(event):
    send_message()

# Result text kaydetme fonksiyonu
def save_results_gui():
    save_result(result_text)

# Result text temizleme fonksiyonu
def clear_results_gui():
    clear_results(result_text)

# Butonlar için çerçeve
button_frame = tk.Frame(middle_frame, bg="#1e1e2e")
button_frame.pack(side="bottom", pady=10)

# Kaydetme butonu
save_button = tk.Button(
    button_frame,
    text="Sonucu Kaydet",
    command=save_results_gui,
    bg="#3c3c5c",
    fg="#1e1e2e",
    activebackground="#1e1e2e",
    bd=0
)
save_button.pack(side=tk.LEFT, padx=10)

# Temizleme butonu
clear_button = tk.Button(
    button_frame,
    text="Sonuçları Temizle",
    command=clear_results_gui,
    bg="#3c3c5c",
    fg="#1e1e2e",
    activebackground="#1e1e2e",
    bd=0
)
clear_button.pack(side=tk.RIGHT, padx=10)

# Alt footer bloğu çerçevesi
footer_frame = tk.Frame(result_frame, bg="#3c3c5c", height=100)
footer_frame.pack(side="bottom", fill="x")
footer_frame.pack_propagate(False)

# İçteki footer çerçevesi
input_frame = tk.Frame(footer_frame, bg="#3c3c5c")
input_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.8)

# Soldaki mikrofon butonu
mic_button = tk.Button(
    input_frame,
    text="🎤",
    font=("Arial", 16),
    bg="#1e1e2e",
    fg="white",
    activebackground="#1e1e2e",
    relief="flat",
    width=3,
    height=1,
    command=record_audio,
    cursor="hand2",
    bd=0,
    highlightthickness=0
)
mic_button.pack(side="left", padx=(10, 5), pady=10)

# Ortadaki mesaj Giriş alanı
message_entry = tk.Entry(
    input_frame,
    font=("Arial", 15),
    bg="#4b4b6b",
    fg="white",
    relief="flat",
    insertbackground="white"
)
message_entry.pack(side="left", fill="both", expand=True, padx=(5, 5), pady=10)
message_entry.bind("<Return>", enter_gonder)

# Gönderme butonu
send_button = tk.Button(
    input_frame,
    text="📩",
    font=("Arial", 16),
    bg="#1e1e2e",
    fg="white",
    activebackground="#1e1e2e",
    relief="flat",
    width=3,
    height=1,
    command=send_message,
    cursor="hand2",
    bd=0,
    highlightthickness=0
)
send_button.pack(side="left", padx=(5, 10), pady=10)

# Başta çıkan bot mesajı
def initial_bot_message():
    result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
    result_text.image_create(tk.END, image=bot_logo)
    result_text.insert(tk.END, " : Merhaba, nasıl yardımcı olabilirim?\n", "bot")
    result_text.see(tk.END)

# Başta çıkan bot mesajının fonksiyonunun çalıştırılması
initial_bot_message()

# Kapatana kadar programı tutar
root.mainloop()