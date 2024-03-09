import random
import sys
import pygame
import pandas as pd
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pygame import event

from principal import Ui_Form
from principal import CustomDialog

pygame.init()


class GuessGame:

    # Data Frame para ler o caminho do csv de musicas
    df_musicas = pd.read_csv(r'C:\workspace\desafio_kaka_1\selecao.csv', names=['Nome', 'Caminho'])

    captura = None

    # Função que sorteia musica
    @staticmethod
    def sorteio(df_musicas):
        captura = random.choice(df_musicas['Caminho'].tolist())
        return captura

    # Função que compara a tentativa com a musica sorteada
    @staticmethod
    def tentativa(captura, tentativa):
        print(captura)
        nome_musica = GuessGame.df_musicas.loc[GuessGame.df_musicas['Caminho'] == captura, 'Nome'].iloc[0]

        tentativa_formatada = ''.join(e for e in tentativa.lower() if e.isalnum())

        print("Tentativa:", tentativa_formatada)
        contagem = 0

        if tentativa_formatada == nome_musica:
           # MainWindow.label_streak.setText(f'Streak: {contagem + 1}')
            return "Parabéns! Você acertou!"
        else:
         #   MainWindow.label_streak.setText("")
            return "Errou. Tenta de novo."


class MainWindow(QWidget, Ui_Form):


    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.media_player = QMediaPlayer()

        self.contador_streak=0

        # conectar resposta ao botão enviar
        self.lineEdit.returnPressed.connect(self.enviarButton.click)
        self.enviarButton.clicked.connect(self.verificar_musica)
        self.enviarButton.clicked.connect(self.lineEdit.clear)

        self.pushButton_proximo.clicked.connect(self.tocar_proxima)


        # Começa o jogo
        self.tocar_proxima()


    def verificar_musica(self):
        try:
            # tentativa na linha de edição
            tentativa = self.lineEdit.text()
            mensagem = GuessGame.tentativa(self.captura, tentativa)
            # condição para o streak
            if "Parabéns!" in mensagem:
                self.contador_streak += 1
                self.label_streak.setText(f'🔥Streak: {self.contador_streak}🔥')
            else:
                self.contador_streak = 0
                self.label_streak.setText("")
        except ValueError as a:
            dialog = CustomDialog("Exceção", "Não existe", str(a))
            dialog.exec_()
            return
        self.label_2.setText(mensagem)


    # Função para tocar próxima música sorteada
    def tocar_proxima(self):
        self.captura = GuessGame.sorteio(GuessGame.df_musicas)
        pygame.mixer.music.load(self.captura)
        pygame.mixer.music.play()


        print("Caminho da música:", self.captura)
        self.label_2.setText("")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
