# Auditoria técnica, operacional e financeira — AI Revenue Engine

**Data do relatório:** 12/11/2026 — America/Sao_Paulo  
**Projeto:** dukenordj-rgb/solana-autonomous-revenue-engine  
**Painel inspecionado:** https://instances-integrate-cant-latest.trycloudflare.com/  
**Destinatário:** AntGravit / responsável pela implementação  
**Natureza:** revisão independente de leitura, sem execução dos robôs, publicação de propostas, operações financeiras ou alteração de funcionalidades.

## 1. Parecer executivo

**REPROVADO como fonte confiável de previsão financeira e certificação de conformidade.**

Há atividade real: o PR Go-Hybrid #3673 foi incorporado e o mantenedor registrou a contribuição no programa de recompensas. Entretanto, o painel mistura descoberta de oportunidades, comentários, propostas, código publicado, código aceito e dinheiro recebido. Percentuais e mensagens de sucesso são produzidos sem comprovação suficiente; oportunidades perdidas ou pausadas continuam sustentando expectativas financeiras.

A possibilidade de obter recompensas existe. Não foi demonstrada a probabilidade de recebimento anunciada, nem a projeção de milhares de dólares, nem a rentabilidade líquida da operação. Não há base suficiente para atribuir fraude intencional a uma pessoa ou concluir que todos os programas são fraudulentos. **Há base técnica para concluir que a apresentação atual é materialmente enganosa.**

Esta é a consolidação completa dos achados desta auditoria, **não uma certificação exaustiva das cerca de 900 entradas anunciadas**. Não foram acessados o processo local integral, contas privadas do Superteam, extratos de corretoras ou todos os históricos de blockchain. Ausência de evidência não foi tratada como prova de inexistência.

## 2. Método e evidências consultadas

- Leitura do painel renderizado, tabelas, JavaScript entregue ao navegador e dashboard_state.json.
- Inspeção dos arquivos públicos auto_attack_pipeline.py, cloud_revenue_agent.py e engine.py.
- Conferência de submissões e comentários diretamente no GitHub.
- Comparação com BOUNTY.md do Go-Hybrid e docs/bug-bounty.md do Paraloom.
- Revisão do anúncio de suspensão do StudentHub e do PR #134.
- Tentativas de leitura do BaseScan e de páginas Superteam sem acesso útil; esses itens permanecem não verificados.
- O ticket agent-bounty-feed #3 retornou 404 pelo conector. Isso significa indisponibilidade para esta consulta, não prova de fraude ou inexistência.

As observações do painel foram coletadas em 11/11/2026, aproximadamente às 23h15–23h16 de Brasília. O relatório e a inspeção adicional de engine.py foram concluídos em 12/11. Dados dinâmicos podem mudar; revalidar antes da correção.

### Fontes

- **E01 — Painel:** https://instances-integrate-cant-latest.trycloudflare.com/
- **E02 — Estado servido:** https://instances-integrate-cant-latest.trycloudflare.com/dashboard_state.json
- **E03 — Pipeline:** https://github.com/dukenordj-rgb/solana-autonomous-revenue-engine/blob/main/auto_attack_pipeline.py
- **E04 — Agente cloud:** https://github.com/dukenordj-rgb/solana-autonomous-revenue-engine/blob/main/cloud_revenue_agent.py
- **E05 — Engine:** https://github.com/dukenordj-rgb/solana-autonomous-revenue-engine/blob/main/engine.py
- **E06 — Regras Go-Hybrid:** https://github.com/limitlessprojects/Go-Hybrid/blob/main/BOUNTY.md
- **E07 — Aceite #3673:** https://github.com/limitlessprojects/Go-Hybrid/pull/3673#issuecomment-6657813317
- **E08 — Decisão #3782:** https://github.com/limitlessprojects/Go-Hybrid/pull/3782#issuecomment-6691063649
- **E09 — Comentário #4381:** https://github.com/limitlessprojects/Go-Hybrid/issues/4381#issuecomment-6800617056
- **E10 — Issue original #4381:** https://github.com/limitlessprojects/Go-Hybrid/issues/4381
- **E11 — Regras Paraloom:** https://github.com/paraloom-labs/paraloom-core/blob/main/docs/bug-bounty.md
- **E12 — Paraloom #1570:** https://github.com/paraloom-labs/paraloom-core/issues/1570
- **E13 — StudentHub suspenso:** https://github.com/BAWES-Universe/studenthub/issues/55#issuecomment-4472215249
- **E14 — StudentHub PR #134:** https://github.com/BAWES-Universe/studenthub/pull/134
- **E15 — Requisitos StudentHub/Algora:** https://github.com/BAWES-Universe/studenthub/issues/55#issuecomment-4450362545
- **E16 — Reiteração da pausa por contributor:** https://github.com/BAWES-Universe/studenthub/issues/55#issuecomment-6126010339

Blobs dos arquivos públicos inspecionados:
- auto_attack_pipeline.py: 17d039ee9c782caa8eb3c35ef03f2d870d70d73d
- cloud_revenue_agent.py: 730ab7b323a784d3aa656ccd1ee8fc844b369b7e
- engine.py: c755b2d4b068596738e109b6a6a0bd7ba48ae173

Os arquivos públicos são evidência da implementação publicada. A equivalência exata com todos os processos executados no computador ainda precisa ser verificada.

## 3. Achados e correções exigidas

Prioridades: **P0** conter antes de novas ações automáticas; **P1** corrigir antes de confiar nos indicadores; **P2** melhorar rastreabilidade e operação.

### A01 — Sucesso registrado mesmo após falha de envio [P0, confirmado no código]

**Evidência:** E03, attack_open_opportunities. Após a tentativa de POST, o fluxo adiciona o ticket a handled, grava a timeline e registra NEW_SUBMISSION com sucesso independentemente de posted_url estar preenchido. Sem token ou após erro HTTP, a URL original pode substituir o comprovante de publicação.

**Impacto:** o painel pode afirmar participação que não aconteceu e impedir uma tentativa posterior legítima.

**Correção:** separar proposta preparada, envio pendente, envio falho e envio confirmado. Só confirmar após resposta válida contendo ID e URL, seguida de leitura de verificação. Preservar erro e permitir retry controlado com idempotência.

**Aceite:** testes de ausência de token, 401, 403, 429, timeout e resposta inválida não geram sucesso nem dinheiro em disputa. Timeout após possível publicação exige reconciliação antes de repetir.

### A02 — Probabilidades e valores genéricos sem modelo [P1, confirmado]

**Evidência:** E03 fixa probability em “85% (ANÁLISE SINTETIZADA)”. A faixa é US$ 250–500 quando o título contém wildcard e US$ 45–75 nos demais casos. O forecast também usa texto de ciclo Go-Hybrid sem validação específica por programa. Na tabela renderizada, 267 linhas tinham o mesmo 85%.

**Impacto:** números sugerem precisão inexistente e transferem regras de um projeto para outro.

**Correção:** remover probabilidades sem histórico calibrado. Registrar prêmio anunciado, fonte, moeda, modalidade, orçamento compartilhado e elegibilidade separadamente. Usar “não estimável” quando faltar evidência.

**Aceite:** nenhuma probabilidade ou faixa nasce apenas de título, comentário publicado ou nome do repositório.

### A03 — Comentário técnico tratado como entrega implementada [P0, confirmado no fluxo publicado]

**Evidência:** E03 lê o corpo da issue, solicita texto à IA e publica comentário. O caminho inspecionado não faz checkout, implementação, compilação, teste ou criação de PR. O título do script promete sintetizar, testar e publicar soluções.

**Exemplo:** E09 propõe um patch conceitual em Go em internal/checker/builtins/a5_escape.go; E10 identifica o componente real em compiler/crates/hy-check/src/builtins.rs, em Rust. A proposta não demonstra correção aplicável ou teste executado.

**Correção:** distinguir análise, proposta e patch. Para fixes, exigir diff sobre commit conhecido, teste de regressão e logs reais. Não chamar plano de teste de “teste aprovado”.

**Aceite:** toda entrega de código aponta para commit/PR e execução verificável; comentários permanecem classificados como comentários.

### A04 — Regras e concorrência não verificadas antes do envio [P0, confirmado no código]

**Evidência:** E03 lê apenas até 2.000 caracteres do corpo da issue no prompt; não consulta regras do programa, comentários existentes, decisão do mantenedor, pausa, escopo ou histórico de duplicatas. Pede avaliação SIM/NÃO, mas não interpreta uma resposta NÃO antes de publicar.

O filtro “0” not in str(comments) aceita contagens como 10, 20 e 100 como se fossem baixa concorrência. Número de comentários, por si só, também não mede concorrentes ou autorização.

**Correção:** gate determinístico por programa, com regras versionadas, escopo, canal, prazo, originalidade, autor do relato e decisão do responsável. Separar concorrência de quantidade de comentários. Uma decisão de inviabilidade deve bloquear o envio.

**Aceite:** comentários=10 não passam por regra de zero comentários; negativa de viabilidade, programa pausado ou elegibilidade desconhecida bloqueiam publicação automática.

### A05 — Orçamento compartilhado contado como oportunidades independentes [P1, confirmado]

**Evidência:** E06 limita o programa principal a US$ 500 por ciclo, para as dez melhores contribuições: US$ 75, 60, 50 e sete de US$ 45. A trilha wildcard tem outros US$ 500, com um vencedor e duas etapas de US$ 250.

**Impacto:** somar US$ 45–75 para cada ocorrência ou US$ 250–500 para cada proposta ignora competição e teto do ciclo.

**Correção:** agrupar por programa/ciclo/trilha e modelar orçamento compartilhado. Merge, reconhecimento, seleção de vencedor e autorização de pagamento são eventos distintos.

**Aceite:** projeções agregadas não ultrapassam o orçamento aplicável e não convertem toda contribuição aceita em prêmio garantido.

### A06 — #3673 real, mas premiação ainda não liquidada [P1, confirmado com limite]

**Evidência:** E07 confirma merge em 05/11 e registro da contribuição no bounty. O mantenedor relata verificações e um ajuste no teste durante a incorporação. Não foi identificado nessa discussão pagamento efetuado ou valor individual definitivamente atribuído.

**Correção:** manter “contribuição aceita / registrada no programa”. Só promover a vencedor, pagamento autorizado ou pago com evidência específica. Preservar o mérito do trabalho real.

**Aceite:** o registro não afirma 100% de chance de recebimento apenas porque houve merge.

### A07 — #3782 perdeu a disputa, mas permanece em expectativa [P1, confirmado]

**Evidência:** E08 informa que a correção de Yumihariii em #3779 foi incorporada primeiro. #3782 ficou aberto como registro da disputa. O painel/agente ainda o associa a testes verdes e aprovação próxima; previsões também o incluem entre referências wildcard, embora seja correção de instalador.

**Correção:** marcar “correção concorrente incorporada primeiro; sem recompensa confirmada”. Retirar de receita prevista e da trilha wildcard. Estado open não pode prevalecer sobre decisão textual do mantenedor.

**Aceite:** reconciliação interpreta a decisão e não reativa o item porque o PR continua aberto.

### A08 — StudentHub pausado e revisão do bot apresentada incorretamente [P0, confirmado]

**Evidência:** E13 anuncia suspensão e pede contato antes de trabalho independente. E16 reitera pausa em 12/10/2026, como contributor. E14 está aberto, sem merge; o bot informa que o repositório não recebe revisão automática por ter menos de dez estrelas. O painel apresenta “APROVADO POR BOTS (CodeRabbit OK)”, US$ 600 e expectativa de recebimento.

E15 exige plano com /attempt, PR com /claim e vídeo curto de demonstração. O PR contém /claim, mas não identifiquei vídeo no material consultado nem confirmação específica de retomada/aceite para essa participação.

**Correção:** suspender a previsão financeira até confirmação do responsável. Registrar os requisitos faltantes. Diferenciar sucesso de execução de um bot, revisão pulada e aprovação técnica.

**Aceite:** nenhum selo de aprovação é produzido por comentário de skip; pausa bloqueia novas ações até reabertura comprovada.

### A09 — Paraloom: autoria, canal e tabela de pagamento incorretamente presumidos [P0, confirmado]

**Evidência:** E11 paga por primeiro relato válido de causa única, após triagem, dentro de pool total de US$ 3.000. High/Critical requerem reporte privado; Medium/Low podem usar issue pública. Os tetos atuais são US$ 1.000/400/150/50 conforme severidade, não a faixa genérica de US$ 45–75.

Em E12, o autor do relato #1570 é outro participante; a conta auditada publicou comentário de proposta. Isso não comprova titularidade do bounty. A ocorrência é descrita como High e está pública, o que exige verificar autorização de divulgação e histórico da regra antes de novas interações.

**Correção:** verificar primeiro relator, duplicidade, escopo, severidade e canal. Não publicar automaticamente detalhes High/Critical. Correção adicional só entra como recompensa se houver acordo explícito aplicável.

**Aceite:** uma resposta em relato alheio não vira crédito próprio; o fluxo respeita canal privado quando exigido. Não reenviar relatos já públicos automaticamente.

### A10 — Superteam e grants confundem material pronto com inscrição [P1, lacuna confirmada no painel]

**Evidência:** E01/E02 usam “texto pronto para postagem”, “dossiê completo” e “repositório publicado” em uma timeline de entregas com probabilidades altas. O MultiHopper tem 90% justificado por repositório aberto. O ChimpX menciona pool de US$ 500 para top 25; isso não autoriza tratar o pool inteiro como prêmio individual.

Não foi possível verificar conta, formulário enviado, recibo, prazo oficial ou resultado dessas participações.

**Correção:** exigir listing específico, regras, recibo/ID de submissão, titularidade do perfil, link final e prazo oficial. Preparação deve ficar fora de “submetidos”.

**Aceite:** GitHub público, conta autenticada ou texto pronto não bastam para participação confirmada. Pool e prêmio individual ficam separados.

### A11 — Outras redes inflacionam “em disputa” [P1, confirmado na apresentação; atividade externa pendente]

**Evidência:** E02 traz extra_mapeados=156 e extra_disputa=156. O JavaScript soma esses extras aos 272 itens GitHub, mostrando 428 em disputa. Exemplos incluem repositórios e issues genéricas, com faixas e chances atribuídas sem comprovante de recompensa ou entrega própria. Logs dizem “código e proposta enviados”, mas links de exemplos apontam só para repositórios/issues.

**Correção:** descoberta não deve incrementar participação. Exigir identificador de comentário/MR/patch próprio e contrato/programa de recompensa. Não usar contagem de issues/patches do projeto como interações da conta.

**Aceite:** um repositório recém-descoberto afeta apenas o inventário; nenhuma renda é estimada sem oferta financeira identificada.

### A12 — “100% conforme” é declaração estática [P1, confirmado]

**Evidência:** E04 contém PROTOCOL_RULES com compliance_status preenchido como conforme e gera relatório com “100% CONFORME” sem validar integralmente cada requisito. A existência de repositórios públicos aparece como justificativa de conformidade Superteam.

**Correção:** substituir certificação textual por verificações individuais com resultado aprovado/reprovado/desconhecido, evidência e validade. Estado desconhecido não é aprovado.

**Aceite:** perder acesso à plataforma, deixar vencer prazo ou faltar recibo resulta em desconhecido/bloqueado, nunca 100% conforme.

### A13 — Monitor financeiro não comprova saldo em USDC [P1, confirmado no agente publicado]

**Evidência:** E04 usa getBalance para SOL e eth_getBalance para ETH na Base. Esses métodos não consultam USDC SPL/ERC-20. Erros retornam 0.0. Não há conciliação de transferências por bounty nesse código.

**Impacto:** pode apresentar saldo zero após falha de RPC ou ignorar pagamento em token. Saldo atual também não demonstra quanto foi recebido historicamente.

**Correção:** consultar tokens corretos por rede, contratos/mints oficiais, casas decimais, movimentações e confirmações. Separar erro, saldo conhecido, receita e transferência própria. Conciliar transação com destinatário, programa, token, valor e evento.

**Aceite:** falha RPC aparece como indisponível; recebimento USDC é detectado mesmo com saldo nativo zero; transferência própria não conta como receita.

### A14 — Monitoramento de e-mails e autonomia não demonstrados [P1, confirmado no código publicado; runtime completo pendente]

**Evidência:** E04 registra “E-mails e carteiras auditados”, mas o fluxo inspecionado consulta carteiras e PRs; não lê e-mail. A função query_gemini_brain é definida, porém não é chamada no ciclo principal. A ausência de heartbeat ativa um rótulo de comando cloud, sem demonstrar execução completa de engenharia.

**Correção:** relatar apenas operações realmente executadas. Provar failover com job, logs, responsável ativo e controle de concorrência. Remover alegação de e-mails auditados se não houver integração real.

**Aceite:** testes de heartbeat vencido demonstram a ação operacional reivindicada e evitam execução duplicada local/nuvem. Chave configurada não equivale a IA executada.

### A15 — Sinais de baleias são simulados em engine.py [P0 para uso financeiro, confirmado]

**Evidência:** E05 documenta explicitamente simulação em scan_whale_signals e retorna SOL/USDC, volume 420.5 e confiança 0.89 fixos. run_cycle imprime o sinal. Não há nesse arquivo leitura real de trades, cálculo de rentabilidade ou execução de ordens.

**Correção:** marcar o componente como demonstração/simulação. Implementação real exige fonte, transações verificadas, metodologia e custos. Não extrapolar este achado para afirmar que todo componente local é simulado sem inspecioná-lo.

**Aceite:** dados simulados não entram em produção, previsão financeira ou gatilho de ordem. Ausência de mercado não mantém um falso sinal “ao vivo”.

### A16 — Alegações de trading não sustentadas por evidências acessíveis [P0 antes de ativar]

**Evidência:** E01 anuncia 315 testes, 10.000 simulações Monte Carlo, disparo no primeiro crédito, limites de risco e win rates. Não foram apresentados, na auditoria, suíte/execução associada, relatório reproduzível, dados, custos ou executor demonstrado. “0% risco” aparece ligado ao módulo em standby; não deve sugerir que copy-trading seja isento de risco.

**Correção:** manter execução financeira desativada até revisão independente do módulo real. Separar standby sem exposição de estratégia sem risco. Mostrar métricas somente com metodologia, período e resultados reproduzíveis. Receber bounty não deve, por si só, autorizar reinvestimento automático.

**Aceite:** depositar ou receber crédito não inicia negociação sem configuração e autorização apropriadas; simulação não é apresentada como desempenho real.

### A17 — Indicadores e sincronização inconsistentes [P1, confirmado]

**Evidência:** o painel exibiu 900 mapeados e 428 em disputa, enquanto o cabeçalho manteve 272; a tabela de entregas dizia 308 mas tinha 464 linhas com extras; oportunidades dizia 419 com 575 linhas. O gráfico exibiu 1584 mapeados junto a referência de 744 para o dia.

O JavaScript usa fallback como servicos_aprovados_aguardando_pagamento || 1 e servicos_avancados_em_disputa || 272: zero legítimo vira valor positivo. A atualização periódica inspecionada altera KPIs/logs, mas não demonstra reconstrução integral das tabelas a partir do mesmo snapshot.

**Correção:** fonte única, categorias explícitas, contagem de IDs únicos, snapshots coerentes e fallback que preserve zero. Falha de atualização deve marcar dados obsoletos. Distinguir hora da coleta de hora de alteração do dado de origem.

**Aceite:** estado zero produz zero em todos os componentes; cabeçalho, gráfico e tabela reconciliam; informação velha não recebe selo de atualização integral.

### A18 — Não há demonstração de lucro líquido [P1, confirmado como ausência de demonstração]

**Evidência:** E01/E02 apresentam US$ 0 recebidos, US$ 35.925 brutos em disputa e US$ 2.850–7.100 realizáveis. A seção menciona conversão de 15–25%, cuja aplicação direta a US$ 35.925 seria US$ 5.388,75–8.981,25, sem explicação para outra faixa. Não há memória de cálculo auditável nem conciliação de custos.

**Correção:** remover projeção atual ou explicitar cenários, probabilidades justificadas, orçamento compartilhado, conversão, custos e dependências. Separar faturamento de lucro; registrar API, infraestrutura, taxas e demais custos efetivos.

**Aceite:** qualquer total pode ser refeito a partir de entradas e evidências. Na falta de base, mostrar “retorno não estimável”, não inventar um novo percentual.

### A19 — Exposição pública desnecessária de dados pessoais [P2, confirmado]

**Evidência:** painel e agente incluem chave Pix e endereços vinculados à identidade do operador.

**Correção:** reduzir dados publicados ao necessário, mascarar identificadores pessoais e avaliar acesso ao painel. Endereço blockchain público não é chave privada; não foi constatado vazamento de chave privada nesta auditoria.

**Aceite:** dashboard público não divulga chave Pix completa ou dados pessoais sem necessidade explícita. Logs não expõem tokens ou credenciais.

## 4. Modelo de dados e estados requerido

Cada oportunidade deve ter ID estável, plataforma, programa, ciclo, URL de regras, versão/data da regra, prazo/fuso, escopo, oferta financeira e orçamento compartilhado.

Cada participação deve registrar autor, tipo de entrega, URL/ID da submissão, commit quando aplicável, teste/CI associado, decisão do mantenedor e origem dessa decisão.

Estados mínimos:
1. Descoberta.
2. Elegibilidade não verificada / elegível / inelegível.
3. Em preparação.
4. Envio pendente / falho.
5. Submetida com comprovante.
6. Em avaliação / ajustes solicitados.
7. Aceita tecnicamente.
8. Selecionada para recompensa.
9. Pagamento autorizado com valor.
10. Pago e conciliado.
11. Rejeitada / duplicada / programa pausado / prazo encerrado.

Nem todo programa exige PR: relato válido ou proposta wildcard pode bastar quando as regras expressamente permitirem. A implementação deve respeitar essas diferenças.

## 5. Ordem de execução para o AntGravit

1. Preservar os registros atuais e vincular cada correção ao achado correspondente.
2. Conter publicação automática sem gate e ativação financeira baseada apenas em crédito recebido.
3. Corrigir A01, A03, A04 e A15 antes de retomar automação.
4. Reconciliar casos conhecidos: #3673, #3782, StudentHub #134 e Paraloom #1570.
5. Revisar todas as entradas, não só a amostra: identificar autoria, recibo, regras, prazo, orçamento e decisão.
6. Retirar da projeção os itens sem comprovação, pausados, perdidos, duplicados ou não submetidos.
7. Corrigir monitor de tokens e registrar custos.
8. Refazer painel a partir do modelo de estados, removendo certificações e probabilidades fixas.
9. Validar o runtime local e os jobs cloud contra os arquivos públicos. Documentar diferenças.
10. Entregar diff, resultados dos testes e reconciliação antes/depois.

Não apagar o histórico para “limpar” os indicadores. Não fabricar comprovantes, testes, fontes ou probabilidade substituta. Não publicar novas mensagens nos projetos para validar o sistema sem autorização específica.

## 6. Testes de aceitação obrigatórios

| Cenário | Resultado exigido |
|---|---|
| Envio sem credencial ou com erro | Estado falho, sem comprovante fictício |
| Timeout após possível POST | Reconciliação antes de retry |
| Resposta de IA inviável | Nenhuma publicação |
| Comentários 0, 1, 10, 20, 100 | Comparação numérica; sem presumir elegibilidade |
| Regra não lida, programa pausado ou prazo vencido | Bloqueio/desconhecido |
| Issue de terceiro com comentário próprio | Autoria preservada; sem prêmio presumido |
| Merge sem decisão de prêmio | Aceite técnico apenas |
| PR aberto com decisão de derrota | Permanece perdido financeiramente |
| Review bot ignorada | Não aprovada |
| Muitos candidatos ao mesmo pool | Respeito ao orçamento do ciclo |
| Todos os KPIs iguais a zero | Zero no painel, sem fallback positivo |
| RPC indisponível | Estado indisponível, não saldo zero |
| USDC recebido com zero ETH/SOL | Token identificado e conciliado |
| Transferência própria | Não classificada como receita |
| Simulação de baleias | Identificação explícita; sem ordens |
| Primeiro crédito recebido | Não ativa trading por acidente |
| Failover local/cloud | Um responsável ativo; evidência de trabalho real |
| Snapshot atualizado | Tabelas, KPIs e gráficos coerentes |

## 7. Pendências que impedem certificação integral

- Acesso ao código e logs efetivamente executados no computador, incluindo geradores das outras redes e suposto motor day trader.
- Comprovantes privados de inscrições Superteam e grants.
- Validação de token, rede e histórico de pagamentos; saldo atual isolado não basta.
- Confirmação de prêmio, valor e cronograma pelo responsável de cada programa.
- Histórico de todas as entradas, duplicidades e possíveis violações de regras.
- Custos efetivos e resultados de uma janela operacional suficiente para avaliar rentabilidade.
- Identificação da metodologia dos win rates e backtests anunciados.

**Critério de encerramento:** cada achado deve estar corrigido com evidência ou explicitamente mantido como pendência. Dashboard verde, novo texto de “100% auditado” e testes que apenas repetem valores fixos não comprovam resolução.
