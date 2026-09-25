import React from "react";
import {
  DoorClosed,
  SlidersHorizontal,
  BatteryCharging,
  Bluetooth,
  KeyRound,
  Fingerprint,
  ShieldAlert
} from "lucide-react";
import { FeatureItem } from "../data/product";

interface FeatureCardsProps {
  features: FeatureItem[];
}

export const FeatureCards: React.FC<FeatureCardsProps> = ({ features }) => {
  const getFeatureIcon = (id: string) => {
    switch (id) {
      case "door-thickness":
        return <DoorClosed className="w-5 h-5 text-stone-700" />;
      case "backset":
        return <SlidersHorizontal className="w-5 h-5 text-stone-700" />;
      case "usb-c":
        return <BatteryCharging className="w-5 h-5 text-stone-700" />;
      case "bluetooth":
        return <Bluetooth className="w-5 h-5 text-stone-700" />;
      case "pin":
        return <KeyRound className="w-5 h-5 text-stone-700" />;
      case "fingerprint":
        return <Fingerprint className="w-5 h-5 text-stone-700" />;
      case "ip54":
        return <ShieldAlert className="w-5 h-5 text-stone-700" />;
      default:
        return <DoorClosed className="w-5 h-5 text-stone-700" />;
    }
  };

  return (
    <section id="one-cikanlar" className="py-12 sm:py-16 border-b border-stone-200/80">
      <div className="space-y-8">
        {/* Section Header */}
        <div className="max-w-2xl space-y-2">
          <div className="text-xs font-bold tracking-wider uppercase text-stone-700">
            Öne Çıkan Nitelikler
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-stone-950">
            Gelişmiş Güvenlik ve Donanım Standartları
          </h2>
          <p className="text-sm text-stone-700 leading-relaxed">
            SecureHome SHL-500, mimari estetiği yüksek seviyeli mekanik ve dijital koruma bileşenleriyle bir araya getirir.
          </p>
        </div>

        {/* Features Grid: 7 Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-5">
          {features.map((item) => (
            <div
              key={item.id}
              className="p-5 rounded-xl bg-white border border-stone-200 hover:border-stone-400 shadow-2xs hover:shadow-xs transition-all flex flex-col justify-between"
            >
              <div>
                <div className="w-10 h-10 rounded-lg bg-stone-100 border border-stone-200 flex items-center justify-center mb-4">
                  {getFeatureIcon(item.id)}
                </div>
                <div className="text-[11px] font-bold text-stone-600 uppercase tracking-wide mb-1">
                  {item.category}
                </div>
                <h3 className="text-base font-bold text-stone-950 mb-1.5">
                  {item.title}
                </h3>
              </div>
              <p className="text-xs text-stone-700 leading-relaxed font-normal">
                {item.subtitle}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
