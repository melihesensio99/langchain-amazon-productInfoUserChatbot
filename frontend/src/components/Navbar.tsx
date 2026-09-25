import React from "react";
import { Shield, MessageSquare, Sun, Moon } from "lucide-react";

interface NavbarProps {
  onOpenAssistant: () => void;
  themeMode: "light" | "warm";
  onToggleTheme: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenAssistant,
  themeMode,
  onToggleTheme
}) => {
  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <header className="sticky top-0 z-30 w-full backdrop-blur-md bg-white/95 border-b border-stone-200/90 shadow-2xs transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Zone 1: Brand title & Model */}
        <div className="flex items-center gap-3">
          <a
            href="#"
            className="flex items-center gap-2.5 group transition-colors"
          >
            <span className="w-8 h-8 rounded-lg bg-stone-900 text-white flex items-center justify-center font-bold tracking-wider text-sm shadow-sm group-hover:bg-stone-800 transition-colors">
              <Shield className="w-4 h-4 stroke-[2.4]" />
            </span>
            <span className="text-lg font-bold tracking-tight text-stone-950">
              SecureHome
            </span>
          </a>
          <span className="hidden sm:inline-block text-stone-400 font-normal text-sm" aria-hidden="true">
            /
          </span>
          <span className="hidden sm:inline-block text-xs font-semibold text-stone-700 bg-stone-100 px-2 py-0.5 rounded border border-stone-200 tracking-wide">
            SHL-500 Smart Lock
          </span>
        </div>

        {/* Zone 2: Nav links with strong contrast & legible hover states */}
        <nav className="hidden md:flex items-center gap-1 sm:gap-2 text-sm font-semibold text-stone-800">
          <button
            onClick={() => scrollToSection("genel-bakis")}
            className="px-3 py-1.5 rounded-lg hover:bg-stone-100 hover:text-stone-950 transition-colors cursor-pointer"
          >
            Genel Bakış
          </button>
          <button
            onClick={() => scrollToSection("one-cikanlar")}
            className="px-3 py-1.5 rounded-lg hover:bg-stone-100 hover:text-stone-950 transition-colors cursor-pointer"
          >
            Öne Çıkanlar
          </button>
          <button
            onClick={() => scrollToSection("teknik-ozellikler")}
            className="px-3 py-1.5 rounded-lg hover:bg-stone-100 hover:text-stone-950 transition-colors cursor-pointer"
          >
            Teknik Özellikler
          </button>
          <button
            onClick={() => scrollToSection("kurulum-destek")}
            className="px-3 py-1.5 rounded-lg hover:bg-stone-100 hover:text-stone-950 transition-colors cursor-pointer"
          >
            Kurulum & Destek
          </button>
          <button
            onClick={() => scrollToSection("yorumlar")}
            className="px-3 py-1.5 rounded-lg hover:bg-stone-100 hover:text-stone-950 transition-colors cursor-pointer"
          >
            Yorumlar (50)
          </button>
        </nav>

        {/* Zone 3: Primary Actions */}
        <div className="flex items-center gap-2">
          {/* Theme Toggle Button */}
          <button
            onClick={onToggleTheme}
            aria-label="Görünüm Tonunu Değiştir"
            title={`Mevcut: ${themeMode === "light" ? "Minimal Beyaz" : "Sıcak Bej"}`}
            className="p-2 text-stone-700 hover:text-stone-950 bg-stone-50 hover:bg-stone-100 border border-stone-200 rounded-lg transition-colors cursor-pointer"
          >
            {themeMode === "light" ? (
              <Sun className="w-4 h-4 stroke-[2]" />
            ) : (
              <Moon className="w-4 h-4 stroke-[2]" />
            )}
          </button>

          {/* Product Assistant CTA */}
          <button
            onClick={onOpenAssistant}
            className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold text-stone-950 bg-stone-100 hover:bg-stone-200 border border-stone-300 rounded-lg transition-all shadow-xs cursor-pointer active:scale-98"
          >
            <MessageSquare className="w-3.5 h-3.5 text-stone-800" />
            <span className="whitespace-nowrap">Ürün Asistanı</span>
          </button>
        </div>
      </div>
    </header>
  );
};
