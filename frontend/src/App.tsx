import React, { useState } from "react";
import { MessageSquare } from "lucide-react";
import { product } from "./data/product";
import { Navbar } from "./components/Navbar";
import { ProductHero } from "./components/ProductHero";
import { FeatureCards } from "./components/FeatureCards";
import { ProductSpecs } from "./components/ProductSpecs";
import { ProductReviews } from "./components/ProductReviews";
import { ProductChat } from "./components/ProductChat";

export default function App() {
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [themeMode, setThemeMode] = useState<"light" | "warm">("light");

  const toggleTheme = () => {
    setThemeMode((prev) => (prev === "light" ? "warm" : "light"));
  };

  const handleOpenAssistant = () => {
    setIsAssistantOpen(true);
  };

  const handleCloseAssistant = () => {
    setIsAssistantOpen(false);
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        themeMode === "light"
          ? "bg-[#FAF9F5] text-stone-900"
          : "bg-[#F4EFEB] text-stone-900"
      }`}
    >
      {/* Top Navbar */}
      <Navbar
        onOpenAssistant={handleOpenAssistant}
        themeMode={themeMode}
        onToggleTheme={toggleTheme}
      />

      {/* Main Product Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-8">
        {/* Main Product Section: Images (left) & Details + Assistant CTA (right) */}
        <ProductHero
          product={product}
          onOpenAssistant={handleOpenAssistant}
        />

        {/* Feature Cards Grid (No installation steps here) */}
        <FeatureCards features={product.highlightFeatures} />

        {/* Technical Specifications Table & Kurulum Yönlendirmesi */}
        <ProductSpecs
          specs={product.specifications}
          onOpenAssistant={handleOpenAssistant}
        />

        {/* Customer Reviews Section (50 uncategorized reviews: 30 positive, 10 negative, 10 neutral) */}
        <ProductReviews />
      </main>

      {/* Floating Quick Action Button for Assistant (Responsive bottom-right) */}
      <div className="fixed bottom-6 right-6 z-40">
        <button
          onClick={handleOpenAssistant}
          className="flex items-center gap-2.5 px-4 py-3 rounded-full bg-stone-900 hover:bg-stone-850 text-white shadow-lg hover:shadow-xl transition-all cursor-pointer active:scale-95 group"
          aria-label="SecureHome Ürün Asistanı"
        >
          <div className="relative">
            <MessageSquare className="w-4 h-4 text-stone-200 group-hover:text-white transition-colors" />
            <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400" />
          </div>
          <span className="text-xs font-semibold tracking-wide whitespace-nowrap">
            Ürün Asistanı
          </span>
        </button>
      </div>

      {/* Quiet Footer */}
      <footer className="mt-16 border-t border-stone-200/80 bg-stone-100/50 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-stone-500">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-stone-700">SecureHome</span>
            <span>·</span>
            <span>SHL-500 Akıllı Kapı Kilidi Resmi Ürün Dökümantasyon Portalı</span>
          </div>
          <div>
            © {new Date().getFullYear()} SecureHome Systems. Tüm hakları saklıdır.
          </div>
        </div>
      </footer>

      {/* Product Chatbot Drawer / Modal */}
      <ProductChat
        isOpen={isAssistantOpen}
        onClose={handleCloseAssistant}
        productId={product.id}
      />
    </div>
  );
}
