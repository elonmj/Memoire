# Notes de Soutenance - Jumeau Numérique

## Slide 1 : Jumeau Numérique pour le Trafic Ouest-Africain

Monsieur le Président du Jury, Honorables membres, Chers Maîtres.

                    Nous avons l'honneur de vous présenter aujourd'hui les résultats de notre travail de fin
                    d'études.

                    Il porte sur la conception d'un "Jumeau Numérique pour le Trafic Ouest-Africain", et son utilisation
                    pour optimiser les feux de signalisation grâce à l'Intelligence Artificielle.

                    Ce travail a été mené sous la direction du Dr. Abel KONNON et l'encadrement technique du Dr. Régis
                    Donald HONTINFINDE.

<div style="page-break-after: always;"></div>

---

## Slide 2 : Plan de la Présentation

Pour cette présentation, nous suivrons une démarche classique en cinq points.

                    D'abord le contexte, pour comprendre pourquoi les solutions actuelles ne suffisent pas.

                    Ensuite, la méthodologie : comment nous avons construit ce simulateur.

                    Puis les résultats, pour voir si l'IA apporte vraiment un gain.

                    Et enfin, les perspectives que ce travail ouvre pour nos villes.

<div style="page-break-after: always;"></div>

---

## Slide 3 : Le Défi du Trafic Ouest-Africain

Le point de départ, c'est un constat que nous vivons tous au quotidien. Le trafic à Cotonou ou Lagos
                    n'a rien à voir avec celui de Paris ou de New York.

                    La différence majeure, c'est l'hétérogénéité. Les motos (les "zems") représentent plus de 70% du
                    flux. Elles se faufilent, changent de voie, créent une dynamique très fluide mais chaotique.

                    Nos infrastructures peinent à suivre, et cela crée la congestion chronique que nous connaissons,
                    avec son lot de pollution et de pertes économiques pour le pays.

<div style="page-break-after: always;"></div>

---

## Slide 4 : Pourquoi les Solutions Classiques Échouent

Le problème, c'est que nos outils de gestion actuels ne sont pas adaptés à cette réalité.

                    Les feux sont à temps fixe : ils sont "aveugles", ils ne voient pas le trafic.

                    Et les logiciels de simulation qu'on importe sont calibrés pour des voitures, en Occident. Ils ne
                    savent pas simuler correctement le comportement d'une nuée de motos.

                    Il y a donc un manque criant d'outils technologiques adaptés à *notre* contexte.

<div style="page-break-after: always;"></div>

---

## Slide 5 : Questions et Objectifs de Recherche

L'objectif de ce mémoire était donc de combler ce vide.

                    Nous nous sommes posé trois questions simples :

                    1. Peut-on modéliser mathématiquement ce trafic mixte ?

                    2. Peut-on le simuler de manière réaliste sans avoir des capteurs partout ?

                    3. Une IA peut-elle faire mieux qu'un feu classique dans ce contexte ?

                    Nos hypothèses sont que le modèle ARZ est la bonne clé théorique, et que le Reinforcement Learning
                    est la bonne méthode de contrôle.

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

## Slide 10 : Schéma Numérique

Pour résoudre ces équations, nous avons dû implémenter un schéma numérique avancé, le WENO5.

                    C'est technique, mais c'est nécessaire. Le trafic crée des ondes de choc (les freinages brusques).
                    Des schémas plus simples auraient créé des erreurs de calcul ou des oscillations fausses.

                    WENO5 garantit que la simulation reste stable et précise, ce qui est indispensable pour que l'IA
                    apprenne correctement.

<div style="page-break-after: always;"></div>

---

## Slide 11 : Cas d'Étude : Corridor Victoria Island

Pour tester tout cela, nous avons modélisé un corridor réel de Victoria Island à Lagos.

                    C'est un cas d'école : 3 carrefours, beaucoup de trafic, et un mélange intense de motos et
                    voitures.

                    Si notre système fonctionne ici, dans ces conditions difficiles, il pourra fonctionner ailleurs.

<div style="page-break-after: always;"></div>

---

## Slide 12 : Environnement RL - API Gymnasium

Pour l'IA, nous avons utilisé l'apprentissage par renforcement.

                    L'agent est comme un policier au carrefour. Il regarde l'état du trafic (densités, vitesses).

                    Il prend une action : laisser vert ou passer au rouge.

                    Et il reçoit une récompense : plus le trafic coule, plus il gagne de points. Il apprend ainsi par
                    essai-erreur à maximiser la fluidité globale.

<div style="page-break-after: always;"></div>

---

## Slide 13 : Clarification : Vers un Jumeau Numérique

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

## Slide 14 : Sans Titre

Voici une démonstration en temps réel de notre jumeau numérique.

                    Ce que vous voyez ici, c'est le modèle ARZ multi-classes en action sur le corridor de Victoria
                    Island :

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

## Slide 15 : Validation H1 : Tests de Riemann

Passons aux résultats. D'abord, la validation mathématique.

                    Nous avons soumis le modèle à des tests standards (les problèmes de Riemann).

                    Comme vous le voyez, le modèle gère parfaitement les ondes de choc et de détente. Il n'y a pas
                    d'aberration numérique. Le moteur est fiable.

<div style="page-break-after: always;"></div>

---

## Slide 16 : Validation H2 : Dynamique du Réseau

Ensuite, la validation systémique du jumeau numérique.

                    Ces instantanés montrent l'évolution temporelle du trafic sur le corridor de Victoria Island.
                    On observe clairement la propagation des ondes de choc (zones rouges) qui remontent le
                    courant.

                    Le modèle reproduit les trois régimes de trafic : fluide, congestionné, et bouchonné.
                    Cela confirme que notre jumeau numérique capture bien la phénoménologie réelle du trafic.

<div style="page-break-after: always;"></div>

---

## Slide 17 : Courbe d'Apprentissage de l'Agent RL

**Monsieur le Président, honorables membres du Jury**, maintenant que nous avons validé
                    l'outil de simulation, voyons ce que l'IA a réussi à faire.

                    Voici la courbe d'apprentissage de l'agent.

                    Au début, il tâtonne. Mais après environ 50 000 itérations, il converge vers une stratégie stable.
                    Il a appris à gérer le carrefour.

<div style="page-break-after: always;"></div>

---

## Slide 18 : Résultats Comparatifs

Concrètement, qu'est-ce que ça donne ?

                    Nous avons comparé l'IA à un feu à temps fixe bien réglé (méthode Webster).

                    En moyenne, l'IA améliore le flux de 4.2%.

                    Mais surtout, en situation de saturation (quand c'est la crise), le gain monte à près de 6%.

<div style="page-break-after: always;"></div>

---

## Slide 19 : Analyse du Gain

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

## Slide 20 : Synthèse des Résultats

En synthèse :

                    Nous avons validé le modèle mathématique (H1).

                    Nous avons validé le réalisme du trafic simulé (H2).

                    Et nous avons montré que l'IA apporte un gain opérationnel, même s'il reste perfectible (H3).

<div style="page-break-after: always;"></div>

---

## Slide 21 : Contributions

Ce travail apporte trois contributions :

                    1. Un modèle mathématique adapté à notre contexte (motos/voitures).

                    2. Une implémentation numérique performante et stable.

                    3. Une plateforme prête à l'emploi pour entraîner d'autres IA sur nos problématiques locales.

<div style="page-break-after: always;"></div>

---

## Slide 22 : Limites et Perspectives

Bien sûr, tout n'est pas parfait.

                    La limite principale reste le manque de données réelles pour calibrer finement les
                    paramètres.

                    Mais les perspectives sont là : on peut tester d'autres algorithmes d'IA, étendre la simulation à
                    tout un quartier, et à terme, connecter de vrais capteurs.

<div style="page-break-after: always;"></div>

---

## Slide 23 : Merci

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

