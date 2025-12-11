from django.db import models

class UsuarioModel (models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    senha = models.CharField(max_length=255)

class ConteudoModel (models.Model):
    id_conteudo = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descricao = models.CharField(max_length=1000)
    dificuldade = models.CharField(max_length=15)

    usuarios = models.ManyToManyField(
        UsuarioModel,
        through="ConteudosUsuariosModel"
    )

class ConteudosUsuariosModel (models.Model):
    id_conteudo = models.ForeignKey(ConteudoModel, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(UsuarioModel, on_delete=models.CASCADE)