# DataQuantum Logger

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Pacote Python para configurar logs de forma simples e reutilizável, permitindo registrar mensagens em arquivos e, opcionalmente, exibi-las no console.

Ideal para aplicações Python, pipelines ETL, APIs e projetos de engenharia de dados que precisam registrar informações de execução, avisos e erros.

## Funcionalidades

- Gravação de logs em arquivo.
- Exibição opcional de logs no console.
- Configuração do nível de logging.
- Personalização do formato das mensagens.
- Definição da codificação do arquivo de log.
- Criação automática dos diretórios necessários.
- Tratamento de erros de configuração e de sistema de arquivos.

## Instalação

Instale o pacote pelo PyPI:

```bash
pip install dataquantum-logger
```

## Como funciona?

A função `setup_logger()` recebe um dicionário Python chamado `logging_config`, que contém as configurações necessárias para inicializar o sistema de logging.

O parâmetro `show_console` controla a exibição das mensagens no console:

- `False`: registra mensagens no arquivo, sem adicionar um handler de console.
- `True`: registra mensagens no arquivo e também no console.

Exemplo:

```python
from dataquantum_logger import setup_logger

setup_logger(logging_config, show_console=True)
```

O argumento `logging_config` deve ser fornecido pelo usuário. O pacote não cria automaticamente esse dicionário nem carrega arquivos de configuração externos.

## Estrutura do parâmetro `logging_config`

O dicionário precisa conter duas seções: `logging` e `logs`.

```python
logging_config = {
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(levelname)s - %(message)s",
        "encoding": "utf-8",
    },
    "logs": {
        "file": "logs/application.log",
    },
}
```

### Parâmetros de configuração

| Chave | Descrição | Exemplo |
|---|---|---|
| `logging_config["logs"]["file"]` | Caminho do arquivo de log | `logs/application.log` |
| `logging_config["logging"]["level"]` | Nível mínimo de logging | `INFO` |
| `logging_config["logging"]["format"]` | Formato das mensagens | `%(levelname)s - %(message)s` |
| `logging_config["logging"]["encoding"]` | Codificação do arquivo | `utf-8` |

### 1. `logging_config["logs"]["file"]`

Define o caminho onde as mensagens serão armazenadas.

```python
"logs": {
    "file": "logs/application.log"
}
```

Nesse exemplo, o arquivo será criado em `logs/application.log`, relativamente ao diretório de trabalho atual do processo Python.

A função cria os diretórios intermediários caso não existam.

### 2. `logging_config["logging"]["level"]`

Define o nível mínimo das mensagens que serão registradas.

```python
"logging": {
    "level": "INFO"
}
```

Níveis comuns:

| Nível | Finalidade |
|---|---|
| `DEBUG` | Informações detalhadas para depuração |
| `INFO` | Eventos normais da aplicação |
| `WARNING` | Situações que merecem atenção |
| `ERROR` | Falhas durante a execução |
| `CRITICAL` | Falhas graves |

Por exemplo, com o nível `INFO`, mensagens `DEBUG` normalmente não serão registradas.

### 3. `logging_config["logging"]["format"]`

Define como cada mensagem será apresentada.

```python
"format": "%(asctime)s - %(levelname)s - %(message)s"
```

Os campos são substituídos automaticamente pelo módulo `logging`:

- `%(asctime)s`: data e hora.
- `%(levelname)s`: nível da mensagem.
- `%(message)s`: conteúdo da mensagem.
- `%(name)s`: nome do logger.

Exemplo de saída:

```text
2026-10-21 14:00:00,000 - INFO - Pipeline iniciado
```

### 4. `logging_config["logging"]["encoding"]`

Define a codificação utilizada para gravar o arquivo.

```python
"encoding": "utf-8"
```

O UTF-8 é uma escolha recomendada para preservar caracteres acentuados e outros caracteres Unicode.

### 5. `show_console`

Esse parâmetro pertence à função, não ao dicionário de configuração.

```python
setup_logger(logging_config)
```

A chamada acima utiliza `show_console=False`, seu valor padrão.

Para exibir mensagens no console:

```python
setup_logger(logging_config, show_console=True)
```

Em ambos os casos, o arquivo continua sendo utilizado.

## Utilizando um arquivo YAML externo

As configurações podem ser mantidas em um arquivo `config/logging.yaml`, separado do código Python.

Estrutura sugerida:

```text
meu_projeto/
├── config/
│   └── logging.yaml
├── src/
│   └── main.py
└── logs/
```

### Arquivo `config/logging.yaml`

```yaml
logging:
  level: INFO
  format: "%(asctime)s - %(levelname)s - %(message)s"
  encoding: utf-8

logs:
  file: logs/application.log
```

### Arquivo `src/main.py`

O YAML precisa ser carregado para um dicionário antes de chamar `setup_logger()`.

```python
import logging
from pathlib import Path

import yaml
from dataquantum_logger import setup_logger


def main() -> None:
    """Load configuration and initialize application logging."""
    config_path = Path("config/logging.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        logging_config = yaml.safe_load(file)

    setup_logger(logging_config, show_console=True)

    logger = logging.getLogger(__name__)
    logger.info("Aplicação iniciada.")
    logger.warning("Exemplo de aviso.")


if __name__ == "__main__":
    main()
```

Para esse exemplo, instale também o PyYAML:

```bash
pip install PyYAML
```

**Importante:** o PyYAML é utilizado apenas pelo código da aplicação que lê o arquivo YAML. Ele não é uma dependência obrigatória do DataQuantum Logger.

Execute o exemplo a partir da raiz do projeto:

```bash
python src/main.py
```

## Tratamento de erros

A função pode gerar as seguintes exceções:

- `ValueError`: quando faltam chaves obrigatórias ou existem tipos incompatíveis na configuração.
- `OSError`: quando ocorre uma falha ao criar diretórios ou abrir o arquivo de log.

Essas exceções permitem identificar problemas de configuração e de acesso ao sistema de arquivos.

## Comportamento global

A função utiliza `logging.basicConfig(..., force=True)`, que substitui os handlers existentes do logger raiz.

Por isso, recomenda-se inicializar a configuração uma vez, no início da aplicação, antes de iniciar o pipeline ou as rotas da API.

## Licença

Este projeto é distribuído sob a licença MIT.

## Autor e contato

**DataQuantum**

- GitHub: [jcarlossc](https://github.com/jcarlossc)
- Repositório: [dataquantum-yaml-reader](https://github.com/jcarlossc/dataquantum-yaml-reader)
- E-mail: jcarlossc1977@gmail.com
