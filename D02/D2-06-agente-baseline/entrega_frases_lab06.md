# Laboratório 06 — entrega (item 5 da entrega final)

**Métrica primária do PEAS** (`agent-spec.md` §4): recall da classe "alto"
= 5/8 = **0,625**, sobre `adaptacao-ams/casos-lab-06-v2.csv` (30 casos, 8
de risco alto — dados reais do AI4I2020, não a reserva do pacote).

**Onde o agente erra, e por quê:** o agente erra mais pro lado de ser
exigente demais — 5 dos 9 erros são casos que passaram do limiar de
desgaste ou vibração e foram mandados parar, quando bastava inspecionar,
porque a regra não tem meio-termo. Nos 3 erros mais graves, o problema é o
oposto: a máquina falhou de verdade sem que desgaste nem vibração
estivessem altos, e o agente não teve motivo pra agir.
