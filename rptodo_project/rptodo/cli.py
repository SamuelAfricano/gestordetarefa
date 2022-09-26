"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import List, Optional

import typer

from rptodo_project.rptodo import( 
    ERRORS, __app_name__, __version__, config, database, rptodo
)

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-BD",
        prompt="Criando a base de dados: ",
    ),
) -> None:
    """Iniciliza as config da Base de dados."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Erro fecheiro de config não criado "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Erro -> "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"A base de dados do app é -> {db_path}", fg=typer.colors.GREEN)

def get_todoer() -> rptodo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Ficheiro de config não encotrado, executa o comando "init" ',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return rptodo.Todoer(db_path)
    else:
        typer.secho(
            'Base de dados não encotrado, executa o comando "ini" ',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(3, "--prioridade", "-p", min=1, max=3),
) -> None:
    """Adicionar uma  nova tarefa"""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
        f'Erro ao adicionar a tarefa "{ERRORS[error]}"',
        )
        raise typer.Exit(1)
    else:
        typer.secho(
        f"""Tarefa: "{todo['Descricao']}"  foi adicionado com sucesso!. \n"""
        f"""Prioridade: {priority} """,
        fg=typer.colors.GREEN
        )

@app.command(name="lista")
def list_all() -> None:
    """Mostrar a lista de tarefa """
    toder = get_todoer()
    todo_list = toder.get_todoer_list()
    if len(todo_list) == 0:
        typer.secho(
            "Não tem itens adicionado",
            fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nLista de Tarefa:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID ",
        "| Prioridade ",
        "| Feito ",
        "| Descricação ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):
        Bio, prioridade, feito = todo.values()
        typer.secho(
            f" {id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({prioridade}){(len(columns[1]) - len(str(prioridade)) - 4) * ' '}"
            f"|  {feito}{(len(columns[2]) - len(str(feito)) - 2) * ' '}"
            f"|  {Bio}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

@app.command(name="completar")
def  set_done(todo_id: int = typer.Argument(...)) -> None:
    """Marquar uma tarefa como completado."""
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f'Tarefa não completada #"{todo_id}" \n Erro -> {ERRORS[error]}',
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""Tarefa #{todo_id} "{todo['Descricao']}" está concluida!.""",
            fg=typer.colors.GREEN
            )

@app.command(name="remover")
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Apaga um item sem SMS de confirmação",
    ),
) -> None:
    """Remove um item da lista"""
    todoer = get_todoer()

    def  _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f'A tarefa #{todo_id} não pode ser removida "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""A tarefa #{todo_id}: '{todo["Descricao"]} foi removido""",
                fg=typer.colors.GREEN
            )

    if force:
        _remove()
    else:
        todo_list = todoer.get_todoer_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Tarefa inválida", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Tens a certeza que queres remover este item: #{todo_id}: {todo['Descricao']}? "
        )
        if delete:
            _remove()
        else:
            typer.Exit("Operação cancelada")

@app.command(name="apagar")
def apagar_tarefas(force: bool = typer.Option(
    False,
    "--force",
    "-f",
    prompt="Deseja apagar todas as Tarefas? ",
    help = "Apaga todos as tarefas da base de dados"
    ),
) -> None:
    todoer = get_todoer()
    if force:
        error = todoer.remove_todos().error
        if error:
            typer.secho(
                f'Erro: Tarefas não removida "{ERRORS[error]}"',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho("Todas as tarefas foram apagadas com sucesso!", 
                fg=typer.colors.GREEN
            )
    else:
        typer.secho("Operação cancelada!")
        


def _version_callback(value: bool) -> None:
    if value:
        typer.secho(f"{__app_name__} v{__version__}", fg=typer.colors.YELLOW)
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Mostra a versão do app.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
