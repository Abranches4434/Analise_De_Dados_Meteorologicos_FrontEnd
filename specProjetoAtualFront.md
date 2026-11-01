# SpecProjetoAtualFront — Interface Tkinter

> Documento de estado atual da interface. Deve ser atualizado após cada alteração relevante.
> Este arquivo descreve o que existe no código, não o que está planejado.

## 1. Identificação

| Item | Valor |
|---|---|
| Projeto | InterfaceAnaliseMeteorologica |
| Diretório | `/home/kaique/Área de trabalho/InterfaceAnaliseMeteorologica` |
| Tipo | Aplicação desktop Tkinter |
| Data desta atualização | 2026-10-31 |
| API consumida | `http://127.0.0.1:5000` por padrão |
| Versionamento | Repositório Git próprio, commit `7c82fa7` |

## 2. Stack

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem |
| Tkinter / ttk | Interface gráfica |
| urllib.request | Chamadas HTTP à API |
| json | Serialização |
| csv | Exportação recebida da API |

Não há dependências externas de pip. O `requirements.txt` documenta que a interface usa apenas a biblioteca padrão e o Tkinter.

## 3. Estrutura atual

```text
InterfaceAnaliseMeteorologica/
├── main.py                  # Janela principal, abas e barra de status
├── config.py                # API_URL e API_TIMEOUT
├── api.py                   # Cliente HTTP e tratamento de erros
├── requirements.txt
├── .gitignore
├── specProjetoAtualFront.md
└── ui/
    ├── __init__.py
    ├── base.py              # BaseFrame, BaseCadastroFrame e helpers
    ├── localidades.py       # CRUD de localidades
    ├── registros.py         # CRUD e filtros de registros
    ├── thresholds.py        # CRUD de thresholds
    └── analises.py          # Estatísticas, comparação, eventos, sazonalidade e CSV
```

## 4. Telas implementadas

As abas de cadastro exibem a barra de ações no topo, logo abaixo do título, com os botões Novo/Limpar, Salvar, Excluir (inativar) e Atualizar lista. A janela calcula o tamanho inicial conforme a resolução da tela, com mínimo de 1024x640.

### 4.1 Localidades

- Formulário com ID, nome, cidade, estado, latitude, longitude e ativo.
- Listagem com todas as localidades, incluindo inativas.
- Botões: novo/limpar, salvar, excluir (inativar) e atualizar lista.
- Seleção de uma linha preenche o formulário.
- Latitude e longitude aceitam vírgula ou ponto decimal.
- Após salvar ou inativar, as demais abas são atualizadas.

### 4.2 Registros

- Filtros por data inicial, data final e localidade.
- Formulário com localidade, data, hora, temperaturas, umidade, precipitação, vento, pressão e ativo.
- Listagem com nome da localidade, data/hora, variáveis e status.
- Botões: novo/limpar, salvar, excluir (inativar), atualizar lista, filtrar e limpar filtros.
- Datas no formato `AAAA-MM-DD` e horas em `HH:MM` ou `HH:MM:SS`.

### 4.3 Thresholds

- Formulário com localidade, variável, tipo de limiar, estação, valor e ativo.
- Variáveis: `TEMPERATURA`, `UMIDADE`, `PRECIPITACAO`, `VELOCIDADEVENTO`, `PRESSAOATMOSFERICA`.
- Tipos: `MAXIMO`, `MINIMO`, `DIASSEMCHUVA`.
- Estações: `ANUAL`, `PRIMAVERA`, `VERAO`, `OUTONO`, `INVERNO`.
- Listagem de todos os thresholds, incluindo inativos.
- Botões: novo/limpar, salvar, excluir (inativar) e atualizar lista.

### 4.4 Análises

- Filtros por data inicial, data final, localidade e agrupamento (`mes` ou `estacao`).
- Lista de localidades para comparação com seleção múltipla.
- Botões: estatísticas, comparação, eventos extremos e sazonalidade.
- Resultados exibidos em tabela dinâmica com rolagem.
- Exportação CSV por tipo: registros, estatísticas, comparação, eventos ou sazonalidade.
- A exportação usa diálogo para escolher o arquivo de destino.
- Eventos extremos exigem uma localidade selecionada.
- Comparação e exportação de comparação exigem pelo menos duas localidades.

## 5. Integração com a API

| Recurso | Uso |
|---|---|
| `GET /localidades` | Carregar localidades ativas e inativas |
| `POST /localidades` | Criar localidade |
| `PUT /localidades/<id>` | Alterar localidade |
| `DELETE /localidades/<id>` | Inativar localidade |
| `GET /registros` | Listar registros com filtros |
| `GET /registros/<id>` | Carregar registro selecionado |
| `POST /registros` | Criar registro |
| `PUT /registros/<id>` | Alterar registro |
| `DELETE /registros/<id>` | Inativar registro |
| `GET /thresholds` | Listar thresholds |
| `GET /thresholds/<id>` | Carregar threshold selecionado |
| `POST /thresholds` | Criar threshold |
| `PUT /thresholds/<id>` | Alterar threshold |
| `DELETE /thresholds/<id>` | Inativar threshold |
| `GET /analises/estatisticas` | Estatísticas descritivas |
| `GET /analises/comparacao` | Comparação entre localidades |
| `GET /analises/eventos-extremos` | Eventos extremos |
| `GET /analises/sazonalidade` | Médias por mês ou estação |
| `GET /exportacoes/<tipo>` | Download do CSV |

Erros da API são exibidos em caixas de diálogo com a mensagem retornada em `{"erro": "..."}`.

## 6. Configuração

Variáveis de ambiente opcionais:

| Variável | Padrão | Descrição |
|---|---|---|
| `API_URL` | `http://127.0.0.1:5000` | URL base da API |
| `API_TIMEOUT` | `15` | Tempo limite das requisições, em segundos |

## 7. Execução

```bash
# Na pasta da API
flask --app app run

# Na pasta da interface
python3 main.py
```

A API deve estar em execução antes de abrir a interface para que as tabelas sejam carregadas.

## 8. Validações realizadas

- `python3 -m compileall` sem erros.
- Importação de `main.py`, `api.py` e dos quatro frames sem erros.
- Cliente HTTP validado contra a API real para localidades, registros, thresholds, análises e CSV.
- Janela aberta com `python3 main.py` e mantida até o encerramento forçado pelo teste, sem traceback.
- Teste programático com Tkinter: criação, alteração e inativação de localidade, registro e threshold.
- Teste programático das quatro análises e preenchimento das tabelas de resultado.
- Capturas reais das abas geradas para a apresentação em PPTX/PDF, com a barra de ações visível.
- Banco restaurado para os dados de demonstração após os testes.

## 9. Problemas conhecidos e limitações

- Não há suíte automatizada de testes da interface; a validação é manual e programática.
- O `.gitignore` foi adicionado e os caches `__pycache__` foram removidos do índice do Git.
- A interface carrega todos os registros do período filtrado; não há paginação.
- Localidades, registros e thresholds inativos aparecem nas listagens, mas não podem ser usados em novos registros/thresholds.
- A interface depende de a API estar em execução e acessível na URL configurada.
- Não há máscara de data/hora; a validação ocorre ao salvar.
- O layout é ajustado à resolução da tela; em 1366x768 a janela abre com 1240x688, mantendo a barra de ações visível.

## 10. Histórico de atualizações

| Data | Alteração documentada |
|---|---|
| 2026-10-30 | Estrutura inicial com abas de localidades, registros, thresholds e análises; CRUD, filtros, análises e exportação CSV |
| 2026-10-31 | Adicionado `.gitignore`, removidos caches do índice e capturas da interface usadas na apresentação |
| 2026-10-31 | Barra de ações reposicionada para o topo das abas e geometria da janela ajustada à resolução da tela |
