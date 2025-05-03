from libraries import *

def run_performance_test_cli(url):
    print(f"[TEST] Performans Testi Başlıyor: {url}")
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        response = requests.get(url)
        # Http kodları ve anlamlarını alıyoruz
        status_code = response.status_code
        status_map = {
            200: "Başarılı istek",
            201: "Kaynak oluşturuldu",
            202: "İstek kabul edildi fakat işlenmedi",
            204: "İçerik yok",
            301: "Kalıcı olarak başka adrese taşındı",
            302: "Geçici yönlendirme",
            400: "Geçersiz istek (Bad Request)",
            401: "Yetkisiz erişim (Unauthorized)",
            403: "Erişim yasaklandı (Forbidden)",
            404: "Kaynak bulunamadı",
            408: "İstek zaman aşımına uğradı",
            429: "Çok fazla istek gönderildi",
            500: "Sunucu problemi var",
            502: "Geçersiz yanıt (Bad Gateway)",
            503: "Hizmet geçici olarak kullanılamıyor",
            504: "Ağ geçidi zaman aşımı"
        }
        status_result = status_map.get(status_code, "İstek başarıyla tamamlandı")

        # Yüklenme süresi ve hesabı
        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        print(f"Sayfa Yüklenme Süresi: {load_time:.2f} saniye")

        # Burada istenen bilgiler yer almakta
        soup = BeautifulSoup(response.content, "html.parser")
        print("Site Başlığı:", soup.title.string if soup.title else "Yok")
        print("HTTP Kod:", status_code)
        print("Durum:", status_result)
        print("Formlar:", len(soup.find_all('form')))
        print("Başlıklar:", len(soup.find_all('h1')))
        print("Paragraflar:", len(soup.find_all('p')))
        print("Butonlar:", len(soup.find_all('button')))
        print("Bağlantılar:", len(soup.find_all('a')))

        driver.quit()
    except Exception as e:
        print(f"[HATA] Performans testi sırasında hata oluştu: {e}")


def run_guvenlik_test_cli(url):

    """
        Normal şekilde güvenlik testi yapılamaz selenium arayıcılığıyla ve çoğu siteyi de bu yonde kullanamayız
        çünkü bot koruması mevcut bende dolaylı yoldan site üzerinden url yi sokarak
        çeşitli güvenlik test sonuçları aldım.
    """
    print("[TEST] Güvenlik Testi Başlatılıyor...")
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.ipqualityscore.com/threat-feeds/malicious-url-scanner")
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)

        # Xpath ile beraber url girme kutusu seçiliyor
        search_input = driver.find_element(
            By.XPATH,
            '//*[@id="url"]')
        search_input.send_keys(url)
        time.sleep(2)
        search_input.send_keys(Keys.RETURN)
        time.sleep(3)

        scroll_pause_time = 1
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        final_url = driver.current_url
        # Xpath ile sonuç ekranının xpath seçiliyor ki sonuçları alabilelim.
        result_element = driver.find_element(
            By.XPATH,
            '/html/body/section[1]/div[2]/div[1]/div/div[4]')
        raw_text = result_element.get_attribute("textContent")
        cleaned_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        result_text_clean = "\n".join(cleaned_lines)

        print("Sonuç URL:", final_url)
        print("Sonuç Detayı:\n", result_text_clean)

        driver.quit()
    except Exception as e:
        print(f"[HATA] Güvenlik testi hatası: {e}")


def run_functionality_test_cli(url):
    print(f"[TEST] Fonksiyonellik Testi Başlatıldı: {url}")
    try:
        start_time = time.time()
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        # Body etiketini alıyoruz
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.TAG_NAME,
            "body")))

        # Body içindeki tüm linkler alınıyor ve yazdırılıyor.
        links = driver.find_elements(By.TAG_NAME, "a")
        total_links = len(links)
        print("Toplam link sayısı:", total_links)
        actions = ActionChains(driver)

        # Döngü ile beraber linkler gezilip geri geliniyor.
        for index, link in enumerate(links):
            try:
                href = link.get_attribute("href")
                link_text = link.text.strip()

                if href:
                    driver.execute_script("arguments[0].setAttribute('target','_self')", link)
                    actions.move_to_element(link).perform()
                    driver.execute_script(
                        "arguments[0].style.backgroundColor = 'gray'; "
                        "arguments[0].style.color = 'white';", link
                    )
                    link.click()
                    time.sleep(2)
                    current_url = driver.current_url
                    status = "Çalışıyor" if current_url != url else "Yönlendirme başarısız"
                else:
                    status = "Href yok"

            except StaleElementReferenceException:
                status = "Stale element"
            except Exception as e:
                status = f"Hata: {e}"

            # En sonda da sitenin linklerinin durumu ve test sonucu yazdırılıyor.
            print(f"[{index+1}] Link: {href} - Durum: {status}")
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.TAG_NAME,
                "body")))

        elapsed = time.time() - start_time
        print(f"Fonksiyonellik testi tamamlandı. Süre: {elapsed:.2f} saniye")
        driver.quit()
    except Exception as e:
        print(f"[HATA] Fonksiyon testi sırasında hata: {e}")

# url kontrolü yapısı
def is_valid_url(url):
    regex = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(regex, url) is not None

# Domain sorgulama fonksiyonu
def domain_sorgula_cli(keyword):
    # Domain sorgusu için en iyi site turkticaret.net kullanılıyor
    url = "https://www.turkticaret.net/domain-sorgulama"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        # Domain ismi yazılan yer bulunuyor
        input_box = driver.find_element(By.XPATH, '//*[@id="dname"]')
        input_box.clear()
        # Ardından enter tıklanıp bekleniyor sonuç çıkması için
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)
        try:
            # Domain sorgu çıkışı bulunarak xpath alınıyor ardından yapıda yazılıyor
            result_element = driver.find_element(
                By.XPATH,
                '/html/body/section[1]/div')
            print("[Domain Sorgu]:\n", result_element.text)
        except Exception:
            print("[HATA] Sonuç ekranı bulunamadı veya değişti.")
    except Exception as e:
        print(f"[HATA] Domain sorgusu başarısız: {e}")
    finally:
        # En son olarak yapıdan çıkılıyor.
        driver.quit()

# Hosting paket bilgileri getirme fonkiyonu
def hosting_paketleri_getir_cli():
    # Hosting sorgusu için yine turkticaret.net kullanıyoruz.
    url = "https://www.turkticaret.net/hosting"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        try:
            # Hosting sorgusu alanı alınarak bu alan bize yazdırılıyor
            section = driver.find_element(
                By.XPATH,
                '//*[@id="content"]/section[3]')
            print("[Hosting Paketleri]:\n", section.text)
        except Exception:
            print("[HATA] Hosting bilgileri bulunamadı veya değişti.")
    except Exception as e:
        print(f"[HATA] Hosting paket hatası: {e}")
    finally:
        # En son tarayıcı kapanıyor.
        driver.quit()

# Marka sorgulama fonksiyonu
def marka_sorgula_cli(keyword):
    # İsim hakkı sorgulama işlemi yapar
    url = "https://www.turkticaret.net/isim-hakki-sorgulama"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(2)
        # Marka sorgulama alanının xpath üzerinden alır.
        input_box = driver.find_element(
            By.XPATH,
            '//*[@id="mark_name"]')
        input_box.clear()

        # Enter tıklayarak giriş yapar
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.RETURN)
        time.sleep(5)
        try:
            # Sonuç ekranının xpath alır
            result_element = driver.find_element(
                By.XPATH,
                '/html/body/div[6]/div[1]/div[2]/div[1]/div/div/div/div/div/div/div')
            print("[Marka/İsim Hakkı]:\n", result_element.text)
        except Exception:
            print("[HATA] Sonuç bulunamadı veya sayfa değişmiş olabilir.")
    except Exception as e:
        print(f"[HATA] Marka sorgusu hatası: {e}")
    finally:
        driver.quit()


def web_paket_getir_cli():
    # Web sitesi paketleri paketlerini getirme işlemi
    url = "https://www.turkticaret.net/hazir-web-sitesi"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        try:
            # Web paketleri yapısını xpath ile alıyoruz
            section = driver.find_element(By.XPATH, '//*[@id="paketler"]')
            print("[Hazır Web Siteleri]:\n", section.text)
        except Exception:
            print("[HATA] Paketler bölgesi bulunamadı veya değişti.")
    except Exception as e:
        print(f"[HATA] Hazır site hatası: {e}")
    finally:
        driver.quit()


def e_posta_getir_cli():
    # e posta paketleri getiriliyor
    url = "https://www.turkticaret.net/kurumsal-e-posta"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        try:
            # e posta paketleri seçilerek getiriliyor
            element = driver.find_element(
                By.XPATH,
                '//*[@id="content"]/section[3]/div/div/div/div/div[2]/div[1]/div')
            print("[E-Posta Paketleri]:\n", element.text)
        except Exception:
            print("[HATA] E-posta bilgileri bulunamadı.")
    except Exception as e:
        print(f"[HATA] E-posta hatası: {e}")
    finally:
        driver.quit()


def sunucu_paket_cli():
    # sunucu paketleri getiriliyor
    url = "https://www.turkticaret.net/server-sunucu"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        try:
            # Sunucu paketleri bölümü alınıyor
            element = driver.find_element(
                By.XPATH,
                '//*[@id="content"]/div[2]')
            print("[Sunucu Paketleri]:\n", element.text)
        except Exception:
            print("[HATA] Sunucu paketleri bulunamadı.")
    except Exception as e:
        print(f"[HATA] Sunucu paket hatası: {e}")
    finally:
        driver.quit()


def yorumlari_getir_cli():
    # Sitedeki yorumlar bölümleri getiriliyor
    url = "https://www.turkticaret.net/musteri-yorumlari"
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(10)
        time.sleep(3)
        try:
            # Yorumların olduğu xpath seçiliyor
            element = driver.find_element(
                By.XPATH,
                '/html/body/div[6]')
            print("[Müşteri Yorumları]:\n", element.text)
        except Exception:
            print("[HATA] Yorumlar bölümü bulunamadı veya değişti.")
    except Exception as e:
        print(f"[HATA] Yorum çekme hatası: {e}")
    finally:
        driver.quit()

def search_url_cli(query):
    """
    CLI ortamı için web araması yapar ve gezilen URL'leri terminale yazdırır.
    """
    if not query.startswith("http"):
        query = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    window = webview.create_window("Search Result", query)

    def track_url():
        current_url = None
        while True:
            try:
                new_url = window.get_current_url()
                if new_url != current_url and new_url is not None:
                    current_url = new_url
                    if "https://www.google.com/search" not in current_url:
                        typewriter_print(f"Ziyaret edilen URL: {current_url}")
                time.sleep(1)
            except Exception as e:
                typewriter_print(f"[HATA] URL takibi sırasında hata: {e}")
                break

    threading.Thread(target=track_url, daemon=True).start()
    webview.start()

def search_url_cli(query):
    """
    CLI ortamı için web araması yapar ve gezilen URL'leri terminale yazdırır.
    """
    if not query.startswith("http"):
        query = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

    window = webview.create_window("Search Result", query)

    def track_url():
        current_url = None
        while True:
            try:
                new_url = window.get_current_url()
                if new_url != current_url and new_url is not None:
                    current_url = new_url
                    if "https://www.google.com/search" not in current_url:
                        typewriter_print(f"Ziyaret edilen URL: {current_url}")
                time.sleep(1)
            except Exception as e:
                typewriter_print(f"[HATA] URL takibi sırasında hata: {e}")
                break

    threading.Thread(target=track_url, daemon=True).start()
    webview.start()

def baslik_getir_cli(url):
    # Yapı olarak soup ile baslıkları çekip yazdırıyoruz, bu yapı yazılan JSON’ları hatırlıyor.
    # Eğer ziyaret edilmişse bir daha girip tekrar yazdırmıyor.
    # JSON klasörü yoksa oluştur
    print(f"[i] {url} adresinden başlıklar getiriliyor...")

    json_path = "jsons/basliklar.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # Daha önce çekilmişse yazdır
    if domain in data:
        print(f"{domain} için önceden alınmış başlıklar:")
        for tag, içerikler in data[domain].items():
            if içerikler:
                print(f" {tag.upper()} etiketleri:")
                for item in içerikler:
                    print(f"   - {item}")
        return

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        basliklar = {
            "title": [soup.title.string.strip()] if soup.title else []
        }
        for i in range(1, 7):
            etiket = f"h{i}"
            basliklar[etiket] = [
                tag.get_text(strip=True) for tag in soup.find_all(etiket)
            ]

        data[domain] = basliklar
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"{domain} için başlıklar alındı:")
        for tag, içerikler in basliklar.items():
            if içerikler:
                print(f" {tag.upper()} etiketleri:")
                for item in içerikler:
                    print(f"   - {item}")

    except Exception as e:
        typewriter_print(f"[HATA] Başlıklar alınamadı: {e}")

    finally:
        driver.quit()

def paragraf_getir_cli(url):
    # Yapı olarak soup ile paragrafları çekip yazdırıyoruz. Bu yapı yazılan JSON’ları hatırlıyor.
    # Eğer ziyaret edilmişse bir daha girip tekrar yazdırmıyor.
    # JSON klasörü yoksa oluştur
    print(f"[i] {url} adresinden paragraflar getiriliyor...")

    json_path = "jsons/paragraflar.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    if domain in data:
        print(f"{domain} için önceden alınmış paragraflar:")
        for i, paragraf in enumerate(data[domain], 1):
            print(f"  p{i}: {paragraf}")
        return

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        paragraflar = [
            p.get_text(strip=True) for p in soup.find_all("p")
            if p.get_text(strip=True)
        ]

        data[domain] = paragraflar
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"{domain} için {len(paragraflar)} paragraf alındı:")
        for i, paragraf in enumerate(paragraflar, 1):
            print(f"  p{i}: {paragraf}")

    except Exception as e:
        print(f"[HATA] Paragraflar alınamadı: {e}")

    finally:
        driver.quit()

def link_getir_cli(url):
    # Yapı olarak soup ile linkleri çekip yazdırıyoruz. Bu yapı yazılan JSON’ları hatırlıyor.
    # Eğer ziyaret edilmişse bir daha girip tekrar yazdırmıyor.
    # JSON klasörü yoksa oluştur
    print(f"[i] {url} adresinden linkler getiriliyor...")

    json_path = "jsons/linkler.json"
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    domain = urlparse(url).netloc.replace("www.", "")

    # JSON yükle veya oluştur
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    if domain in data:
        print(f"{domain} için önceden alınmış linkler:")
        print(f"  Kaynak URL: {data[domain].get('url', 'bilinmiyor')}")
        for i, item in enumerate(data[domain].get("linkler", []), 1):
            print(f"  a{i}: {item['metin']} = {item['href']}")
        return

    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        linkler = []
        for a in soup.find_all("a", href=True):
            metin = a.get_text(strip=True) or "(metin yok)"
            href = a["href"].strip()
            if href:
                linkler.append({"metin": metin, "href": href})

        data[domain] = {
            "url": url,
            "linkler": linkler
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"{domain} için {len(linkler)} link alındı:")
        print(f"  Kaynak URL: {url}")
        for i, item in enumerate(linkler, 1):
            print(f"  a{i}: {item['metin']} = {item['href']}")

    except Exception as e:
        print(f"[HATA] Linkler alınamadı: {e}")

    finally:
        driver.quit()

# Konsol özet alma yapısı
def ozet_al_cli(url):

    # Buradaki yapı meta etiketlerini çekerek site hakkında özet yapı oluşturmaktadır.
    try:
        typewriter_print(" : Tarayıcı başlatılıyor...")

        options = Options()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Sitenin içeriklerinin alındığı bilgisi selenium tarayıcısı acılınca ortaya cıkmakta
        typewriter_print(" : Web sitesi açıldı, içerik analiz ediliyor...")

        time.sleep(2)

        # bs ile beraber html verileri çekilmekte
        soup = BeautifulSoup(driver.page_source, "html.parser")

        typewriter_print(" : Meta veriler toplanıyor...")

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

        typewriter_print(" : " + output)

    except Exception as e:
        typewriter_print(f" : Site bilgisi alınamadı. Hata: {str(e)}")

# Delay olan bir konsol yazımı print yapısına gecikme veriliyor
def typewriter_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()