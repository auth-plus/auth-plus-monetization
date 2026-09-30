# AGENTS.md - Auth+ Monetization Service

> **Propósito:** Ponto de entrada técnico e guia de regras de negócio para Agentes de IA atuando no microsserviço `auth-plus-monetization`.
>
> **Bounded Context:** Monetização, Modelos de Cobrança (Pré-pago e Pós-pago), Livro-Razão Contábil (Ledger), Tarifação de Eventos (Metering/Usage-based Pricing) e Conversão de Planos.

---

## 1. Visão Geral e Stack Tecnológica

O `auth-plus-monetization` gerencia como o uso dos serviços da plataforma é tarifado e faturado, suportando modelos de consumo pré-pago com compra de créditos e modelos pós-pagos por faturamento de eventos.

- **Runtime / Linguagem:** Python 3.10+ gerenciado com Poetry
- **Framework Web:** FastAPI com Uvicorn
- **Persistência Relacional:** PostgreSQL 15.1 (`database:5432/monetization`) via SQLAlchemy
- **Mensageria:** Apache Kafka (`kafka:9092`) via `confluent-kafka`
- **Observabilidade:** OpenTelemetry Python SDK com instrumentação automática FastAPI integrado ao Uptrace (`uptrace:4317`)
- **Porta:** Host `5004` $\rightarrow$ Container `8000`

---

## 2. Regras de Negócio e Modelos de Monetização

### 2.1. Tipos de Assinatura e Planos (`AccountType`)
O sistema suporta quatro modalidades de subscrição:
- **`PRE_PAID`**: O cliente compra créditos previamente. Cada ação/evento consome saldo do livro-razão (ledger).
- **`POST_PAID_MONTH`**: O cliente consome eventos ao longo do mês; os itens são acumulados e cobrados na fatura mensal emitida pelo serviço de `billing`.
- **`POST_PAID_SEMESTER`** / **`POST_PAID_ANNUAL`**: Planos pós-pagos com janelas estendidas de apuração.

### 2.2. Livro-Razão Contábil (Ledger de Crédito e Débito)
1. **Transações Imutáveis:** Cada movimentação financeira gera um registro imutável em `transaction` vinculado à conta (`account_id`), com valor (`amount`), descrição e data.
2. **Saldo Total:** O saldo do usuário (`GET /ledger/{external_id}`) é computado a partir do somatório de todas as transações de crédito e débito registradas no histórico.

### 2.3. Fluxo Pré-Pago (`PRE_PAID`)
1. **Aquisição de Créditos (`POST /ledger/credit`):**
   - Válido exclusivamente para contas `PRE_PAID`. Tentativas de creditar em contas pós-pagas resultam em `FlowPrePaidError`.
   - Ao receber a requisição, o serviço gera uma chamada HTTP síncrona para o serviço `billing` (`POST /invoice` e cobrança imediata).
   - Uma vez confirmada a cobrança pelo `billing`, o crédito positivo é lançado no ledger do usuário.
2. **Consumo de Saldo:**
   - Eventos tarifáveis debitam o valor configurado na tabela `event`.

### 2.4. Fluxo Pós-Pago (`POST_PAID_MONTH`)
1. **Tarifação Reativa por Evento (`POST /ledger/debit`):**
   - Ao receber a notificação de um evento tarifável (ex.: envio de SMS, validação de 2FA), o serviço:
     1. Registra o débito correspondente no ledger local para auditoria de consumo.
     2. Dispara uma requisição para o serviço `billing` inserindo um item correspondente (`InvoiceItem`) na fatura em aberto do usuário.

### 2.5. Migração de Modelo de Cobrança (Transformação de Conta)
- **`PATCH /account/to_post_paid`**: Converte a conta para pós-paga. Exige encerramento da subscrição pré-paga ativa e criação da nova vigência.
- **`PATCH /account/to_pre_paid`**: Converte a conta para pré-paga. Faturas pós-pagas pendentes no `billing` devem ser liquidadas antes ou associadas ao ciclo final.

---

## 3. Contratos de API (Endpoints Principais)

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/health` | Healthcheck do serviço |
| `POST` | `/account` | Inicialização de conta de monetização para um `external_id` |
| `GET` | `/ledger/{external_id}` | Consulta o saldo contábil atual de créditos do usuário |
| `POST` | `/ledger/credit` | Injeção de créditos pré-pagos (aciona faturamento no `billing`) |
| `POST` | `/ledger/debit` | Consumo de evento tarifável (debita saldo ou agenda no `billing`) |
| `PATCH` | `/account/to_post_paid` | Migração para o modelo pós-pago |
| `PATCH` | `/account/to_pre_paid` | Migração para o modelo pré-pago |

---

## 4. Instruções de Desenvolvimento e Testes

```bash
# Instalação de dependências do projeto
poetry install

# Execução do servidor web FastAPI com reload
poetry run uvicorn src.presentation.server:app --host 0.0.0.0 --port 8000 --reload

# Execução de workers de background/kafka
poetry run python -m src.presentation.worker

# Suíte de testes unitários e de integração
poetry run pytest

# Formatação e checagem de tipos
poetry run black .
poetry run flake8
```

---

## 5. Diretrizes para Agentes de IA

1. **Integridade do Ledger:** Jamais realize mutações ou deletes diretos na tabela `transaction`. O saldo deve ser estritamente auditável através de eventos append-only de crédito ou débito.
2. **Comunicação com o Billing:** Chamadas para o serviço `billing` devem respeitar os contratos de API de fatura e tolerar falhas de rede com logs apropriados.
3. **Propagação OTel:** Mantenha a instrumentação automática do FastAPI e inclua atributos semânticos (`account.id`, `event.type`, `monetization.plan`) nos spans gerados.
