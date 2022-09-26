"""Top-level package for RP To-Do."""

__app_name__ = "To_do"
__version__ = "1.0.1"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "Erro -> Na config do diretório",
    FILE_ERROR: "Erro -> Ficheiro de config não criado",
    DB_READ_ERROR: "Erro -> O programa não conseguio aceder a base de dados",
    DB_WRITE_ERROR: "Erro -> Dados não gavado",
    ID_ERROR: "Erro -> Id não identificado",
}
