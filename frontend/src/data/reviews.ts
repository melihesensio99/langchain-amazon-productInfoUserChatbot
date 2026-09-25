export interface ReviewItem {
  id: string;
  author: string;
  rating: number; // 1 to 5
  date: string;
  comment: string;
  verifiedPurchase: boolean;
}

// 50 reviews total: 30 positive, 10 neutral, 10 negative
// Naturally sorted without category labels or tags
export const REVIEWS: ReviewItem[] = [
  // 1 (Positive)
  {
    id: "rev-01",
    author: "Ahmet Yılmaz",
    rating: 5,
    date: "18 Eylül 2026",
    comment: "Parmak izi okuyucusu inanılmaz hızlı, kulba dokunur dokunmaz anında açılıyor. 43 mm çelik kapıma montajı yaklaşık 25 dakikada tamamladım.",
    verifiedPurchase: true
  },
  // 2 (Positive)
  {
    id: "rev-02",
    author: "Zeynep Kaya",
    rating: 5,
    date: "16 Eylül 2026",
    comment: "Tasarımı son derece şık ve modern. Kapının üzerinde çok kaliteli duruyor. Misafirler için geçici PIN oluşturma özelliği çok pratik.",
    verifiedPurchase: true
  },
  // 3 (Neutral)
  {
    id: "rev-03",
    author: "Murat Demir",
    rating: 3,
    date: "14 Eylül 2026",
    comment: "Ürün genel olarak işini yapıyor ancak Bluetooth menzili kapının 5-6 metre ötesine geçince zayıflıyor. Doğrudan kapı önündeyken sorunsuz.",
    verifiedPurchase: true
  },
  // 4 (Negative)
  {
    id: "rev-04",
    author: "Caner Öztürk",
    rating: 2,
    date: "12 Eylül 2026",
    comment: "Doğrudan Wi-Fi olmaması benim için büyük eksi oldu. Uzaktan açmak için mutlaka yakında Bluetooth mesafesinde olmak gerekiyor.",
    verifiedPurchase: true
  },
  // 5 (Positive)
  {
    id: "rev-05",
    author: "Elif Şahin",
    rating: 5,
    date: "10 Eylül 2026",
    comment: "Çocuklar okuldan gelince anahtar kaybetme derdi tamamen bitti. Parmak izlerini 2 dakikada kaydettik, çok memnunuz.",
    verifiedPurchase: true
  },
  // 6 (Positive)
  {
    id: "rev-06",
    author: "Burak Arslan",
    rating: 5,
    date: "08 Eylül 2026",
    comment: "Gövde metal hissi ve işçilik harika. Plastik hissi veren ucuz kilitlerle uzaktan yakından alakası yok.",
    verifiedPurchase: true
  },
  // 7 (Neutral)
  {
    id: "rev-07",
    author: "Selin Çelik",
    rating: 3,
    date: "06 Eylül 2026",
    comment: "Yağmurlu günlerde parmak tamamen ıslakken bazen ikinci denemede okuyor. Kurulayıp dokununca hemen açılıyor.",
    verifiedPurchase: true
  },
  // 8 (Negative)
  {
    id: "rev-08",
    author: "Emre Koç",
    rating: 1,
    date: "05 Eylül 2026",
    comment: "Eski kapımdaki delik 38 mm idi, adaptör halkasını takarken epey zorlandım. Kılavuzdaki çizimler daha detaylı olabilirdi.",
    verifiedPurchase: true
  },
  // 9 (Positive)
  {
    id: "rev-09",
    author: "Büşra Aydın",
    rating: 4,
    date: "03 Eylül 2026",
    comment: "Dokunmatik tuş takımı gizli ve şık. Sayılara dokunduğunuzda hafif beyaz led yanıyor, gece kullanımı çok rahat.",
    verifiedPurchase: true
  },
  // 10 (Positive)
  {
    id: "rev-10",
    author: "Serkan Güneş",
    rating: 5,
    date: "01 Eylül 2026",
    comment: "Backset ayarının 60 ve 70 mm olarak seçilebilmesi kurtarıcı oldu. Standart ahşap kapıma sıfıra sıfır oturdu.",
    verifiedPurchase: true
  },
  // 11 (Neutral)
  {
    id: "rev-11",
    author: "Derya Doğan",
    rating: 3,
    date: "29 Ağustos 2026",
    comment: "Pil kapağını açmak ilk başta biraz sert geldi, tırnakla zorlandım. Onun haricinde kilit mekanizması gayet sessiz çalışıyor.",
    verifiedPurchase: true
  },
  // 12 (Negative)
  {
    id: "rev-12",
    author: "Kemal Aksoy",
    rating: 2,
    date: "27 Ağustos 2026",
    comment: "Kutu içerisinden çıkan vidalardan biri 55 mm kalınlığındaki kapım için sınırda kaldı. Kendim nalburdan daha uzun vida temin etmek zorunda kaldım.",
    verifiedPurchase: true
  },
  // 13 (Positive)
  {
    id: "rev-13",
    author: "Merve Tekin",
    rating: 5,
    date: "25 Ağustos 2026",
    comment: "Ofisimizin toplantı odası için aldık. 20 personelin parmak izini ve PIN kodlarını tanımladık, herkes çok rahat etti.",
    verifiedPurchase: true
  },
  // 14 (Positive)
  {
    id: "rev-14",
    author: "Onur Kurt",
    rating: 5,
    date: "23 Ağustos 2026",
    comment: "USB-C acil durum besleme portunu test ettim, powerbank takınca anında enerji geliyor ve kilit açılıyor. Çok güven verici.",
    verifiedPurchase: true
  },
  // 15 (Neutral)
  {
    id: "rev-15",
    author: "Hakan Yıldız",
    rating: 3,
    date: "21 Ağustos 2026",
    comment: "Tuş sesleri bir tık yüksek geldi bana, gerçi ayarlardan kısılıyor ama fabrika çıkışı ses seviyesi biraz fazlaydı.",
    verifiedPurchase: true
  },
  // 16 (Positive)
  {
    id: "rev-16",
    author: "Tolga Acar",
    rating: 4,
    date: "19 Ağustos 2026",
    comment: "Kargo çok hızlı geldi. Kutu içeriği eksiksiz ve vidalar poşetler halinde ayrılmıştı.",
    verifiedPurchase: true
  },
  // 17 (Negative)
  {
    id: "rev-17",
    author: "Gülşah Korkmaz",
    rating: 2,
    date: "17 Ağustos 2026",
    comment: "Piller kutudan çıkmıyor, 4 adet AA alkalin pili kendiniz almanız gerekiyor. Bu fiyattaki bir üründe piller dahil olmalıydı.",
    verifiedPurchase: true
  },
  // 18 (Positive)
  {
    id: "rev-18",
    author: "Kerem Polat",
    rating: 5,
    date: "15 Ağustos 2026",
    comment: "Eski mekanik kilitlerden sonra çağ atladık resmen. Anahtar unutma stresine son.",
    verifiedPurchase: true
  },
  // 19 (Positive)
  {
    id: "rev-19",
    author: "Seda Yıldırım",
    rating: 5,
    date: "13 Ağustos 2026",
    comment: "Gövdesi mat siyah ve parmak izi tutmuyor. Temizliği de çok kolay, hafif nemli bezle silmek yetiyor.",
    verifiedPurchase: true
  },
  // 20 (Neutral)
  {
    id: "rev-20",
    author: "İsmail Eren",
    rating: 3,
    date: "11 Ağustos 2026",
    comment: "Kurulum sırasında vida uzunluğunu kapı kalınlığına göre dikkatli seçmek gerekiyor, ben 42 mm kapı için siyah vidaları kullandım.",
    verifiedPurchase: true
  },
  // 21 (Positive)
  {
    id: "rev-21",
    author: "Gizem Erdoğan",
    rating: 5,
    date: "09 Ağustos 2026",
    comment: "Yaşlı annem için aldık, anahtarı çevirmekte zorlanıyordu. Parmak izini tanıttık, tek hamlede rahatça içeri giriyor.",
    verifiedPurchase: true
  },
  // 22 (Negative)
  {
    id: "rev-22",
    author: "Alper Tan",
    rating: 1,
    date: "07 Ağustos 2026",
    comment: "Kilit dili mekanizmasını 70 mm'ye uzatırken biraz zorlandım, yay mekanizması biraz sert. Dikkatli olmak lazım.",
    verifiedPurchase: true
  },
  // 23 (Positive)
  {
    id: "rev-23",
    author: "Fatma Aslan",
    rating: 5,
    date: "05 Ağustos 2026",
    comment: "IP54 koruması sayesinde bina içi esintili ve nemli koridorda hiç sorunsuz çalışıyor.",
    verifiedPurchase: true
  },
  // 24 (Positive)
  {
    id: "rev-24",
    author: "Volkan Çetin",
    rating: 4,
    date: "03 Ağustos 2026",
    comment: "Pil ömrü gayet iyi gidiyor, 3 aydır aynı 4 adet AA pille kullanıyoruz pil göstergesi hala dolu.",
    verifiedPurchase: true
  },
  // 25 (Neutral)
  {
    id: "rev-25",
    author: "Ece Avcı",
    rating: 3,
    date: "01 Ağustos 2026",
    comment: "Fiyat performans olarak kabul edilebilir seviyede. Kulp açısı ergonomik ancak çok hızlı bastırınca bir tık yay sesi geliyor.",
    verifiedPurchase: true
  },
  // 26 (Positive)
  {
    id: "rev-26",
    author: "Oğuzhan Bulut",
    rating: 5,
    date: "30 Temmuz 2026",
    comment: "Mekanik anahtar yuvasının alt kısımda gizlenmiş olması hem estetik hem de güvenli. Yedek anahtarlar da kutuda mevcut.",
    verifiedPurchase: true
  },
  // 27 (Negative)
  {
    id: "rev-27",
    author: "Melis Şen",
    rating: 2,
    date: "28 Temmuz 2026",
    comment: "Kullanım kılavuzundaki yazı puntoları çok küçüktü, okumakta zorlandım. Asistana sorarak kurulumu tamamlayabildim.",
    verifiedPurchase: true
  },
  // 28 (Positive)
  {
    id: "rev-28",
    author: "Barış Yavuz",
    rating: 5,
    date: "26 Temmuz 2026",
    comment: "100 adet PIN kodu kapasitesi çok geniş. Apartman yöneticisi olarak sığınak ve ortak alan kapısına taktık, çok memnunuz.",
    verifiedPurchase: true
  },
  // 29 (Positive)
  {
    id: "rev-29",
    author: "Banu Keskin",
    rating: 5,
    date: "24 Temmuz 2026",
    comment: "Sade ve şık tasarım, kapıda gereksiz kalabalık yapmıyor. Misafirler gördüğünde hayran kalıyor.",
    verifiedPurchase: true
  },
  // 30 (Neutral)
  {
    id: "rev-30",
    author: "Deniz Kaplan",
    rating: 3,
    date: "22 Temmuz 2026",
    comment: "Kilit ağırlığı beklediğimden biraz fazlaydı ama kapıya sağlam oturdu. Montaj öncesi kapı delik ölçüsünü mutlaka kontrol edin.",
    verifiedPurchase: true
  },
  // 31 (Positive)
  {
    id: "rev-31",
    author: "Tarkan Özkan",
    rating: 5,
    date: "20 Temmuz 2026",
    comment: "Bluetooth bağlantısı telefonla saniyeler içinde kuruldu. Gecikme olmadan komutları algılıyor.",
    verifiedPurchase: true
  },
  // 32 (Negative)
  {
    id: "rev-32",
    author: "Ceyda Uçar",
    rating: 1,
    date: "18 Temmuz 2026",
    comment: "Parmak izi sensörünün üzerine küçük bir çizik geldiğinde okuma hızı biraz düştü. Yüzey koruması daha sert olabilirdi.",
    verifiedPurchase: true
  },
  // 33 (Positive)
  {
    id: "rev-33",
    author: "Umut Bozkurt",
    rating: 4,
    date: "16 Temmuz 2026",
    comment: "Kapı arkasından kilitleme mandalı da çok akıcı dönüyor. İçeriden çıkarken hiç zorluk çıkarmıyor.",
    verifiedPurchase: true
  },
  // 34 (Positive)
  {
    id: "rev-34",
    author: "Ayşe Taşkın",
    rating: 5,
    date: "14 Temmuz 2026",
    comment: "Eve girip çıkarken çanta içinde anahtar arama derdi sona erdi. Alınabilecek en iyi akıllı ev yatırımı.",
    verifiedPurchase: true
  },
  // 35 (Neutral)
  {
    id: "rev-35",
    author: "Koray Güler",
    rating: 3,
    date: "12 Temmuz 2026",
    comment: "Standart 54 mm delikli kapılarda doğrudan uyuyor ama eski tip nostaljik ahşap kapılarda marangoz yardımı gerekebilir.",
    verifiedPurchase: true
  },
  // 36 (Positive)
  {
    id: "rev-36",
    author: "Cem Altın",
    rating: 5,
    date: "10 Temmuz 2026",
    comment: "Çinko alaşım döküm gövde güven hissi veriyor. Darbelere karşı oldukça mukavemetli görünüyor.",
    verifiedPurchase: true
  },
  // 37 (Negative)
  {
    id: "rev-37",
    author: "Tuğçe Erdem",
    rating: 2,
    date: "08 Temmuz 2026",
    comment: "Tuş takımındaki sayıların boyutu biraz daha büyük olabilirdi, gözlük takmadan bazen yanlış rakama basabiliyorum.",
    verifiedPurchase: true
  },
  // 38 (Positive)
  {
    id: "rev-38",
    author: "Levent Karaca",
    rating: 5,
    date: "06 Temmuz 2026",
    comment: "Fiyatının karşılığını fazlasıyla veriyor. Özellikle acil durum için hem mekanik anahtar hem USB-C olması çift güvenlik sağlıyor.",
    verifiedPurchase: true
  },
  // 39 (Positive)
  {
    id: "rev-39",
    author: "Nazlı Dinç",
    rating: 5,
    date: "04 Temmuz 2026",
    comment: "Tasarımı aşırı sade ve kibar. Kaba saba güvenlik kilitleri gibi değil, modern mimari kapılara yakışıyor.",
    verifiedPurchase: true
  },
  // 40 (Neutral)
  {
    id: "rev-40",
    author: "Gökhan Saygın",
    rating: 3,
    date: "02 Temmuz 2026",
    comment: "Pillerin alkalin olması şart, şarjlı pillerle voltaj uyuşmazlığı yapabiliyor. Kılavuzda belirtilen 1.5V AA alkalin pil kullanılmalı.",
    verifiedPurchase: true
  },
  // 41 (Positive)
  {
    id: "rev-41",
    author: "Hande Vural",
    rating: 4,
    date: "30 Haziran 2026",
    comment: "Parmak izi açısı çok doğal, başparmağınız kulbu kavradığı an sensörün üzerine denk geliyor.",
    verifiedPurchase: true
  },
  // 42 (Negative)
  {
    id: "rev-42",
    author: "Ferhat Duman",
    rating: 1,
    date: "28 Haziran 2026",
    comment: "Kapı kanat kalınlığım 32 mm idi, minimum 35 mm desteklediği için montaj yapamadım ve iade etmek zorunda kaldım. Ölçülere dikkat edin.",
    verifiedPurchase: true
  },
  // 43 (Positive)
  {
    id: "rev-43",
    author: "Pınar Aktaş",
    rating: 5,
    date: "26 Haziran 2026",
    comment: "Temizlik görevlimize belirli günlerde geçerli şifre verdik, gün bitince kod otomatik devre dışı kalıyor. Mükemmel özellik.",
    verifiedPurchase: true
  },
  // 44 (Positive)
  {
    id: "rev-44",
    author: "Serdar Özdemir",
    rating: 5,
    date: "24 Haziran 2026",
    comment: "Ürünün kutulaması ve ambalajı Apple ürünleri kalitesinde. Parçalar tıkır tıkır yerine oturdu.",
    verifiedPurchase: true
  },
  // 45 (Neutral)
  {
    id: "rev-45",
    author: "Tülay Sevim",
    rating: 3,
    date: "22 Haziran 2026",
    comment: "Kurulumu kendim yaptım, matkap kullanmaya gerek kalmadı. Ancak tornavida biraz kaliteli olmalı vidaları sıyırmamak için.",
    verifiedPurchase: true
  },
  // 46 (Negative)
  {
    id: "rev-46",
    author: "Yasin Bilgin",
    rating: 2,
    date: "20 Haziran 2026",
    comment: "Güneş doğrudan vurduğunda dokunmatik panel biraz ısınıyor. Doğrudan batı cephesine bakan dış kapılarda gölgelik gerekebilir.",
    verifiedPurchase: true
  },
  // 47 (Positive)
  {
    id: "rev-47",
    author: "Aslıhan Koçer",
    rating: 5,
    date: "18 Haziran 2026",
    comment: "Kilit kapandığında verilen onay sesi ve yeşil led bildirimi çok net anlaşılıyor. Ailecek çok sevdik.",
    verifiedPurchase: true
  },
  // 48 (Positive)
  {
    id: "rev-48",
    author: "Mehmet Çakır",
    rating: 5,
    date: "16 Haziran 2026",
    comment: "48 mm çelik daire kapımıza taktık. Kilit dili sağlam ve sarsıntısız kilitliyor.",
    verifiedPurchase: true
  },
  // 49 (Positive)
  {
    id: "rev-49",
    author: "Sevgi Ilgaz",
    rating: 4,
    date: "14 Haziran 2026",
    comment: "Sipariş verdikten 1 gün sonra elimdeydi. Montajı çok rahat yaptık, parmak izi okuma hızı etkileyici.",
    verifiedPurchase: true
  },
  // 50 (Positive)
  {
    id: "rev-50",
    author: "Kadir Meriç",
    rating: 5,
    date: "12 Haziran 2026",
    comment: "Kendi sınıfındaki diğer kilitlere göre tasarımı çok daha sade ve dayanıklı. 4 adet AA pille uzun süre sorunsuz çalışıyor, kesinlikle tavsiye ederim.",
    verifiedPurchase: true
  }
];
