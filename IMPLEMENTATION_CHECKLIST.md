# Prompt d'Implémentation - Corrections Soutenance

## Contexte

Tu dois implémenter les corrections de la présentation de soutenance basées sur les retours de répétition.

**Fichiers sources :**
- `defense-revealjs/index.html` - Présentation Reveal.js (slides + notes)
- `defense-presentation/FEEDBACK_ANALYSIS_AND_PLAN.md` - Analyse des retours et ressources

---

## Méthodologie de Travail

Pour **CHAQUE point** du fichier `FEEDBACK_ANALYSIS_AND_PLAN.md`, tu DOIS suivre ces étapes dans l'ordre :

### Étape 1 : LIRE
- Lis le retour et son action prévue dans le tableau
- Identifie la section "Ressources et Liens" correspondante si applicable

### Étape 2 : CHERCHER
- Localise précisément dans `index.html` la slide ou le texte concerné
- Consulte les liens de référence fournis si tu as besoin de contexte (définitions, données)

### Étape 3 : DÉCIDER
- Formule clairement ce que tu vas modifier/ajouter/déplacer
- Justifie brièvement pourquoi cette approche répond au feedback

### Étape 4 : IMPLÉMENTER
- Applique la modification dans `index.html`
- Mets à jour les `<aside class="notes">` si le contenu oral doit changer

### Étape 5 : MARQUER
- Après chaque point terminé, reviens ici et coche la case correspondante

---

## Checklist des Corrections

### Section 1 : Contenu et Contexte

- [x] **1.1 Victoria Island** → Ajouter "Lagos, Nigéria"
- [x] **1.2 Pourquoi Lagos** → Justifier le choix (cas extrême)
- [x] **1.3 Impliquer le Bénin** → Inverser la logique (Bénin avant Lagos)
- [x] **1.4 Motos** → Dire "Motos (Zemidjans)" au lieu de "mixité"
- [x] **1.5 Définition Jumeau Numérique** → Ajouter définition rigoureuse
- [x] **1.6 Solution Floue** → Clarifier "plateforme logicielle"
- [x] **1.7 Exemple Concret** → Ajouter scénario "Carrefour IITA"
- [x] **1.8 Gain 4.2%** → Convertir en temps/économie

### Section 2 : Technique et Rigueur

- [x] **2.1 Agent IA → Agent DQN** → Remplacer terminologie
- [x] **2.2 Origine DQN** → Citer DeepMind (2014/2015)
- [x] **2.3 Hypothèses** → Formaliser "Soit H1..."
- [x] **2.4 WENO5** → Créer/intégrer animation
- [x] **2.5 Validation Systémique** → Agrandir image ou découper slide

---

## Finalisation

- [x] Relire toutes les slides modifiées
- [x] Vérifier cohérence des notes de présentation
- [x] `git add .`
- [x] `git commit -m "fix(slides): corrections soutenance post-répétition"`
- [ ] `git push`
