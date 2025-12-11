# Notes de Soutenance - Jumeau Numérique

## Slide 1 : Jumeau Numérique pour le Trafic Ouest-Africain

Excellence Monsieur le Président du Jury, Honorables membres du Jury, chers parents, amis et invités Bonjour

                    Nous avons l'honneur de vous présenter aujourd'hui les résultats de notre travail de fin d'études.

                    Il porte sur la conception d'un "Jumeau Numérique pour le Trafic Ouest-Africain", et son utilisation pour optimiser les feux de signalisation grâce à l'Intelligence Artificielle.

<div style="page-break-after: always;"></div>

---

## Slide 2 : Plan de la Présentation

Pour cette présentation, nous suivrons une démarche classique.

                    Nous commencerons par le contexte et une revue de la littérature, pour comprendre pourquoi les solutions actuelles ne suffisent pas.

                    Ensuite, la méthodologie : comment nous avons construit ce simulateur.

                    Puis les résultats, pour voir si l'IA apporte vraiment un gain.

                    Et enfin, les perspectives que ce travail ouvre pour nos villes.

<div style="page-break-after: always;"></div>

---

## Slide 3 : Le Défi du Trafic Ouest-Africain

Le point de départ, c'est un constat que nous vivons tous au quotidien.

                    À Lagos, ville la plus congestionnée au monde selon l'indice Numbeo 2024, les embouteillages coûtent environ 6 milliards de dollars par an.

                    Chez nous à Cotonou, sur l'axe Carrefour Étoile Rouge - Saint-Michel, un trajet de 20 minutes peut en prendre 90 aux heures de pointe.

                    Cette mixité crée une dynamique fluide mais difficile à gérer, avec des pertes économiques considérables.

                    Et aux carrefours de Cotonou, la pollution atmosphérique atteint 181 µg/m³ de PM2.5, soit 36 fois la norme recommandée par l'OMS.

<div style="page-break-after: always;"></div>

---

## Slide 4 : Pourquoi les Solutions Classiques Échouent

Le problème, c'est que nos infrastructures de gestion actuelles ne sont pas adaptées à cette réalité.

                    Les feux sont à temps fixe : ils sont "aveugles", ils ne voient pas le trafic.

                    Et les simulateurs qui existent sont calibrés pour un trafic homogène de voitures. Ils ne savent pas représenter correctement le comportement d'un flux mixte motos-voitures.

                    Il y a donc une absence d'outils technologiques adaptés à *notre* contexte.

<div style="page-break-after: always;"></div>

---

## Slide 5 : Questions et Objectifs de Recherche

L'objectif de ce mémoire était donc de combler ce vide.

                    Nous nous sommes posé trois questions simples :

                    1. Peut-on modéliser mathématiquement ce trafic mixte ?

                    2. Peut-on le simuler de manière réaliste sans avoir des capteurs partout ?

                    3. Une IA peut-elle faire mieux qu'un feu tricolore classique dans ce contexte ?

                    Pour y répondre, nous avons fait le pari du modèle ARZ pour la physique du trafic, et de l'apprentissage par renforcement pour le contrôle intelligent.

<div style="page-break-after: always;"></div>

---

## Slide 6 : Évolution des Modèles de Trafic

Théoriquement, nous ne partons pas de rien.

                    Les modèles de trafic ont évolué depuis 1955. On est passé de modèles simples (comme de l'eau dans
                    un tuyau) à des modèles plus complexes qui prennent en compte l'inertie des conducteurs
                    (ARZ).

                    Récemment, des modèles multi-classes sont apparus.

                    Notre travail a consisté à étendre ces modèles pour capturer spécifiquement les interactions
                    agressives de notre trafic ouest-africain.

<div style="page-break-after: always;"></div>

---

## Slide 7 : Gap Scientifique Identifié

C'est ici que se situe notre apport scientifique.

                    Les modèles classiques sont trop simples pour nous.

                    Les gros simulateurs commerciaux (comme SUMO) sont des boîtes noires difficiles à calibrer pour nos
                    réalités.

                    Nous proposons une approche intermédiaire : un modèle mathématique rigoureux, mais adapté localement
                    et conçu dès le départ pour être piloté par une IA.

<div style="page-break-after: always;"></div>

---

## Slide 8 : Architecture Globale du Système

Voici l'architecture du système que nous avons développé. C'est un triptyque :

                    1. Le Modèle Physique (ARZ) : les équations qui décrivent le mouvement.

                    2. Le Solveur Numérique : le code qui calcule l'évolution du trafic pas à pas.

                    3. L'Agent IA : le cerveau qui contrôle les feux.

                    C'est l'ensemble de ces trois blocs qui constitue notre "Jumeau Numérique".

<div style="page-break-after: always;"></div>

---

## Slide 9 : Modèle ARZ Multi-Classes

Rapidement sur la physique : nous utilisons le modèle ARZ multi-classes.

                    Il est constitué de deux équations pour chaque classe de véhicules (motos et voitures) :

                    1. La conservation de la masse : les véhicules ne disparaissent pas.

                    2. L'équation de la dynamique : elle décrit comment la propriété \(w\) (qui combine vitesse et
                    anticipation) est transportée par le flot.

                    Le terme de droite est crucial : c'est la relaxation. Il dit que les conducteurs tendent à ajuster
                    leur vitesse vers une vitesse d'équilibre \(V_e\) qui dépend de la densité du trafic (et donc des
                    autres véhicules).

<div style="page-break-after: always;"></div>

---

## Slide 10 : Schéma Numérique (Volumes Finis)

Pour résoudre ces équations, nous utilisons la méthode des Volumes Finis (FVM).

                    C'est le cadre qui garantit que les véhicules ne disparaissent pas (conservation).

                    À l'intérieur de ce cadre, nous utilisons la reconstruction WENO5. C'est le "moteur" de précision qui permet de capturer les ondes de choc (freinages brusques) sans créer d'oscillations numériques fausses.

                    Ce couple FVM + WENO5 est indispensable pour que la simulation soit stable et que l'IA apprenne sur une physique correcte.

<div style="page-break-after: always;"></div>

---


## Slide 11 : Environnement RL - API Gymnasium

Pour l'IA, nous avons utilisé l'apprentissage par renforcement.

                    L'agent est comme un policier au carrefour. Il regarde l'état du trafic (densités, vitesses).

                    Il prend une action : laisser vert ou passer au rouge.

                    Et il reçoit une récompense : plus le trafic coule, plus il gagne de points. Il apprend ainsi par
                    essai-erreur à maximiser la fluidité globale.

<div style="page-break-after: always;"></div>

---

## Slide 12 : Clarification : Vers un Jumeau Numérique

Alors, une précision importante sur le terme "Jumeau Numérique".

                    On pourrait penser que c'est un mot un peu à la mode, peut-être exagéré. Mais pour nous, c'est un
                    choix délibéré.

                    Notre stratégie a été de construire d'abord le **cerveau** du système. Ce que nous
                    avons là n'est pas une simple animation ; c'est le moteur de décision, qui contient déjà toute la
                    physique de notre trafic si particulier.

                    Ce moteur est prêt. Demain, nous pouvons le brancher à des capteurs réels. Ce que nous avons bâti,
                    ce n'est pas juste un simulateur pour un article. C'est la **première pierre** d'un
                    vrai système de gestion intelligente du trafic pour nos villes.

<div style="page-break-after: always;"></div>

---

## Slide 13 : Démonstration Jumeau Numérique

Voici une démonstration en temps réel de notre jumeau numérique.

                    Il s'agit de la modélisation du corridor de Victoria Island à Lagos, avec ses 3 intersections majeures.

                    Ce que vous voyez ici, c'est le modèle ARZ multi-classes en action :

                    - Les **traînées orange** représentent les motos (70% du flux).

                    - Les **traînées bleues** représentent les voitures.

                    - Les **colonnes 3D** aux intersections sont les feux de signalisation qui changent de
                    couleur.

                    Observez comment le trafic ralentit naturellement aux intersections, et comment les ondes de densité
                    se propagent vers l'amont (effet accordéon).

                    Cette visualisation tourne en temps réel dans votre navigateur. C'est le même type de dynamique que
                    notre agent RL apprend à optimiser.

<div style="page-break-after: always;"></div>

---

## Slide 14 : Validation H1 : Tests de Riemann

Passons aux résultats. D'abord, la validation mathématique.

                    Nous avons soumis le modèle à des tests standards (les problèmes de Riemann).

                    Comme vous le voyez, le modèle gère parfaitement les ondes de choc et de détente. Il n'y a pas
                    d'aberration numérique. Le moteur est fiable.

<div style="page-break-after: always;"></div>

---

## Slide 15 : Validation H2 : Dynamique du Réseau

Ensuite, la validation systémique du jumeau numérique.

                    Ces instantanés montrent l'évolution temporelle du trafic sur le corridor de Victoria Island.
                    On observe clairement la propagation des ondes de choc (zones rouges) qui remontent le
                    courant.

                    Le modèle reproduit les trois régimes de trafic : fluide, congestionné, et bouchonné.
                    Cela confirme que notre jumeau numérique capture bien la phénoménologie réelle du trafic.

<div style="page-break-after: always;"></div>

---

## Slide 16 : Courbe d'Apprentissage de l'Agent RL

**Monsieur le Président, honorables membres du Jury**, maintenant que nous avons validé
                    l'outil de simulation, voyons ce que l'IA a réussi à faire.

                    Voici la courbe d'apprentissage de l'agent.

                    Au début, il tâtonne. Mais après environ 50 000 itérations, il converge vers une stratégie stable.
                    Il a appris à gérer le carrefour.

<div style="page-break-after: always;"></div>

---

## Slide 17 : Résultats Comparatifs

Concrètement, qu'est-ce que ça donne ?

                    Nous avons comparé l'IA à un feu à temps fixe bien réglé (méthode Webster).

                    En moyenne, l'IA améliore le flux de 4.2%.

                    Mais surtout, en situation de saturation (quand c'est la crise), le gain monte à près de 6%.

<div style="page-break-after: always;"></div>

---

## Slide 18 : Analyse du Gain

Ce gain de 4.2% mérite une analyse. Il peut paraître modeste, mais il est en réalité très
                    significatif.

                    D'abord, nous nous comparons à une baseline déjà optimisée, la méthode de Webster, qui est une
                    référence. Nous ne trichons pas en nous comparant à un feu mal réglé.

                    Ensuite, notre simulateur est exigeant : il modélise l'inertie, les temps de réaction. C'est un gain
                    obtenu dans des conditions réalistes, pas dans un monde idéal.

                    Ce chiffre est donc honnête et robuste. Il représente des minutes de trajet en moins pour des
                    milliers de personnes, chaque jour.

<div style="page-break-after: always;"></div>

---

## Slide 19 : Synthèse des Résultats

En synthèse :

                    Nous avons validé le modèle mathématique (H1).

                    Nous avons validé le réalisme du trafic simulé (H2).

                    Et nous avons montré que l'IA apporte un gain opérationnel, même s'il reste perfectible (H3).

<div style="page-break-after: always;"></div>

---

## Slide 20 : Contributions

Ce travail apporte trois contributions :

                    1. Un modèle mathématique adapté à notre contexte (motos/voitures).

                    2. Une implémentation numérique performante et stable.

                    3. Une plateforme prête à l'emploi pour entraîner d'autres IA sur nos problématiques locales.

<div style="page-break-after: always;"></div>

---

## Slide 21 : Limites et Perspectives

Bien sûr, tout n'est pas parfait.

                    La limite principale reste le manque de données réelles pour calibrer finement les
                    paramètres.

                    Mais les perspectives sont là : on peut tester d'autres algorithmes d'IA, étendre la simulation à
                    tout un quartier, et à terme, connecter de vrais capteurs.

<div style="page-break-after: always;"></div>

---

## Slide 22 : Merci

Pour conclure, ce mémoire est une première pierre.

                    Il démontre qu'il est possible de construire ici, en Afrique, des solutions technologiques de pointe
                    qui répondent précisément à nos propres défis, au lieu de simplement importer des modèles qui ne
                    nous correspondent pas.

                    C'est la preuve qu'une ingénierie locale et ambitieuse est non seulement possible, mais
                    nécessaire.

                    Nous vous remercions de votre attention et sommes maintenant à votre disposition pour répondre à vos
                    questions.

<div style="page-break-after: always;"></div>

---

## Slide Bonus : FVM vs WENO (Explication Technique)

Si on vous demande la différence ou le lien entre FVM et WENO :

                    C'est une excellente question de précision.

                    Le **FVM (Finite Volume Method)** est le **cadre** de notre schéma. C'est lui qui découpe la route en cellules et garantit la conservation des véhicules (ce qui rentre moins ce qui sort).

                    Le **WENO (Weighted Essential Non-Oscillatory)** est la **méthode de reconstruction** utilisée *au sein* du FVM. C'est le "moteur" qui calcule les flux aux frontières des cellules.

                    Pourquoi insister sur WENO ? Parce que c'est lui qui fait la différence. Un FVM classique serait soit trop flou (ordre 1), soit instable (oscillations). WENO nous donne le meilleur des deux mondes : la haute précision (ordre 5) et la stabilité face aux chocs.

<div style="page-break-after: always;"></div>

---

