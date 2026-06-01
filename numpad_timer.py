"""
Numpad Exercise Timer - Contador de tempo para exercícios controlado pelo teclado numérico

Uso:
    - Digite tempo total em minutos para iniciar
    - Use o teclado numérico para registrar tempos de exercícios
    - Numpad Enter (78) para confirmar
    - Numpad + (74) para limpar
    - Botão quadrado desativa/ativa captura de teclas

Dependências:
    pip install keyboard
"""

import keyboard
import tkinter as tk
from datetime import datetime

pressed_keys = set()
total = None
resto = "0000"
hora_inicial = datetime.now()
cronometro = datetime.now()
minutos, segundos = 0,0
contador = 0
KEYCODE_MAP = {
    71: 7, 72: 8, 73: 9,
    75: 4, 76: 5, 77: 6, 79: 1, 80: 2,
    81: 3, 82: 0
}

def validar_entrada(entrada):
    # Verifica a entrada
    """Aceita apenas até 4 dígitos numéricos."""
    return entrada.isdigit() and len(entrada) <= 4 or entrada == ""

def Separacao_de_unidades(captura):
    # Separa minutos e segundos
    comprimento = len(captura)
    if comprimento > 2:
        minutos = int(captura[0:comprimento-2])
        segundos = int(captura[-2:comprimento])
    else:
        minutos = 0
        segundos = int(captura)
    return minutos, segundos

def Verificacao(minutos, segundos):
    # Checa quantidade limite de segundos
    if segundos < 0:
        minutos -= 1 + (segundos // -60)
        segundos = segundos % 60
    elif segundos >= 60:
        minutos += segundos // 60
        segundos = segundos % 60
    return minutos, segundos

def Resto(minutos, segundos):
    # Define tempo restante
    global total
    if segundos == 0:
        segundos = 60
    else:
        minutos+=1
    return f"{total-minutos:02}{60-segundos:02}"

def capturar_entrada():
    if btn.config('bg')[4] == color_btn_inactivate:
        for keycode in KEYCODE_MAP:
            if keyboard.is_pressed(keycode):
                if keycode not in pressed_keys:
                    pressed_keys.add(keycode)
                    entrada.insert(tk.END, KEYCODE_MAP[keycode])
            else:
                pressed_keys.discard(keycode)
    if keyboard.is_pressed(78):
        processar_entrada(entrada.get())
    elif keyboard.is_pressed(74):
        entrada.delete(0,'end')     
    janela.after(50, capturar_entrada)
    
def processar_entrada(captura):
    global total, resto, minutos, segundos, contador, hora_inicial, cronometro
    # captura = entrada.get()
    if not captura:
        return
    if total is None:
        iniciar(captura)
    else:
        if captura.startswith('0'):
            if int(captura) == 0:
                cronometrar()
            elif rotulo_tempo['text'] != '(TIME)':
                subitrair(captura)
        else:
            adicionar(captura)
            
def cronometrar():
    global cronometro
    if rotulo_tempo['text'] == '(TIME)':
        cronometro = datetime.now() - cronometro
        adicionar(str(cronometro.seconds//60)+str(cronometro.seconds%60))
    else:
        rotulo_tempo.config(text='(TIME)')
        cronometro = datetime.now()
        entrada.delete(0, tk.END)

def adicionar(captura):
    global contador, minutos, segundos, resto
    contador += 1
    captura_minutos, captura_segundos = Separacao_de_unidades(captura)
    rotulo_tempo.config(text=f'({captura_minutos:02}:{captura_segundos:02})')
    minutos, segundos = minutos + captura_minutos, segundos + captura_segundos
    minutos, segundos = Verificacao(minutos, segundos)
    resto = Resto(minutos, segundos)
    if int(resto) > 0:
        atualizar_rotulo()
    else:
        finalizar()
        
def iniciar(captura):
    global hora_inicial, total, resto
    hora_inicial = datetime.now()
    total = int(captura)
    resto = f'{total:02}00'
    atualizar_rotulo()

def finalizar():
    global hora_inicial, minutos, segundos, resto
    tempo_passado = datetime.now() - hora_inicial
    tempo_aproveitado = minutos*60+segundos
    resto = f"0000\nConcluído em {contador} exercício,\nDurando {tempo_passado.seconds//60}m e {tempo_passado.seconds%60}s"
    atualizar_rotulo()
    janela.after(10000, janela.destroy)

def subitrair(captura):
    global minutos, segundos, resto, contador
    if captura.startswith('00'):
            captura_minutos, captura_segundos = Separacao_de_unidades(captura[2:]+'00')
    else:
        captura_minutos, captura_segundos = Separacao_de_unidades(captura[1:])
    
    captura_minutos, captura_segundos = Verificacao(captura_minutos, captura_segundos)
    rotulo_minutos, rotulo_segundos = rotulo_tempo['text'].split(':')
    rotulo_minutos = int(rotulo_minutos[1:])
    rotulo_segundos = int(rotulo_segundos[:-1])
    
    if (rotulo_minutos*60+rotulo_segundos) >= (captura_minutos*60+captura_segundos):
        resto = ''.join(\
            f'{v:02}' for v in Verificacao(         \
                int(resto[:2])+captura_minutos,     \
                int(resto[2:])+captura_segundos     \
                ))
        minutos = minutos - captura_minutos
        segundos = segundos - captura_segundos
        minutos, segundos = Verificacao(minutos, segundos)
        rotulo_minutos = rotulo_minutos-captura_minutos
        rotulo_segundos = rotulo_segundos-captura_segundos
        if (rotulo_minutos + rotulo_segundos) == 0:
            contador -= 1
            rotulo_tempo.config(text=f'(00:00)')
        else:
            rotulo_minutos, rotulo_segundos = Verificacao(rotulo_minutos, rotulo_segundos)
            novo_rotulo = f'{rotulo_minutos:02}:{rotulo_segundos:02}'
            rotulo_tempo.config(text=f'({novo_rotulo})')
    atualizar_rotulo()

def atualizar_rotulo():
    global minutos, segundos, total, resto
    rotulo.config(text=f"{minutos:02}:{segundos:02} de {total:2}:00, faltam {resto[:2]}:{resto[2:]}")
    entrada.delete(0, tk.END)

def iniciar_mover(event):
    janela.x = event.x
    janela.y = event.y

def mover_janela(event):
    dx = event.x - janela.x
    dy = event.y - janela.y
    x = janela.winfo_x() + dx
    y = janela.winfo_y() + dy
    janela.geometry(f'+{x}+{y}')

def fechar():
    janela.destroy()

def main():
    '''Funcção principal de inicialização'''    
    global janela, entrada, rotulo, rotulo_tempo, btn. color_btn_activate, color_btn_inactivate
    
    # Janela principal
    janela = tk.Tk()
    janela.title("Contador de tempo")
    janela.attributes("-topmost", True)
    janela.overrideredirect(True)
    
    # Posição no canto superior direito
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenmmheight()
    posicao_x = largura_tela - 175
    posicao_y = altura_tela
    janela.geometry(f"170x60+{posicao_x}+{int(posicao_y*3.37)}")
    
    # Barra personalizada
    barra = tk.Frame(janela, bg='gray20', height=10)
    barra.pack(fill=tk.X)
    barra.bind("<Button-1>", iniciar_mover)
    barra.bind("<B1-Motion>", mover_janela)
    
    # Botão de fechar
    btn_fechar = tk.Button(barra, font=("Arial", 6), text="[ X ]", command=fechar, bg='gray20', fg='white', bd=0)
    btn_fechar.pack(side=tk.RIGHT, padx=3)
    
    # Texto inicial
    rotulo = tk.Label(janela, text="Digite tempo total em minutos:", font=("Arial", 9))
    rotulo.pack(pady=1)
    
    # Entrada com validação
    vcmd = (janela.register(validar_entrada), "%P")
    entrada = tk.Entry(janela, font=("Arial", 9), validate="key", validatecommand=vcmd, justify='center', width=9)
    entrada.pack(side='left',pady=1, padx=3)
    
    # Tepo do ultimo exercicio
    rotulo_tempo = tk.Label(janela, text="(00:00)", fg='gray', font=("Arial", 9))
    rotulo_tempo.pack(side='left', pady=1, padx=3)
    
    # Botão:
    color_btn_activate = "gray80"
    color_btn_inactivate = "gray20"
    def toggle():
        btn.config(bg=color_btn_inactivate if btn.config('bg')[4] == color_btn_activate else color_btn_activate)
    btn = tk.Button(janela, bg=color_btn_inactivate, command=toggle, width=4, height=1)
    btn.pack(side='right', padx=3, pady=1)
    
    capturar_entrada()
    janela.mainloop()

# Bloco principal
if __name__ == "__main__":
    main()
