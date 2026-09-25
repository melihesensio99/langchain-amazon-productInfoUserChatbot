import React, { useState } from "react";
import { Star, CheckCircle, ChevronDown } from "lucide-react";
import { REVIEWS, ReviewItem } from "../data/reviews";

export const ProductReviews: React.FC = () => {
  // Show 12 reviews initially, then load more
  const [visibleCount, setVisibleCount] = useState<number>(12);

  const visibleReviews = REVIEWS.slice(0, visibleCount);

  // Compute average score from the 50 reviews
  const totalRating = REVIEWS.reduce((acc, curr) => acc + curr.rating, 0);
  const averageRating = (totalRating / REVIEWS.length).toFixed(1);

  const handleLoadMore = () => {
    setVisibleCount((prev) => Math.min(prev + 12, REVIEWS.length));
  };

  return (
    <section id="yorumlar" className="py-12 sm:py-16 border-b border-stone-200/80">
      <div className="space-y-8">
        {/* Section Header with Overall Score Summary */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-4 border-b border-stone-200">
          <div className="space-y-2 max-w-xl">
            <div className="text-xs font-bold tracking-wider uppercase text-stone-700">
              Kullanıcı Deneyimleri
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold tracking-tight text-stone-950">
              Müşteri Değerlendirmeleri
            </h2>
            <p className="text-sm text-stone-700 font-normal leading-relaxed">
              SecureHome SHL-500 kullanıcılarının montaj, kullanım kolaylığı ve güvenlik deneyimleri.
            </p>
          </div>

          {/* Average Rating Scorecard */}
          <div className="flex items-center gap-4 bg-white p-3.5 sm:p-4 rounded-xl border border-stone-200 shadow-2xs shrink-0">
            <div className="text-3xl font-extrabold text-stone-950 tabular-nums">
              {averageRating}
            </div>
            <div className="flex flex-col justify-center">
              <div className="flex items-center text-amber-500 gap-0.5 mb-1">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-3.5 h-3.5 ${
                      i < Math.round(Number(averageRating))
                        ? "fill-amber-400 text-amber-500"
                        : "text-stone-300"
                    }`}
                  />
                ))}
              </div>
              <span className="text-xs font-semibold text-stone-700 tabular-nums">
                Toplam {REVIEWS.length} değerlendirme
              </span>
            </div>
          </div>
        </div>

        {/* Reviews Grid (No category tags, purely clean review cards) */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
          {visibleReviews.map((rev: ReviewItem) => (
            <div
              key={rev.id}
              className="p-5 rounded-xl bg-white border border-stone-200 hover:border-stone-300 shadow-2xs hover:shadow-xs transition-all flex flex-col justify-between"
            >
              <div>
                {/* Header: Stars + Date */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="flex items-center text-amber-500 gap-0.5">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-3.5 h-3.5 ${
                          i < rev.rating
                            ? "fill-amber-400 text-amber-500"
                            : "text-stone-200 fill-stone-100"
                        }`}
                      />
                    ))}
                  </div>
                  <span className="text-[11px] font-medium text-stone-500">
                    {rev.date}
                  </span>
                </div>

                {/* Comment Text */}
                <p className="text-xs sm:text-sm text-stone-800 leading-relaxed font-normal">
                  {rev.comment}
                </p>
              </div>

              {/* Author & Verified Purchase Info */}
              <div className="mt-4 pt-3 border-t border-stone-100 flex items-center justify-between text-xs">
                <span className="font-bold text-stone-900">
                  {rev.author}
                </span>

                {rev.verifiedPurchase && (
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-emerald-800">
                    <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Doğrulanmış Alıcı</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Load More Button */}
        {visibleCount < REVIEWS.length && (
          <div className="pt-4 text-center">
            <button
              onClick={handleLoadMore}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-white hover:bg-stone-50 text-stone-900 font-semibold text-xs sm:text-sm border border-stone-300 shadow-2xs transition-all cursor-pointer active:scale-98"
            >
              <span>Daha Fazla Yorum Göster ({visibleCount}/{REVIEWS.length})</span>
              <ChevronDown className="w-4 h-4 text-stone-600" />
            </button>
          </div>
        )}
      </div>
    </section>
  );
};
