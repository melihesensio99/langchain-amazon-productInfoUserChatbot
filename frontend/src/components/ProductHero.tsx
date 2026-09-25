import React from "react";
import { Star, MessageSquare, ShieldCheck, CheckCircle2, HelpCircle } from "lucide-react";
import { Product } from "../data/product";
import { ProductImages } from "./ProductImages";

interface ProductHeroProps {
  product: Product;
  onOpenAssistant: () => void;
}

export const ProductHero: React.FC<ProductHeroProps> = ({
  product,
  onOpenAssistant
}) => {
  return (
    <section id="genel-bakis" className="pt-6 pb-12 sm:pb-16 border-b border-stone-200/80">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
        {/* Left Column: Product Images Gallery (lg: 7 cols) */}
        <div className="lg:col-span-7">
          <ProductImages />
        </div>

        {/* Right Column: Product Detail & Purchase Context (lg: 5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          {/* Brand & Category Hierarchy - High Contrast & Crisp Readability */}
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2 text-xs font-semibold text-stone-700">
              <span className="uppercase tracking-wider font-bold text-stone-900 bg-stone-100 px-2 py-0.5 rounded border border-stone-200">
                {product.brand}
              </span>
              <span className="text-stone-400" aria-hidden="true">·</span>
              <span className="text-stone-800 font-medium">{product.type}</span>
              <span className="text-stone-400" aria-hidden="true">·</span>
              <span className="font-mono text-stone-600 bg-stone-100 px-1.5 py-0.5 rounded border border-stone-200 text-[11px]">
                {product.id}
              </span>
            </div>

            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-stone-950 text-balance leading-tight">
              {product.name}
            </h1>
          </div>

          {/* Ratings & Social Proof (Clean & Legible) */}
          <div className="flex items-center gap-3 text-sm">
            <div className="flex items-center text-amber-500 gap-0.5">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < 4
                      ? "fill-amber-400 text-amber-500"
                      : i === 4
                      ? "fill-amber-400/50 text-amber-500"
                      : "text-stone-300"
                  }`}
                />
              ))}
            </div>
            <span className="font-bold text-stone-950 tabular-nums">
              4.2
            </span>
            <span className="text-stone-400" aria-hidden="true">
              ·
            </span>
            <a
              href="#yorumlar"
              className="text-stone-700 hover:text-stone-950 underline underline-offset-2 font-semibold text-xs transition-colors"
            >
              50 doğrulanmış kullanıcı değerlendirmesi
            </a>
          </div>

          {/* Pricing & Stock Status */}
          <div className="p-4 sm:p-5 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-2.5">
            <div className="flex items-baseline gap-2.5">
              <span className="text-xs text-stone-600 font-semibold">Tavsiye Edilen Satış Fiyatı</span>
              <div className="text-2xl sm:text-3xl font-extrabold tracking-tight text-stone-950 tabular-nums">
                {product.currency}{product.mockPrice}
              </div>
              <span className="text-xs text-stone-500 font-medium">KDV Dahil</span>
            </div>

            <div className="flex items-center gap-2 text-xs text-emerald-900 font-semibold bg-emerald-50/80 border border-emerald-200/70 px-2.5 py-1.5 rounded-lg w-fit">
              <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
              <span>{product.stockStatusText}</span>
            </div>
          </div>

          {/* Short Description */}
          <p className="text-sm leading-relaxed text-stone-700 font-normal">
            {product.shortDescription}
          </p>

          {/* Quick Specifications Snapshot with High Contrast */}
          <div className="grid grid-cols-2 gap-2.5 text-xs">
            <div className="p-3 rounded-lg bg-white border border-stone-200 shadow-2xs">
              <span className="block text-stone-500 text-[11px] font-medium mb-0.5">Kapı Kalınlığı</span>
              <span className="font-bold text-stone-900 text-xs sm:text-sm">{product.specifications.doorThickness}</span>
            </div>
            <div className="p-3 rounded-lg bg-white border border-stone-200 shadow-2xs">
              <span className="block text-stone-500 text-[11px] font-medium mb-0.5">Backset Mesafesi</span>
              <span className="font-bold text-stone-900 text-xs sm:text-sm">{product.specifications.backset}</span>
            </div>
            <div className="p-3 rounded-lg bg-white border border-stone-200 shadow-2xs">
              <span className="block text-stone-500 text-[11px] font-medium mb-0.5">Kullanıcı Kapasitesi</span>
              <span className="font-bold text-stone-900 text-xs sm:text-sm">50 Parmak İzi + 100 PIN</span>
            </div>
            <div className="p-3 rounded-lg bg-white border border-stone-200 shadow-2xs">
              <span className="block text-stone-500 text-[11px] font-medium mb-0.5">Acil Durum Desteği</span>
              <span className="font-bold text-stone-900 text-xs sm:text-sm">{product.specifications.emergencyPower}</span>
            </div>
          </div>

          {/* Primary Action: Product Assistant CTA (Strictly NO Cart or Buy Button) */}
          <div className="pt-2">
            <button
              onClick={onOpenAssistant}
              className="w-full py-3.5 px-5 rounded-xl bg-stone-950 hover:bg-stone-850 text-white text-sm font-semibold flex items-center justify-center gap-2.5 shadow-sm transition-all cursor-pointer active:scale-99"
            >
              <MessageSquare className="w-4 h-4 text-stone-200" />
              <span>Ürün Asistanına Sor</span>
            </button>
            <p className="mt-2.5 text-center text-xs text-stone-600 font-medium">
              Ölçüler, vida seçimi, adaptör ve uyumluluk için anında teknik yanıt alın.
            </p>
          </div>

          {/* Verified Guarantee trust markers */}
          <div className="pt-3 border-t border-stone-200 flex flex-wrap items-center justify-between gap-2 text-xs text-stone-700 font-medium">
            <div className="flex items-center gap-1.5">
              <ShieldCheck className="w-4 h-4 text-stone-800" />
              <span>2 Yıl Resmi Üretici Garantisi</span>
            </div>
            <div className="flex items-center gap-1.5">
              <HelpCircle className="w-4 h-4 text-stone-800" />
              <span>Teknik Kurulum Rehberliği</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
