import React, { useState, useRef, useEffect } from "react";
import { X, Send, Shield, Sparkles, RotateCcw, ArrowRight, BookOpen } from "lucide-react";
import { READY_QUESTIONS } from "../data/chatbotAnswers";
import { AssistantApiError, queryProductAssistant } from "../services/productAssistant";

interface Message {
  id: string;
  sender: "user" | "assistant";
  text: string;
  source?: string;
  timestamp: string;
}

interface ProductChatProps {
  isOpen: boolean;
  onClose: () => void;
  productId: string;
}

export const ProductChat: React.FC<ProductChatProps> = ({ isOpen, onClose, productId }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "initial-greeting",
      sender: "assistant",
      text: "Merhaba! SecureHome SHL-500 Akıllı Kapı Kilidi ürün asistanıyım. Kapı uyumluluğu, vida seçimi, backset ayarı veya acil durum beslemesi hakkında aklınıza takılanları sorabilirsiniz.",
      source: "SecureHome SHL-500 Resmi Ürün Belgeleri",
      timestamp: "Şimdi"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      setTimeout(() => {
        inputRef.current?.focus();
      }, 200);
    }
  }, [isOpen, messages, isLoading]);

  const handleSendMessage = async (textToSend: string) => {
    const trimmed = textToSend.trim();
    if (!trimmed || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      sender: "user",
      text: trimmed,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response = await queryProductAssistant(trimmed, productId);
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        sender: "assistant",
        text: response.answer,
        source: response.source,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const isApiUnavailable =
        error instanceof AssistantApiError && error.status >= 500;
      const errorMessage: Message = {
        id: `err-${Date.now()}`,
        sender: "assistant",
        text: isApiUnavailable
          ? "Asistan şu anda yanıt üretemiyor. API limiti veya bağlantı sorunu olabilir. Lütfen biraz sonra tekrar deneyin."
          : "Bu bilgi SecureHome SHL-500 ürün belgelerinde bulunamadı.",
        source: isApiUnavailable
          ? "Mistral API / Chat servisi"
          : "SecureHome SHL-500 Doğrulanmış Teknik Dokümantasyon",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSendMessage(inputValue);
    }
  };

  const handleResetChat = () => {
    setMessages([
      {
        id: "initial-greeting",
        sender: "assistant",
        text: "Merhaba! SecureHome SHL-500 Akıllı Kapı Kilidi ürün asistanıyım. Kapı uyumluluğu, vida seçimi, backset ayarı veya acil durum beslemesi hakkında aklınıza takılanları sorabilirsiniz.",
        source: "SecureHome SHL-500 Resmi Ürün Belgeleri",
        timestamp: "Şimdi"
      }
    ]);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="fixed inset-0 bg-stone-900/30 backdrop-blur-xs transition-opacity"
        aria-hidden="true"
      />

      {/* Drawer Container: Slide from right on desktop, Bottom sheet on mobile */}
      <div
        className="relative z-10 w-full sm:w-[460px] h-[85vh] sm:h-full mt-auto sm:mt-0 bg-stone-50 border-t sm:border-t-0 sm:border-l border-stone-200/90 shadow-2xl flex flex-col rounded-t-2xl sm:rounded-none overflow-hidden animate-slideUp sm:animate-slideLeft transition-all"
        role="dialog"
        aria-modal="true"
        aria-labelledby="chat-title"
      >
        {/* Header */}
        <div className="p-4 sm:p-5 bg-white border-b border-stone-200 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-stone-900 text-white flex items-center justify-center shadow-xs">
              <Shield className="w-4 h-4" />
            </div>
            <div>
              <h2 id="chat-title" className="text-sm font-bold text-stone-950 leading-tight">
                SecureHome Ürün Asistanı
              </h2>
              <div className="text-[11px] text-stone-700 font-medium flex items-center gap-1.5 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
                <span>Yalnızca SHL-500 Teknik Veritabanı</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={handleResetChat}
              title="Sohbeti Temizle"
              className="p-2 text-stone-600 hover:text-stone-950 hover:bg-stone-100 rounded-lg transition-colors cursor-pointer"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
            <button
              onClick={onClose}
              title="Kapat"
              className="p-2 text-stone-600 hover:text-stone-950 hover:bg-stone-100 rounded-lg transition-colors cursor-pointer"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-4">
          {/* Quick Notice Badge */}
          <div className="p-2.5 rounded-xl bg-stone-100 border border-stone-200 text-xs text-stone-800 font-medium flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-stone-700 shrink-0" />
            <span>Asistan yalnızca doğrulanmış SHL-500 montaj ve donanım dökümanlarından yanıt verir.</span>
          </div>

          {messages.map((msg) => {
            const isUser = msg.sender === "user";
            return (
              <div
                key={msg.id}
                className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl px-4 py-3 text-xs sm:text-sm leading-relaxed ${
                    isUser
                      ? "bg-stone-900 text-white rounded-br-xs shadow-xs font-medium"
                      : "bg-white text-stone-950 border border-stone-200 rounded-bl-xs shadow-2xs font-normal"
                  }`}
                >
                  <p>{msg.text}</p>

                  {/* Kaynak Bölümü (Source section for assistant replies) */}
                  {!isUser && msg.source && (
                    <div className="mt-2.5 pt-2 border-t border-stone-200 text-[11px] text-stone-700 flex items-center gap-1.5 font-semibold">
                      <span className="text-stone-500 font-medium">Kaynak:</span>
                      <span className="truncate">{msg.source}</span>
                    </div>
                  )}
                </div>

                <span className="text-[10px] text-stone-500 font-medium mt-1 px-1">
                  {msg.timestamp}
                </span>
              </div>
            );
          })}

          {/* Loading Animation Bubble */}
          {isLoading && (
            <div className="flex flex-col items-start">
              <div className="bg-white border border-stone-200 rounded-2xl rounded-bl-xs px-4 py-3 shadow-2xs">
                <div className="flex items-center gap-1.5 py-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-stone-500 animate-bounce" />
                  <span
                    className="w-1.5 h-1.5 rounded-full bg-stone-500 animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <span
                    className="w-1.5 h-1.5 rounded-full bg-stone-500 animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
              <span className="text-[10px] text-stone-500 font-medium mt-1 px-1">
                Dökümanlar taranıyor...
              </span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Ready Questions Section (Hazır sorular) */}
        <div className="px-4 py-2.5 bg-stone-100 border-t border-stone-200 shrink-0">
          <div className="text-xs font-bold text-stone-800 mb-2">
            Önerilen Sorular
          </div>
          <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none">
            {READY_QUESTIONS.map((question) => (
              <button
                key={question}
                onClick={() => handleSendMessage(question)}
                disabled={isLoading}
                className="whitespace-nowrap px-3 py-1.5 rounded-lg bg-white hover:bg-stone-50 border border-stone-300 text-stone-900 font-semibold text-xs transition-colors shadow-2xs disabled:opacity-50 cursor-pointer"
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        {/* Input Bar */}
        <div className="p-3 sm:p-4 bg-white border-t border-stone-200 shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage(inputValue);
            }}
            className="flex items-center gap-2"
          >
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="SHL-500 hakkında soru sorun..."
              disabled={isLoading}
              className="flex-1 px-3.5 py-2.5 text-xs sm:text-sm bg-white border border-stone-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-stone-500 text-stone-950 placeholder:text-stone-400 font-medium"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="p-2.5 rounded-xl bg-stone-900 text-white hover:bg-stone-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all cursor-pointer shadow-xs active:scale-95"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
