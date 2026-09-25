import React, { useState } from "react";
import { ShieldCheck, DoorClosed, Cpu, Sparkles } from "lucide-react";

export const ProductImages: React.FC = () => {
  const [activeImageIndex, setActiveImageIndex] = useState(0);

  const images = [
    {
      id: "studio",
      title: "SecureHome SHL-500 Studio",
      label: "Ön Gövde & Kulp",
      description: "Dokunmatik tuş takımı ve biyometrik parmak izi kulpu"
    },
    {
      id: "door",
      title: "Kapı Üzerinde Montaj",
      label: "Kapı Uygulaması",
      description: "35–55 mm ahşap kanat üzerinde minimalist duruş"
    },
    {
      id: "detail",
      title: "Backset & Acil Güç",
      label: "Mekanizma Detayı",
      description: "USB-C 5V acil besleme ve 60/70 mm ayarlanabilir dil"
    }
  ];

  return (
    <div className="flex flex-col gap-4">
      {/* Main Large Visual Stage */}
      <div className="relative w-full aspect-[4/3] rounded-2xl bg-stone-100/80 border border-stone-200/80 overflow-hidden flex items-center justify-center p-6 sm:p-10 transition-all select-none">
        {/* Visual 1: Studio Shot */}
        {activeImageIndex === 0 && (
          <div className="relative w-full h-full flex items-center justify-center animate-fadeIn">
            {/* Soft backdrop ambient light */}
            <div className="absolute w-64 h-64 rounded-full bg-stone-200/60 blur-3xl pointer-events-none" />

            {/* Smart Lock Main Body Graphic */}
            <div className="relative flex flex-col items-center">
              {/* Top Escutcheon Panel */}
              <div className="w-28 sm:w-32 h-64 sm:h-72 rounded-3xl bg-gradient-to-b from-stone-900 via-stone-850 to-stone-950 p-2.5 shadow-xl border border-stone-700/60 flex flex-col items-center justify-between relative">
                {/* Brand Logo & Status indicator */}
                <div className="w-full flex items-center justify-between px-2 pt-1">
                  <span className="text-[9px] font-mono tracking-widest text-stone-400">SHL-500</span>
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                </div>

                {/* Backlit Touch Keypad */}
                <div className="grid grid-cols-3 gap-2 sm:gap-2.5 w-full px-2 py-1 text-center font-mono text-stone-200 text-xs">
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">1</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">2</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">3</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">4</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">5</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">6</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">7</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">8</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">9</span>
                  <span className="py-1 text-stone-400 font-sans text-[10px]">*</span>
                  <span className="py-1 rounded bg-stone-800/80 border border-stone-700/40">0</span>
                  <span className="py-1 text-stone-400 font-sans text-[10px]">#</span>
                </div>

                {/* Handle Pivot with Fingerprint Scanner */}
                <div className="w-full flex items-center justify-start relative pt-2 pb-1">
                  {/* Lever Handle extending to right */}
                  <div className="absolute left-8 w-36 sm:w-44 h-8 rounded-r-xl bg-gradient-to-r from-stone-850 to-stone-900 border-y border-r border-stone-700/70 shadow-lg flex items-center px-3 z-10">
                    {/* Fingerprint Sensor on Handle Thumb Rest */}
                    <div className="w-5 h-5 rounded-full border border-stone-600 bg-stone-950 flex items-center justify-center relative">
                      <div className="w-3.5 h-3.5 rounded-full border border-stone-700 flex items-center justify-center">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400/90 shadow-[0_0_6px_rgba(52,211,153,0.7)]" />
                      </div>
                    </div>
                    <span className="ml-2 text-[9px] font-sans tracking-wide text-stone-400 select-none">
                      Biyometrik Sensör
                    </span>
                  </div>

                  {/* Circular Pivot Collar */}
                  <div className="w-12 h-12 rounded-full bg-stone-800 border border-stone-600 flex items-center justify-center shadow-inner ml-2">
                    <div className="w-6 h-6 rounded-full bg-stone-900 border border-stone-700" />
                  </div>
                </div>

                {/* Emergency USB-C & Key Cylinder Cap */}
                <div className="w-full flex items-center justify-center pb-1 text-stone-500 text-[9px]">
                  <span className="tracking-widest uppercase">SecureHome</span>
                </div>
              </div>

              {/* Bottom USB-C Port indicator */}
              <div className="mt-1 flex items-center gap-1.5 text-[10px] text-stone-500 font-medium">
                <span className="w-2 h-1 rounded bg-stone-400" />
                <span>USB-C Acil Güç Portu (Alt Panel)</span>
              </div>
            </div>

            {/* Floating Quality Callout */}
            <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-xs px-2.5 py-1.5 rounded-lg border border-stone-200/80 shadow-xs flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-stone-700" />
              <span className="text-[11px] font-medium text-stone-700">Çinko Alaşım & IP54</span>
            </div>
          </div>
        )}

        {/* Visual 2: Door Installation View */}
        {activeImageIndex === 1 && (
          <div className="relative w-full h-full flex items-center justify-center animate-fadeIn">
            {/* Door Surface Representation */}
            <div className="w-full h-full rounded-xl bg-gradient-to-r from-amber-900/15 via-amber-800/10 to-amber-900/20 border border-amber-900/10 flex items-center justify-center relative overflow-hidden">
              {/* Wood Grain Lines */}
              <div className="absolute inset-0 opacity-15 pointer-events-none bg-[radial-gradient(#78350f_1px,transparent_1px)] [background-size:16px_16px]" />

              {/* Door Frame Edge */}
              <div className="absolute right-0 top-0 bottom-0 w-8 border-l border-stone-300/60 bg-stone-200/40" />

              {/* Installed Lock Representation */}
              <div className="relative flex items-center">
                {/* Escutcheon on Wood */}
                <div className="w-24 sm:w-28 h-56 sm:h-64 rounded-2xl bg-stone-900 border border-stone-700 shadow-2xl p-2 flex flex-col justify-between items-center">
                  <div className="w-full text-center pt-1">
                    <span className="text-[8px] text-stone-400 font-mono">SECUREHOME</span>
                  </div>

                  <div className="w-16 h-20 rounded-lg bg-stone-950/80 border border-stone-800 flex items-center justify-center p-1">
                    <div className="grid grid-cols-3 gap-1 text-[8px] text-stone-300 font-mono">
                      <span>•</span><span>•</span><span>•</span>
                      <span>•</span><span>•</span><span>•</span>
                      <span>•</span><span>•</span><span>•</span>
                    </div>
                  </div>

                  {/* Handle with Hand Icon simulation */}
                  <div className="w-full relative h-10 flex items-center">
                    <div className="w-10 h-10 rounded-full bg-stone-800 border border-stone-600" />
                    <div className="absolute left-6 w-32 h-7 bg-stone-850 rounded-r-lg border border-stone-700 shadow-md flex items-center px-2">
                      <div className="w-3 h-3 rounded-full bg-emerald-400/80" />
                    </div>
                  </div>

                  <div className="text-[8px] text-stone-500 pb-1">
                    40–50 mm Önerilen
                  </div>
                </div>

                {/* Door Thickness callout */}
                <div className="ml-6 hidden sm:flex flex-col gap-1 text-xs text-stone-600">
                  <div className="font-semibold text-stone-800 flex items-center gap-1.5">
                    <DoorClosed className="w-4 h-4 text-stone-600" />
                    Standart Kapı Uyumu
                  </div>
                  <p className="text-[11px] text-stone-500 max-w-[150px] leading-relaxed">
                    35–55 mm arası tüm ahşap, çelik ve kompozit kapılara doğrudan montaj.
                  </p>
                </div>
              </div>
            </div>

            {/* Badge */}
            <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-xs px-2.5 py-1.5 rounded-lg border border-stone-200/80 shadow-xs flex items-center gap-2">
              <DoorClosed className="w-3.5 h-3.5 text-stone-700" />
              <span className="text-[11px] font-medium text-stone-700">35–55 mm Ahşap / Çelik Kapı</span>
            </div>
          </div>
        )}

        {/* Visual 3: Backset & Technical Detail */}
        {activeImageIndex === 2 && (
          <div className="relative w-full h-full flex items-center justify-center animate-fadeIn">
            <div className="w-full h-full rounded-xl bg-stone-100 flex flex-col items-center justify-center p-4">
              <div className="flex items-center gap-6 sm:gap-10">
                {/* Latch Mechanism */}
                <div className="flex flex-col items-center">
                  <div className="w-32 h-14 rounded-lg bg-stone-800 border border-stone-600 shadow-md flex items-center justify-between px-3 relative">
                    {/* Adjustable 60 / 70 mm latch */}
                    <div className="w-6 h-6 rounded bg-stone-400 border border-stone-300" />
                    <div className="text-[10px] font-mono text-stone-300 text-center">
                      <span>BACKSET</span>
                      <div className="text-amber-400 font-bold">60 / 70 mm</div>
                    </div>
                    <div className="w-4 h-8 rounded-r bg-stone-300 border-l border-stone-400" />
                  </div>
                  <span className="mt-2 text-[10px] text-stone-600 font-medium">
                    Ayarlanabilir Sürgü Dili
                  </span>
                </div>

                {/* Emergency Port Diagram */}
                <div className="flex flex-col items-center">
                  <div className="w-20 h-20 rounded-xl bg-stone-900 border border-stone-700 p-2 flex flex-col items-center justify-center gap-1 shadow-md">
                    <span className="text-[9px] text-stone-400 font-mono">USB-C</span>
                    <div className="w-6 h-2 rounded-full border border-stone-500 bg-stone-950 flex items-center justify-center">
                      <div className="w-3 h-0.5 bg-stone-400 rounded-full" />
                    </div>
                    <span className="text-[8px] text-stone-400">5V / 1A</span>
                  </div>
                  <span className="mt-2 text-[10px] text-stone-600 font-medium">
                    Acil Harici Besleme
                  </span>
                </div>
              </div>

              <div className="mt-4 text-center text-xs text-stone-500">
                <span>Standart 54 mm delik çapı · 38 mm delik adaptör halkası dahil</span>
              </div>
            </div>

            {/* Badge */}
            <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-xs px-2.5 py-1.5 rounded-lg border border-stone-200/80 shadow-xs flex items-center gap-2">
              <Cpu className="w-3.5 h-3.5 text-stone-700" />
              <span className="text-[11px] font-medium text-stone-700">Mekanizma & Acil Güç</span>
            </div>
          </div>
        )}
      </div>

      {/* Thumbnails Row */}
      <div className="grid grid-cols-3 gap-3">
        {images.map((img, idx) => {
          const isActive = idx === activeImageIndex;
          return (
            <button
              key={img.id}
              onClick={() => setActiveImageIndex(idx)}
              className={`p-3 rounded-xl text-left border transition-all cursor-pointer ${
                isActive
                  ? "bg-white border-stone-900 shadow-sm ring-1 ring-stone-900/10"
                  : "bg-white/80 hover:bg-white border-stone-200 text-stone-700 hover:text-stone-950 shadow-2xs"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-stone-950">
                  {img.label}
                </span>
                {isActive && (
                  <span className="w-1.5 h-1.5 rounded-full bg-stone-900" />
                )}
              </div>
              <p className="text-[11px] text-stone-600 font-medium line-clamp-1">
                {img.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
