export interface AssistantResponse {
  answer: string;
  source: string;
}

interface BackendSource {
  product_id?: string;
  product_name?: string;
  source_type?: string;
  source_file?: string;
  section?: string;
}

interface ChatResponse {
  answer: string;
  sources?: BackendSource[];
}

export class AssistantApiError extends Error {
  constructor(public readonly status: number) {
    super(`Chat API hatası: ${status}`);
    this.name = "AssistantApiError";
  }
}

function formatSources(sources: BackendSource[] = []): string {
  const formatted = sources
    .map((source) => [source.source_file, source.section].filter(Boolean).join(" · "))
    .filter(Boolean);

  return formatted.length > 0
    ? formatted.join(" | ")
    : "SecureHome SHL-500 ürün belgeleri";
}

/** Ürün ID'sini backend'e göndererek gerçek RAG chatbotunu çağırır. */
export async function queryProductAssistant(
  userQuery: string,
  productId: string,
): Promise<AssistantResponse> {
  const response = await fetch("/api/v1/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question: userQuery,
      product_id: productId,
    }),
  });

  if (!response.ok) {
    throw new AssistantApiError(response.status);
  }

  const data = (await response.json()) as ChatResponse;
  return {
    answer: data.answer,
    source: formatSources(data.sources),
  };
}
