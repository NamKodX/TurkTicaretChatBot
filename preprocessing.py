from libraries import *

# Mantıksal sembol eşlemesi
logic_map = {
    "ve": "∧",
    "veya": "∨",
    "değil": "¬",
    "eğer": "⇒",
    "ise": "⇒"
}

# Özel stopwords listesi
# mantıksal kelimeler hariç
# çünkü bu ifadeler ileride geliştirmede semantik yapılarda anlam kazanacaktır

stopwords = [
    "bir", "bu", "şu", "o", "çok", "az", "daha", "en", "her", "bazı", "hiç", "kimi", "bazıları"
]

# Temel ön işleme fonksiyonları
# Kelimeleri küçük harfe dönüştürme
def to_lower(text):
    return text.lower().strip()

# Noktalama işaretleri kaldırma
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# Sayıları temizleme
def remove_numbers(text):
    return re.sub(r'\d+', '', text)

# Stopwords temizleme
def remove_stopwords(text):
    words = text.split()
    filtered = [word for word in words if word not in stopwords]
    return " ".join(filtered)

# Mantıksal ifadeleri sembollerle değiştirme
def replace_logical_words(text):
    words = text.split()
    replaced = [logic_map[word] if word in logic_map else word for word in words]
    return " ".join(replaced)

# Basit kök bulma fonksiyonu
# Ekleri kesme işlemi yaptım bir modül ve kütüphane kullanmaktansa
def simple_stem(word):
    suffixes = [
        "lar", "ler", "lık", "lik", "luk", "lük", "cı", "ci", "cu", "cü",
        "dan", "den", "tan", "ten", "ın", "in", "un", "ün", "ı", "i", "u", "ü",
        "m", "n", "miz", "niz", "leri", "leri", "dir", "dır", "dur", "dür",
        "muş", "miş", "muş", "müş", "ti", "tı", "tu", "tü", "ken", "ecek", "acak"
    ]

    for suffix in sorted(suffixes, key=lambda x: -len(x)):
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

# Kelimelere kök işlemi uygulayıp yeniden oluşturur
def apply_stemming(text):
    words = text.split()
    stemmed_words = [simple_stem(word) for word in words]
    return " ".join(stemmed_words)

def stemming(text):
    stemmer = SnowballStemmer("turkish")
    # Daha profesyonel kütüphane ile beraber kök alma işlemi
    tokens = nltk.word_tokenize(text, language="turkish")  # Kelimelere ayır
    stemmed_words = [stemmer.stem(word) for word in tokens]
    return " ".join(stemmed_words)

# Toplu ön işleme fonksiyonu
def preprocess_text(text):
    text = to_lower(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_stopwords(text)
    text = replace_logical_words(text)
    # text = stemming(text)
    # text = apply_stemming(text)

    return text

# Bu kısım isteğe bağlı vektör temsili yapısı
# Bu yapı kullandıgım uygulamada gereksiz yapıda
# Ben anlam çıkarma yani semantik yapı yerine sembolik sentaktik yapı kullandım
try:
    import gensim.downloader as api
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    # Word2Vec modeli (Google Geliştirdi)
    word2vec_model = api.load("glove-wiki-gigaword-50")

    def get_vector_representation(text):
        """
        Word2Vec modeli kullanarak metni ortalama kelime vektörü ile temsil eder.
        """
        words = preprocess_text(text).split()
        vectors = [word2vec_model[word] for word in words if word in word2vec_model]
        if vectors:
            return np.mean(vectors, axis=0)
        return np.zeros(word2vec_model.vector_size)

    def semantic_similarity(query, docs):
        """
        Word2Vec temelli semantik benzerlik: Cosine skoruna göre en yakın sonucu döner.
        """
        query_vector = get_vector_representation(query)
        doc_vectors = [get_vector_representation(doc) for doc in docs]
        similarities = cosine_similarity([query_vector], doc_vectors)[0]
        best_idx = np.argmax(similarities)
        return docs[best_idx], similarities[best_idx]

except Exception as e:
    def get_vector_representation(text):
        return f"[Vektör modeli yüklenemedi: {str(e)}]"

    def semantic_similarity(query, docs):
        return None, 0.0

# Bağlam Çıkarma Fonksiyonu
def retrieve_context(text):
    """
    Giriş metninden bağlam çıkarır ve
    nicelik, özne, eylem, konum, zaman, sıfat, zarf, bağlaç, edat, sayı, zamir bilgilerini döndürür.
    """
    text = text.lower().strip()
    words = text.split()
    quantifier, subject, action, location, time = None, [], None, None, None
    adjectives, adverbs, conjunctions, prepositions, numbers, pronouns = [], [], [], [], [], []

    quantifiers = {
        # Orijinal maddeler
        "her": "her",
        "bazı": "bazı",
        "bir": 1,
        "iki": 2,
        "çoğu": "çoğu",
        "birkaç": "birkaç",
        "hiçbiri": "hiçbiri",
        "tüm": "her",

        # Sayısal ifadeler
        "üç": 3,
        "dört": 4,
        "beş": 5,
        "altı": 6,
        "yedi": 7,
        "sekiz": 8,
        "dokuz": 9,
        "on": 10,
        "on bir": 11,
        "on iki": 12,
        "on üç": 13,
        "on dört": 14,
        "on beş": 15,
        "on altı": 16,
        "on yedi": 17,
        "on sekiz": 18,
        "on dokuz": 19,
        "yirmi": 20,
        "yirmi bir": 21,
        "yirmi iki": 22,
        "yirmi üç": 23,
        "yirmi dört": 24,
        "yirmi beş": 25,
        "yirmi altı": 26,
        "yirmi yedi": 27,
        "yirmi sekiz": 28,
        "yirmi dokuz": 29,
        "otuz": 30,
        "otuz bir": 31,
        "otuz iki": 32,
        "otuz üç": 33,
        "otuz dört": 34,
        "otuz beş": 35,
        "otuz altı": 36,
        "otuz yedi": 37,
        "otuz sekiz": 38,
        "otuz dokuz": 39,
        "kırk": 40,

        # Farklı nicelik belirten ifadeler
        "pek çok": "pek çok",
        "birçok": "birçok",
        "az": "az",
        "çok az": "çok az",
        "oldukça fazla": "oldukça fazla",
        "bir o kadar": "bir o kadar",
        "yaklaşık yarısı": "yaklaşık yarısı",
        "hepsi": "hepsi",
        "tamamı": "tamamı",
        "neredeyse hepsi": "neredeyse hepsi",
        "yeterince": "yeterince",
        "kâfi miktarda": "kâfi miktarda",
        "sınırlı sayıda": "sınırlı sayıda",
        "onlarca": "onlarca",
        "yüzlerce": "yüzlerce",
        "binlerce": "binlerce",
        "milyonlarca": "milyonlarca",
        "kimisi": "kimisi",
        "kimileri": "kimileri",
        "bir kesim": "bir kesim",
        "büyük bölümü": "büyük bölümü",
        "küçük bölümü": "küçük bölümü",
        "bir kısmı": "bir kısmı",
        "kalanı": "kalanı",
        "her biri": "her biri",
        "bazıları": "bazıları",
        "çoğunluğu": "çoğunluğu",
        "azınlığı": "azınlığı",
        "bollukla": "bollukla",
        "bir hayli": "bir hayli",
        "hayli çok": "hayli çok",
        "geriye kalanlar": "geriye kalanlar",
        "pek az": "pek az",
        "ortalama": "ortalama",
        "vasat miktarda": "vasat miktarda",
        "maksimum": "maksimum",
        "minimum": "minimum",
        "yeterli düzeyde": "yeterli düzeyde",
        "nadir": "nadir",
        "sıfır": 0,
        "mutlak hiç": "mutlak hiç",
        "tam sayısı bilinmeyen": "tam sayısı bilinmeyen",
        "belirsiz miktar": "belirsiz miktar",
        "tümü": "her",
        "gereğinden fazla": "gereğinden fazla",
        "gereğinden az": "gereğinden az",
        "fazlasıyla": "fazlasıyla",
        "neredeyse hiç": "neredeyse hiç",
        "kimi zaman tümü": "kimi zaman tümü",
        "öyle böyle": "öyle böyle",
        "eksiksiz tümü": "eksiksiz tümü",
        "bütünü": "bütünü",
        "çeyrek": "çeyrek",
        "üçte biri": "üçte biri",
        "beşte biri": "beşte biri",
        "yarıdan çoğu": "yarıdan çoğu",
        "yarıdan azı": "yarıdan azı",
        "tam yarısı": "tam yarısı",
        "dörde üçü": "dörde üçü",
        "bir elin parmakları kadar": "bir elin parmakları kadar",
        "dile kolay": "dile kolay",
        "en azından birkaç": "en azından birkaç",
        "belki bazı": "belki bazı",
        "çoğu kimse": "çoğu kimse",
        "az sayıda": "az sayıda",
        "orta miktarda": "orta miktarda",
        "yüksek miktarda": "yüksek miktarda",
        "düşük miktarda": "düşük miktarda",
        "en az bir": "en az bir",
        "en fazla birkaç": "en fazla birkaç",
        "halkın çoğu": "halkın çoğu",
        "toplumun azı": "toplumun azı",
        "neredeyse tamamı": "neredeyse tamamı",
        "geniş bir kesim": "geniş bir kesim",
        "dar bir kesim": "dar bir kesim",
        "küçücük bir grup": "küçücük bir grup",
        "kayda değer miktarda": "kayda değer miktarda",
        "oldukça yüksek": "oldukça yüksek",
        "oldukça düşük": "oldukça düşük"
    }

    verbs = [
        # Fiiller listesi
        "gidiyor", "yapıyor", "oturuyor", "çalışıyor", "gider", "geliyor",
        "bakıyor", "seviyor", "koşuyor", "uçuyor", "yazıyor", "yürüyor",
        "duruyor", "uçar","okuyor", "okur", "konuşuyor", "konuşur", "dinliyor", "dinler",
        "bekliyor", "bekler", "kalkıyor", "kalkar", "uyuyor", "uyur",
        "öğreniyor", "öğrenir", "öğretiyor", "öğretir", "soruyor", "sorar",
        "cevaplıyor", "cevaplar", "açıyor", "açar", "kapatıyor", "kapar",
        "arıyor", "arar", "izliyor", "izler", "gönderiyor", "gönderir",
        "alıyor", "alır", "veriyor", "verir", "başlıyor", "başlar",
        "bitiriyor", "bitirir", "satıyor", "satar", "satın alıyor", "satın alır",
        "ağlıyor", "ağlar", "gülüyor", "güler", "silkeliyor", "sirkeler",
        "düşünüyor", "düşünür", "tasarlıyor", "tasarlar", "çiziyor", "çizer",
        "boyuyor", "boyar", "pişiriyor", "pişirir", "yiyor", "yer",
        "içiyor", "içer", "sevk ediyor", "sevk eder", "düzenliyor", "düzenler",
        "araştırıyor", "araştırır", "keşfediyor", "keşfeder", "kaydediyor", "kaydeder",
        "siliyor", "siler", "topluyor", "toplar", "devam ediyor", "devam eder",
        "ziyaret ediyor", "ziyaret eder", "gösteriyor", "gösterir", "dinleniyor", "dinlenir",
        "hazırlıyor", "hazırlar", "temizliyor", "temizler", "boyutlandırıyor", "boyutlandırır",
        "işliyor", "işler", "gözetliyor", "gözetler", "sunuyor", "sunar",
        "paylaşıyor", "paylaşır", "karşılaştırıyor", "karşılaştırır", "anlatıyor", "anlatır",
        "yaklaşıyor", "yaklaşır", "uzaklaşıyor", "uzaklaşır", "ayarlıyor", "ayarlar",
        "arzuluyor", "arzular", "tamamlıyor", "tamamlar", "yetiştiriyor", "yetiştirir",
        "bakım yapıyor", "bakım yapar", "yönlendiriyor", "yönlendirir", "bağırıyor", "bağırır",
        "fısıldıyor", "fısıldar"
    ]

    locations = [
        # Mekanlar
        "pazara", "okula", "eve", "bahçeye", "işe", "markete", "denize",
        "dağa", "kütüphaneye", "sınıfa", "odalara","hastaneye", "karakola",
        "tiyatroya", "sinemaya", "restorana","kafeye", "müzeye", "sergiye",
        "otobüs durağına", "istasyona","havaalanına", "otogara", "fabrikaya",
        "atölyeye", "stadyuma","spor salonuna", "park yerine", "otoparka", "düğüne",
        "mahkemeye", "postaneye", "bankaya", "fırına", "pastaneye",
        "bakkala", "çiftliğe", "tarlaya", "ormanlık alana", "koruya",
        "otel odasına", "kamelyaya", "teras katına", "çatının üzerine", "balkona",
        "kamp alanına", "karavan bölgesine", "göle", "nehir kenarına", "kırsala",
        "kasabaya", "köye", "şehir merkezine", "merkeze", "çarşıya",
        "alışveriş merkezine", "mağazaya", "butiğe", "eczaneye", "laboratuvara",
        "ameliyathaneye", "rehabilitasyon merkezine", "konsere", "festivale", "stüdyoya",
        "iç bahçeye", "arka odaya", "salona", "misafir odasına", "çatıkatı deposuna",
        "garaja", "depo alanına", "arsaya", "yokuşa", "plaja",
        "sahil kenarına", "limana", "iskelenin ucuna", "köprüye", "kanyon bölgesine",
        "vadiye", "uçurum kenarına", "yol kenarına", "kümesin içine", "ahıra",
        "seraya", "kelebek bahçesine", "hayvanat bahçesine", "lunaparka", "piknik alanına",
        "gezi teknesine", "kır evine", "motora", "kışlaya", "konferans salonuna",
        "toplantı odasına", "ofise", "resepsiyona", "kulise", "oturma odasına","meclise",
        "çocuk parkına", "oyun alanına", "sığınak odasına", "çatı katına", "kütüphane raflarına",
        "özel kasaya", "şantiye alanına", "rüzgar gülüne", "enerji santraline", "köşk avlusuna"
    ]

    time_phrases = [
        # Zaman ifadeleri
        "her zaman", "bazen", "genellikle", "sık sık", "nadiren",
        "her sabah", "bu hafta", "akşamları", "gündüzleri", "sabah",
        "her akşam", "her öğle", "her gece", "ara sıra", "ara ara",
        "zaman zaman", "her ay", "her yıl", "hafta sonları", "kışın",
        "yazın", "ilkbaharda", "sonbaharda", "her tatilde", "bayramlarda",
        "her cuma", "her pazartesi", "sabahları erken", "gece yarısı",
        "öğleden sonra", "öğle tatilinde", "ikindi vakti", "her fırsatta",
        "kesintisiz olarak", "arada bir", "bir keresinde", "iki günde bir",
        "üç günde bir", "haftada bir", "ayda bir", "iki haftada bir",
        "yılda bir", "sık aralıklarla", "seyrek aralıklarla", "art arda",
        "peş peşe", "her dakika", "her saniye", "zaman kalmadığında",
        "müsait olduğunda", "çabukça", "hemen", "vakit buldukça", "her öğleden sonra",
        "çok geç olmadan", "en kısa sürede", "bazı sabahlar", "nadiren akşamları",
        "gelecek hafta", "önümüzdeki ay", "gelecek yıl", "kısa süre içinde",
        "uzun vadede", "aniden", "plansız şekilde", "aceleyle", "günü gününe",
        "tam vaktinde", "vakitlice", "esnasında", "eski zamanlarda", "yakın geçmişte",
        "uzak geçmişte", "ilerleyen günlerde", "mümkün oldukça erken", "aralıksız",
        "toplantı sırasında", "ders arasında", "evvelden beri", "bazı akşamüstleri",
        "çok nadir", "akşam yemeğinden sonra", "öğle yemeğinden önce", "tatillerde",
        "festival zamanında", "yarın", "yarından sonra", "dün", "evvelsi gün",
        "haftaya çarşamba", "her perşembe", "her cumartesi", "yaklaşık bir saat içinde",
        "biraz sonra", "biraz önce", "az önce", "hemen ardından", "günün ilk ışıklarında",
        "tam öğle vaktinde", "mesai bitiminde", "ara tatillerde", "ders bitiminde",
        "işe başlamadan önce", "iş çıkışında", "gece yarısından sonra", "gün doğarken",
        "gün batarken", "en yoğun zamanda", "en sakin vakitte", "bayram tatili süresince"
    ]

    adjectives_list = [
        # Sıfat ifadeleri
        "büyük", "küçük", "uzun", "kısa", "geniş", "dar", "hızlı", "yavaş", "güzel", "çirkin",
        "yaşlı", "genç", "temiz", "kirli", "hafif", "ağır", "kalın", "ince", "sert", "yumuşak",
        "yüksek", "alçak", "soğuk", "sıcak", "parlak", "karanlık", "mutlu", "üzgün", "zengin", "fakir",
        "yeni", "eski", "açık", "kapalı", "derin", "sığ", "doğru", "yanlış", "keskin", "körelmiş",
        "kalabalık", "tenha", "dolu", "boş", "düz", "eğik", "şişman", "zayıf", "ağırbaşlı", "sakar",
        "karışık", "basit", "şaşırtıcı", "sıradan", "sert", "kırılgan", "parlak", "donuk", "nazik", "sert",
        "yorgun", "dinç", "lezzetli", "tatsız", "hoş", "rahatsız", "cesur", "korkak", "sadık", "vefasız",
        "sakin", "sinirli", "kibar", "kaba", "sağlıklı", "hasta", "şişman", "zayıf", "doğal", "yapay",
        "hassas", "duygusuz", "ciddi", "alaycı", "mütevazı", "gururlu", "sıkıcı", "eğlenceli", "önemli", "önemsiz",
        "çalışkan", "tembel", "uyumlu", "inatçı", "akıllı", "aptal", "sabırlı", "sabırsız", "anlamlı", "anlamsız"
    ]

    adverbs_list = [
        # Zarf Listeleri
        "hızlıca", "yavaşça", "dikkatlice", "tamamen", "yavaşça", "aniden", "sessizce", "yüksek sesle", "şiddetle",
        "nazikçe",
        "aceleyle", "düşüncesizce", "mantıklı bir şekilde", "farklı olarak", "genellikle", "bazen", "nadiren",
        "sürekli", "kesinlikle", "büyük ihtimalle",
        "muhtemelen", "şüphesiz", "belki", "asla", "hiçbir zaman", "daima", "önceden", "sonradan", "şimdi", "hemen",
        "sonra", "önce", "yakında", "geçmişte", "bir zamanlar", "birden", "ara sıra", "art arda", "aralıksız",
        "arada bir",
        "yavaş yavaş", "hızla", "hızlı", "hafifçe", "derinden", "derinlemesine", "dikkatli bir şekilde", "güzelce",
        "çirkin bir şekilde", "iyi",
        "kötü", "hoş bir şekilde", "rahatsız edici şekilde", "sabırsızca", "sabırla", "kesintisiz",
        "kararlı bir şekilde", "tutarsız bir şekilde", "anlamlı bir şekilde", "rastgele",
        "kasıtlı olarak", "bilinçli olarak", "bilinçsizce", "güvensizce", "şüpheyle", "cesurca", "çekingen bir şekilde",
        "kibarca", "agresifçe", "sert bir şekilde",
        "yumuşakça", "inatla", "ısrarla", "nezaketle", "korkusuzca", "korkakça", "utangaçça", "kendine güvenerek",
        "emin bir şekilde", "endişeyle",
        "şaşkınlıkla", "öfkeyle", "sevgiyle", "nefretle", "coşkuyla", "sessizce", "bağırarak", "mırıldanarak",
        "içtenlikle", "duygusuzca"
    ]

    conjunctions_list = [
        "ve", "veya", "ama", "fakat", "çünkü", "ya da", "lakin", "oysa", "halbuki", "buna rağmen",
        "ancak", "sonuç olarak", "hatta", "yani", "nitekim", "zira", "dolayısıyla", "şayet", "yoksa",
        "bununla birlikte",
        "böylece", "bu yüzden", "demek ki", "oysa ki", "ne var ki", "şu halde", "nasıl ki", "öyle ki", "sanki", "çünkü",
        "binaenaleyh", "keza", "bunun yanı sıra", "bu bağlamda", "hem de", "ne de", "değil mi ki", "madem", "yeter ki",
        "öyleyse"
    ]

    prepositions_list = [
        "ile", "için", "hakkında", "boyunca", "sonra", "önce", "altında", "üstünde", "arasında", "yanında",
        "karşı", "etrafında", "tarafından", "göre", "üzere", "doğru", "ile birlikte", "haricinde", "mütevellit",
        "kadar",
        "den dolayı", "itibariyle", "nedeniyle", "yüzünden", "dolayısıyla", "sayesinde", "belli ki", "hususunda",
        "ilişkin", "doğrultusunda"
    ]

    numbers_list = [
        "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz", "on",
        "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan", "yüz", "bin"
    ]

    pronouns_list = [
        "ben", "sen", "o", "biz", "siz", "onlar", "bunu", "şunu", "onu", "bunlar",
        "şunlar", "onlar", "kim", "ne", "hangi", "bazısı", "kimi", "birisi", "hiç kimse", "herkes", "kendisi"
    ]

    current_phrase = []
    is_action = False

    for phrase in time_phrases:
        if text.startswith(phrase):
            time = phrase
            text = text[len(phrase):].strip()

    for word in words:
        if word in quantifiers and not quantifier:
            quantifier = quantifiers[word]
            text = text.replace(word, "").strip()

    def retrieve_context(text):
        """
        Giriş metninden bağlam çıkarır ve eksik konumları, zaman ifadelerini düzeltir.
        BU yapılar genel olarak semantk işlemlerde kullanılır bunu bilmek gerekir.
        """
        text = text.lower().strip()
        words = text.split()
        quantifier, subject, action, location, time = None, [], None, None, None
        adjectives, adverbs, conjunctions, prepositions, numbers, pronouns = [], [], [], [], [], []

        time_phrases = ["her zaman", "bazen", "genellikle", "sık sık", "nadiren", "her sabah", "bu hafta", "akşamları",
                        "gündüzleri", "sabah"]


    for word in text.split():
        if word in verbs and not action:
            if current_phrase and not is_action:
                subject = " ".join(current_phrase).strip(".")
                current_phrase = []
            action = word
            is_action = True
        elif word in locations:
            location = word
        elif word in adjectives_list:
            adjectives.append(word)
        elif word in adverbs_list:
            adverbs.append(word)
        elif word in conjunctions_list:
            conjunctions.append(word)
        elif word in prepositions_list:
            prepositions.append(word)
        elif word in numbers_list:
            numbers.append(word)
        elif word in pronouns_list:
            pronouns.append(word)
        elif word in time_phrases and not time:
            time = word
        else:
            current_phrase.append(word)

    if not subject and current_phrase:
        subject = " ".join(current_phrase).strip()  # Fazladan boşlukları temizle

    if not action and subject:
        for verb in verbs:
            if verb in subject:
                action = verb
                subject = subject.replace(verb, "").strip(".")
                break

    return {
        "quantifier": quantifier,
        "subject": subject if subject else None,
        "action": action if action else None,
        "location": location if location else None,
        "time": time if time else None,
        "adjectives": adjectives if adjectives else None,
        "adverbs": adverbs if adverbs else None,
        "conjunctions": conjunctions if conjunctions else None,
        "prepositions": prepositions if prepositions else None,
        "numbers": numbers if numbers else None,
        "pronouns": pronouns if pronouns else None
    }
