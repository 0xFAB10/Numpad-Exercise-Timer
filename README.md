# Numpad-Exercise-Timer
Um contador de tempo minimalista para exercícios físicos, controlado **exclusivamente pelo teclado numérico** (numpad). Perfeito para séries de treino onde você não quer interromper o ritmo para usar o mouse.
![Demo](https://img.shields.io/badge/platform-Windows-blue) ![Python](https://img.shields.io/badge/python-3.6+-green)

## 🎯 Funcionalidades

- **Controle 100% via numpad** - sem necessidade de mouse
- **Overlay flutuante** - sempre visível sobre outras janelas
- **Registro de tempo por exercício** - marca quanto tempo cada repetição levou
- **Contador regressivo** - mostra o tempo restante do treino
- **Janela arrastável** e com botão de fechar minimalista

## Arquitetura

- **Frontend**: Tkinter (overlay topmost, janela sem bordas)
- **Input Handler**: Biblioteca `keyboard` (escuta raw keycodes)
- **Lógica**: Máquina de estados simples (aguardando total → contabilizando)

## ⌨️ Comandos do Teclado

| Tecla | Função |
|-------|--------|
| `0-9` (numpad) | Digitar minutos/segundos |
| `Numpad Enter` (78) | Confirmar/processar entrada |
| `Numpad +` (74) | Limpar campo atual |

## 🚀 Como Usar

1. **Iniciar** - Digite o tempo total do treino em minutos (ex: `20` para 20 min)
2. **Registrar exercício** - Digite quanto tempo levou e pressione `Enter`
   - `30` = 30 segundos
   - `130` = 1 minuto e 30 segundos
3. **Adicionar tempo extra** - Digite o valor sem zero à esquerda
4. **Subtrair tempo** - Digite com zero à esquerda (ex: `030` = subtrai 30 segundos)
5. **Cronômetro rápido** - Digite `0` para usar o modo cronômetro (marca o tempo entre teclas)

## Instalação e Uso

```bash
git clone https://github.com/seu-usuario/numpad-exercise-timer.git
cd numpad-exercise-timer
pip install -r requirements.txt
python numpad_timer.py
