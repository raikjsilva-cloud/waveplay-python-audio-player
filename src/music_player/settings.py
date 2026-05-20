"""Leitura e escrita de configurações simples do app."""
from __future__ import annotations

import json
from pathlib import Path

ARQUIVO_CONFIG = Path("settings.json")

def carregar_config() -> dict:
    """Lê o arquivo de configuração, se exitir."""
    if not ARQUIVO_CONFIG.exists():
        return {}
    
    try:
        with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError):
        return {}

def salvar_config(config: dict) -> None:
    """Salva as configurações no arquivo JSON."""
    with ARQUIVO_CONFIG.open("w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, ensure_ascii=False, indent=4)

def obter_ultima_pasta() -> str | None:
    """Retorna a última pasta salva, se existir."""
    config = carregar_config()
    return config.get("ultima_pasta")

def salvar_ultima_pasta(pasta: str) -> None:
    """Atualiza a última pasta aberta."""
    config = carregar_config()
    config["ultima_pasta"] = pasta
    salvar_config(config)

def obter_ultima_musica() -> str | None: 
    """Retorna o caminho da última música tocada, se existir."""
    config = carregar_config()
    return config.get("ultima_musica")

def salvar_ultima_musica(caminho: str) -> None:
    config = carregar_config()
    config["ultima_musica"] = caminho
    salvar_config(config)

def obter_volume() -> float:
    """Retorna o volume salvo, ou 1.0 se não existir."""
    config = carregar_config()
    return config.get("volume", 0.5)

    if not isinstance(volume, (int, float)):
        return 0.5
    
    return max(0.0, min(1.0, float(volume)))

def salvar_volume(volume: float) -> None:
    """Salva o volume atual."""
    config = carregar_config()
    config["volume"] = max(0.0, min(1.0, float(volume)))
    salvar_config(config)


def obter_tempo_reproduzido() -> int:
    """Retorna o tempo reproduzido salvo, ou 0.0 se não existir."""
    config = carregar_config()
    return config.get("tempo_reproduzido", 0.0)

def salvar_tempo_reproduzido(tempo: int) -> None:
    """Salva o tempo reproduzido atual."""
    config = carregar_config()
    config["tempo_reproduzido"] = max(0.0, int(tempo))
    salvar_config(config)