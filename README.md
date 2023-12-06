# pyHeat1D

Solução de um problema de tranferencia de `calor 1D` em `volume finitos`.

Rodando uma análise:

```bash
pyheat1d run simulations/newton.json
```

plotando resultados:

```bash
pyheat1d plot simulations --steps "0, 50, 100, 150, 200"
```

## Arquivo de enrada

Exemplo de arquivo de entrada:

```json
{
    "length": 50.0,
    "ndiv": 100,
    "dt": 5.0,
    "nstep": 1000,
    "write_every_steps": 10,
    "lbc": {
        "type": 1,
        "params": {
            "value": 10.0
        }
    },
    "rbc": {
        "type": 3,
        "params": {
            "value": 30.0,
            "h": 1.0
        }
    },
    "initialt": 20.0,
    "prop": {
        "k": 1.0,
        "ro": 2.0,
        "cp": 3.0
    }
}
```

Informações:

    * length: Dimensão do dominio.
    * ndiv: número de divisões da malha.
    * dt: Passo de termpo.
    * write_every_steps: Escreve os resultas a cada `N` passos de tempo.
    * lbc: Condição de contorno a esquerda.
    * rbc: Condição de contorno a direita.
    * initialt: Temperatura inicial.
    * prop: Propriedades do material.
