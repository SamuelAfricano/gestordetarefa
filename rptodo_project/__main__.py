"""Ponto de entrada do script."""
from rptodo_project.rptodo import cli

def main():
    cli.app(prog_name="constantes.__app_name__")

if __name__ == "__main__":
    main()