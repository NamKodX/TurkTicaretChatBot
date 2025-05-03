from preprocessing import preprocess_text
from tests import search_url, archive, interactive_ddos
from cli_fonksiyonlar import (
    run_performance_test_cli,
    run_guvenlik_test_cli,
    run_functionality_test_cli,
    domain_sorgula_cli,
    hosting_paketleri_getir_cli,
    marka_sorgula_cli,
    web_paket_getir_cli,
    e_posta_getir_cli,
    sunucu_paket_cli,
    yorumlari_getir_cli,
    baslik_getir_cli,
    paragraf_getir_cli,
    search_url_cli,
    link_getir_cli, ozet_al_cli
)
from libraries import *

# Url kontrol fonksiyonu
def is_valid_url(url):
    regex = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(regex, url) is not None

""" 
    Bu cli yapısı belgede yer alıyordu bende gui yaninda bu şekilde bir cli şeklinde çalışacak duruma soktum
    Bunun için yapıdaki fonksiyonları düzenleyip cli_fonksiyonlar içinde koyup düzenledim
    Çünkü genel olarak fonksiyonlar gui için yazılmıştı
    En sonunda yavas yavas ve interaktif yazması icin islem getirdim bu güzel oldu yapı olarak
"""
def handle_cli_request(text):
    # Preprocessing içerisinden metin önişleme fonksiyonlarını alıp kullandık.
    cleaned_text = preprocess_text(text)
    sentence = cleaned_text.lower()
    words = text.split()

    # Konsol hosting işlemleri için koşul
    if "hosting" in sentence:
        hosting_paketleri_getir_cli()

    # Konsol eposta işlemleri için koşul
    elif "eposta" in sentence or "posta" in sentence:
        e_posta_getir_cli()

    # Konsol sunucu işlemleri için koşul
    elif "sunucu" in sentence or "server" in sentence:
        sunucu_paket_cli()

    # Konsol yorum işlemleri için koşul
    elif "yorum" in sentence:
        yorumlari_getir_cli()

    # Konsol hazır site işlemleri için koşul
    elif "hazır site" in sentence:
        web_paket_getir_cli()

    # Konsol isim sorgulama işlemleri için koşul
    elif "isim" in sentence or "marka" in sentence:
        keyword = words[0] if words else "marka"
        marka_sorgula_cli(keyword)

    # Konsol domain işlemleri için koşul
    elif "domain" in sentence or "dom" in sentence:
        keyword = words[0] if words else "turkticaret"
        domain_sorgula_cli(keyword)

    # Konsol güvenlik testi işlemleri için koşul
    elif "güvenlik" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        run_guvenlik_test_cli(url)

    # Konsol performans testi işlemleri için koşul
    elif "performans" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        run_performance_test_cli(url)

    # Konsol fonksiyon testi işlemleri için koşul
    elif "fonksiyon" in sentence and "test" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        run_functionality_test_cli(url)

    # Konsol arşivleme fonksiyonu işlemleri için koşul
    elif "kaydet" in sentence or "arşiv" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        archive(url, print)

    # Konsol ddos saldırıları işlemleri için koşul
    elif any(word in sentence for word in ["dos", "saldır", "atak"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        interactive_ddos(url, print, None)

    # Konsol nasılsın işlemleri için koşul
    elif any(word in sentence for word in ["nasılsın", "nasıl gidiyor", "naber"]):
        typewriter_print("Bot: İyiyim, teşekkür ederim. Siz nasılsınız?")

    # Konsol selamlaşma işlemleri için koşul
    elif any(word in sentence for word in ["merhaba", "selam"]):
        typewriter_print("Bot: Merhaba! Size nasıl yardımcı olabilirim?")

    # Konsol teşekkür işlemleri için koşul
    elif any(word in sentence for word in ["teşekkür", "sağol"]):
        typewriter_print("Bot: Rica ederim! Yardımcı olabileceğim başka bir konu var mı?")

    # Konsol yardımcı işlemleri için koşul
    elif any(word in sentence for word in ["yardım", "destek"]):
        typewriter_print("Bot: Elbette. Size yardımcı olmak için buradayım.")

    # Konsol yapılabilir işlemleri için koşul
    elif any(word in sentence for word in
             ["yapabildiklerin", "yaptıkların", "sırala", "ne yapıyorsun", "listele", "yap"]):
        typewriter_print("Bot: Size aşağıdaki hizmetlerde yardımcı olabilirim:\n")

        typewriter_print("**GENEL HİZMETLER:**")
        typewriter_print("- Domain sorgulama")
        typewriter_print("- Marka / İsim hakkı sorgulama")
        typewriter_print("- Hosting paketlerini listeleme")
        typewriter_print("- Hazır web sitesi paketlerini gösterme")
        typewriter_print("- Kurumsal e-posta hizmetlerini sunma")
        typewriter_print("- Sunucu (server) paketlerini görüntüleme")
        typewriter_print("- Sitenin başlıklarını listeleme ve kaydetme")
        typewriter_print("- Paragrafları listeleme ve kaydetme")
        typewriter_print("- Linkleri listeleme ve kaydetme")
        typewriter_print("- Sitenin kodlarını ve dosyalarını kaydetme")
        typewriter_print("- Müşteri yorumlarını listeleme\n")

        typewriter_print("**TEST ARAÇLARI:**")
        typewriter_print("- Performans testi (site hızı, öğe sayısı, HTTP durumu)")
        typewriter_print("- Güvenlik testi (zararlı bağlantı analizi)")
        typewriter_print("- Fonksiyonellik testi (tüm linklerin çalışabilirlik kontrolü)")
        typewriter_print("- Arama (URL veya anahtar kelime ile web'de gez)")
        typewriter_print("- Arşivleme (sayfaları PDF olarak kaydetme)")
        typewriter_print("- Etkileşimli DDoS simülasyonu (gelişmiş yapı, test amaçlı)\n")

        typewriter_print("Bot: Lütfen yapmak istediğiniz işlemi yazın.")

    # İyilik işlemleri koşulu
    elif any(word in sentence for word in ["iyiyim", "iyi"]):
        typewriter_print("Bot: İyi olmana sevindim! Herhangi bir konuda yardımcı olabilir miyim?")

    # Konsol kimlik işlemleri için koşul
    elif any(word in sentence for word in ["kimsin", "nesin", "kim"]):
        typewriter_print("Bot: Merhaba! Ben dijital dünyada size rehberlik eden bir asistanım.")
        typewriter_print("Yaratıcım Namıkcan GÖLOVA (NamKodX) tarafından geliştirildim.")
        typewriter_print("Amacım, dijital hizmetler ve web testleri konusunda size hızlı, akıllı ve etkili destek sunmak.\n")

        typewriter_print("**Sunabildiğim Hizmetler:**")
        typewriter_print("- Domain sorgulama")
        typewriter_print("- Marka / İsim hakkı sorgulama")
        typewriter_print("- Hosting ve sunucu paketlerini listeleme")
        typewriter_print("- Hazır web sitesi ve kurumsal e-posta çözümleri")
        typewriter_print("- Kurumsal e-posta hizmetlerini sunma")
        typewriter_print("- Sunucu (server) paketlerini görüntüleme")
        typewriter_print("- Sitenin başlıklarını listeleme ve kaydetme")
        typewriter_print("- Paragrafları listeleme ve kaydetme")
        typewriter_print("- Linkleri listeleme ve kaydetme")
        typewriter_print("- Sitenin kodlarını ve dosyalarını kaydetme")
        typewriter_print("- Müşteri yorumlarını gösterme\n")

        typewriter_print("**Test Araçlarım:**")
        typewriter_print("- Performans testi (site hızı, öğe sayısı, HTTP durumu)")
        typewriter_print("- Güvenlik testi (zararlı bağlantı analizi)")
        typewriter_print("- Fonksiyonellik testi (link kontrolü)")
        typewriter_print("- Web arama ve URL tarayıcı")
        typewriter_print("- Arşivleme (PDF olarak sayfa kaydı)")
        typewriter_print("- Etkileşimli DDoS simülasyonu (test amaçlı)\n")

        typewriter_print("Bot: Sadece komut verin, gerekeni hemen yapayım! 😊")

    # Konsol başlıkları getirme işlemleri koşulu
    elif  any(word in sentence for word in ["başlık", "etiket", "başlıkları getir"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        baslik_getir_cli(url)

    # Konsol linkleri getirme işlemleri koşulu
    elif  "link" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        link_getir_cli(url)

    # Konsol paragrafları getirme işlemleri koşulu
    elif "paragraf" in sentence:
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        paragraf_getir_cli(url)

    # Konsol siteyi arama işlemleri koşulu
    elif any(word in sentence for word in ["ara", "siteye git", "git"]):
        words_lower = [w.lower() for w in words]
        for i, word in enumerate(words_lower):
            if word in ["ara", "git"]:
                if i > 0:
                    keyword = ' '.join(words[:i])
                else:
                    keyword = "turkticaret"
                break
        else:
            keyword = "turkticaret"
        search_url_cli(keyword)

    # Konsol linkleri getirme işlemleri koşulu
    elif any(word in sentence for word in ["hakkında", "nedir", "hakkında bilgi", "özet"]):
        url = next(
            (word for word in words if is_valid_url(word)),
            "https://www.turkticaret.net"
        )
        ozet_al_cli(url)

    else:
        typewriter_print("Bot: Ne dediğinizi anlayamadım. Lütfen daha açık bir şekilde tekrar deneyin.")

# Yukarıdaki anahtar kelimeli if yapıyı çağıracak fonksiyon
def run_cli():
    typewriter_print("\n[-----TürkTicaret Chatbot-----]")
    typewriter_print("Çıkmak için 'çık' yazın.\n")
    typewriter_print("Bot: Merhaba! Size nasıl yardımcı olabilirim?")
    while True:
        user_input = input("Siz: ")
        # Çık demedikçe devam eden yapı
        if user_input.lower().strip() in ["çık", "exit", "quit"]:
            typewriter_print("Bot: Görüşmek üzere!")
            break
        handle_cli_request(user_input)

# Delay olan bir konsol yazımı print yapısına gecikme veriliyor
def typewriter_print(text, delay=0.02):
    for word in text:
        for char in word:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
    print()

if __name__ == "__main__":
    run_cli()
    input("\nDevam etmek için Enter tuşuna basın...")

