## Lab 01
**Executando com NORMALIZAR = False**

``` bash
(ams) PS C:\temp\UTFPR\Projeto-AMS> uv run .\D03\D3-01-vetores-do-meu-dominio\esqueleto.py 
conjunto: dados/manutencao · 200 frases · 384 dimensões
normalizar: False  (troque a linha NORMALIZAR e rode de novo — a comparação do slide 18 é esta linha)

mais parecidos (por cosseno):
   1. cos 0.9780  eucl 0.7966  ( 35,  36) "Afrouxe os parafusos do mancal em ordem cru…" / "Aperte os parafusos do mancal em ordem cruz…"
   2. cos 0.9426  eucl 1.3691  ( 30,  31) "Abra a válvula de alívio antes de iniciar o…" / "Feche a válvula de alívio antes de iniciar …"
   3. cos 0.9348  eucl 1.4036  ( 32,  33) "Suba a pressão do sistema lentamente até o …" / "Baixe a pressão do sistema lentamente até o…"
   4. cos 0.8866  eucl 1.8324  (  0,   1) "A vibração da bomba centrífuga subiu para 7…" / "A vibração da bomba centrífuga não subiu pa…"
   5. cos 0.8407  eucl 2.2871  (  9,  10) "O compressor parafuso está operando com tem…" / "O compressor parafuso não está operando com…"
   6. cos 0.8190  eucl 2.5602  ( 68, 104) "A malha de controle de temperatura do forno…" / "O forno de recozimento atingiu a temperatur…"
   7. cos 0.8034  eucl 2.6698  ( 68, 107) "A malha de controle de temperatura do forno…" / "A chaminé do forno precisa de inspeção de r…"
   8. cos 0.8024  eucl 2.2974  ( 89,  90) "O registro de manutenção da caldeira está a…" / "O registro de manutenção da caldeira não es…"
   9. cos 0.7675  eucl 2.5908  ( 15, 102) "A pista externa do rolamento do ventilador …" / "O ventilador exaustor da cabine de pintura …"
  10. cos 0.7670  eucl 2.6366  ( 52,  53) "O CLP da linha registrou falha intermitente…" / "O controlador programável da linha registro…"

mais distantes (por cosseno):
   1. cos -0.2128  eucl 6.0165  ( 26, 143) "Registre as horas-homem da intervenção no s…" / "O líquido penetrante nas soldas do tanque n…"
   2. cos -0.1959  eucl 6.0758  ( 72, 178) "A chaveta da polia da bomba está com folga …" / "As compras de longo prazo da parada foram l…"
   3. cos -0.1769  eucl 5.6800  ( 23, 145) "Planeje a parada programada da linha dois p…" / "O ensaio por ultrassom das juntas soldadas …"
   4. cos -0.1749  eucl 5.7913  (  3,  26) "A análise de óleo do redutor não detectou p…" / "Registre as horas-homem da intervenção no s…"
   5. cos -0.1727  eucl 5.4726  ( 41, 149) "O bloqueio e a etiquetagem da chave geral s…" / "A termografia da chaminé não indicou infilt…"
   6. cos -0.1712  eucl 5.9650  ( 18, 121) "A correia dentada apresenta trincas na face…" / "O motor da bomba de incêndio tem potência d…"
   7. cos -0.1695  eucl 5.8378  (  3,  23) "A análise de óleo do redutor não detectou p…" / "Planeje a parada programada da linha dois p…"
   8. cos -0.1612  eucl 5.8336  ( 41, 143) "O bloqueio e a etiquetagem da chave geral s…" / "O líquido penetrante nas soldas do tanque n…"
   9. cos -0.1559  eucl 5.3783  (  3, 113) "A análise de óleo do redutor não detectou p…" / "O nobreak da sala de controle está operando…"
  10. cos -0.1532  eucl 5.7809  (  1,  41) "A vibração da bomba centrífuga não subiu pa…" / "O bloqueio e a etiquetagem da chave geral s…"

agora: escolha DOIS pares que surpreenderam — um PRÓXIMO sem razão aparente e um DISTANTE que deveria estar junto (slide 19) — e anote-os em pares-surpreendentes.md. Eles voltam na D7.
(ams) PS C:\temp\UTFPR\Projeto-AMS> 
``` 

---

**Executando com NORMALIZAR = True**

``` bash
(ams) PS C:\temp\UTFPR\Projeto-AMS> uv run .\D03\D3-01-vetores-do-meu-dominio\esqueleto.py
conjunto: dados/manutencao · 200 frases · 384 dimensões
normalizar: True  (troque a linha NORMALIZAR e rode de novo — a comparação do slide 18 é esta linha)

mais parecidos (por cosseno):
   1. cos 0.9780  eucl 0.2099  ( 35,  36) "Afrouxe os parafusos do mancal em ordem cru…" / "Aperte os parafusos do mancal em ordem cruz…"
   2. cos 0.9426  eucl 0.3389  ( 30,  31) "Abra a válvula de alívio antes de iniciar o…" / "Feche a válvula de alívio antes de iniciar …"
   3. cos 0.9348  eucl 0.3612  ( 32,  33) "Suba a pressão do sistema lentamente até o …" / "Baixe a pressão do sistema lentamente até o…"
   4. cos 0.8866  eucl 0.4763  (  0,   1) "A vibração da bomba centrífuga subiu para 7…" / "A vibração da bomba centrífuga não subiu pa…"
   5. cos 0.8407  eucl 0.5644  (  9,  10) "O compressor parafuso está operando com tem…" / "O compressor parafuso não está operando com…"
   6. cos 0.8190  eucl 0.6016  ( 68, 104) "A malha de controle de temperatura do forno…" / "O forno de recozimento atingiu a temperatur…"
   7. cos 0.8034  eucl 0.6270  ( 68, 107) "A malha de controle de temperatura do forno…" / "A chaminé do forno precisa de inspeção de r…"
   8. cos 0.8024  eucl 0.6286  ( 89,  90) "O registro de manutenção da caldeira está a…" / "O registro de manutenção da caldeira não es…"
   9. cos 0.7675  eucl 0.6819  ( 15, 102) "A pista externa do rolamento do ventilador …" / "O ventilador exaustor da cabine de pintura …"
  10. cos 0.7670  eucl 0.6826  ( 52,  53) "O CLP da linha registrou falha intermitente…" / "O controlador programável da linha registro…"

mais distantes (por cosseno):
   1. cos -0.2128  eucl 1.5574  ( 26, 143) "Registre as horas-homem da intervenção no s…" / "O líquido penetrante nas soldas do tanque n…"
   2. cos -0.1959  eucl 1.5466  ( 72, 178) "A chaveta da polia da bomba está com folga …" / "As compras de longo prazo da parada foram l…"
   3. cos -0.1769  eucl 1.5342  ( 23, 145) "Planeje a parada programada da linha dois p…" / "O ensaio por ultrassom das juntas soldadas …"
   4. cos -0.1749  eucl 1.5329  (  3,  26) "A análise de óleo do redutor não detectou p…" / "Registre as horas-homem da intervenção no s…"
   5. cos -0.1727  eucl 1.5315  ( 41, 149) "O bloqueio e a etiquetagem da chave geral s…" / "A termografia da chaminé não indicou infilt…"
   6. cos -0.1712  eucl 1.5305  ( 18, 121) "A correia dentada apresenta trincas na face…" / "O motor da bomba de incêndio tem potência d…"
   7. cos -0.1695  eucl 1.5294  (  3,  23) "A análise de óleo do redutor não detectou p…" / "Planeje a parada programada da linha dois p…"
   8. cos -0.1612  eucl 1.5239  ( 41, 143) "O bloqueio e a etiquetagem da chave geral s…" / "O líquido penetrante nas soldas do tanque n…"
   9. cos -0.1559  eucl 1.5204  (  3, 113) "A análise de óleo do redutor não detectou p…" / "O nobreak da sala de controle está operando…"
  10. cos -0.1532  eucl 1.5187  (  1,  41) "A vibração da bomba centrífuga não subiu pa…" / "O bloqueio e a etiquetagem da chave geral s…"

agora: escolha DOIS pares que surpreenderam — um PRÓXIMO sem razão aparente e um DISTANTE que deveria estar junto (slide 19) — e anote-os em pares-surpreendentes.md. Eles voltam na D7.
(ams) PS C:\temp\UTFPR\Projeto-AMS> 
```
