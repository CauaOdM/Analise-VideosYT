# Analise-VideosYT

**Autor:** [CauaOdM](https://github.com/CauaOdM)

## 📋 Sobre o Projeto

Um projeto Python que automatiza a análise de vídeos do YouTube usando Inteligência Artificial. O programa extrai a transcrição de qualquer vídeo e gera uma análise detalhada usando o modelo Gemini da Google, salvando o resultado em um arquivo Markdown.

## 🚀 Como Funciona

1. Insira a URL de um vídeo do YouTube
2. O programa extrai a transcrição automaticamente
3. A IA analisa o conteúdo e gera um resumo crítico
4. O resultado é salvo em `analise_video.md`

## 📦 Dependências e Imports

### `dotenv` (load_dotenv)
Carrega variáveis de ambiente do arquivo `.env.local`, permitindo armazenar a API Key do Google de forma segura sem expô-la no código.

### `os`
Módulo padrão do Python para interagir com o sistema operacional. Usado para ler variáveis de ambiente (`os.getenv`).

### `youtube_transcript_api`
Biblioteca que busca e extrai transcrições (legendas) de vídeos do YouTube. Suporta múltiplos idiomas.
- **YouTubeTranscriptApi**: Classe principal para buscar transcrições
- **TextFormatter**: Converte a transcrição para formato de texto simples

### `google.generativeai` (genai)
SDK oficial do Google para usar modelos de IA Generativa (Gemini). Permite enviar prompts e receber análises textuais.

## 🔧 Funções do Código

### `extrair_ID_video(url)`
Extrai o identificador único do vídeo a partir da URL do YouTube, removendo parâmetros extras como `&t=2s`.
- **Entrada:** URL completa do YouTube
- **Retorno:** ID do vídeo (ex: `dQw4w9WgXcQ`)

### `transcript_video(video_id)`
Busca a transcrição do vídeo no YouTube e formata como texto simples.
- **Entrada:** ID do vídeo
- **Retorno:** Transcrição formatada em texto
- **Idiomas suportados:** Português e Inglês

### `analise_IA(text_formatted)`
Envia a transcrição para o modelo Gemini 2.5 Flash e solicita uma análise crítica detalhada.
- **Entrada:** Texto da transcrição
- **Retorno:** Análise gerada pela IA com resumo, avaliação e contexto
- **Análises incluídas:**
  - Resumo em tópicos
  - Vale a pena assistir?
  - O que se pode aprender?
  - Nicho do vídeo
  - Relação com a atualidade

### `main()`
Função principal que orquestra todo o fluxo: solicita URL, processa o vídeo e salva a análise em arquivo.

## ⚙️ Configuração

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env.local` na raiz com sua API Key do Google:
   ```
   API_KEY=sua_chave_aqui
   ```
4. Execute: `python analisador.py`

---

*Este README foi elaborado com auxílio de Inteligência Artificial.*

**Bem-vindo ao meu perfil! 🎉**
