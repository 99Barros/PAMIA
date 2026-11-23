# Plano de Testes — Módulo A (ISO/IEC/IEEE 29119)

**Projeto:** PAMIA — Prevenção ao Assédio contra Mulheres com Inteligência Artificial  
**Disciplina:** Qualidade de Software — PFC  
**Equipe:** 4 integrantes (2 desenvolvimento/QA e 2 documentação)  
**Versão:** MVP — Protótipo em desenvolvimento

## 1. Objetivo e Escopo

Este plano, fundamentado na ISO/IEC/IEEE 29119, estabelece a estratégia, os critérios e os recursos para validar componentes auxiliares do PAMIA.

| Componente | Funcionalidade testada | Requisito |
|---|---|---|
| Geometria | Distância euclidiana 3D e invasão espacial | RF01 |
| Score | Sanitização entre 0 e 100 e entradas inválidas | RF03 |
| Decisão multimodal | Combinações de vídeo, áudio e indicador de decaimento | RF03 |
| Desempenho | Simulação de ciclos concorrentes | RNF01 (parcial) |

**Fora do escopo:** inferência real de MediaPipe/YAMNet, processamento acústico completo (RF02), integração Android, monitoramento térmico, serviços B2B e webhooks.

## 2. Estratégia e Ambiente de Testes

São utilizados testes unitários automatizados com Pytest, aplicando classes de equivalência, análise de valores-limite (AVL), tabela de decisão com oito combinações booleanas e testes de regressão.

O `unittest.mock` simula coordenadas de um extrator de pose, sem executar MediaPipe. O desempenho é avaliado por um microbenchmark de 50 ciclos concorrentes das funções auxiliares.

**Ambiente:** Linux, Python 3.13.3, Pytest 9.2.0, pytest-cov 7.1.0 e processador AMD Ryzen 5 7535HS.

Execução a partir de `qa/`:

```bash
python -m pytest tests/ -v \
  --cov=pamia_sdk --cov-branch \
  --cov-report=term-missing \
  --junitxml=resultado-testes.xml
```

## 3. Critérios de Entrada e Saída

**Entrada:** código disponível, ambiente configurado, testes automatizados definidos e resultados esperados documentados.

**Saída:** todos os testes críticos executados e aprovados, ausência de defeitos graves conhecidos no escopo validado, relatório de cobertura e registro de defeitos e retestes.

**Resultados observados:**

| Indicador | Resultado |
|---|---:|
| Testes executados / aprovados | 32 / 32 |
| Cobertura dos módulos auxiliares | 100% |
| Instruções cobertas | 39/39 |
| Branches cobertos | 26/26 |
| Ciclos de desempenho | 250/250 corretos |
| Tempo médio por ciclo | 0,00776 ms |

A cobertura refere-se exclusivamente a `qa/pamia_sdk/geometria.py` e `threshold.py`. O teste de desempenho não inclui inferência real nem execução no Android.

## 4. Análise de Pontos de Função (APF)

Foi realizada uma estimativa funcional preliminar para o SDK local:

| Função candidata | Tipo | PF |
|---|---|---:|
| Entrada de eventos visuais | EE | 4 |
| Entrada de eventos acústicos | EE | 4 |
| Consulta do estado de decisão | CE | 3 |
| Emissão de alerta | SE | 4 |
| Configurações e limiares | ALI | 7 |
| Estado de risco e logs | ALI | 7 |
| Dados externos de referência | AIE | 5 |
| **Total preliminar** | | **34** |

Os 34 pontos representam uma aproximação acadêmica. As classificações e complexidades ainda dependem de validação por DET, RET e FTR, especialmente a classificação de dados externos como AIE. Não se trata de uma contagem IFPUG definitiva.

## 5. Estimativa de Esforço — COCOMO II

Adotou-se o modelo COCOMO II Post-Architecture com parâmetros nominais e tamanho aproximado de 2.500 SLOC (2,5 KSLOC).

**Parâmetros:** A = 2,94; B = 0,91; C = 3,67; D = 0,28; soma dos fatores de escala = 18,97; produto dos multiplicadores de esforço = 1.

**Expoente de escala:**

\[
E=0{,}91+0{,}01(18{,}97)=1{,}0997
\]

**Esforço estimado:**

\[
PM=2{,}94(2{,}5)^{1{,}0997}\approx8{,}05\text{ pessoas-mês}
\]

**Prazo nominal:**

\[
F=0{,}28+0{,}2(E-0{,}91)=0{,}31794
\]

\[
TDEV=3{,}67(8{,}05)^{0{,}31794}\approx7{,}12\text{ meses}
\]

**Equipe nominal média:**

\[
8{,}05/7{,}12\approx1{,}13\text{ FTE}
\]

### Disponibilidade da Equipe

O PAMIA possui dois desenvolvedores, cada um com oito horas semanais disponíveis, totalizando 16 horas por semana ou **0,4 FTE**, considerando jornada referencial de 40 horas.

Uma conversão simplificada do esforço estimado pela capacidade técnica disponível resulta em aproximadamente 20,1 meses, caso todo o esforço fosse atribuído aos dois desenvolvedores. Esse valor não substitui o prazo nominal do COCOMO II.

Os outros dois integrantes atuam prioritariamente na documentação. A estimativa possui caráter acadêmico e não considera detalhadamente código reutilizado, produtividade histórica e dedicação documental.


## 6. Matriz de Riscos Técnicos

| Risco | Probabilidade | Impacto | Estratégia de mitigação |
|---|---|---|---|
| Falhas na detecção espacial | Média | Alto | Testes de valores-limite e entradas inválidas |
| Falsos positivos na decisão multimodal | Média | Alto | Tabela de decisão e testes parametrizados |
| Consumo excessivo de recursos no Android | Alta | Alto | Microbenchmark local e futura validação no dispositivo |
| Falhas na integração audiovisual | Média | Alto | Mocks, testes auxiliares e integração incremental |

Os riscos foram classificados qualitativamente conforme seu impacto potencial no protótipo. Os testes automatizados atuais mitigam parcialmente esses riscos, sem comprovar o comportamento integral dos modelos de IA ou do aplicativo Android. 

## 7. Considerações Finais

O plano estabelece uma estratégia reproduzível de verificação funcional, análise de limites, automação e registro de defeitos. Os 32 testes aprovados e a cobertura integral dos módulos auxiliares representam resultados positivos no escopo avaliado.

Contudo, a validação não abrange integralmente os componentes reais de inteligência artificial e o aplicativo móvel. A APF e o COCOMO II são estimativas preliminares de planejamento, com limitações explicitadas.

## Referências

- BOEHM, B. et al. *Software Cost Estimation with COCOMO II*. Prentice Hall, 2000.
- ISO/IEC/IEEE 29119. *Software and Systems Engineering — Software Testing*.
- IFPUG. *Function Point Counting Practices Manual*.
- PRESSMAN, R.; MAXIM, B. *Engenharia de Software: Uma Abordagem Profissional*. 9. ed., 2021.