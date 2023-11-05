# Guia de Desenvolvimento

## Ambiente de desenvolvimento

Para gerenciar o as dependencias foi utilizado poetry. Para criar instala-las basta

```bash
poerty install
```

## Qualidade de código

Formatador com `black` e `ruff`:

```bash
task fmt
```

Linter com `ruff` e `mypy`:

```bash
task linter
```

Testes com o `pytest`:

```bash
task tests
```

## Pre-commit

Para configura o pre-commmit pela a primeira fez:

```bash
pre-commit install
```


## Gerando a documentação

Para a documenntação foi utilizado o `mkdocs`. Para subir o servidor local da documentação:

```
task doc
```
