import React from "react";
import { MessageSquare, FileCheck2, HelpCircle } from "lucide-react";
import { ProductSpecifications } from "../data/product";

interface ProductSpecsProps {
  specs: ProductSpecifications;
  onOpenAssistant: () => void;
}

export const ProductSpecs: React.FC<ProductSpecsProps> = ({
  specs,
  onOpenAssistant
}) => {
  const specList = [
    { label: "Kapı Kalınlığı", value: specs.doorThickness, note: `Önerilen: ${specs.recommendedDoorThickness}` },
    { label: "Backset Mesafesi", value: specs.backset, note: "Ayarlanabilir gömme sürgü" },
    { label: "Standart Delik Çapı", value: specs.boreHole, note: "Standart kapı delik normu" },
    { label: "38 mm Adaptör Desteği", value: specs.adapter, note: "Kutu içeriğine dahildir" },
    { label: "Acil Güç Bağlantısı", value: specs.emergencyPower, note: "Harici powerbank veya adaptör" },
    { label: "Pil Tipi & Adedi", value: specs.battery, note: "Standart 1.5V silindirik piller" },
    { label: "Bluetooth Bağlantısı", value: specs.connectivity, note: "Doğrudan yerel BLE eşleşmesi" },
    { label: "Koruma Sınıfı", value: specs.protection, note: "Toz ve sıçrayan sulara dayanıklı" },
    { label: "PIN Kapasitesi", value: specs.pinCapacity, note: "Farklı erişim rolleri tanımlanabilir" },
    { label: "Parmak İzi Kapasitesi", value: specs.fingerprintCapacity, note: "Hızlı biyometrik okuma (≤0.3s)" }
  ];

  return (
    <section id="teknik-ozellikler" className="py-12 sm:py-16 border-b border-stone-200/80">
      <div className="space-y-12">
        {/* Section Header */}
        <div className="max-w-2xl space-y-2">
          <div className="text-xs font-bold tracking-wider uppercase text-stone-700">
            Detaylı Parametreler
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-stone-950">
            Teknik Özellikler
          </h2>
          <p className="text-sm text-stone-700 leading-relaxed font-normal">
            SecureHome SHL-500 modelinin fiziksel, elektriksel ve operasyonel verileri.
          </p>
        </div>

        {/* Clean Specifications Table */}
        <div className="rounded-2xl border border-stone-200 bg-white overflow-hidden shadow-2xs">
          <div className="divide-y divide-stone-200">
            {specList.map((item, index) => (
              <div
                key={item.label}
                className={`grid grid-cols-1 sm:grid-cols-12 px-6 py-4 items-center gap-2 sm:gap-4 transition-colors ${
                  index % 2 === 0 ? "bg-white" : "bg-stone-50/70"
                } hover:bg-stone-100/60`}
              >
                <div className="sm:col-span-4 text-xs sm:text-sm font-bold text-stone-900">
                  {item.label}
                </div>
                <div className="sm:col-span-4 text-sm font-extrabold text-stone-950 font-mono sm:font-sans">
                  {item.value}
                </div>
                <div className="sm:col-span-4 text-xs font-medium text-stone-600">
                  {item.note}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Kurulum Yönlendirmesi (Installation Support Banner) */}
        <div
          id="kurulum-destek"
          className="rounded-2xl bg-white border border-stone-200 p-6 sm:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 shadow-2xs"
        >
          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2 text-stone-800 font-bold text-xs uppercase tracking-wide">
              <HelpCircle className="w-4 h-4 text-stone-800" />
              <span>Teknik Danışma & Uyumluluk</span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold text-stone-950 tracking-tight">
              Kurulum veya uyumluluk hakkında sorunuz mu var?
            </h3>
            <p className="text-sm text-stone-700 font-normal leading-relaxed">
              Kapı kalınlığı, vida seçimi, delik çapı, backset ayarı ve acil açma prosedürleri hakkında bilgi almak için Ürün Asistanı’na danışın.
            </p>
          </div>

          <button
            onClick={onOpenAssistant}
            className="shrink-0 px-6 py-3.5 rounded-xl bg-stone-950 hover:bg-stone-850 text-white text-sm font-semibold flex items-center gap-2.5 shadow-sm transition-all cursor-pointer active:scale-98"
          >
            <MessageSquare className="w-4 h-4 text-stone-200" />
            <span>Ürün Asistanına Sor</span>
          </button>
        </div>
      </div>
    </section>
  );
};
