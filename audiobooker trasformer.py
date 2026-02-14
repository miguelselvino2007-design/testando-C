import requests
import io
import os
from pypdf import PdfReader
from gtts import gTTS

def criar_audiolivro():
    # 1. Entrada do usuário (Link ou Caminho Local)
    entrada = input("Digite a URL do PDF ou o caminho do arquivo local: ").strip()
    entrada = entrada.replace('"', '').replace("'", "") # Limpa aspas

    try:
        # 2. Obter o PDF
        if entrada.startswith("http"):
            print("Baixando PDF da internet...")
            resposta = requests.get(entrada)
            resposta.raise_for_status()
            leitor = PdfReader(io.BytesIO(resposta.content))
        else:
            leitor = PdfReader(entrada)

        # 3. Extrair texto de todas as páginas
        print("Extraindo texto...")
        texto_completo = ""
        for pagina in leitor.pages:
            resumo = pagina.extract_text()
            if resumo:
                texto_completo += resumo + " "

        if not texto_completo.strip():
            print("Não foi possível ler o texto do PDF.")
            return

        # 4. Gerar o MP3 usando o Google (Voz mais natural)
        print("Gerando áudio MP3 (Google)... Isso pode demorar um pouco.")
        
        # 'pt' para português, 'br' para sotaque brasileiro
        tts = gTTS(text=texto_completo, lang='pt', tld='com.br')
        
        arquivo_saida = "audiolivro.mp3"
        tts.save(arquivo_saida)

        print(f"\nSucesso! O arquivo '{arquivo_saida}' foi criado e é um MP3 real.")
        
        # Opcional: Tenta abrir o arquivo automaticamente
        os.startfile(arquivo_saida) if os.name == 'nt' else None

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    criar_audiolivro()