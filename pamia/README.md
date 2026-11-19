# PAMIA - Prevenção ao Assédio contra Mulheres com Inteligência Artificial

Este repositório contém o código-fonte do App Simulador de Demonstração do projeto PAMIA, focado nos Objetivos de Desenvolvimento Sustentável (ODS) 5 (Igualdade de Gênero) e 11 (Cidades e Comunidades Sustentáveis).

O aplicativo atua como uma interface de visualização e orquestração para um sistema de segurança preditiva integrado a um modelo de IA offline (YOLO).

## 👥 Equipe Desenvolvedora
* Caio Rocha
* Guilherme Spinola
* João Barros
* Paulo Henrique

## 🛠️ Stack Tecnológica (MVP)
* **Front-end:** React Native
* **Framework:** Expo (SDK 56)
* **Navegação:** React Navigation (Native Stack)
* **Persistência Local:** SQLite (Planejado)
* **Inteligência Artificial:** TensorFlow Lite (YOLO - Planejado para processamento Edge)

## 💻 Pré-requisitos e Ambiente de Desenvolvimento

Para garantir a padronização do ambiente entre todos os integrantes do grupo, as seguintes ferramentas são **obrigatórias**:

1. **Node.js** (Versão LTS recomendada).
2. **Git** para versionamento de código.
3. **Android Studio**: Obrigatório para a emulação e validação de interface. 
   * **Por que não usar o celular físico agora?** Para agilizar o desenvolvimento do fluxo de telas. O uso de celular físico será focado na fase de testes do modelo de IA.
   * **Configuração do Emulador (AVD):** Crie um dispositivo virtual com perfil de **hardware médio** (ex: 6GB a 8GB de RAM) para refletir o público-alvo de passageiras e motoristas.

## 🚀 Como rodar o projeto localmente

1. **Clone o repositório:**
```
git clone https://github.com/99Barros/PAMIA.git
```
Acesse a pasta do projeto:
```
cd PAMIA
```
Instale as dependências base do projeto:

```
npm install
```
Instale as dependências de Navegação (React Navigation):

```
npm install @react-navigation/native @react-navigation/native-stack
npx expo install react-native-screens react-native-safe-area-context
```
Inicie o servidor do Expo:

```
npx expo start
```
Abra no Emulador: Com o Android Studio aberto e o emulador rodando, pressione a tecla a no terminal onde o Expo está executando para abrir o aplicativo no dispositivo virtual Android.

⚙️ Diretrizes de Execução (Kanban)
Para manter o fluxo contínuo e sem sobrecargas, adotamos as seguintes regras de desenvolvimento ágil:

Limite de WIP (Work in Progress): Máximo de 4 tarefas simultâneas na coluna "Em Execução" (uma por integrante).

Daily Sync: Reuniões rápidas para alinhamento e destravamento de impedimentos.

Critério de Conclusão (DoD): Nenhuma tarefa vai para Done sem revisão de código (Peer Review) de outro integrante.

Estratégia de Testes (IA): O processamento pesado de visão computacional será testado via Mock de Câmera (injeção de vídeo local) para contornar as limitações de FPS do emulador.
