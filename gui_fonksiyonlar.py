from libraries import *

# Başlık ekleme fonksiyonu
def baslik(frame, text, bg, fg, fw, side, px):
    label = tk.Label(
        frame,
        text=text,
        font=("Arial", fw, "bold"),
        bg=bg,
        fg=fg,
        anchor="center"
    )
    label.pack(pady=10, padx=px, side=side)

# Radio Buton Ekleme Fonksiyonu
def add_radio_button(frame, text, value, row, column, bg, fg):
    radio_button = tk.Radiobutton(
        frame,
        text=text,
        value=value,
        bg=bg,
        fg=fg,
        anchor="center",
        justify="center",
        font=("Arial", 12, "bold"),
        width=10
    )
    radio_button.grid(row=row, column=column, sticky="w", padx=5, pady=6)

# Buton Ekleme Fonksiyonu
def add_button(frame, text, command, row, column, bg, fg):
    button = tk.Button(
        frame,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        width=7,
        height=1
    )
    button.grid(row=row, column=column, padx=15, pady=2)

# Sonuçları kaydetme fonksiyonu
def save_result(result_text):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(result_text.get("1.0", tk.END))

# Sonuçları temizleme fonksiyonu
def clear_results(result_text):
    result_text.delete("1.0", tk.END)

# Domain sorgulama fonksiyonu
def domain_sorgula(keyword, result_text=None, bot_logo=None):
    # Domain sorgusu için en iyi site turkticaret.net kullanılıyor
    url = "https://www.turkticaret.net/domain-sorgulama"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)

        # Domain giriş kutusu seçiliyor xpath ile beraber
        input_box = driver.find_element(By.XPATH, '//*[@id="dname"]')
        input_box.clear()
        # Yazıldıktan sonra enter basılıyor
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)
        # Sonuç ekranını alma ve yazdırma işlemleri
        try:
            result_element = driver.find_element(By.XPATH, '/html/body/section[1]/div')
            result_text_content = result_element.text
        except Exception:
            result_text_content = "Sonuç ekranı bulunamadı veya değişti."

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Domain Sorgu Sonucu:\n{result_text_content}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Domain sorgu sonucu:\n{result_text_content}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end", f" : Sorgulama sırasında hata oluştu: {str(e)}\n"
            )
            result_text.see("end")
        print(f"Sorgulama hatası: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Hosting paketlerin getirme fonksiyonu
def hosting_paketleri_getir(result_text=None, bot_logo=None):
    # Hosting paketlerin listesi için en iyi site seçiliyor
    url = "https://www.turkticaret.net/hosting"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)

        try:
            # Hosting yapılarının olduğu kısım seçiliyor xpath
            hosting_section = driver.find_element(
                By.XPATH, '//*[@id="content"]/section[3]'
            )
            # Textleri alınıyor ve yazdırılıyor
            hosting_text = hosting_section.text
        except Exception:
            hosting_text = "Hosting bilgileri bulunamadı veya değişti."

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Hosting Paketleri:\n{hosting_text}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Hosting paketleri:\n{hosting_text}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end", f" : Hosting bilgisi alınamadı. Hata: {str(e)}\n"
            )
            result_text.see("end")
        print(f"Hosting sorgulama hatası: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Marka sorgulama fonksiyonu
def marka_sorgula(keyword, result_text=None, bot_logo=None):
    # Verilen anahtara göre marka sorgulama yapılıyor
    url = "https://www.turkticaret.net/isim-hakki-sorgulama"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(2)

        # Marka sorgulama alanının xpath ile seçiliyor
        input_box = driver.find_element(By.XPATH, '//*[@id="mark_name"]')
        input_box.clear()
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            # Çıkan sonuçların kısmı xpath ile alınıyor ve sonuçlar yazdırılıyor
            result_element = driver.find_element(
                By.XPATH,
                '/html/body/div[6]/div[1]/div[2]/div[1]/div/div/div/div/div/div/div'
            )
            result_text_content = result_element.text
        except Exception:
            result_text_content = "Sonuç bulunamadı veya sayfa değişmiş olabilir."

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Marka/İsim Hakkı Sorgu Sonucu:\n{result_text_content}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Marka sorgu sonucu:\n{result_text_content}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end", f" : Sorgulama sırasında hata oluştu: {str(e)}\n"
            )
            result_text.see("end")
        print(f"Sorgulama hatası: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Web paketleri getirme fonksiyonu
def web_paket_getir(result_text=None, bot_logo=None):
    # Hazır web sitesi paketleri getiriliyor
    url = "https://www.turkticaret.net/hazir-web-sitesi"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        # Paketlerin olduğu kısım alınıyor ve textleri ekranda yazdırılıyor
        try:
            paketler_section = driver.find_element(By.XPATH, '//*[@id="paketler"]')
            paketler_text = paketler_section.text
        except Exception:
            paketler_text = "Web sitesi paketleri bulunamadı veya sayfa değişmiş."

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Hazır Web Sitesi Paketleri:\n{paketler_text}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Hazır Web Sitesi Paketleri:\n{paketler_text}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end",
                f" : Web sitesi paketleri alınamadı. Hata: {str(e)}\n"
            )
            result_text.see("end")
        print(f"Hazır Web Sitesi paket sorgulama hatası: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# E posta hizmetlerini getirme fonksiyonları
def e_posta_getir(result_text=None, bot_logo=None):
    # Kurumsal eposta hizmetleri için en iyi firmaya gidiliyor
    url = "https://www.turkticaret.net/kurumsal-e-posta"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        driver.implicitly_wait(10)
        time.sleep(3)

        try:
            # Eposta elemanlarının xpath alır ve textini yazdırır
            eposta_element = driver.find_element(
                By.XPATH,
                '//*[@id="content"]/section[3]/div/div/div/div/div[2]/div[1]/div'
            )
            eposta_text = eposta_element.text
        except Exception:
            eposta_text = "Kurumsal e-posta paketleri bulunamadı."

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Kurumsal E-Posta Paketleri:\n{eposta_text}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Kurumsal e-posta paketleri:\n{eposta_text}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end",
                f" : Kurumsal e-posta paketleri alınamadı. Hata: {str(e)}\n"
            )
            result_text.see("end")
        print(f"Hata: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Sunucu paketlerini getiren fonksiyon
def sunucu_paket(result_text=None, bot_logo=None):
    # Sunucu paket listesi için en iyi siteye gidiliyor
    url = "https://www.turkticaret.net/server-sunucu"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        driver.implicitly_wait(10)
        time.sleep(3)

        try:
            # Sunucuların elemanlarının text alınıyor ve yazdırılıyor
            server_element = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]')
            server_text = server_element.text
        except Exception:
            server_text = (
                "Server/Sunucu paketleri bulunamadı veya XPath değişmiş olabilir."
            )

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="brown", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Server/Sunucu Paketleri:\n{server_text}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Server/Sunucu paketleri:\n{server_text}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end",
                f" : Server/Sunucu paket bilgisi alınamadı. Hata: {str(e)}\n",
                "bot"
            )
            result_text.see("end")
        print(f"Hata: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Sitelerin yorumları getiren fonksiyon
def yorumları_getir(result_text=None, bot_logo=None):
    url = "https://www.turkticaret.net/musteri-yorumlari"
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        driver.implicitly_wait(10)
        time.sleep(3)

        try:
            # Yorumların olduğu kısımın xpath seçilip text alınıp yazdırılıyor
            yorumlar_element = driver.find_element(By.XPATH, '/html/body/div[6]')
            yorumlar_text = yorumlar_element.text
        except Exception:
            yorumlar_text = (
                "Müşteri yorumları bulunamadı veya XPath değişmiş olabilir."
            )

        if result_text:
            result_text.tag_configure(
                "bot", justify="left", foreground="red", font=("Arial", 12)
            )
            if bot_logo:
                result_text.image_create("end", image=bot_logo)
            result_text.insert(
                "end",
                f" : Müşteri Yorumları:\n{yorumlar_text}\n",
                "bot"
            )
            result_text.see("end")

        print(f"Müşteri yorumları:\n{yorumlar_text}")

    except Exception as e:
        if result_text:
            result_text.insert(
                "end",
                f" : Müşteri yorumları alınamadı. Hata: {str(e)}\n",
                "bot"
            )
            result_text.see("end")
        print(f"Hata: {str(e)}")

    finally:
        driver.quit()
        print("Tarayıcı kapatıldı.")

# Siteyi kaydeden fonksiyon
def kaydet_site(url, result_text=None, bot_logo=None):
    from urllib.parse import urlparse, urljoin
    from selenium.webdriver.chrome.options import Options
    import os
    import requests
    from bs4 import BeautifulSoup

    # Dosya kayıt yerlerini ayarlayıp ardından adrese gidip içerikleri indiriyor
    # Bu fonksiyon uzun süren işlemlere sahip olduğundan tavsiye edilmez kullanmayı
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    save_folder = os.path.join("save", domain)

    # OS ile kaydetme işlemi
    os.makedirs(save_folder, exist_ok=True)

    # Dosya analiz bilgisi veriliyor
    if result_text:
        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        if bot_logo:
            result_text.image_create("end", image=bot_logo)
        result_text.insert(
            "end",
            f" : '{url}' adresindeki site analiz ediliyor ve dosyalar indiriliyor.\n",
            "bot"
        )
        result_text.see("end")

    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        html = driver.page_source
        html_path = os.path.join(save_folder, "index.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        soup = BeautifulSoup(html, "html.parser")
        static_tags = {
            "link": "href",
            "script": "src",
            "img": "src"
        }

        # Yüklenen dosya bilgisi değişken içerisinde yer alıyor
        downloaded_files = 0

        for tag, attr in static_tags.items():
            elements = soup.find_all(tag)
            for elem in elements:
                resource_url = elem.get(attr)
                if resource_url:
                    full_url = urljoin(url, resource_url)
                    try:
                        response = requests.get(full_url, timeout=5)
                        if response.status_code == 200:
                            filename = os.path.basename(urlparse(full_url).path)
                            if not filename:
                                continue
                            local_path = os.path.join(save_folder, filename)
                            with open(local_path, "wb") as f:
                                f.write(response.content)
                            downloaded_files += 1
                    except Exception:
                        continue

        driver.quit()

        if result_text:
            result_text.insert(
                "end",
                f" : Site içeriği ve {downloaded_files} adet dosya indirildi.\n"
                f"   'save/{domain}' klasörüne başarıyla kaydedildi.\n",
                "bot"
            )
            result_text.see("end")

    except Exception as e:
        if result_text:
            result_text.insert("end", f" : Hata oluştu: {str(e)}\n", "bot")
            result_text.see("end")

# Özet bilgileri meta etiketinden çekme fonksiyonu
def ozet_al(url, result_text=None, bot_logo=None):
    # Buradaki yapı meta etiketlerini çekerek site hakkında özet yapı oluşturmaktadır.
    try:
        if result_text:
            result_text.insert(tk.END, " : Tarayıcı açılıyor...\n", "bot")
            result_text.see(tk.END)

        options = Options()
        options.add_argument("--start-maximized")  # gerçek tarayıcı hissi
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Sitenin içeriklerinin alındığı bilgisi selenium tarayıcısı acılınca ortaya cıkmakta
        if result_text:
            result_text.insert(tk.END, " : Web sitesi açıldı, içerik analiz ediliyor...\n", "bot")
            result_text.see(tk.END)

        time.sleep(2)

        # bs ile beraber html verileri çekilmekte
        soup = BeautifulSoup(driver.page_source, "html.parser")

        if result_text:
            result_text.insert(tk.END, " : Meta veriler toplanıyor...\n", "bot")
            result_text.see(tk.END)

        driver.quit()

        domain = urlparse(url).netloc.replace("www.", "")

        # meta etiketleri alınmakta
        def get_meta(*keys):
            for key in keys:
                tag = soup.find("meta", attrs={**key})
                if tag and tag.get("content"):
                    return tag["content"].strip()
            return None

        # Ardından meta etiketlerinin yapıları birbirinden ayrılmakta
        title = soup.title.string.strip() if soup.title else domain
        description = get_meta({"name": "description"}, {"property": "og:description"})
        keywords = get_meta({"name": "keywords"})
        site_name = get_meta({"property": "og:site_name"})
        publish_time = get_meta({"property": "article:published_time"})
        canonical = soup.find("link", rel="canonical")
        canonical_url = canonical["href"] if canonical and canonical.has_attr("href") else url

        h1 = soup.find("h1")
        h1_text = h1.text.strip() if h1 else None

        json_ld = soup.find("script", type="application/ld+json")
        if json_ld:
            try:
                json_data = json.loads(json_ld.string)
                if isinstance(json_data, dict):
                    site_name = site_name or json_data.get("name")
                    publish_time = publish_time or json_data.get("foundingDate")
            except Exception:
                pass

        # Açıklama çıktısı
        output = f"{site_name or title}, {domain} adresinde yayın yapan bir web sitesidir.\n"

        # Meta içerikleri doluysa ekleme yap acıklamaya
        if description:
            output += f" Sitenin açıklaması olarak {description}\n"
        elif h1_text:
            output += f"Genel olarak: {h1_text}\n"

        if publish_time:
            output += f"Yayın başlangıç yılı: {publish_time[:4]}.\n"

        if keywords:
            output += f"İlgili konular: {keywords}.\n"

        output += f"Ziyaret etmek için: {canonical_url}\n"

        if result_text:
            result_text.insert("end", f" : {output}\n", "bot")
            result_text.see("end")

    except Exception as e:
        if result_text:
            result_text.insert("end", f" : Site bilgisi alınamadı. Hata: {str(e)}\n", "bot")
            result_text.see("end")

# Başlık etiketlerini getirip kaydeden fonksiyon
def baslik_getir(url, result_text=None, bot_logo=None, json_path="jsons/basliklar.json"):
    # Yapı olarak soup ile baslıkları cekip yazdırıyoruz bu yapı yazılan jsonları hatırlıyor
    # Eğer ziyaret edilmis ise birdaha girip tekrar yazdırmıyor
    # JSON klasörü yoksa oluştur
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Daha önce varsa JSON'dan oku ve yazdır
    if domain in data:
        if result_text:
            result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
            if bot_logo:
                result_text.image_create(tk.END, image=bot_logo)
            result_text.insert(tk.END, f" : {domain} için kayıtlı başlıklar bulundu:\n", "bot")
            for tag in ["title", "h1", "h2", "h3", "h4", "h5", "h6"]:
                içerikler = data[domain].get(tag, [])
                if içerikler:
                    result_text.insert(tk.END, f" {tag.upper()} etiketleri:\n", "bot")
                    for item in içerikler:
                        result_text.insert(tk.END, f"    - {item}\n", "bot")
            result_text.see(tk.END)
        return

    # Analiz başladığında yazan yazı
    if result_text:
        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        if bot_logo:
            result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(tk.END, f" : {domain} için başlıklar çekiliyor, tarayıcı açılıyor...\n", "bot")
        result_text.see(tk.END)

    # Selenium ayarları
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", False)
    # options.add_argument("--headless")  # bu aktif edilirse tarayıcı görünmez

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Başlık verilerini çıkarıyoruz soup ile beraber
        basliklar = {
            "title": [soup.title.string.strip()] if soup.title else []
        }
        for i in range(1, 7):
            etiket = f"h{i}"
            basliklar[etiket] = [tag.get_text(strip=True) for tag in soup.find_all(etiket)]

        # JSON'a kaydet
        data[domain] = basliklar
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Result text yazdır
        if result_text:
            result_text.insert(tk.END, f" : {domain} için başlıklar başarıyla alındı:\n", "bot")
            for tag in ["title", "h1", "h2", "h3", "h4", "h5", "h6"]:
                içerikler = basliklar.get(tag, [])
                if içerikler:
                    result_text.insert(tk.END, f"  {tag.upper()} etiketleri:\n", "bot")
                    for item in içerikler:
                        result_text.insert(tk.END, f"    - {item}\n", "bot")
            result_text.see(tk.END)

    except Exception as e:
        if result_text:
            result_text.insert(tk.END, f" : Başlıklar alınamadı. Hata: {str(e)}\n", "bot")
            result_text.see(tk.END)

    finally:
        driver.quit()

# Paragraf etiketlerini getirip kaydeden fonksiyon
def paragraf_getir(url, result_text=None, bot_logo=None, json_path="jsons/paragraflar.json"):
    # Yapı olarak soup ile paragrafları çekip yazdırıyoruz. Bu yapı yazılan jsonları hatırlıyor.
    # Eğer ziyaret edilmiş ise bir daha girip tekrar yazdırmıyor.
    # JSON klasörü yoksa oluştur
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Daha önce varsa JSON'dan oku ve yazdır
    if domain in data:
        if result_text:
            result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
            if bot_logo:
                result_text.image_create(tk.END, image=bot_logo)
            result_text.insert(tk.END, f" : {domain} için kayıtlı paragraflar bulundu:\n", "bot")
            for i, paragraf in enumerate(data[domain], 1):
                result_text.insert(tk.END, f"  p{i}: {paragraf}\n", "bot")
            result_text.see(tk.END)
        return

    # Analiz başladığında yazan yazı
    if result_text:
        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        if bot_logo:
            result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(tk.END, f" : {domain} için paragraflar çekiliyor, tarayıcı açılıyor...\n", "bot")
        result_text.see(tk.END)

    # Selenium ayarları
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", False)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Paragraf verilerini çıkarıyoruz soup ile beraber
        paragraflar = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]

        # JSON'a kaydet
        data[domain] = paragraflar
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Result text'e yazdır
        if result_text:
            result_text.insert(tk.END, f" : {domain} için {len(paragraflar)} paragraf başarıyla alındı:\n", "bot")
            for i, paragraf in enumerate(paragraflar, 1):
                result_text.insert(tk.END, f"  p{i}: {paragraf}\n", "bot")
            result_text.see(tk.END)

    except Exception as e:
        if result_text:
            result_text.insert(tk.END, f" : Paragraflar alınamadı. Hata: {str(e)}\n", "bot")
            result_text.see(tk.END)

    finally:
        driver.quit()

# Link (a etiketlerini) getirip kaydeden fonksiyon
def link_getir(url, result_text=None, bot_logo=None, json_path="jsons/linkler.json"):
    # Yapı olarak soup ile linkleri çekip yazdırıyoruz. Bu yapı yazılan jsonları hatırlıyor.
    # Eğer ziyaret edilmiş ise bir daha girip tekrar yazdırmıyor.
    # JSON klasörü yoksa oluştur
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Daha önce varsa JSON'dan oku ve yazdır
    if domain in data:
        if result_text:
            result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
            if bot_logo:
                result_text.image_create(tk.END, image=bot_logo)
            result_text.insert(tk.END, f" : {domain} için kayıtlı linkler bulundu:\n", "bot")
            result_text.insert(tk.END, f"  Kaynak URL: {data[domain].get('url', 'bilinmiyor')}\n", "bot")
            for i, item in enumerate(data[domain].get("linkler", []), 1):
                result_text.insert(tk.END, f"  a{i}: {item['metin']} = {item['href']}\n", "bot")
            result_text.see(tk.END)
        return

    # Analiz başladığında yazan yazı
    if result_text:
        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        if bot_logo:
            result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(tk.END, f" : {domain} için linkler çekiliyor, tarayıcı açılıyor...\n", "bot")
        result_text.see(tk.END)

    # Selenium ayarları
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", False)
    # options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Link verilerini çıkarıyoruz soup ile beraber
        linkler = []
        for a in soup.find_all("a", href=True):
            metin = a.get_text(strip=True) or "(metin yok)"
            href = a['href'].strip()
            if href:
                linkler.append({
                    "metin": metin,
                    "href": href
                })

        # JSON'a kaydet
        data[domain] = {
            "url": url,
            "linkler": linkler
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Result text'e yazdır
        if result_text:
            result_text.insert(tk.END, f" : {domain} için {len(linkler)} link başarıyla alındı:\n", "bot")
            result_text.insert(tk.END, f"  Kaynak URL: {url}\n", "bot")
            for i, item in enumerate(linkler, 1):
                result_text.insert(tk.END, f"  a{i}: {item['metin']} {item['href']}\n", "bot")
            result_text.see(tk.END)

    except Exception as e:
        if result_text:
            result_text.insert(tk.END, f" : Linkler alınamadı. Hata: {str(e)}\n", "bot")
            result_text.see(tk.END)

    finally:
        driver.quit()

# Etiket getirme işlemleri hep aynı tekrar yaptıgından bu yapı icin en iyi olarak tek fonksiyon yaratma yapılabilir.
# Ama yaptıgım yapıyı bozmak hic istemem
# Kullanmak icin:
# etiket_getir(url, ["title", "h1", "h2", "h3", "h4", "h5", "h6"], "jsons/basliklar.json", result_text, bot_logo)
def etiket_getir(url, etiketler, json_path, result_text=None, bot_logo=None, link_mi=False):
    # JSON klasörü yoksa oluştur
    os.makedirs(os.path.dirname(json_path), exist_ok=True)

    domain = urlparse(url).netloc.replace("www.", "")

    # JSON'u yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Daha önce kayıtlıysa yazdır ve çık
    if domain in data:
        if result_text:
            result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
            if bot_logo:
                result_text.image_create(tk.END, image=bot_logo)

            result_text.insert(tk.END, f" : {domain} için kayıtlı içerik bulundu:\n", "bot")
            if link_mi:
                result_text.insert(tk.END, f"  Kaynak URL: {data[domain].get('url', 'bilinmiyor')}\n", "bot")
                for i, item in enumerate(data[domain].get("linkler", []), 1):
                    result_text.insert(tk.END, f"  a{i}: {item['metin']} = {item['href']}\n", "bot")
            else:
                for tag in etiketler:
                    içerikler = data[domain].get(tag, [])
                    if içerikler:
                        result_text.insert(tk.END, f"  {tag.upper()} etiketleri:\n", "bot")
                        for i, item in enumerate(içerikler, 1):
                            result_text.insert(tk.END, f"    - {item}\n", "bot")
            result_text.see(tk.END)
        return

    # Bilgilendirme mesajı
    if result_text:
        result_text.tag_configure("bot", justify="left", foreground="red", font=("Arial", 12))
        if bot_logo:
            result_text.image_create(tk.END, image=bot_logo)
        result_text.insert(tk.END, f" : {domain} için içerik çekiliyor, tarayıcı açılıyor...\n", "bot")
        result_text.see(tk.END)

    # Selenium ayarları
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        if link_mi:
            linkler = []
            for a in soup.find_all("a", href=True):
                metin = a.get_text(strip=True) or "(metin yok)"
                href = a['href'].strip()
                if href:
                    linkler.append({"metin": metin, "href": href})
            data[domain] = {"url": url, "linkler": linkler}
        else:
            içerik = {}
            for etiket in etiketler:
                if etiket == "title":
                    içerik["title"] = [soup.title.string.strip()] if soup.title else []
                else:
                    içerik[etiket] = [tag.get_text(strip=True) for tag in soup.find_all(etiket)]
            data[domain] = içerik

        # JSON'a yaz
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Ekrana yazdır
        if result_text:
            result_text.insert(tk.END, f" : {domain} için içerik başarıyla alındı:\n", "bot")
            if link_mi:
                result_text.insert(tk.END, f"  Kaynak URL: {url}\n", "bot")
                for i, item in enumerate(linkler, 1):
                    result_text.insert(tk.END, f"  a{i}: {item['metin']} {item['href']}\n", "bot")
            else:
                for tag in etiketler:
                    içerikler = data[domain].get(tag, [])
                    if içerikler:
                        result_text.insert(tk.END, f"  {tag.upper()} etiketleri:\n", "bot")
                        for i, item in enumerate(içerikler, 1):
                            result_text.insert(tk.END, f"    - {item}\n", "bot")
            result_text.see(tk.END)

    except Exception as e:
        if result_text:
            result_text.insert(tk.END, f" : İçerik alınamadı. Hata: {str(e)}\n", "bot")
            result_text.see(tk.END)

    finally:
        driver.quit()







