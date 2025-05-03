from libraries import *

def run_performance_test(url,  result_text):
    """
    Bu test yapısında site yüklenme süresi, HTTP kodu ve HTML öğe sayımları yapılır.
    """
    result_text.insert(tk.END, f"Performans Testi Başlıyor: {url}\n")
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        # Http kodları alınıyor ve anlamları listeleniyor
        response = requests.get(url)
        status_code = response.status_code

        http_status_descriptions = {
            100: "Devam et (Continue)",
            200: "İstek başarıyla tamamlandı",
            201: "Kaynak oluşturuldu",
            204: "İçerik yok",
            301: "Kalıcı olarak başka adrese taşındı",
            302: "Geçici olarak başka adrese taşındı",
            304: "Değişiklik yok",
            400: "Geçersiz istek",
            401: "Yetkilendirme gerekli",
            403: "Erişim yasaklandı",
            404: "Kaynak bulunamadı",
            408: "İstek zaman aşımına uğradı",
            429: "Çok fazla istek gönderildi",
            500: "Sunucu problemi var",
            502: "Geçersiz ağ geçidi",
            503: "Sunucu hizmet veremiyor",
        }

        status_result = http_status_descriptions.get(status_code, "Bilinmeyen HTTP durumu")

        start_time = time.time()
        driver.get(url)
        load_time = time.time() - start_time
        result_text.insert(tk.END, f"Sayfa Yüklenme Süre: {load_time:.2f} saniye\n")

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Performans testi sonucunu yazdırma yapıyor
        site_title = soup.title.string if soup.title else "Site Başlığı Yok"
        result_text.insert(tk.END, f"Site Başlığı: {site_title}\n")
        result_text.insert(tk.END, f"HTTP Durum Kodu: {status_code}\n")
        result_text.insert(tk.END, f"HTTP Anlamı: {status_result}\n")
        result_text.insert(tk.END, f"Form Sayısı: {len(soup.find_all('form'))}\n")
        result_text.insert(tk.END, f"Başlık (h1) Sayısı: {len(soup.find_all('h1'))}\n")
        result_text.insert(tk.END, f"Paragraf (p) Sayısı: {len(soup.find_all('p'))}\n")
        result_text.insert(tk.END, f"Buton Sayısı: {len(soup.find_all('button'))}\n")
        result_text.insert(tk.END, f"Link (a) Sayısı: {len(soup.find_all('a'))}\n")

        time.sleep(1)
        driver.quit()
    except Exception as e:
        result_text.insert(tk.END, f"Hata: {str(e)}\n")
        result_text.update_idletasks()


def run_guvenlik_test(url, result_text):
    """
     Bu test verilen url icin güvenlik testini selenium ile dolaylı yoldan
     bir sitedeki web url testi işlemlerini yapıyor
    """
    result_text.insert(tk.END, "Güvenlik testi başlatılıyor...\n")

    try:
        driver = webdriver.Chrome()

        # IPQualityScore sitesini aç
        ipquality_url = "https://www.ipqualityscore.com/threat-feeds/malicious-url-scanner"
        driver.get(ipquality_url)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(2)

        # URL alanına kullanıcı URL'sini gir
        search_input = driver.find_element(
            By.XPATH,
            '//*[@id="url"]')
        time.sleep(1)
        search_input.send_keys(url)
        time.sleep(2)
        search_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Sayfanın tamamen yüklenmesini bekle
        scroll_pause_time = 1
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Sonuçları al
        final_url = driver.current_url
        result_element = driver.find_element(
            By.XPATH,
            '/html/body/section[1]/div[2]/div[1]/div/div[4]'
        )

        raw_text = result_element.get_attribute("textContent")
        cleaned_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        result_text_clean = "\n".join(cleaned_lines)

        # Sonuçları GUI'ye yazdır
        result_text.insert(tk.END, f"Result URL: {final_url}\n")
        result_text.insert(tk.END, f"Sonuç Detayı:\n{result_text_clean}\n")

        driver.quit()

    except Exception as e:
        result_text.insert(tk.END, f"Hata oluştu: {e}\n")

def run_functionality_test(url, result_text):
    """
    Bu test ile verilen url üzerindeki tüm yapılar taranarak ve sonrasında verilen
    url dönülererek bize fonksiyonal olarak linklerin çalışılabilirlik testi yapar
    """
    result_text.insert(tk.END, f"Fonksiyon testi başlatıldı: {url}\n")

    start_time = time.time()

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    WebDriverWait(driver, 10).until(
        # Body kısmını seçeriz
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Link elemanlarını seçeriz
    links = driver.find_elements(By.TAG_NAME, "a")
    total_links = len(links)
    result_text.insert(tk.END, f"Toplam link sayısı: {total_links}\n")

    actions = ActionChains(driver)
    results = []

    for index in range(total_links):
        try:
            links = driver.find_elements(By.TAG_NAME, "a")
            link = links[index]
            link_text = link.text.strip()
            href = link.get_attribute("href")

            if href:
                # Farklı sekmeye gidişi engelleme işlemi
                driver.execute_script(
                    "arguments[0].setAttribute('target','_self')", link
                )

                actions.move_to_element(link).perform()
                time.sleep(1)

                # Takip için gezinilen linklerin arkaplan rengini gri yaparız
                driver.execute_script(
                    "arguments[0].style.backgroundColor = 'gray';"
                    "arguments[0].style.color = 'white';", link
                )

                try:
                    link.click()
                    time.sleep(2)
                except WebDriverException:
                    status = "Tıklama hatası: Link açılamadı"
                    continue

                # Varolan url alınarak işlem tamamlanır
                current_url = driver.current_url
                status = "Çalışıyor" if current_url != url else \
                         "Yönlendirme başarısız veya çalışmıyor"
            else:
                status = "Href bulunamadı"

        except StaleElementReferenceException:
            status = "Hata: Element geçersiz (stale)"
        except Exception as e:
            status = f"Hata oluştu: {str(e)}"

        result = (
            f"Sıra: {index + 1}\n"
            f"Link: {href}\n"
            f"İsim: {link_text or 'Bilinmiyor'}\n"
            f"Durum: {status}\n\n"
            f"{'-' * 68}\n\n"
        )
        results.append(result)
        result_text.insert(tk.END, result)

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            result_text.insert(tk.END, "Ana sayfaya dönerken zaman aşımı hatası.\n")
            break

    driver.quit()

    elapsed_time = time.time() - start_time
    result_text.insert(tk.END, "Fonksiyon testi tamamlandı.\n")
    result_text.insert(tk.END, f"Toplam geçen süre: {elapsed_time:.2f} saniye.\n")
    result_text.update_idletasks()

    return results
    # Bitmeden çıkarsak result text kısmında hata kodları dondurmesi normaldir!!!

def search_url(query, log_callback):
    """
    URL veya anahtar kelime ile webview araması yapma fonksiyonu.
    Gezinilen gerçek URL'leri log_callback'e çağırır.
    Bu yapı ayrı bir browser açar ve kaydolmaz girilen yapılar bir yerde
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
                        log_callback(current_url)
                time.sleep(1)
            except Exception as e:
                log_callback(f"URL takibi sırasında hata: {e}\n")
                break

    thread = threading.Thread(target=track_url, daemon=True)
    thread.start()

    webview.start()


def archive(url, log_callback):
    """
    Belirtilen url ve oradaki linkleri teker teker girerek tüm sayfaları
    interaktif olacak şekilde pdf olarak arşivler
    """
    log_callback(f"Arşivleme başlatıldı: {url}\n")
    start_time = time.time()

    driver = webdriver.Chrome()
    driver.get(url)
    driver.maximize_window()

    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
    main_title = driver.title.strip()
    # Pdfler aynı adda bir klasör oluşturulup kaydolur
    pdf_folder = os.path.join("pdf", main_title.replace(' ', '_').replace('/', '_'))

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        total_links = len(links)
        log_callback(f"Toplam link sayısı: {total_links}\n")

        actions = ActionChains(driver)

        for index in range(total_links):
            try:
                links = driver.find_elements(By.TAG_NAME, "a")
                link = links[index]
                link_text = link.text.strip()
                href = link.get_attribute("href")

                if href:
                    # Kara liste kontrolü
                    # Bu tip birkaç site hata verdiriyor
                    if (
                        "books2read.com" in href
                        or ("action=edit" in href and "title=" in href)
                        or link.get_attribute("accesskey") == "e"
                    ):
                        log_callback(f"[ATLANAN] Kara listedeki veya engellenmiş bir link: {href}\n")
                        continue

                    if href.startswith("#"):
                        log_callback(f"[ATLANAN] Aynı sayfa bağlantısı: {href}\n")
                        continue

                    base_url = urlparse(url)
                    parsed_href = urlparse(href)
                    if parsed_href.netloc == base_url.netloc and parsed_href.path == base_url.path:
                        log_callback(f"[ATLANAN] Sayfa içi yönlendirme: {href}\n")
                        continue

                    if link.size['width'] == 0 or link.size['height'] == 0:
                        log_callback(f"[ATLANAN] Görünmez bağlantı: {link_text} (href: {href})\n")
                        continue

                    driver.execute_script("arguments[0].setAttribute('target','_self')", link)

                    driver.execute_script(
                        "arguments[0].style.backgroundColor = 'gray';"
                        "arguments[0].style.color = 'white';",
                        link
                    )

                    actions.move_to_element(link).perform()
                    time.sleep(0.2)
                    link.click()

                    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))

                    page_title = driver.title.strip()
                    safe_title = f"{index + 1}_{page_title.replace(' ', '_').replace('/', '_')}.pdf"
                    page_pdf_path = os.path.join(pdf_folder, safe_title)

                    pdf_result = driver.execute_cdp_cmd("Page.printToPDF", {"printBackground": True})
                    with open(page_pdf_path, 'wb') as pdf_file:
                        pdf_file.write(base64.b64decode(pdf_result['data']))

                    log_callback(
                        f"[KAYDEDİLDİ] Sayfa: {page_title} (URL: {href}) -> {page_pdf_path}\n"
                    )

                    driver.get(url)
                    WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))

                else:
                    log_callback(f"[ATLANAN] Geçersiz link: {link_text}\n")

            except (StaleElementReferenceException, WebDriverException, TimeoutException) as e:
                log_callback(f"[HATA] Link işlenirken hata oluştu: {str(e)}\n")
                driver.get(url)
                WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "body")))
                continue

        elapsed_time = time.time() - start_time
        log_callback(f"Arşivleme işlemi tamamlandı. PDF'ler '{pdf_folder}' klasörüne kaydedildi.\n")
        log_callback(f"Toplam geçen süre: {elapsed_time:.2f} saniye.\n")

    except Exception as e:
        log_callback(f"[GENEL HATA] {str(e)}\n")

    finally:
        driver.quit()
        log_callback("Tarayıcı kapatıldı.\n")
    # BU yapı aynı fonksyion testi gibi gezinir ama fark olarak her yeri kaydeder pdf olarak


def interactive_ddos(url, result_text, bot_logo, request_interval=0.01):
    """
    Belirtilen URL'ye karşı etkileşimli DDoS simülasyonu.
    Tarayıcı açık kaldığı sürece istek gönderilir.
    Bu yapı çok gelişmiş ve işlevli olmasa da ek olarak eklemek istedim
    """
    total_requests = 0
    successful_requests = 0
    failed_requests = 0
    stop_attack = False
    driver = None

    def attack():
        nonlocal total_requests, successful_requests, failed_requests, stop_attack
        while not stop_attack:
            try:
                response = requests.get(url, timeout=3)
                total_requests += 1
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
            except Exception:
                total_requests += 1
                failed_requests += 1
            time.sleep(request_interval)

    try:
        options = Options()
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        attack_thread = threading.Thread(target=attack, daemon=True)
        attack_thread.start()

        while True:
            try:
                driver.title
                time.sleep(1)
                result_text.tag_configure(
                    "bot",
                    justify="left",
                    foreground="red",
                    font=("Arial", 12)
                )
                result_text.image_create("end", image=bot_logo)
                result_text.insert(
                    "end",
                    f" : İstekler: {total_requests}, "
                    f"Başarılı: {successful_requests}, "
                    f"Başarısız: {failed_requests}\n",
                    "bot"
                )
                result_text.see("end")
            except Exception:
                print("Tarayıcı kapandı, saldırı durduruluyor...")
                break

    finally:
        stop_attack = True
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

        result_text.tag_configure(
            "bot",
            justify="left",
            foreground="red",
            font=("Arial", 12)
        )
        result_text.image_create("end", image=bot_logo)
        result_text.insert(
            "end",
            f" : Saldırı Sonuçları =\n Toplam İstek: {total_requests}, "
            f"Başarılı: {successful_requests}, "
            f"Başarısız: {failed_requests}\n",
            "bot"
        )
        result_text.see("end")
        print("Saldırı tamamlandı.")
