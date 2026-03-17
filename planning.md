# 📘 Plano de Orientação – Definição de CRAS por Bairro (Santos)

## 🎯 Objetivo

Este documento orienta a criação de um script no AntiGravity que:

* Leia uma base de dados de estudantes
* Identifique o bairro de cada estudante
* Associe automaticamente o CRAS de referência
* Gere um campo adicional com essa informação

Esse processo será utilizado para orientar estudantes a realizarem o Cadastro Único (CadÚnico) no CRAS correto.

---

## 📊 Tabela de referência (Bairro → CRAS)

| Bairro         | CRAS de Referência                        |
| -------------- | ----------------------------------------- |
| Alemoa         | CRAS Alemoa / Chico de Paula              |
| Saboó          | CRAS Alemoa / Chico de Paula              |
| Chico de Paula | CRAS Alemoa / Chico de Paula              |
| São Manoel     | CRAS Alemoa / Chico de Paula / São Manoel |
| Piratininga    | CRAS Alemoa / Chico de Paula              |
| Bom Retiro     | CRAS Bom Retiro                           |
| Castelo        | CRAS Bom Retiro                           |
| Caneleira      | CRAS Bom Retiro                           |
| Areia Branca   | CRAS Bom Retiro                           |
| Vila São Jorge | CRAS Bom Retiro                           |
| Santa Maria    | CRAS Bom Retiro                           |
| Rádio Clube    | CRAS Rádio Clube                          |
| Nova Cintra    | CRAS Nova Cintra                          |
| São Bento      | CRAS São Bento                            |
| Centro         | CRAS Região Central                       |
| Vila Nova      | CRAS Região Central                       |
| Paquetá        | CRAS Região Central                       |
| Valongo        | CRAS Região Central                       |
| Estuário       | CRAS Zona da Orla                         |
| Macuco         | CRAS Zona da Orla                         |
| Aparecida      | CRAS Zona da Orla                         |
| Embaré         | CRAS Zona da Orla                         |
| Boqueirão      | CRAS Zona da Orla                         |
| Gonzaga        | CRAS Zona da Orla                         |
| Pompéia        | CRAS Zona da Orla                         |
| José Menino    | CRAS Zona da Orla                         |
| Marapé         | CRAS Zona da Orla                         |

---
aqui vai os dados completos dos cras:

 SECRAS Chico de Paula Endereço: Marginal Anchieta, 218 - Chico de Paula Telefones: 3203-5258 / 3203-1909 / 3299-3777 SECRAS Bom Retiro Endereço: Av. Nossa Senhora de Fátima, 517 - Chico de Paula Telefones: 3203-2116 / 3291-6279 / 3221-6921 SECRAS Centro Endereço: Rua Sete de Setembro, 45 - Vila Nova Telefones: 3223-5473 / 3225-8085 / 3237-1797 SECRAS Nova Cintra Endereço: Av. Guilherme Russo, 77 - Morro Nova Cintra Telefones: 3258-8222 / 3258-7348 SECRAS Rádio Clube Endereço: Rua Tenente Durval do Amaral, 366 - Rádio Clube Telefones: 3299-5331 / 3291-2655 SECRAS São Bento Endereço: Rua Santa Ângela, 156 - Morro São Bento Telefones: 3232-3479 / 3222-8098 SECRAS São Manoel Endereço: R. Cel. Feliciano Narciso Bicudo, 655 - Jd. São Manoel Telefones: 3299-1010 / 3219-5201 SECRAS ZOI Endereço: Avenida Afonso Pena, 185 - Macuco Telefones: 3221-6942 / 3203-2903 / 3221-6520

## ⚙️ Requisitos do Script

O script a ser gerado deve:

### 1. Entrada de dados

* Receber uma tabela com pelo menos:

  * Nome do estudante
  * Bairro

### 2. Processamento

* Criar um dicionário (mapa) Bairro → CRAS
* Para cada linha:

  * Buscar o bairro informado
  * Retornar o CRAS correspondente

### 3. Tratamento de exceções

* Caso o bairro não seja encontrado:

  * Preencher com: "CRAS não identificado"
  * (Opcional) registrar log para análise posterior

### 4. Saída

* Gerar nova tabela com coluna adicional:

  * "CRAS de Referência"

---

## 🧠 Regras importantes

* Comparação de bairro deve ser:

  * Case insensitive
  * Ignorar acentos (ex: "Jose Menino" = "José Menino")

* Evitar erros por variação de escrita

---

## 💻 Estrutura sugerida (pseudo-código)

```javascript
const mapaCRAS = {
  "alemao": "CRAS Alemoa / Chico de Paula",
  "saboo": "CRAS Alemoa / Chico de Paula",
  ...
}

function normalizar(texto) {
  return texto
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
}

for (linha of tabela) {
  bairroNormalizado = normalizar(linha.bairro)

  cras = mapaCRAS[bairroNormalizado] || "CRAS não identificado"

  linha.cras = cras
}
```

---

## 📦 Possível evolução futura

* Adicionar endereço completo do CRAS
* Gerar mensagem personalizada para cada estudante
* Integrar com envio automático (WhatsApp / e-mail)

---

## ✅ Resultado esperado

Uma base final contendo:

* Nome do estudante
* Bairro
* CRAS de referência

Pronta para uso em comunicação e orientação sobre o Cadastro Único.
