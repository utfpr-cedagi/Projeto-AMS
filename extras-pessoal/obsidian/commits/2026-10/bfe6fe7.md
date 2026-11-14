---
gerado: true
hash: bfe6fe7d33b35ea49316398eefa95b53e870e9b9
data: 2026-10-24
autor: Daniel Martinhao
branches:
  - feature/D02_E04
  - feature/D03_E01
  - uv-setup
tags:
  - commit
  - disciplina/D02
---

# bfe6fe7 — Re-rotula consultas_ams.py (D2-03/04/05) pro domínio de manutenção segura

**Data:** 2026-10-24 · **Autor:** Daniel Martinhao
**Branches:** [[feature-D02_E04]], [[feature-D03_E01]], [[uv-setup]]
**Pais:** [[71c7d99]]

- Troca o vocabulário de produção/estoque (peças vendidas, insumos,
  fornecedor) pelo de diagnóstico de manutenção (vibração, temperatura
  do mancal, histórico de intervenções, pendências de OS) nas três
  cópias de consultas_ams.py e no bloco colado em agent-spec.md §7 —
  coerente com o resto do PEAS/dimensões/restrições, que já é sobre
  risco de falha e LOTO, não planejamento de produção
- Latências e estrutura de cobertura (quais fontes fornecem quais
  fatos) ficam IDÊNTICAS às anteriores — só o texto muda, então as
  tabelas de busca já medidas nos labs 04/05 continuam válidas sem
  re-rodar (confirmado: verificar-formulacao.py 6/6 verde, esqueleto.py
  reproduz os mesmos números, pytest 6/6 verde)
- Corrige uma citação ao nome antigo da fonte ("consultoria externa de
  capacidade") no parágrafo da dominância de D2-05/tabela_resultado_01.md
- D02/PLANO-renomeacao-dominio-consultas.md: registra o mapa completo
  de renomeação e o raciocínio da decisão (anotação de trabalho, não
  entregável)

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

## Relacionado

- [[D2-03-formular-como-busca]]
- [[D2-04-busca-nao-informada]]
- [[D2-05-busca-informada]]
- [[D02]]
- [[agent-spec-07-Formulacao-por-busca]]

## Arquivos (6)

- `D02/D2-03-formular-como-busca/comum/problemas/consultas_ams.py`
- `D02/D2-04-busca-nao-informada/comum/problemas/consultas_ams.py`
- `D02/D2-05-busca-informada/comum/problemas/consultas_ams.py`
- `D02/D2-05-busca-informada/tabela_resultado_01.md`
- `D02/PLANO-renomeacao-dominio-consultas.md`
- `agent-spec.md`

<!-- manual -->
