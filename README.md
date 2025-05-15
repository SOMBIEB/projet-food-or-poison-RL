# 🎮 PROJET_RL — "Food or Poison" avec IA(Agent) et Joueur Humain

Bienvenue dans mon projet de fin de module en **apprentissage par renforcement**. J’ai développé un petit jeu interactif en Python dans lequel un robot ou le joueur lui-même peut **manger de la nourriture** ou **tomber sur du poison**, dans un environnement quadrillé. L’objectif est de montrer comment un agent peut apprendre à jouer **grâce à une IA (PPO ou Q-Learning)**, ou être contrôlé **manuellement par un humain**.

Ce jeu pourrait même avoir une application pédagogique pour les enfants de 3 à 6 ans, afin de leur apprendre les principes de récompense et de conséquence. Des améliorations futures pourraient inclure une palette de couleurs et d’éléments plus variée, chacun avec une signification précise.



## 🎯 Objectifs spécifiques du projet

1. **Créer un mini-jeu avec Pygame** où un agent se déplace dans une grille pour atteindre de la nourriture (+1 point) et éviter les ennemis (-1 point).
2. **Appliquer des techniques d’apprentissage par renforcement** pour entraîner l’agent à jouer de façon autonome :
   - PPO (Proximal Policy Optimization)
   - Q-Learning (table de valeurs)

---
### 🎮 Règles du jeu


| Condition                                | Effet                                                            |
|------------------------------------------|------------------------------------------------------------------|
| 🟢 Le joueur mange 1 nourriture          | Récompense positive : **+250**                                   |
| 🔴 Le joueur mange 1 poison              | Récompense négative : **-250**                                   |
| 🚶 Déplacements inutiles                 | Récompense négative : **-1**                                             |
| ☠️ Le joueur mange 4 poisons             | Fin de la partie : affichage de **Game Over 💀**                 |
| 🎯 Le joueur mange 5 nourritures         | Passage au **niveau supérieur 🚀**                               |
| ▶️ Lancer une partie (mode manuel)       | Compiler : `play_as_human_ppogame.py` ou `play_as_human_QLgame.py` |



## 📁 Organisation du projet

```
├── blob_base.py                 # Déplacement des entités pour Q-Learning
├── blob_base2.py                # Déplacement des entités pour PPO
├── train_ppo.py                 # Entraînement de l'agent PPO
├── train_qlearning.py           # Entraînement de l'agent Q-Learning
├── play_or_watch.py             # Menu interactif pour jouer ou observer l'IA PPO
├── play_as_human_ppogame.py     # Jouer soi-même avec l’environnement PPO
├── play_as_human_QLgame.py      # Jouer soi-même avec l’environnement Q-Learning
├── test_ppoAgent.py             # Observer l’agent PPO jouer seul
├── test_Agent_Qlearning.py      # Observer l’agent Q-Learning jouer seul
├── ppo_blob.zip                 # Modèle PPO entraîné (poids)
├── ppo_rewards.txt              # Historique des scores PPO pendant l'entraînement
├── demo_apprentissage_Qlearning.mp4           # montre l'apprentissage en cours
├── demo_Qlearning_appris.mp4                  # montre l’agent déjà entraîné
├── demo_jouer_par_un_humain.mp4               # montre un humain en train de jouer
├── requirements.txt             # Bibliothèques Python nécessaires
└── README.md                    # Ce fichier ici 📄

---

## 🧪 Installation de l’environnement

### 🔹 Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
venv\Scripts\activate
```

### 🔹 Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 Lancer le projet

### 🧠 PPO — Agent IA (Stable-Baselines3)

#### 🟡 Menu interactif pour tester le jeu s'il fonctinne normalement (humain ou IA PPO)
```bash
python play_or_watch.py
```

#### 👤 Jouer en tant qu’humain (environnement PPO)
```bash
python play_as_human_ppogame.py
```

#### 🤖 Observer l’agent PPO jouer seul
```bash
python test_ppoAgent.py
```

---

### 📘 Q-Learning — Agent IA basé sur table de Q-valeurs

#### 👤 Jouer en tant qu’humain (Q-Learning)
```bash
python play_as_human_QLgame.py
```

#### 🤖 Observer l’agent Q-Learning jouer seul
```bash
python test_Agent_Qlearning.py
```

🎥 Démonstrations vidéo – Agent Q-Learning

▶️ **Apprentissage de l'agent Q-Learning**  
[Lancer la vidéo](C:\Projet_apprentissage_par_renforcement\demo_apprentissage_Qlearning.mp4)

▶️ **Agent Q-Learning entraîné (jeu final)**  
[Lancer la vidéo](C:\Projet_apprentissage_par_renforcement\demo_Qlearning_appris.mp4)

**Partie jouée par un humain (mode manuel)**  
  [▶️ Voir la vidéo](C:\Projet_apprentissage_par_renforcement\demo_jouer_par_un_humain.mp4)
---

---

## 📝 Remarques

- L’agent gagne **+250** en mangeant la nourriture.
- Il perd **-250** s’il touche un ennemi.
- Il perd **-1** en effectuant des deplacements inutils
- L’interface graphique s’adapte automatiquement selon le mode (PPO ou Humain).
- L’environnement est basé sur une **grille de 15x15** avec rendu Pygame.
  ## 🔗 Lien du projet 
  https://github.com/SOMBIEB/projet-food-or-poison-RL.git
