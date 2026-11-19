# PAMIA QA — Suíte de Qualidade de Software

Pasta de QA do projeto **PAMIA** (Prevenção ao Assédio contra Mulheres com Inteligência Artificial).
Desenvolvida como Entrega Única Final da disciplina de Qualidade de Software (PFC).

## Estrutura

```
qa/
├── pamia_sdk/              # Módulos locais de lógica do SDK (Edge Computing)
│   ├── __init__.py
│   ├── geometria.py        # Distância euclidiana 3D e classificação de invasão espacial
│   └── threshold.py        # Sanitização de score e fusão multimodal
├── tests/                  # Suíte de testes (Módulo C)
│   ├── __init__.py
│   ├── test_sdk_local.py       # Testes unitários: CE, AVL, Tabela de Decisão, Mocks
│   └── test_desempenho_local.py # Teste de carga concorrente (50 threads)
└── docs/                   # Documentação de QA (Módulos A e B)
    ├── plano_testes_modulo_a.md        # ISO/IEC 29119, APF e COCOMO II
    ├── design_testes_modulo_b.md       # CE, AVL, Tabela de Decisão, IHC, Casos de Teste
    └── relatorio_qualidade_final.md    # Matriz de rastreabilidade e registro de defeitos
```

## Como Executar

```bash
# Dentro da pasta qa/
pip install pytest pytest-cov

# Suíte completa com cobertura
pytest --cov=pamia_sdk --cov-report=term-missing -v

# Teste de desempenho local isolado
python tests/test_desempenho_local.py
```

## Cobertura Esperada

- `pamia_sdk/geometria.py` — ≥ 95%
- `pamia_sdk/threshold.py` — 100%
