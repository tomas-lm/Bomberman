# 🎮 Bomberman Game

Uma implementação em Python do clássico jogo Bomberman com interface moderna e sistema de pontuação.

## 👥 Integrantes do Grupo

- **Tomas Lacerda Muniz**
- **Rodrigo Sales Nascimento** 
- **Lucas Almeida Santos de Souza**

## 🎯 Sobre o Projeto

Este projeto é uma recriação completa do clássico jogo Bomberman, desenvolvido seguindo princípios de engenharia de software e arquitetura modular. O jogo implementa todas as mecânicas tradicionais do Bomberman com um sistema moderno de interface e persistência de dados.

## ✨ Características Principais

### 🎮 Mecânicas de Jogo
- **Gameplay Clássico**: Navegue pelo labirinto, plante bombas e derrote inimigos
- **Sistema de Vidas**: 3 vidas com invencibilidade temporária ao renascer
- **Power-ups**: BombUp, FireUp, SpeedUp e Heart com efeitos únicos
- **Explosões Realistas**: Sistema de raycasting que respeita paredes
- **Colisão Precisa**: Detecção de colisão pixel-perfect com paredes e obstáculos

### 🖥️ Interface e Sistema
- **Menu Moderno**: Sistema de navegação intuitivo
- **HUD Informativo**: Exibe vidas, bombas ativas, raio de fogo
- **Sistema de Pontuação**: Persistência em banco de dados JSON
- **High Scores**: Ranking de melhores pontuações

### 🏗️ Arquitetura
- **Design Modular**: Separação clara de responsabilidades
- **Código Limpo**: Seguindo princípios SOLID
- **Testes Unitários**: Cobertura de testes para componentes críticos
- **Extensibilidade**: Fácil adição de novas funcionalidades

## 🎮 Controles do Jogo

- **Movimento**: WASD ou Setas do Teclado
- **Plantar Bomba**: Barra de Espaço
- **Navegação no Menu**: Setas + Enter
- **Voltar/Sair**: ESC

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.7+
- Pygame 2.5.0+

### Instalação
1. Clone o repositório:
```bash
git clone <repository-url>
cd Bomberman
```

2. Ative o ambiente conda:
```bash
conda activate bomberman
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o jogo:
```bash
python run_game.py
```

## 🏗️ Arquitetura do Sistema

### Estrutura do Projeto
```
Bomberman/
├── src/
│   ├── game/              # Lógica principal do jogo
│   │   ├── game_engine.py    # Motor principal e loop do jogo
│   │   ├── game_map.py       # Geração e gerenciamento do mapa
│   │   ├── player.py         # Lógica do jogador
│   │   ├── bomb.py           # Sistema de bombas e explosões
│   │   ├── enemy.py          # IA dos inimigos
│   │   ├── explosion.py      # Sistema de chamas
│   │   └── powerup.py        # Sistema de power-ups
│   ├── ui/                 # Componentes de interface
│   │   ├── menu.py            # Sistema de menus
│   │   └── score_display.py   # Exibição de pontuações
│   ├── database/           # Persistência de dados
│   │   └── score_manager.py   # Gerenciamento de pontuações
│   ├── utils/              # Utilitários e constantes
│   │   └── constants.py       # Configurações do jogo
│   └── main.py             # Ponto de entrada da aplicação
├── tests/                  # Testes unitários
├── data/                   # Armazenamento do banco JSON
├── assets/                 # Recursos do jogo (sprites, sons)
├── requirements.txt        # Dependências
├── setup.py               # Configuração do pacote
└── run_game.py            # Launcher do jogo
```

### Padrões Arquiteturais

#### 1. **Separação de Responsabilidades**
- **Game Engine**: Gerencia o loop principal, eventos e estado
- **Game Objects**: Cada entidade tem sua própria lógica (Player, Enemy, Bomb)
- **UI Layer**: Interface separada da lógica de jogo
- **Data Layer**: Persistência isolada em camada própria

#### 2. **Padrão Observer/Event-Driven**
- Sistema de eventos centralizado
- Comunicação desacoplada entre componentes
- Facilita extensibilidade e manutenção

#### 3. **Factory Pattern**
- Criação de objetos de jogo (bombas, power-ups, inimigos)
- Configuração centralizada em constants.py

#### 4. **State Pattern**
- Diferentes estados do jogo (menu, jogando, game over)
- Transições de estado bem definidas

## 🛠️ Tecnologias Utilizadas

### **Linguagem Principal**
- **Python 3.10+**: Linguagem principal do projeto
  - Tipagem estática com type hints
  - F-strings para formatação de strings
  - Context managers para gerenciamento de recursos

### **Framework de Jogos**
- **Pygame 2.6.1**: Framework principal para desenvolvimento de jogos
  - Renderização 2D e sprites
  - Sistema de eventos e input
  - Gerenciamento de áudio e imagens
  - Detecção de colisões

### **Persistência de Dados**
- **JSON**: Formato de armazenamento para pontuações
  - Estrutura simples e legível
  - Fácil manipulação e debug
  - Compatibilidade cross-platform

### **Testes e Qualidade**
- **pytest**: Framework de testes unitários
  - Testes automatizados para componentes críticos
  - Cobertura de código
  - Fixtures para setup de testes

### **Gerenciamento de Dependências**
- **pip**: Gerenciador de pacotes Python
- **conda**: Gerenciamento de ambientes virtuais
- **requirements.txt**: Especificação de dependências

### **Ferramentas de Desenvolvimento**
- **Git**: Controle de versão
- **Type Hints**: Tipagem estática para melhor manutenibilidade
- **Docstrings**: Documentação inline do código

## 🎯 Mecânicas de Jogo Implementadas

### **Sistema de Bombas**
- **Plantio**: Limite de bombas por jogador (1-6)
- **Cooldown**: Tempo entre plantios (0.5s)
- **Explosão**: Raycasting em 4 direções respeitando paredes
- **Chamas**: Duração visual de 500ms

### **Sistema de Power-ups**
- **BombUp** (Ciano): +1 capacidade de bombas
- **FireUp** (Laranja): +1 raio de explosão
- **SpeedUp** (Amarelo): +0.5 velocidade
- **Heart** (Rosa): +1 vida extra
- **Drop Rate**: 25% chance ao destruir blocos

### **Sistema de Vidas**
- **3 Vidas**: Sistema de vidas múltiplas
- **Invencibilidade**: 1.25s após renascer
- **Respawn**: Retorno à posição inicial
- **Efeito Visual**: Cor ciano durante invencibilidade

### **IA dos Inimigos**
- **Movimento Aleatório**: Direções aleatórias com intervalos
- **Colisão**: Respeitam paredes e obstáculos
- **Dano**: Morrem por explosão ou contato com jogador

## 🧪 Desenvolvimento e Testes

### **Executando Testes**
```bash
python -m pytest tests/ -v
```

### **Adicionando Novas Funcionalidades**
1. Crie novos módulos nos diretórios apropriados
2. Siga as convenções de nomenclatura (snake_case)
3. Adicione testes unitários para nova funcionalidade
4. Atualize constants.py para novos valores de configuração

### **Configuração do Jogo**
As configurações podem ser modificadas em `src/utils/constants.py`:
- Dimensões da tela
- Velocidade do jogo
- Timer e raio de explosão das bombas
- Valores de pontuação
- Tamanho do mapa

## 📊 Sistema de Pontuação

### **Pontos por Ação**
- **Inimigo**: 100 pontos
- **Bloco Destrutível**: 50 pontos
- **Completar Nível**: 500 pontos bônus

### **Persistência**
- **Formato**: JSON com timestamp
- **Limite**: Top 10 pontuações
- **Estatísticas**: Jogos jogados, pontuação máxima, média

## 🎨 Elementos Visuais

### **Cores e Identificação**
- **Jogador**: Azul (Ciano quando invencível)
- **Inimigos**: Vermelho
- **Bombas**: Vermelho com timer
- **Chamas**: Laranja translúcido
- **Paredes**: Cinza (sólidas) e Marrom (destrutíveis)
- **Power-ups**: Cores específicas por tipo

## 📈 Possíveis Extensões

### **Funcionalidades Futuras**
- **Múltiplos Níveis**: Sistema de progressão
- **Power-ups Adicionais**: Kicker, Flame Pass, Remote Bomb
- **Multiplayer**: Modo cooperativo ou competitivo
- **Sprites**: Substituir formas geométricas por sprites
- **Sons**: Efeitos sonoros e música de fundo
- **Diferentes Inimigos**: Tipos com comportamentos únicos

### **Melhorias Técnicas**
- **Otimização**: Culling de objetos fora da tela
- **Configuração**: Menu de opções para ajustes
- **Save System**: Sistema de save/load de progresso
- **Modding**: Sistema de mods para comunidade

## 📄 Licença

Este projeto é open source e está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ por Tomas, Rodrigo e Lucas**