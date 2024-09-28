import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox, Frame, StringVar, Canvas, Scrollbar, VERTICAL, RIGHT, LEFT, Y, BOTH
from PIL import Image, ImageTk, ImageEnhance
from PIL.ImageTk import PhotoImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pop(titulo, passos):
    pasta = os.path.join(os.path.expanduser("~"), "POP")
    pasta_pop = os.path.join(pasta, 'POP_Gerados')

    if not os.path.exists(pasta_pop):
        os.makedirs(pasta_pop)


    arquivo_pdf = criar_nome_arquivo_unico(pasta_pop, titulo, ".pdf")
    c = canvas.Canvas(arquivo_pdf, pagesize=A4)
    largura, altura = A4
    margem = 50

    c.setFont("Helvetica", 24)
    c.drawString(margem, altura - 60, titulo)
    c.setFont("Helvetica", 16)

    y_position = altura - 120
    for i, (descricao, imagem) in enumerate(passos):
        if y_position < 150:
            c.showPage()  # Cria uma nova página
            c.setFont("Helvetica", 16)  # Reconfigura a fonte para o tamanho desejado
            y_position = altura - 80

        c.drawString(margem, y_position, f"{i + 1}. {descricao}")
        y_position -= 20

        if imagem:
            img = Image.open(imagem)
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            img.thumbnail((500, 500), Image.LANCZOS)

            # Verifica se há espaço para a imagem na página atual
            if y_position - img.size[1] < 50:
                c.showPage()  # Cria uma nova página
                c.setFont("Helvetica", 16)  # Reconfigura a fonte para o tamanho desejado
                y_position = altura - 80

            temp_img_path = os.path.join(pasta_pop, f"temp_img_{i}.jpg")
            img.save(temp_img_path, quality=95)
            c.drawImage(temp_img_path, margem, y_position - img.size[1], width=img.size[0], height=img.size[1])
            y_position -= img.size[1] + 20

    c.save()

    for i in range(len(passos)):
        temp_img_path = os.path.join(pasta_pop, f"temp_img_{i}.jpg")
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

    messagebox.showinfo("Sucesso", f"POP gerado com sucesso.")


def criar_nome_arquivo_unico(diretorio, nome_base, extensao):
    contador = 1
    arquivo = os.path.join(diretorio, f"{nome_base}{extensao}")

    # Enquanto existir um arquivo com o mesmo nome, incrementa o contador e altera o nome do arquivo
    while os.path.exists(arquivo):
        arquivo = os.path.join(diretorio, f"{nome_base} ({contador}){extensao}")
        contador += 1

    return arquivo

def criar_pop():
    root = Tk()
    root.title("Automação POP - Sistema de Criação")
    root.geometry("610x550")
    root.configure(bg='white')
    root.resizable(False, False)

    icon_path = os.path.join(os.path.dirname(__file__), "imagens", "logNovoMix.png")
    print(f"Caminho do ícone: {icon_path}")
    try:
        img_icon = PhotoImage(file=icon_path)
        root.iconphoto(False, img_icon)
    except Exception as e:
        print(f"Erro ao carregar o ícone: {e}")

    passos = []

    # Frame principal para os passos (parte rolável)
    main_frame = Frame(root, bd=0, bg='white')  # Remover a borda
    main_frame.pack(fill=BOTH, expand=True)

    # Canvas para adicionar a barra de rolagem
    canvas = Canvas(main_frame, bg='white', bd=0, highlightthickness=0)  # Remove bordas
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Barra de rolagem vertical
    scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)  # Associa a barra de rolagem ao canvas

    # Frame onde os passos serão adicionados
    form_frame = Frame(canvas, bg='white', bd=0, relief="flat")  # Remove bordas

    try:
        icon_path = os.path.join(os.path.dirname(__file__), "imagens", "logNovoMix.png")  # Caminho do ícone
        img = Image.open(icon_path)  # Abre a imagem .ico
        img = img.resize((250, 150), Image.LANCZOS)  # Redimensiona se necessário
        img_icon = ImageTk.PhotoImage(img)  # Converte para um formato compatível com o Tkinter

        img_label = Label(form_frame, image=img_icon, bg='white')  # Exibe a imagem
        img_label.grid(row=0, column=0, columnspan=3, pady=5)
    except Exception as e:
        print(f"Erro ao carregar o ícone: {e}")

    # Configura o canvas para sempre atualizar a região de rolagem
    def atualizar_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    form_frame.bind("<Configure>", atualizar_scroll_region)  # Configura para ajustar a rolagem dinamicamente

    canvas.create_window((0, 0), window=form_frame, anchor="nw")

    # Header - Remover espaço extra
    header_label = Label(form_frame, text="Gerador de POP", font=("Poppins", 16, "bold"), bg='white', fg='black')
    header_label.grid(row=1, column=0, columnspan=3, pady=5)  # Ajustar o pady para reduzir o espaço

    # Campo para o título do POP
    titulo_label = Label(form_frame, text="Digite o nome do POP", font=("Poppins", 13), bg='white')
    titulo_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    titulo_var = StringVar()
    titulo_entry = Entry(form_frame, textvariable=titulo_var, font=("Poppins", 13), width=30, bd=0, relief="flat",
                         highlightthickness=1, highlightbackground="#8f8f8f", highlightcolor="#5e9cff")
    titulo_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Função para adicionar passo
    def adicionar_passo():
        row = len(passos) + 3  # Ajustar para a linha correta (depois do título)
        passo_var = StringVar()

        passo_label = Label(form_frame, text=f"Descreva o passo {row-2}", font=("Poppins", 12), bg='white')
        passo_label.grid(row=row, column=0, padx=5, pady=2, sticky="w")

        passo_entry = Entry(form_frame, textvariable=passo_var, font=("Poppins", 12), width=30, bd=0, relief="flat",
                            highlightthickness=1, highlightbackground="#8f8f8f", highlightcolor="#5e9cff")
        passo_entry.grid(row=row, column=1, padx=5, pady=2, sticky="w")

        adicionar_imagem_btn = Button(form_frame, text="Adicionar Imagem", command=lambda: selecionar_imagem(row - 3),
                                      bg="#225CBF", fg="white", bd=0, font=("Poppins", 10, "bold"))
        adicionar_imagem_btn.grid(row=row, column=2, padx=5, pady=2)

        passos.append((passo_var, None))

    def selecionar_imagem(idx):
        imagem = filedialog.askopenfilename(title="Selecione a imagem",
                                            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if imagem:
            passos[idx] = (passos[idx][0], imagem)

    def gerar_pdf():
        titulo = titulo_var.get()
        if not titulo:
            messagebox.showerror("Erro", "Você deve fornecer um título!")
            return

        passos_descricao = [(p[0].get(), p[1]) for p in passos]

        for i, (descricao, imagem) in enumerate(passos_descricao):
            if not descricao:
                messagebox.showerror("Erro", f"O passo {i + 1} não possui descrição!")
                return

        gerar_pop(titulo, passos_descricao)

    # Função para habilitar a rolagem com o mouse
    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Bind do scroll do mouse
    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    # Separando os botões da área rolável em um novo frame fixo
    button_frame = Frame(root, bg='white')
    button_frame.pack(side='bottom', fill='x')

    adicionar_passo_btn = Button(button_frame, text="Adicionar Passo", command=adicionar_passo, bg="#225CBF", fg="white",
                                 font=("Poppins", 14, "bold"), bd=0, padx=300)
    adicionar_passo_btn.pack(side='top', pady=2)

    gerar_pdf_btn = Button(button_frame, text="Gerar POP", command=gerar_pdf, bg="#F73C3E", fg="white",
                           font=("Poppins", 14, "bold"), padx=300, pady=10, bd=0)
    gerar_pdf_btn.pack(side='top', pady=0)

    adicionar_passo()  # Adiciona o primeiro passo ao iniciar
    root.mainloop()

if __name__ == "__main__":
    criar_pop()
