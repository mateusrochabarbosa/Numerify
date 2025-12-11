from dominio.entidades import Usuario

class CadastrarUsuarioCasoUso:
    def __init__ (self, usuario_repo):
        self.usuario_repo = usuario_repo

    def execute(self, usuario_dados):
        usuario = Usuario(**usuario_dados)
        self.usuario_repo.create(usuario)

class LoginUsuarioCasoUso:
    def __init__ (self, usuario_repo):
        self.usuario_repo = usuario_repo
    
    def execute(self, nome, senha):
        pass