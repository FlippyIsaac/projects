import subprocess as sub
import win32clipboard
import tkinter
import pygame
import random
import json
import time
import sys
import os

from PIL import Image
from win32api import GetSystemMetrics as GSM
from pygame.locals import *
from io import BytesIO, StringIO

pygame.init()
pygame.mixer.init()

# funções usadas no programa
# a = tkinter.filedialog.askdirectory(**options)
# print(a)


pasta_mae = sys.argv[0][:( (len(sys.argv[0]) - 1) - sys.argv[0][::-1].find('\\') )]


def inter(var):
	'''vai testa a variavel "var"
	if for true vai transformala em false
	if for false vai transformala em true'''
	return False if var else True

def limitador(var1, lista):
	'''vai testa a var1 para ver se ela ta com o mountante 
	mair que que a lista ou se ele ta menor que 0'''
	if var1 < 0:
		var1 = int(len(lista) - 1)
	if var1 > int(len(lista) - 1):
		var1 = 0
	return var1

def procura_imagens(local):
	arquivos_locais = {
		'arquivos':[],
		'locais' :[],
	}
	for item in os.listdir(local):
		'''
		if '.png' in item:
			arquivos_locais['arquivo'].append(item)
		else:
			arquivos_locais['locais'].append(item)
		'''
		encontra_ponto = item[::-1].find('.')
		# print(encontra_ponto)
		extensao = item[int(len(item) - 1) - int(encontra_ponto):]
		if (extensao == '.png') or (extensao == '.jpg') or (extensao == '.gif'):
			arquivos_locais['arquivos'].append(os.path.join(local, item))
			# print(f'nome: {item}',extensao in '.png.jpg')

		else:
			try:
				os.listdir(os.path.join(local, item))
				arquivos_locais['locais'].append(os.path.join(local, item))

			except:
				pass
	for pasta in arquivos_locais['locais']:
		for item in os.listdir(pasta):
			encontra_ponto = item[::-1].find('.')
			# print(encontra_ponto)
			extensao = item[int(len(item) - 1) - int(encontra_ponto):]
			if (extensao == '.png') or (extensao == '.jpg') or (extensao == '.gif'):
				arquivos_locais['arquivos'].append(os.path.join(pasta, item))
				# print(f'nome: {item}',extensao in '.png.jpg')

	#arquivos_locais['arquivos'] = sorted(arquivos_locais['arquivos'])
	#arquivos_locais['locais']   = sorted(arquivos_locais['locais'])
	return arquivos_locais

def copy_clip(clip_type, data):
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardData(clip_type, data)
	win32clipboard.CloseClipboard()

def procura(nome, lista):
	contador = 0
	tem_sim = False
	for e in lista:
		if e == lista:
			tem_sim = True
			break
		else:
			contador += 1
	return [tem_sim, contador]

def criar_arquivos(file, text=None):
	try:
		arquivo = open(file, 'r')
		arquivo.close()
		return False
	except FileNotFoundError:
		arquivo = open(file, 'w')
		if not text is None:
			arquivo.write(text+'\n')
		arquivo.close()

def escrever_em_arquivo(file, texto, reset=False):
	try:
		if not reset:
			arquivo = open(file, 'a')
			arquivo.write(texto+'\n')
			arquivo.close()

		elif reset:
			arquivo = open(file, 'w')
			arquivo.write(texto+'\n')
			arquivo.close()

	except Exception as e:
		raise e

def escrever_arquivo(file, text, substituir=False, incremento=''):
	if not substituir:
		arquivo = open(file, 'a')
		arquivo.write(text+'\n')
		arquivo.close()

	elif substituir:
		arquivo_ler = open(file, 'r')
		leitura = arquivo_ler.read()

		arquivo_escrever = open(file, 'w')
		leitura = leitura.replace(text, text+incremento)
		arquivo_escrever.write(leitura)
		arquivo_escrever.close()
		arquivo_ler.close()

def registra_tag(file, name, tag=None, utima_id=0, delete=False, deleteAll=False):
	'''registra_tag(file, name, tag, utima_id, delete, deleteAll)
	feito para registra tag numa image correspondente e adcionar 
	uma tag que ainda falte no conjunto de tags
	file == ao arquivo onde ta as tags,
	name == ao nome da imagem a ser testada
	tag == a nova tag da imagem ou do conjunto
	as tags já existentes não seram adcionadas
	utima_id == é onde fica a imagem o numero 
	da ordem correspondente a do carregamento 
	de imagens sempre sera testada quando for 
	adcinar uma tag nova ou ver ser já tem uma
	tag
	delete == é usada para deletar uma tag de uma
	imagen correspondente sera deletada somente da 
	imagem
	deleteAll == é usada para deletar uma tag tanto 
	de uma imagem quanto do conjunto.'''
	saida = "PAUSE" # prepara para saida
	arquivo = open(file, 'r') # arquivo json
	mudanca = False # para possiveis mudanças no arquivo json
	ler_json = json.loads(arquivo.read()) # arquivo json carregado
	#"name": {"utima_id":"utima_id", "tags":"#tag"} base de uma item
	if name in ler_json: # testa se o nome da imagen ta registrada
		if ler_json[name]['utima_id'] != utima_id: # atualizar o utima_id da imagem
			ler_json[name]['utima_id'] = utima_id
			mudanca = True # para mudaças

		if not tag is None: # se tag for diferente de None
			if "#"+tag in ler_json[name]['tags'].replace(',', ' ').split() and delete: # testa se precisa deletar a tag de uma imagen
				ler_json[name]['tags'] = ler_json[name]['tags'].replace(f'#{tag},', '')
				saida = f'#{tag} removida'
				mudanca = True

			elif not '#'+tag in ler_json[name]['tags']  and not delete: #testa se tem uma tag na imagem se não tiver colar a tag na imagem
				saida = f'Agora tem uma tag de nome #{tag}!'
				ler_json[name]['tags'] += f'#{tag},'
				mudanca = True

			else:
				saida = f'Já tem uma tag de nome #{tag}!'
			
			if not '#'+tag in ler_json['conjunto']['tags']:
				# testa se tem a tag no conjuto de tags
				ler_json['conjunto']['tags'] += f'#{tag}'

		if deleteAll:
			del(ler_json[name])
			saida = f'{name} foi deletado!'

	elif not name in ler_json and not deleteAll:
		# para adcionar um novo item no json sobre a imagem
		if not tag is None: # se tiver uma tag criar um novo item da imagem com tag
			ler_json[name] = {"utima_id":utima_id, "tags":f"{tag},"} 
			mudanca = True

		else:
			ler_json[name] = {"utima_id":utima_id, "tags":""} 
			mudanca = True

	if mudanca:
		# arquivar novas mudaças
		arquivo = open(file, 'w')
		arquivo.writelines(json.dumps(ler_json))

	arquivo.close()

	return saida


class TEMPORIZADOR(object):
	def __init__(self, game, texto, fps, segundo, fonte, pos=pygame.Vector2(0, 0), cor=(0, 0, 0), background=None):
		'''criado para colocar textos temporizados
		texto apresentado, fps para pegar o time
		segundo que é o tempo limite da aparição do texto
		font que vai ser usada para escrever o texto
		pos para a posição do texto, cor para a cor do texto
		e background para o fundo do texto'''
		self.fps  = fps
		self.segundos = segundo
		self.fonte = fonte
		self.texto = fonte.render(f'{texto}', True, cor, background)
		self.frame = 0
		self.fps_maximo = 0
		self.posTxt = pos
		self.cor = cor
		self.time = 0
		self.mili = 0

	def time_out(self):
		# atualizar os times do temporizador
		if not self.mili > self.fps:
			self.mili += 1

		else:
			self.time += 1
			self.mili = 0

		if self.time >= int(int(self.fps) * self.segundos):
			self.time = 0
			return True

		else:
			return False

# programa
class VIEW_IMAGES(object):
	'''onde vai roda todo o programa 
	w == width da janela
	h == height da janela
	t == titlee da janela'''
	def __init__(self, w, h, t, fps=None):
		self.width = w
		self.height = h
		self.title = t
		# self.musicas = [pygame.mixer.Sound('music.ogg'), pygame.mixer.Sound('toque_sexo.mp3')]
		self.run(fps=fps)

	def _set_title(self, title):
		'''criar um titulo para a janela'''
		pygame.display.set_caption(title)

	def video(self, width, height, modo=None):
		'''para carregar video da janela'''
		return pygame.display.set_mode((width, height), flags=modo, vsync=10, depth=1)

	def start_programmer(self):
		'''iniciar as variaveis do programa'''
		self.tags_contador = 0
		self.tags = sorted(json.loads(open('information.json', 'r').read())['conjunto']['tags'].replace('#', ' ').split())
		# print(self.tags)
		self.window = self.video(
			# criar uma janela

			width=self.width, 
			height=self.height, 
			modo=RESIZABLE)

		self._set_title(self.title) # dar um titulo pra janela

		self.text_tela = {} # os textos que temporizados
		font = pygame.font.SysFont('Verdana', int((width * 5)/100))

		txt  = font.render('carregando Imagens Aguarde...', True, (255, 255, 255), (10, 10, 10))
		size = font.size('carregando Imagens Aguarde...')
		xt = int(width/2)  - int(size[0]/2)
		yt = int(height/2) - int(size[1]/2)-1
		self.window.blit(txt, [xt, yt])
		pygame.display.update()

		self.clock = pygame.time.Clock() # times do programa

		self.images_dir = procura_imagens(os.path.join(pasta_mae, 'hentai')) # escolhe onde fica as imagens no caso "hentai"

		self.resultados = self.images_dir.copy() # resultado de pesquisar

		self.posImage   = pygame.Vector2(0, 0) # posição da imagem

		self.ir_sozinho = False # passa as imagens automaticamente
		
		self.pause = False # pausa a musica se tiver

		self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))

		self.unidade       = int(self.posNumero['atual'])
		self.unidade_atual = None #int(self.posNumero['anterior'])
		self.atualizar_imagem = False

		# self.image = pygame.image.load( self.resultados['arquivos'][self.unidade] ).convert_alpha()

		self.dar_zoom = False
		self.modo = False

		self.digitando = False
		self.input_text = ''

		self.centralizar = True

		self.ajustar_largura = True
		self.ajustar_altura = False

		self.Fnt = self.carregar_fontes()

		self.reset_pos = True

		self.temporizador_loop = TEMPORIZADOR(game=self, texto='', fps=self.clock.get_fps(), segundo=100, fonte=self.Fnt[0])

		self.frame = TEMPORIZADOR(game=self, texto='', fps=self.clock.get_fps(), segundo=.3, fonte=self.Fnt[0])

		self.atualizar_forcado = False

		#self.musicas[0].play()

		self.time_next_images = 0

		self.saida_real = False

		self.avaca = False

		self.mostrar_resultados = [False, None]

		self.gif = None

		self.nova_etiqueta = None

		self.numero_musica = 0

		self.wait = True
		self.iniciar_tela = True

	def rodar_gif(self):
		obj = self.resultados['arquivos'][self.unidade]
		extensao = obj[int(len(obj) - 1) - int(obj[::-1].find('.')):]
		saida  = [False, True]
		if extensao == '.gif':
			if self.frame.time_out():
				saida[1] = True

			saida[0] = True
			return saida
		else:
			saida

	def escrever_temporizado(self):
		delete = []
		x = y = 0
		for e in self.text_tela:
			obj = self.text_tela[e]
			
			self.window.blit(obj.texto, [x, y])

			y += int(obj.fonte.get_linesize())
			if obj.time_out():
				delete.append(e)

		for i in delete:
			del(self.text_tela[i])

	def carregar_fontes(self, fonte='Verdana', tamanhos=[10, 14, 18, 24, 32]):
		fontes_carregadas = []
		for tamanho in tamanhos:
			fontes_carregadas.append(pygame.font.SysFont(fonte, tamanho))

		return fontes_carregadas

	def event_mouse(self, event):
		ww, hw = self.window.get_size()
		ww = int(((ww+hw) * 1.2)/100)
		if event.y > 0:
			# print('cima')
			self.posImage.y += int(ww*3)
		if event.y < 0:
			# print('baixo')
			self.posImage.y -= int(ww*2)

	def events_repetitivos(self):
		key = pygame.key.get_pressed()
		
		ww, hw = self.window.get_size()
		ww = int(((ww+hw) * 1.2)/100)

		if key[K_w] or key[K_UP]:   self.posImage.y += ww
		if key[K_s] or key[K_DOWN]: self.posImage.y += -ww

		if key[K_a]: self.posImage.x += ww
		if key[K_d]: self.posImage.x += -ww

	def event_teclas_escrever(self, var, event):
		abc = '\\/asdfghjklqwertyuiopzxcvbnmASDFGHJKLQWERTYUIOPZXCVBNM1234567890#_-.,'.replace('', ' ').split()
		if event.key == K_ESCAPE:
			self.digitando = inter(self.digitando)

		if (event.key == K_RIGHT and len(self.input_text) > 1) and (self.input_text[0] in '-#') and (self.input_text[-1] != ',' or self.input_text[-1] != '#'):
			var += ',#'

		if ((event.key == K_SPACE and len(self.input_text) > 0) and (self.input_text[0] in '-#') and (self.input_text[-1] != ',' or self.input_text[-1] != '#') or 
			(event.key == K_SPACE and len(self.input_text) > 0) and (self.input_text[-1] != ',' or self.input_text[-1] != '#')):
			var += '_'

		if (event.key == K_UP and len(self.input_text) > 0) and (self.input_text[0] in '-#'):
			if not self.input_text.find(',') != -1:
				self.tags_contador = limitador(self.tags_contador, self.tags)
				var = f'{self.input_text[0]}{self.tags[self.tags_contador]}'
				self.tags_contador+=1

			elif ',' in self.input_text:
				texto = self.input_text
				ponto = texto.find(',')
				pontotst = ponto
				while pontotst != -1:
					pontotst = self.input_text[ponto+1:].find(',')
					if pontotst > 0:
						ponto += 1

					elif pontotst == 0:
						ponto += 1

				self.tags_contador = limitador(self.tags_contador, self.tags)
				var = var+(self.input_text[:ponto] + f',#{self.tags[self.tags_contador]}')
				self.tags_contador += 1

			'''
			elif self.input_text[-1] == ',':
				self.tags_contador+=1
				self.tags_contador = limitador(self.tags_contador, self.tags)
				ponto = int(len(self.input_text) - 1)
				var = self.input_text[:ponto+1]+f'{self.input_text[0]}{self.tags[self.tags_contador]}'
			'''

		if (event.key == K_DOWN and len(self.input_text) > 0) and (self.input_text[0] in '-#'):
			if not self.input_text.find(',') != -1:
				self.tags_contador-=1
				self.tags_contador = limitador(self.tags_contador, self.tags)
				var = f'{self.input_text[0]}{self.tags[self.tags_contador]}'

			elif ',' in self.input_text:
				texto = self.input_text
				ponto = texto.find(',')
				pontotst = ponto
				while pontotst != -1:
					pontotst = self.input_text[ponto+1:].find(',')
					if pontotst > 0:
						ponto += 1
					elif pontotst == 0:
						ponto += 1

				self.tags_contador-=1
				self.tags_contador = limitador(self.tags_contador, self.tags)
				var = self.input_text[:ponto]+f',#{self.tags[self.tags_contador]}'

			'''
			elif self.input_text[-1] == ',':
				self.tags_contador-=1
				self.tags_contador = limitador(self.tags_contador, self.tags)
				ponto = int(len(self.input_text) - 1)
				var = self.input_text[:ponto+1]+f'{self.input_text[0]}{self.tags[self.tags_contador]}'
			'''

		if event.key == K_RETURN:
			if self.input_text.isnumeric():
				self.unidade = int(self.input_text)
				self.unidade = limitador(self.unidade, self.resultados['arquivos'])

			elif len(self.input_text) > 0:
				if self.input_text[0] == '#' and len(self.input_text) > 1:
					for e in self.input_text.replace(' ', '_').replace(',', ' ').replace('#', '').split():
						if len(e) > 0:
							a = registra_tag(file='information.json', name=self.resultados['arquivos'][self.unidade], tag=f'{e.lower()}', utima_id=self.unidade)
							self.tags = sorted(json.loads(open('information.json', 'r').read())['conjunto']['tags'].replace('#', ' ').split())

							self.text_tela[e] = TEMPORIZADOR(
										  	game=self,
											texto=f'{a}',
											fps=int(self.clock.get_fps()),
											segundo=.1,
											fonte=self.Fnt[0],
											cor=(0, 255, 10))

				elif self.input_text[0] == '-' and len(self.input_text) > 1:
					a = registra_tag(file='information.json', name=self.resultados['arquivos'][self.unidade], tag=f'{self.input_text[1:].lower()}', utima_id=self.unidade, delete=True)
					self.text_tela[self.input_text[1:]] = TEMPORIZADOR(
								  	game=self,
									texto=f'{a}',
									fps=int(self.clock.get_fps()),
									segundo=.1,
									fonte=self.Fnt[0],
									cor=(0, 255, 10))

				elif self.input_text[0] == '/' and len(self.input_text) > 1:
					txt = self.input_text[1:]
					obj = self.infos = json.loads(open('information.json', 'r').read())
					if txt in obj['conjunto']['tags']:
						obj['conjunto']['tags'] = obj['conjunto']['tags'].replace(f'#{txt}', '')

						obj = json.dumps(obj)
						arq = open('information.json', 'w')
						arq.write(obj)
						arq.close()
						self.tags = sorted(json.loads(open('information.json', 'r').read())['conjunto']['tags'].replace('#', ' ').split())
						self.text_tela[self.input_text[1:]] = TEMPORIZADOR(
								  	game=self,
									texto=f'a tag {txt} foi removida com sucesso do save',
									fps=int(self.clock.get_fps()),
									segundo=.1,
									fonte=self.Fnt[0],
									cor=(0, 255, 10))

					else:
						self.text_tela[self.input_text[1:]] = TEMPORIZADOR(
								  	game=self,
									texto=f'não existe a tag de nome {txt} no save',
									fps=int(self.clock.get_fps()),
									segundo=.1,
									fonte=self.Fnt[0],
									cor=(0, 255, 10))

				elif self.input_text[0] == '\\' and len(self.input_text) > 1:
					a = registra_tag(file='information.json', name=self.resultados['arquivos'][self.unidade], deleteAll=True)
					self.text_tela[self.input_text[1:]] = TEMPORIZADOR(
								  	game=self,
									texto=f'{a}',
									fps=int(self.clock.get_fps()),
									segundo=.1,
									fonte=self.Fnt[0],
									cor=(0, 255, 10))

				elif len(self.input_text) > 0 and not self.input_text[0] in '-#\\/':
					novo_resultados = []
					infos = json.loads(open('information.json', 'r').read())
					tags_pesquisar = self.input_text.replace(' ', '_').replace(',', ' ').replace('#', '').strip().split()

					for item in self.images_dir['arquivos']:
						if item in infos:
							res = True
							obj = infos[item]
							for tag in tags_pesquisar:
								if tag in obj['tags']:
									res = True

								else:
									res = False

							if res == True:
								novo_resultados.append(item)

						else:
							continue

					if len(novo_resultados) > 0:
						self.resultados['arquivos'] = novo_resultados

						if not self.mostrar_resultados[0]:
							self.posNumero['atual_antes_res']     = self.unidade
							self.posNumero['anterior_antes_res']  = self.unidade_atual

							self.posNumero = json.dumps(self.posNumero)
							arq = open('posUnidade.json', 'w')
							arq.write(self.posNumero)
							arq.close()
							self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))
							print('oi')

						self.mostrar_resultados = [True, tags_pesquisar]
						self.unidade = -1
						self.unidade = limitador(self.unidade, self.resultados['arquivos'])
						
			else:
				pass

			#if len(self.input_text):
			self.digitando = inter(self.digitando)

		if event.key == K_BACKSPACE:
			if len(var) > 0:
				return var[:-1]

		else:
			if event.unicode in abc:
				var += event.unicode

				if var[-1] == ',' and var[0] == '#':
					var += '#'

			#if len(self.input_text) > 0 and not '0' in abc:
			#	abc.append('0')
			#	abc.remove('/')

			#elif len(self.input_text) < 1 and '0' in abc:
			#	abc.append('/')
			#	abc.remove('0')

		return var

	def events_teclas(self, event):
		if event.key == K_ESCAPE:
			if self.mostrar_resultados[0]:
				self.posNumero['atual']    = self.posNumero['atual_antes_res']
				self.posNumero['anterior'] = self.posNumero['anterior_antes_res']

				self.posNumero = json.dumps(self.posNumero)
				arq = open('posUnidade.json', 'w')
				arq.write(self.posNumero)
				arq.close()
				self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))

			self.saida_real = True
			self.wait = False

		if event.key == K_F5:
			self.wait = False

		if event.key == K_BACKSPACE:
			if self.mostrar_resultados[0]:
				self.resultados = self.images_dir.copy()
				self.mostrar_resultados[0] = False
				self.atualizar_imagem  = True
				self.atualizar_forcado = True
				self.unidade = self.posNumero['atual_antes_res']
				self.posNumero['atual']    = self.posNumero['atual_antes_res']
				self.posNumero['anterior'] = self.posNumero['anterior_antes_res']

				self.posNumero = json.dumps(self.posNumero)
				arq = open('posUnidade.json', 'w')
				arq.write(self.posNumero)
				arq.close()
				self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))

				# 64034

		if event.key == K_SEMICOLON:
			self.digitando = inter(self.digitando)
			self.input_text = '#'
			self.tags_contador = 0

		if event.key == K_RETURN:
			self.digitando = inter(self.digitando)
			self.input_text = ''
			self.tags_contador = 0

		if event.key == K_F11:
			self.modo = inter(self.modo)
			if self.modo:
				self.window = self.video(width=int(GSM(0)), height=int(GSM(1)), modo=FULLSCREEN)
				self.atualizar_imagem = True

			else:
				self.window = self.video(width=self.width, height=self.height, modo=RESIZABLE)
				self.atualizar_imagem = True

		if event.key == K_u:
			self.pause = inter(self.pause)

		if event.key == K_LEFT:
			self.unidade -= 1
			if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
			self.unidade = limitador(self.unidade, self.resultados['arquivos'])

		if event.key == K_RIGHT:
			self.unidade += 1
			if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
			self.unidade = limitador(self.unidade, self.resultados['arquivos'])

		if event.key == K_z:
			self.avaca = inter(self.avaca)
			self.text_tela['avanso'] = TEMPORIZADOR(
				game=self,
				texto=f'pode avança? {self.avaca}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_p:
			w, h = self.image.get_size()
			self.image = pygame.image.load(self.resultados['arquivos'][self.unidade]).convert_alpha()
			self.image = pygame.transform.scale(self.image, (int(w * 1.1), int(h * 1.1)))
			self.calculos()

		if event.key == K_b:
			if not self.posNumero['anterior'] is None:
				self.unidade = int(self.posNumero['anterior'])
				if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
				self.atualizar_imagem = True

		if event.key == K_c:
			filepath = self.resultados['arquivos'][self.unidade]

			imagec = Image.open(filepath)
			output = BytesIO()
			imagec.convert("RGBA").save(output, "BMP")
			data = output.getvalue()[14:]
			output.close()

			copy_clip(win32clipboard.CF_DIB, data)
			self.text_tela['self.resultados["arquivos"][self.unidade]'] = TEMPORIZADOR(
				game=self,
				texto=f'copiado: {self.resultados["arquivos"][self.unidade]}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0])

		if event.key == K_o:
			w, h = self.image.get_size()
			self.image = pygame.image.load(self.resultados['arquivos'][self.unidade]).convert_alpha()
			self.image = pygame.transform.smoothscale(self.image, (int(w * .9), int(h * .9)))
			self.calculos()

		if event.key == K_r:
			#
			self.reset_pos = inter(self.reset_pos)

		if event.key == K_SPACE:
			self.unidade = random.randint(0, len(self.resultados['arquivos'])-1)
			if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
			self.atualizar_imagem = True

		if event.key == K_DELETE:
			'''clicando em DELETE para deletar uma palavra'''
			self.text_tela[self.images_dir["arquivos"][self.unidade]] = TEMPORIZADOR(
								  	game=self,
									texto=f'{self.images_dir["arquivos"][self.unidade]} foi removida com sucesso do save',
									fps=int(self.clock.get_fps()),
									segundo=.5,
									fonte=self.Fnt[0],
									cor=(0, 255, 10))
			sub.Popen(['del', f'{self.images_dir["arquivos"][self.unidade]}'], shell=True)
			registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], deleteAll=False)
			del(self.images_dir['arquivos'][self.unidade])
			del(self.images_dir['arquivos'][self.unidade])
			if self.reset_pos: posImage = pygame.Vector2(0, 0)
			self.atualizar_imagem = True
			self.atualizar_forcado = True

		if event.key == K_HOME:
			self.unidade = 0
			if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
			self.atualizar_imagem = True
			self.atualizar_forcado = True

		if event.key == K_END:
			self.unidade = int(len(self.resultados['arquivos'])-1)
			if self.reset_pos: self.posImage = pygame.Vector2(0, 0)
			self.atualizar_imagem = True
			self.atualizar_forcado = True

		if event.key == K_EQUALS:
			if not self.ajustar_largura:
				if self.reset_pos:
					self.posImage = pygame.Vector2(0, 0)
			self.ajustar_largura = inter(self.ajustar_largura)
			self.atualizar_imagem = True
			self.atualizar_forcado = True

		if event.key == K_MINUS:
			if not self.ajustar_altura:
				if self.reset_pos:
					self.posImage = pygame.Vector2(0, 0)

			self.ajustar_altura = inter(self.ajustar_altura)
			self.atualizar_imagem = True
			self.atualizar_forcado = True

		if event.key == K_RIGHTBRACKET:
			self.image = pygame.transform.flip(self.image, 0, -1)
			pass

		if event.key == K_LEFTBRACKET:
			self.image = pygame.transform.flip(self.image, -1, 0)
			pass
				
		if event.key == K_1: #loli
			self.nova_etiqueta = 'loli'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_2: #shota
			self.nova_etiqueta = 'shota'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_3: #furry
			self.nova_etiqueta = 'furry'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_4: #trap
			self.nova_etiqueta = 'trap'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_5: #peitoes
			self.nova_etiqueta = 'peitao'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_6:
			self.nova_etiqueta = 'yuri'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_7:
			self.nova_etiqueta = 'yaoi'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_8:
			self.nova_etiqueta = 'colecao'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_9:
			self.nova_etiqueta = 'no_hentai'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))

		if event.key == K_0:
			self.nova_etiqueta = 'elfa'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
				game=self,
				texto=f'{a}',
				fps=int(self.clock.get_fps()),
				segundo=.1,
				fonte=self.Fnt[0],
				cor=(0, 255, 10))
		if event.key == K_m:
			self.nova_etiqueta = 'succubus'
			a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
			self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
							game=self,
							texto=f'{a}',
							fps=int(self.clock.get_fps()),
							segundo=.1,
							fonte=self.Fnt[0],
							cor=(0, 255, 10))

	def events(self):
		for event in pygame.event.get():
			#print(event)
			#if event.type == 32781: #maxmização da janela
			#	print(event)

			if event.type == QUIT:
				if self.mostrar_resultados[0]:
					self.posNumero['atual']    = self.posNumero['atual_antes_res']
					self.posNumero['anterior'] = self.posNumero['anterior_antes_res']

					self.posNumero = json.dumps(self.posNumero)
					arq = open('posUnidade.json', 'w')
					arq.write(self.posNumero)
					arq.close()
					self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))
					
				self.saida_real = True
				self.wait = False

			if event.type == MOUSEBUTTONDOWN:
				'''pegue os eventos dos botões do mouse'''
				new_w = self.window.get_rect()
				if event.button == 1:
					if event.pos[0] > int(int(new_w.width/3)*2):
						# print('direita')
						self.unidade += 1
						if self.reset_pos: 
							self.posImage = pygame.Vector2(0, 0)
						self.atualizar_imagem = True

					elif event.pos[0] < int(new_w.width/3): 
						# print('esquerda')
						self.unidade -= 1
						if self.reset_pos: 
							self.posImage = pygame.Vector2(0, 0)
						self.atualizar_imagem = True

					else:
						'''
						self.nova_etiqueta = 'succubus'
						a = registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)
						self.text_tela[self.nova_etiqueta] = TEMPORIZADOR(
							game=self,
							texto=f'{a}',
							fps=int(self.clock.get_fps()),
							segundo=.1,
							fonte=self.Fnt[0],
							cor=(0, 255, 10))
						'''
						# print('meio')
						#self.unidade = random.randint(0, len(self.resultados['arquivos'])-1)
						#if self.reset_pos: 
						#	self.posImage = pygame.Vector2(0, 0)
						#self.atualizar_imagem = True
						pass

			if event.type == VIDEORESIZE:
				nw, nh = event.size
				self.window = self.video(width=nw, height=nh, modo=RESIZABLE)
				self.atualizar_forcado = True
				self.atualizar_imagem = True
				# print('mexeu?')


			if event.type == MOUSEWHEEL:
				if not self.digitando: 
					self.event_mouse(event)

			if event.type == KEYDOWN:
				if not self.digitando: 
					self.events_teclas(event)

				else:
					# print(f'{self.input_text}')
					self.input_text = self.event_teclas_escrever(var=self.input_text, event=event)

	def nextee_images(self):
		if self.frame.time_out():
			saida_dado = False
			if not self.time_next_images > 2*30:
				self.time_next_images += 1
				saida_dado = False

			else:
				self.unidade += 1
				self.time_next_images = 1
				self.atualizar_imagem = True
				saida_dado = True
				#if self.reset_pos:self.posImage = pygame.Vector2(0, 0)
			contagem_time = self.Fnt[1].render(f'{self.time_next_images}', True, (0, 0, 0), (255, 255, 255))
			self.window.blit(contagem_time, [10, 10])

	def ajustar_altura_tela(self):
		'''para que eu possa ajusta a largura da imagem com a da tela'''
		win = self.window.get_rect()
		img =  self.image.get_rect()
		xi = yi = 0
		size = self.image.get_size()
		dumb = self.image

		while True:
			# testa se a altura da imagem é maior que a da tela se for ele ira diminuir
			if win.height > img.height:
				xi, yi = dumb.get_size()
				size = ( int(xi * 1.1), int(yi * 1.1))
				dumb = pygame.transform.smoothscale(dumb, size)

			else:
				break

			img = dumb.get_rect()
			# print('menor')

		while True:
			# testa se a altura da imagem é menor que a da tela se for ele ira aumentar
			if win.height < img.height:
				xi, yi = dumb.get_size()
				size = ( int(xi * .9), int(yi * .9)) 
				dumb = pygame.transform.smoothscale(dumb,  size)

			else:
				break
			img = dumb.get_rect()
			# print('maior')

		# ira carregar a imagem de novo para remimencionar a imagem com a nova dimensão
		self.image = pygame.image.load(self.resultados['arquivos'][self.unidade]).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, size)

	def ajustar_largura_tela(self):
		'''para que eu possa ajusta a largura da imagem com a da tela'''
		win = self.window.get_rect()
		img =  self.image.get_rect()
		xi = yi = 0
		size = self.image.get_size()
		dumb = pygame.Surface((size))

		while True:
			# testa se a largura da imagem é maior que a da tela se for ele ira diminuir
			if win.width > img.width:
				xi, yi = dumb.get_size()
				size = ( int(xi * 1.1), int(yi * 1.1))
				dumb = pygame.transform.smoothscale(dumb, size)
			else:
				break

			img = dumb.get_rect()
			# print('menor')

		while True:
			# testa se a largura da imagem é menor que a da tela se for ele ira aumenta
			if win.width < img.width:
				xi, yi = dumb.get_size()
				size = ( int(xi * .9), int(yi * .9)) 
				dumb = pygame.transform.smoothscale(dumb,  size)
				if not win.height < img.height:
					break
			else:
				break
			img = dumb.get_rect()
			# print('maior')

		# ira carregar a imagem de novo para remimencionar a imagem com a nova dimensão
		self.image = pygame.image.load(self.resultados['arquivos'][self.unidade]).convert_alpha()
		self.image = pygame.transform.smoothscale(self.image, size)

	def colar_image(self):
		'''para pintar a imagem na tela'''
		self.window.fill((20, 20, 20)) # limpa a tela

		imagetst = self.image.get_rect()
		windotst = self.window.get_rect()
		if ((int(self.posImage.x+imagetst.width) < 0) or (self.posImage.x > windotst.width) 
		or (int(self.posImage.y+imagetst.height) < 0) or (self.posImage.y > windotst.height)):
			# se a imagem tiver fora da tela ela apareceu uma linnha indicando a posi~ção da imagem
			centerW = self.window.get_rect().center
			centerI = self.image.get_rect()
			centerI.move_ip(self.posImage)

			#desenha uma linha do centro da tela ate o centro da imagem
			pygame.draw.line(self.window, (255, 255, 32), centerI.center, centerW, 2)

		#if not self.rodar_gif()[0]:
		self.window.blit(self.image, self.posImage)

		if self.avaca:
			# para passa a imagem sozinho
			#print('miau2')
			self.nextee_images()

		else:
			self.time_next_images = 1

		#else:
		#	self.atualizar_frame()
		#	self.window.blit(self.image, self.posImage)

	def atualizar_frame(self):
		formato = 'RGBA'
		self.gif.seek(self.frame.frame)
		data = self.gif.tobytes('raw', formato)
		self.image = pygame.image.fromstring(data, self.image.get_size(), formato)

	def teste(self):
		# a = open('information.json', 'r+')
		# info = json.loads(a.read())
		return 0

	def calculos(self):
		w, h = self.image.get_size()
		sizei = (w + h) / 2
		sizet = (500 + 500) / 2
		#if sizet > sizei:
		#	sub.Popen(['del', f'{self.images_dir["arquivos"][self.unidade]}'], shell=True)
		#	del(self.images_dir['arquivos'][self.unidade])
		#	del(self.images_dir['arquivos'][self.unidade])
		#	if self.reset_pos: posImage = pygame.Vector2(0, 0)
		#	self.atualizar_imagem = True

		self.teste()

		if (self.ajustar_largura and self.unidade_atual != self.unidade) or self.atualizar_forcado and self.ajustar_largura:
			self.ajustar_largura_tela()

		if (self.ajustar_altura and self.unidade_atual != self.unidade) or self.atualizar_forcado and self.ajustar_altura:
			self.ajustar_altura_tela()

		if (self.centralizar and self.unidade_atual != self.unidade) or self.atualizar_forcado:
			new_photo =  self.image.get_rect()
			new_window = self.window.get_rect()
			new_photo.center = new_window.center
			self.posImage.x = new_photo.x

		#if self.rodar_gif()[0]:
		#	formato = 'RGBA'
		#	image = Image.open(self.resultados['arquivos'][(self.unidade)])
		#	self.gif = image.resize(self.image.get_size())
		#	self.gif = self.gif.convert(formato)
		#	data = self.gif.tobytes('raw', formato)
		#	self.image = pygame.image.fromstring(data, self.image.get_size(), formato)

	def escolher_imagem(self):
		if self.unidade_atual != self.unidade or self.atualizar_imagem:
			# print(self.resultados['arquivos'][(self.unidade)])
			self.image = pygame.image.load( self.resultados['arquivos'][self.unidade] ).convert_alpha()

			self.calculos()
			if self.iniciar_tela: # para quando o programa iniciar ele pegar os utimos pos
				self.unidade_atual = int(self.posNumero['anterior'])
				self.iniciar_tela = False
			
			if self.posNumero['atual'] != self.unidade:
				self.posNumero['atual']     = self.unidade
				self.posNumero['anterior']  = self.unidade_atual

				self.posNumero = json.dumps(self.posNumero)
				arq = open('posUnidade.json', 'w')
				arq.write(self.posNumero)
				arq.close()
				self.posNumero = json.loads(open('posUnidade.json', 'r').read().replace('\n', ''))

			self.unidade_atual = self.unidade
			self.atualizar_forcado = False
			self.atualizar_imagem  = False

			if not self.mostrar_resultados[0]:
				registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=self.unidade)

			else:
				teste = json.loads(open('information.json', 'r').read())

				if self.images_dir['arquivos'][self.unidade] in teste:
					obj = teste[self.images_dir['arquivos'][self.unidade]]
					registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta, utima_id=obj['utima_id'])

				else:
					registra_tag(file='information.json', name=self.images_dir['arquivos'][self.unidade], tag=self.nova_etiqueta)

	def update(self):
		self.events()
		if not self.digitando:
			self.events_repetitivos()

		self.escolher_imagem()
		self.rodar_gif()
		self.colar_image()
		self.escrever_temporizado()
		
	def run(self, fps=None):
		self.start_programmer()
		while self.wait:
			self.nova_etiqueta = None
			if not fps is None and str(fps).isnumeric():
				self.clock.tick(fps)
			self.update()

			w, h = self.image.get_size()
			if self.digitando:
				rgb = (255, 255, 255)
				teste = json.loads(open('information.json', 'r').read())
				tags = f'index atual: [{teste[self.resultados["arquivos"][self.unidade]]["utima_id"]}] tags: [{teste[self.resultados["arquivos"][self.unidade]]["tags"][:-1]}]'

				fnt = self.Fnt[2]
				fnt2 = self.Fnt[1]
				size = fnt2.size(tags)
				text = fnt2.render(f'{tags}', True, rgb)

				txt1 = fnt.render(f'{self.input_text}', True, rgb)
				txt2 = fnt.render(f'{"-"*w}', True, rgb)

				pygame.draw.rect(self.window, (0, 0, 0), (0, 0, int(self.window.get_size()[0]), int(size[1] * 2)))

				self.window.blit(txt1, [int(fnt.get_linesize()/2), int(fnt.get_linesize()/2)])
				self.window.blit(txt2, [0, fnt.get_linesize()])
				self.window.blit(text, [int(self.window.get_size()[0] - size[0] - 2), int(fnt2.get_linesize() / 2) - int(size[1] / 2)])

			if self.mostrar_resultados[0]:
				fnt = self.Fnt[0]
				txt = f'{len(self.resultados["arquivos"])} resultados de {self.mostrar_resultados[1]}'
				size = fnt.size(txt)
				res = fnt.render(f'{txt}', True, (0, 0, 0), (255, 255, 255))
				xp = int(self.window.get_size()[0] - size[0] - 2)
				yp = int(self.window.get_size()[1] - size[1] - 2)
				self.window.blit(res, [xp, yp])

			tutorial = self.Fnt[1].render(f'1 - loli, 2 - shota, 3 - furry, 4 - trap, 5 - peitoes, 6 - yuri, 7 - yaoi, 8 - colecao, 9 - no_hentai, 0 - elfa', True, (255, 34, 54))
			self.window.blit(tutorial, [10, self.window.get_size()[1]-32])

			'''
			if self.pause:
				pygame.mixer.pause()

			else:
				pygame.mixer.unpause()
			'''

			self._set_title(f'{self.title} - numero imagem: {self.unidade} fps: {str(int(self.clock.get_fps()))} [w:{w}x{h}:h]')
			pygame.display.update()

width  = int(GSM(0) / 1.5)#1.1)
height = int(GSM(1) / 1.5)#1.1)
title = 'VIEW_IMAGES'

criar_arquivos('posUnidade.json', text='{"anterior":0, "atual":0}')
criar_arquivos('information.json')
if __name__ == '__main__':
	saida_real = True
	while saida_real:
		app = VIEW_IMAGES(
			w=width,
			h=height,
			t=title,
			fps=30
		)
		if app.saida_real:
			saida_real = False
pygame.quit()
sys.exit(0)
