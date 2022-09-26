## Gestor de Tarefa.
Criei um aplicativo de tarefas pendentes funcional para a linha de comando usando Python e Typer.
Este aplicativo foi criado para gerenciar a tarefas do dia-dia, 
atraves da CLI com ele voçê pode criar, marcar como conluido 
as suas tarefas.


## Instruções para executar.
> Execute o seguite comamdo no ponto de entrada para listar todas suas tarefas:
	- py -m rptodo_project lista

> Inicializa a BD(Base de Dados)
	- py -m rptodo_project init


> Crie tarefas, adicione prioridade para cada tarefa, marca como concluido:
	- py -m rptodo_project add "nome da tarefa".
	- py -m rptodo_project add "nome da tarefa" -p 2.


## Requerimentos:
- python
- typer
- colorama


## Meta
Samuel K. Africano  – kandumboafricano@gmail.com


## Contribuir

1. Faça o _fork_ do projeto (https://github.com/SamuelAfricano/GestordeTarefa.git)
2. Crie uma _branch_ para sua modificação (`git checkout -b feature/fooBar`)
3. Faça o _commit_ (`git commit -am 'Add some fooBar'`)
4. _Push_ (`git push origin feature/fooBar`)
5. Crie um novo _Pull Request_

