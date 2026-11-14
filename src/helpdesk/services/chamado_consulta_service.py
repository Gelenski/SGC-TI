from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria


class ChamadoConsultaService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria):
        self.chamado_repo = chamado_repo

    # F10 - Listar todos os chamados
    def listar_chamados(self):
        return sorted(
            self.chamado_repo.listar_todos(),
            key=lambda chamado: chamado.id
        )

    # F10 - Buscar chamado pelo ID
    def buscar_chamado(self, chamado_id):
        return self.chamado_repo.buscar_por_id(chamado_id)

    # F11 - Filtrar chamados
    def filtrar_chamados(
        self,
        status=None,
        categoria=None,
        solicitante_id=None,
        responsavel_id=None,
        termo=None
    ):
        chamados = self.chamado_repo.listar_todos()
        resultado = []

        for chamado in chamados:
            if status is not None and chamado.status != status:
                continue

            if categoria and chamado.categoria.nome.casefold() != categoria.strip().casefold():
                continue

            if solicitante_id and chamado.solicitante.id != solicitante_id:
                continue

            if responsavel_id and (
                chamado.responsavel is None
                or chamado.responsavel.id != responsavel_id
            ):
                continue

            if termo:
                termo_busca = termo.strip().casefold()
                campos = [
                    chamado.titulo,
                    chamado.descricao,
                    chamado.categoria.nome
                ]

                if not any(
                    termo_busca in (campo or "").casefold()
                    for campo in campos
                ):
                    continue

            resultado.append(chamado)

        return sorted(resultado, key=lambda chamado: chamado.id)

    consultar_com_filtros = filtrar_chamados