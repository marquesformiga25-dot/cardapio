from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_ifpb'

respostas = []

usuario_admin = 'cozinha'
senha_admin = 'ifpb123'


@app.route('/')
def inicial():
    return render_template('index.html')


@app.route('/identificar', methods=['POST'])
def identificar():

    nome = request.form.get('nome')
    matricula = request.form.get('matricula')

    session['nome'] = nome
    session['matricula'] = matricula

    return render_template('decisao.html', nome=nome)


@app.route('/decisao', methods=['POST'])
def decisao():

    escolha = request.form.get('refeicao')

    if escolha == 'nao':

        respostas.append({
            'nome': session.get('nome'),
            'matricula': session.get('matricula'),
            'refeicao': 'Não',
            'alimentos': []
        })

        return render_template(
            'agradecimento.html',
            nome=session.get('nome'),
            titulo='Obrigado pela colaboração!',
            mensagem='Sua resposta ajuda a reduzir o desperdício de alimentos.',
            alimentos=[]
        )

    return render_template(
        'cardapio.html',
        nome=session.get('nome')
    )


@app.route('/finalizar', methods=['POST'])
def finalizar():

    alimentos = request.form.getlist('alimentos')

    respostas.append({
        'nome': session.get('nome'),
        'matricula': session.get('matricula'),
        'refeicao': 'Sim',
        'alimentos': alimentos
    })

    return render_template(
        'agradecimento.html',
        nome=session.get('nome'),
        titulo='Pré-seleção realizada!',
        mensagem='Obrigado por participar! Sua escolha contribui para a redução do desperdício.',
        alimentos=alimentos
    )


# LOGIN DO RESPONSÁVEL
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        if usuario == usuario_admin and senha == senha_admin:

            session['admin_logado'] = True

            return redirect('/painel_admin')

        return redirect('/admin')

    return render_template('login_admin.html')


# PAINEL COM AS TABELAS
@app.route('/painel_admin')
def painel_admin():

    if not session.get('admin_logado'):
        return redirect('/admin')

    quantidade_sim = 0
    quantidade_nao = 0
    alunos_que_vao_comer = []

    for resposta in respostas:

        if resposta['refeicao'] == 'Sim':
            quantidade_sim += 1
            alunos_que_vao_comer.append(resposta)

        else:
            quantidade_nao += 1

    return render_template(
        'admin.html',
        quantidade_sim=quantidade_sim,
        quantidade_nao=quantidade_nao,
        alunos_que_vao_comer=alunos_que_vao_comer,
        respostas=respostas
    )


# SAIR
@app.route('/sair_admin')
def sair_admin():

    session.pop('admin_logado', None)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)