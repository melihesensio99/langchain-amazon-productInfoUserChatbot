export interface ProductSpecifications {
  doorThickness: string;
  recommendedDoorThickness: string;
  backset: string;
  boreHole: string;
  adapter: string;
  emergencyPower: string;
  connectivity: string;
  battery: string;
  protection: string;
  pinCapacity: string;
  fingerprintCapacity: string;
}

export interface FeatureItem {
  id: string;
  title: string;
  subtitle: string;
  category: string;
}

export interface Product {
  id: string;
  name: string;
  brand: string;
  type: string;
  rating: number;
  reviewCount: number;
  mockPrice: string;
  currency: string;
  inStock: boolean;
  stockStatusText: string;
  shortDescription: string;
  specifications: ProductSpecifications;
  highlightFeatures: FeatureItem[];
}

export const product: Product = {
  // Geçici demo ID'si: ürün oluşturma endpoint'inin PostgreSQL'de ürettiği gerçek ID.
  id: "3ca19032-7a98-4564-a342-9f8f06c6fa3c",
  name: "SecureHome SHL-500 Smart Lock",
  brand: "SecureHome",
  type: "Akıllı kapı kilidi",
  rating: 4.7,
  reviewCount: 128,
  mockPrice: "4.850",
  currency: "₺",
  inStock: true,
  stockStatusText: "Stokta Var · Ücretsiz Kargo",
  shortDescription:
    "Gelişmiş biyometrik tanıma, çift mandallı ayarlanabilir backset mekanizması ve USB-C acil durum güç desteğiyle tasarlanmış, konut ve ofis kapılarına uyumlu birinci sınıf akıllı kapı kilidi.",
  specifications: {
    doorThickness: "35–55 mm",
    recommendedDoorThickness: "40–50 mm",
    backset: "60 mm / 70 mm",
    boreHole: "54 mm",
    adapter: "38 mm delik için adaptör halkası",
    emergencyPower: "USB-C, 5V / 1A",
    connectivity: "Bluetooth 5.0",
    battery: "4 adet AA alkalin pil (1.5V)",
    protection: "IP54 toza ve su sıçramasına dayanıklı",
    pinCapacity: "100 PIN kodu desteği",
    fingerprintCapacity: "50 parmak izi desteği"
  },
  highlightFeatures: [
    {
      id: "door-thickness",
      title: "35–55 mm Kapı Uyumluluğu",
      subtitle: "Önerilen 40–50 mm standart kanat kalınlığı",
      category: "Montaj"
    },
    {
      id: "backset",
      title: "60 / 70 mm Backset",
      subtitle: "Ayarlanabilir gömme kilit dili",
      category: "Mekanizma"
    },
    {
      id: "usb-c",
      title: "USB-C Acil Güç",
      subtitle: "Pil bitiminde 5V / 1A harici besleme girişi",
      category: "Güvenlik"
    },
    {
      id: "bluetooth",
      title: "Bluetooth 5.0",
      subtitle: "Düşük enerji tüketimli doğrudan yerel bağlantı",
      category: "Bağlantı"
    },
    {
      id: "pin",
      title: "100 PIN Desteği",
      subtitle: "Misafir, geçici ve kalıcı şifre yönetimi",
      category: "Erişim"
    },
    {
      id: "fingerprint",
      title: "50 Parmak İzi",
      subtitle: "Kulp üzeri yarı iletken biyometrik okuyucu",
      category: "Biyometri"
    },
    {
      id: "ip54",
      title: "IP54 Koruma",
      subtitle: "Dış mekan su sıçramaları ve toza karşı dayanım",
      category: "Dayanıklılık"
    }
  ]
};
