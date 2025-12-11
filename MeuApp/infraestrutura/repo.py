from dominio.entidades import Conteudo
from adaptadores.models import ConteudoModel
from dominio.entidades import Usuario
from adaptadores.models import UsuarioModel

class UsuarioRepo:
    def create(self, usuario: Usuario):
        usuario_model = UsuarioModel(
            nome = usuario.nome,
            senha = usuario.senha
        )
        usuario_model.save()
        return usuario_model

class ConteudoRepo:
    def create(self, conteudo: Conteudo):
        conteudo_model = ConteudoModel(
            titulo = conteudo.titulo,
            descricao = conteudo.descricao,
            dificuldade = conteudo.dificuldade
        )
        conteudo_model.save()
        return conteudo_model