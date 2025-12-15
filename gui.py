#ESSE CÓDIGO INTEIRO DA INTERFACE GRÁFICA FOI GERADO POR IA GENERATIVA E REVISADO POR MIM
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

# Import backend functions without changing them
from analisador import extrair_ID_video, transcript_video, analise_IA


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # YouTube-inspired theme (modern, clean)
        self.title("Análise de Vídeos YouTube")
        self.geometry("960x640")
        self.minsize(820, 560)

        self.configure(bg="#F7F7F7")

        # Global style (ttk)
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Palette
        yt_red = "#FF0000"
        dark_bg = "#0F0F0F"
        light_bg = "#F7F7F7"
        card_bg = "#FFFFFF"
        text_primary = "#0F0F0F"
        text_secondary = "#606060"

        # Buttons
        style.configure(
            "Accent.TButton",
            background=yt_red,
            foreground="#FFFFFF",
            padding=10,
            borderwidth=0,
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#CC0000")],
        )
        style.configure("TButton", padding=10)

        # Entry
        style.configure("TEntry", padding=8)

        # Labels
        style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), foreground=text_primary)
        style.configure("Muted.TLabel", foreground=text_secondary)

        # Header bar
        header = tk.Frame(self, bg=dark_bg, height=72)
        header.pack(side=tk.TOP, fill=tk.X)

        title = tk.Label(
            header,
            text="Analise-VideosYT",
            fg="#FFFFFF",
            bg=dark_bg,
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(side=tk.LEFT, padx=24, pady=18)

        # Main content area
        canvas = tk.Canvas(self, bg=light_bg, highlightthickness=0)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        container = tk.Frame(canvas, bg=light_bg)
        window_item = canvas.create_window((0, 0), window=container, anchor="nw")

        def on_resize(event):
            # Keep container width equal to canvas width for consistent proportions
            canvas.itemconfigure(window_item, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", on_resize)

        # Card: Input & actions
        card = tk.Frame(container, bg=card_bg, highlightbackground="#E6E6E6", highlightthickness=1)
        card.pack(side=tk.TOP, fill=tk.X, padx=24, pady=(24, 14))

        ttk.Label(card, text="URL do vídeo", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(card, textvariable=self.url_var)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky="we", padx=16, pady=(0, 8))
        card.columnconfigure(0, weight=1)

        # Placeholder behavior
        placeholder = "https://www.youtube.com/watch?v=..."
        self.url_entry.insert(0, placeholder)
        def on_focus_in(_):
            if self.url_entry.get() == placeholder:
                self.url_entry.delete(0, tk.END)
        def on_focus_out(_):
            if not self.url_entry.get().strip():
                self.url_entry.insert(0, placeholder)
        self.url_entry.bind("<FocusIn>", on_focus_in)
        self.url_entry.bind("<FocusOut>", on_focus_out)

        # Actions
        actions = tk.Frame(card, bg=card_bg)
        actions.grid(row=2, column=0, columnspan=2, sticky="we", padx=16, pady=(6, 14))
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)

        self.analyze_btn = ttk.Button(actions, text="Analisar Vídeo", command=self.on_analyze, style="Accent.TButton")
        self.analyze_btn.grid(row=0, column=0, sticky="w")

        self.save_btn = ttk.Button(actions, text="Salvar análise…", command=self.on_save, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, sticky="e")

        # Status and progress
        status_frame = tk.Frame(container, bg=light_bg)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=24, pady=(2, 0))

        self.status_var = tk.StringVar(value="Pronto")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Muted.TLabel")
        self.status_label.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(status_frame, mode="indeterminate", length=220)
        self.progress.pack(side=tk.RIGHT, pady=8)

        # Card: Result area
        result_card = tk.Frame(container, bg=card_bg, highlightbackground="#E6E6E6", highlightthickness=1)
        result_card.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=24, pady=(14, 24))

        ttk.Label(result_card, text="Resultado", style="CardTitle.TLabel").pack(anchor="w", padx=16, pady=(14, 6))
        self.output = ScrolledText(result_card, wrap="word", height=22)
        self.output.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 18))
        self.output.configure(font=("Segoe UI", 10), spacing1=4, spacing3=4)

        # Keyboard shortcuts
        self.bind("<Return>", lambda _: self.on_analyze())
        self.bind("<Control-s>", lambda _: self.on_save())

        self.analysis_text = None

    def set_busy(self, busy: bool, message: str = ""):
        if busy:
            self.status_var.set(message or "Processando…")
            self.progress.start(10)
            self.analyze_btn.configure(state=tk.DISABLED)
        else:
            self.status_var.set(message or "Pronto")
            self.progress.stop()
            self.analyze_btn.configure(state=tk.NORMAL)

    def on_analyze(self):
        url = self.url_var.get().strip()
        if not url or url.startswith("http") is False:
            messagebox.showwarning("URL necessária", "Por favor, insira a URL válida do vídeo do YouTube.")
            return

        # Run in background thread to keep UI responsive
        def worker():
            try:
                self.set_busy(True, "Extraindo transcrição e gerando análise…")
                video_id = extrair_ID_video(url)
                texto = transcript_video(video_id)
                analysis = analise_IA(texto)
                self.analysis_text = analysis

                def update_ui():
                    self.output.delete("1.0", tk.END)
                    self.output.insert(tk.END, analysis)
                    self.save_btn.configure(state=tk.NORMAL)
                    self.set_busy(False, "Análise concluída")

                self.after(0, update_ui)
            except Exception as e:
                def show_err():
                    self.set_busy(False, "Ocorreu um erro")
                    messagebox.showerror("Erro", str(e))
                self.after(0, show_err)

        threading.Thread(target=worker, daemon=True).start()

    def on_save(self):
        if not self.analysis_text:
            messagebox.showinfo("Sem análise", "Não há análise para salvar ainda.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvar análise como",
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Texto", "*.txt")],
            initialfile="analise_video.md",
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.analysis_text)
            messagebox.showinfo("Salvo", f"Arquivo salvo em:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
