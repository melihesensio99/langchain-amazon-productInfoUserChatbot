class RagException(Exception):
    """RAG katmanındaki özel hataların temel sınıfıdır."""


class ConfigurationError(RagException):
    """Eksik veya hatalı uygulama konfigürasyonu hatasıdır."""

    pass
