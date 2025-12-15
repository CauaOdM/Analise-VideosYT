from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai

load_dotenv(".env.local")

api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables (.env or .env.local).")

genai.configure(api_key=api_key)

def extrair_ID_video(url):
    # Extrai o ID removendo parâmetros extras como &t=2s
    video_id = url.split("v=")[1].split("&")[0]
    return video_id

def transcript_video(video_id):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=['pt', 'en'])
    formatter = TextFormatter()
    text_formatted = formatter.format_transcript(transcript)
    return text_formatted

def analise_IA(text_formatted):
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Você é um analista de textos profissional com uma criticidade acima da média. A partir dessa transcrição feita de um vídeo: {text_formatted}. Faça um resumo detalhado em tópicos. Além disso faça analises como: 1. Vale a pena assistir o vídeo ? 2. O que se pode aprender com o vídeo? 3. Qual nicho o vídeo aborda? 4. Como o tema do texto se relaciona com a atualidade?"
    response = model.generate_content(prompt)

    return response.text

def main():
    url = input("Insira a URL do vídeo do YouTube: ")
    video_id = extrair_ID_video(url)
    text_formatted = transcript_video(video_id)
    analise = analise_IA(text_formatted)

    nome_arquivo = "analise_video.md"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(analise)
    
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")


if __name__ == "__main__":
    main()

