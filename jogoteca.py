from flask import Flask, render_template, request, redirect, session, flash, url_for 


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

    def toDict(self):
        return {"nome" : self.nome, "console" : self.console, "categoria" : self.categoria} #[self.nome, self.console, self.categoria]

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo1 = jogo1.toDict()
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo2 = jogo2.toDict()
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
jogo3 = jogo3.toDict()
lista = [ jogo1, jogo2, jogo3 ]

class Usuario:
    def __init__ (self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha =senha

usuario1 = Usuario("Isabel Martins", "IM", "alohomora")
usuario2 = Usuario("Edvandro Silva", "ES", "bela2018")
usuario3 = Usuario("Ninguem do Nada", "NDoD", "naodigo")

usuarios = { usuario1.nickname : usuario1, 
             usuario2.nickname : usuario2, 
             usuario3.nickname : usuario3}

app = Flask(__name__)
app.secret_key = 'naodigo'

@app.route('/')
def index():
    return render_template('table.html', titulo='Jogos', jogos=lista)

@app.route('/lista')
def new_lista():
    if 'usuario_logado' not in session or session ['usuario_logado'] == None:
        return redirect ('/table')
    return render_template('lista.html', titulo= 'Novo Jogo', jogos=lista)

#def new_table(jogo1, jogo2, jogo3):
   # lista = [jogo1, jogo2, jogo3]
    #return lista, redirect ('lista.html', titulo= 'Novo Jogo')

@app.route ('/add', methods = ['POST']) 
def criar():
    nome = request.form ['nome']
    categoria = request.form ['categoria']
    console = request.form ['console']
    jogo = Jogo (nome, categoria, console)
    lista.append(jogo.toDict())
    return redirect (url_for('index'))

@app.route('/login')
def login ():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods = ['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios: 
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
        flash(session ['usuario_logado'] + 'logado com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect('/{}'.format(proxima_pagina))
    else:
        flash('Usuário não logado')
        return redirect (url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect (url_for('index'))       

app.run(debug=True) 