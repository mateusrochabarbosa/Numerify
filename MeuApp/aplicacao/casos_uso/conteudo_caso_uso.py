from dominio.entidades import Conteudo

class FiltrarConteudoCasoUso:
    def __init__ (self, conteudo_repo):
        self.conteudo_repo = conteudo_repo

    def execute (self, conteudo_dados):
        conteudo = Conteudo(**conteudo_dados)
        self.conteudo_repo.create(conteudo)