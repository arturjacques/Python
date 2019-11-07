red = '#ff0000'
cortexto = '[color=#000000]'
fimcor = '[/color]'

import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from kivy.uix.label import Label
from random import choice

widgets = list()
nomes = list()
partida = list()
regras = dict()

Config.setdefault('graphics', 'height', '600')
Config.setdefault('graphics', 'width', '300')


class jogadores():
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, nome):
        if len(nome) > 25:
            nome = nome[:25]
        self._name = str(nome).capitalize().strip()

    @property
    def cartas(self):
        return self._cartas

    @cartas.setter
    def cartas(self, Ncartas):
        self._cartas = Ncartas

    def del_carta(self, a):
        if self.cartas > a:
            self.cartas -= a
        else:
            self.cartas = 0

    def mais_leva(self):
        if self.leva < self.cartas:
            self.leva += 1
            atualizar()

    def menos_leva(self):
        if self.leva > 0:
            self.leva -= 1
            atualizar()

    def mais_levou(self):
        soma = 0
        for i in partida:
            soma+=i.levou
        if self.levou < self.cartas and soma<regras['Ncartas']:
            self.levou += 1
            atualizar2()

    def menos_levou(self):
        if self.levou > 0:
            self.levou -= 1
            atualizar2()


def text_cor(text):
    return f'{cortexto}' + str(text) + f'{fimcor}'


class MeuTexto(TextInput):
    pass


class MeuBotao(Button):
    pass


class MeuLabel(Label):
    pass


class MeuToggle(ToggleButton):
    pass


class Inicio(FloatLayout):

    def new_game(self):
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(AddJogador())
        for i in widgets:
            self.remove_widget(i)
        for i in nomes:
            self.remove_widget(i)


class AddJogador(StackLayout):

    def __init__(self, **kwargs):
        super(AddJogador, self).__init__(**kwargs)
        widgets.append(MeuBotao(text='Remover Jogador'))
        widgets.append(MeuBotao(text='Adicionar Jogador'))
        widgets.append(MeuBotao(text='Voltar'))
        widgets.append(MeuBotao(text='Continuar', ))
        widgets[0].on_press = self.del_jogador
        widgets[1].on_press = self.add_jogador
        widgets[2].on_press = self.voltar
        widgets[3].on_press = self.continuar
        for count, i in enumerate(widgets):
            if count == 2:
                for j in nomes:
                    self.add_widget(j)
            self.add_widget(i)
        if len(nomes) < 1:
            self.add_jogador()
            self.add_jogador()

    def add_jogador(self):
        if len(nomes) < 8:
            a = len(nomes) + 1
            nomes.append(MeuTexto(text=f'Jogador {a}'))
            self.add_widget(nomes[-1], index=2)

    def del_jogador(self):
        if len(nomes) > 2:
            a = len(nomes) - 1
            self.remove_widget(nomes[a])
            nomes.remove(nomes[a])

    def voltar(self):
        janela.root_window.remove_widget(janela.root)
        widgets.clear()
        janela.root_window.add_widget(Inicio())
        for i in nomes:
            self.remove_widget(i)
        for i in widgets:
            self.remove_widget(i)

    def continuar(self):
        for i in nomes:
            partida.append(jogadores())
            partida[-1].name = i.text
        for i in widgets:
            self.remove_widget(i)
        for i in nomes:
            self.remove_widget(i)
        widgets.clear()
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Opcoes())


class Opcoes(StackLayout):

    def __init__(self, **kwargs):
        super(Opcoes, self).__init__(**kwargs)
        # Texto de início do módulo
        widgets.append(
            MeuLabel(text=f'[b]{cortexto}Opções de jogo[/color][/b]', markup=True, size_hint=(1, 1 / 10)))
        # Apresentação dos jogadores
        text = f'{cortexto}Os jogadores são: '
        for count, i in enumerate(partida):
            if count != len(partida) - 1:
                text = text + i.name + ', '
            else:
                text = text + i.name + f'{fimcor}'
            if len(text) / (text.count('\n') + 1) > (70 + text.count('\n') * 2):
                text = text + '\n'
        widgets.append(MeuLabel(text=text))
        widgets[-1].font_size = '20sp'
        widgets[-1].size_hint = 1, 1 / 10
        widgets[-1].halign = 'justify'
        widgets[-1].markup = True
        widgets[-1].max_lines = 2
        # Escolher número de carta
        # Explicação
        widgets.append(MeuLabel(text=f'{cortexto}Número inícial de Cartas{fimcor}', markup=True))
        widgets[-1].font_size = '20sp'
        widgets[-1].size_hint = 5 / 10, 1 / 10
        # Tirar carta
        widgets.append(MeuBotao(text='<'))
        widgets[-1].size_hint = 1 / 10, 1 / 10
        widgets[-1].on_press = self.del_carta
        # Mostrar número de cartas
        regras['Ncartas'] = 5
        widgets.append(MeuLabel(text=str(regras['Ncartas'])))
        widgets[-1].size_hint = 3 / 10, 1 / 10
        widgets[-1].background_color = 255, 0, 0, 1
        # Colocar carta
        widgets.append(MeuBotao(text='>'))
        widgets[-1].size_hint = 1 / 10, 1 / 10
        widgets[-1].on_press = self.add_carta
        # Embuchar
        widgets.append(MeuLabel(text=f'{cortexto}Regra de Embucha{fimcor}', markup=True))
        widgets[-1].font_size = '20sp'
        widgets[-1].size_hint = 5 / 10, 1 / 10
        # On
        widgets.append(MeuToggle(text='Habilitado', state='down'))
        widgets[-1].size_hint = 5 / 10, 1 / 10
        widgets[-1].on_press = self.empata
        regras['embucha'] = True
        # Sortear quem começa
        # Botão
        widgets.append(MeuToggle(text='Sortear quem começa'))
        widgets[-1].font_size = '20sp'
        widgets[-1].size_hint = 1 / 2, 1 / 10
        widgets[-1].on_press = self.sortear
        # Label
        regras['começa'] = partida[0]
        widgets.append(MeuLabel(text=regras['começa'].name))
        # Voltar a tela anterior
        widgets.append(MeuBotao(text='Voltar'))
        widgets[-1].on_press = self.voltar
        widgets[-1].size_hint = 1 / 2, 1 / 10
        # Continuar
        widgets.append(MeuBotao(text='Jogar'))
        widgets[-1].on_press = self.jogar
        widgets[-1].size_hint = 1 / 2, 1 / 10
        for i in widgets:
            self.add_widget(i)

    def voltar(self):
        for i in widgets:
            self.remove_widget(i)
        for i in nomes:
            self.remove_widget(i)
        widgets.clear()
        partida.clear()
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(AddJogador())

    def add_carta(self):
        regras['Ncartas'] = regras['Ncartas'] + 1
        widgets[4].text = str(regras['Ncartas'])

    def del_carta(self):
        if regras['Ncartas'] == 1:
            pass
        else:
            regras['Ncartas'] = regras['Ncartas'] - 1
            widgets[4].text = str(regras['Ncartas'])

    def empata(self):
        if widgets[7].state == 'normal':
            widgets[7].text = 'Desabilitado'
            regras['embucha'] = False
        else:
            widgets[7].text = 'Habilitado'
            regras['embucha'] = True

    def sortear(self):
        if widgets[8].state == 'normal':
            pass
            widgets[8].state = 'down'
        else:
            A = choice(partida)
            widgets[9].text = A.name
            regras['começa'] = A

    def jogar(self):
        for i in widgets:
            self.remove_widget(i)
        for i in partida:
            i.cartas = regras['Ncartas']
        widgets.clear()
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Jogo1())


class Jogo1(StackLayout):

    def __init__(self, **kwargs):
        super(Jogo1, self).__init__(**kwargs)
        while partida[0] != regras['começa']:
            partida.insert(0, partida[-1])
            partida.pop()

        widgets.append(MeuLabel(text=f'{cortexto}{regras["começa"].name} começa{fimcor}',
                                size_hint=(1, 1 / 11), markup=True, font_size='20sp'))
        widgets.append(MeuLabel(text=text_cor('cartas'), size_hint=(1 / 10, 1 / 11), font_size='20sp', markup=True))
        widgets.append(MeuLabel(text=text_cor('Jogador'), size_hint=(6 / 10, 1 / 11), font_size='20sp', markup=True))
        widgets.append(MeuLabel(text=text_cor('Leva'), size_hint=(3 / 10, 1 / 11), font_size='20sp', markup=True))
        for i in partida:
            widgets.append(MeuLabel(text=text_cor(i.cartas), markup=True, size_hint=(1 / 10, 1 / 11)))
            widgets.append(MeuLabel(text=text_cor(i.name), size_hint=(6 / 10, 1 / 11), markup=True))
            widgets.append(MeuBotao(text='<', size_hint=(1 / 10, 1 / 11)))
            widgets[-1].on_press = i.menos_leva
            i.leva = 0
            widgets.append(MeuLabel(text=text_cor(i.leva), size_hint=(1 / 10, 1 / 11), markup=True))
            i.indexWidget = len(widgets) - 1
            widgets.append(MeuBotao(text='>', size_hint=(1 / 10, 1 / 11)))
            widgets[-1].on_press = i.mais_leva
        # Ocupando espaço
        if len(partida) < 8:
            widgets.append(Label(size_hint=(1, (8 - len(partida)) / 11)))
        # Continuar
        widgets.append(MeuBotao(text='Continuar'))
        widgets[-1].on_press = self.continuar
        widgets[-1].size_hint = 1 / 2, 1 / 11
        # Embucha
        if regras['embucha'] == True:
            widgets.append(Label(text='[color=#00FF00]Não Embucha[/color]', markup=True, font_size='30sp'))
            widgets[-1].size_hint = 1 / 2, 1 / 11
        for i in widgets:
            self.add_widget(i)

    def continuar(self):
        for i in widgets:
            self.remove_widget(i)
        widgets.clear()
        janela.root_window.remove_widget(janela.root)
        janela.root_window.add_widget(Jogo2())

class Jogo2(StackLayout):

    def __init__(self, **kwargs):
        super(Jogo2, self).__init__(**kwargs)
        widgets.append(MeuLabel(text=f'{cortexto}Resultado{fimcor}',
                                size_hint=(1, 1 / 11), markup=True, font_size='20sp'))
        widgets.append(MeuLabel(text=text_cor('Levaria'), size_hint=(1 / 10, 1 / 11), font_size='20sp', markup=True))
        widgets.append(MeuLabel(text=text_cor('Jogador'), size_hint=(6 / 10, 1 / 11), font_size='20sp', markup=True))
        widgets.append(MeuLabel(text=text_cor('Levou'), size_hint=(3 / 10, 1 / 11), font_size='20sp', markup=True))
        for i in partida:
            widgets.append(MeuLabel(text=text_cor(i.leva), markup=True, size_hint=(1 / 10, 1 / 11)))
            widgets.append(MeuLabel(text=text_cor(i.name), size_hint=(6 / 10, 1 / 11), markup=True))
            widgets.append(MeuBotao(text='<', size_hint=(1 / 10, 1 / 11)))
            widgets[-1].on_press = i.menos_levou
            i.levou = 0
            widgets.append(MeuLabel(text=text_cor(i.levou), size_hint=(1 / 10, 1 / 11), markup=True))
            i.indexWidget = len(widgets) - 1
            widgets.append(MeuBotao(text='>', size_hint=(1 / 10, 1 / 11)))
            widgets[-1].on_press = i.mais_levou
        # Ocupando espaço
        if len(partida) < 8:
            widgets.append(Label(size_hint=(1, (8 - len(partida)) / 11)))
        # Continuar
        widgets.append(MeuBotao(text='Continuar'))
        widgets[-1].on_press = self.continuar
        widgets[-1].size_hint = 1 / 2, 1 / 11
        for i in widgets:
            self.add_widget(i)

    def continuar(self):
        max=0
        for i in partida:
            if i.leva==i.levou:
                pass
            elif i.leva>i.levou:
                i.cartas+=i.levou-i.leva
            elif i.leva<i.levou:
                i.cartas+=i.leva-i.levou
            if i.cartas>max:
                max=i.cartas
            if i.cartas==0:
                partida.remove(i)
        regras['Ncartas']=max
        for i in widgets:
            self.remove_widget(i)
        widgets.clear()
        janela.root_window.remove_widget(janela.root)
        if len(partida)>1:
            regras['começa'] = partida[1]
            janela.root_window.add_widget(Jogo1())
        else:
            janela.root_window.add_widget(Inicio())

def atualizar():
    soma = 0
    for i in partida:
        widgets[i.indexWidget].text = text_cor(i.leva)
        soma += i.leva
    if regras['embucha'] == True:
        if soma >= regras['Ncartas']:
            widgets[-1].text = '[color=ff0000]Embucha[/color]'
        else:
            widgets[-1].text = '[color=#00FF00]Não Embucha[/color]'

def atualizar2():
    for i in partida:
        widgets[i.indexWidget].text = text_cor(i.levou)

class JanelaApp(App):
    def build(self):
        return Inicio()


janela = JanelaApp()
janela.run()
