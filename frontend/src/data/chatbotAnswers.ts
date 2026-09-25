export interface ChatbotQA {
  id: string;
  question: string;
  answer: string;
  source: string;
  keywords: string[];
}

export const READY_QUESTIONS: string[] = [
  "42 mm kapı için hangi vida kullanılmalı?",
  "38 mm delik için uyumlu mu?",
  "70 mm backset nasıl ayarlanır?",
  "Piller biterse nasıl açılır?",
  "Hangi pil kullanılmalı?",
  "Bu kilit Wi-Fi’a bağlanıyor mu?",
  "Kapı kalınlığı kaç mm olmalı?"
];

export const KNOWLEDGE_BASE: ChatbotQA[] = [
  {
    id: "screw-42mm",
    question: "42 mm kapı için hangi vida kullanılmalı?",
    answer: "42 mm kapı için siyah montaj vidaları kullanılmalıdır.",
    source: "SecureHome SHL-500 Montaj Paketi & Vida Seçim Tablosu (Bölüm 4)",
    keywords: ["42 mm", "42mm", "vida", "vida seçimi", "hangi vida", "siyah vida", "montaj vidası"]
  },
  {
    id: "hole-38mm",
    question: "38 mm delik için uyumlu mu?",
    answer: "38 mm delik için adaptör halkası kullanılmalıdır.",
    source: "SecureHome SHL-500 Delik Çapı & Adaptör Yönergesi (Bölüm 2.1)",
    keywords: ["38 mm", "38mm", "delik", "delik çapı", "adaptör", "halka", "uyumlu mu", "çap"]
  },
  {
    id: "backset-70mm",
    question: "70 mm backset nasıl ayarlanır?",
    answer: "70 mm backset için kilit dili uzatılarak ayarlanmalıdır.",
    source: "SecureHome SHL-500 Kilit Dili & Backset Kurulum Kılavuzu (Bölüm 3.1)",
    keywords: ["70 mm", "70mm", "backset", "nasıl ayarlanır", "kilit dili", "dil ayarı", "60 70"]
  },
  {
    id: "dead-battery-emergency",
    question: "Piller biterse nasıl açılır?",
    answer: "Piller biterse USB-C portuna 5V/1A powerbank bağlanabilir veya mekanik anahtar kullanılabilir.",
    source: "SecureHome SHL-500 Acil Açma & Güç Prosedürleri (Bölüm 5)",
    keywords: ["pil biterse", "piller biterse", "acil açma", "nasıl açılır", "usb-c", "powerbank", "mekanik anahtar", "enerji yok"]
  },
  {
    id: "battery-type",
    question: "Hangi pil kullanılmalı?",
    answer: "4 adet 1.5V AA alkalin pil kullanılmalıdır.",
    source: "SecureHome SHL-500 Pil & Güç Özellikleri (Bölüm 1.4)",
    keywords: ["hangi pil", "pil tipi", "pil", "alkalin", "batarya", "aa pil", "kaç pil"]
  },
  {
    id: "wifi-connectivity",
    question: "Bu kilit Wi-Fi’a bağlanıyor mu?",
    answer: "Kilit doğrudan Wi-Fi’a bağlanmaz; Bluetooth 5.0 kullanır.",
    source: "SecureHome SHL-500 Kablosuz Bağlantı Spesifikasyonu (Bölüm 2.2)",
    keywords: ["wifi", "wi-fi", "internet", "ağ", "bluetooth", "bağlanıyor mu", "uzaktan erişim"]
  },
  {
    id: "door-thickness",
    question: "Kapı kalınlığı kaç mm olmalı?",
    answer: "Kapı kalınlığı 35–55 mm arasında olmalıdır (önerilen kalınlık: 40–50 mm).",
    source: "SecureHome SHL-500 Kapı Uyumluluk Ölçütleri (Bölüm 1.1)",
    keywords: ["kapı kalınlığı", "kalınlık", "kaç mm", "mm olmalı", "kapı payı", "kanat kalınlığı"]
  }
];

export const FALLBACK_ANSWER = {
  answer: "Bu bilgi SecureHome SHL-500 ürün belgelerinde bulunamadı.",
  source: "SecureHome SHL-500 Doğrulanmış Teknik Dökümantasyon"
};
