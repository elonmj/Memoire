# 🚦 Guide de l'Animation Trafic ARZ - Victoria Island

## Vue d'ensemble

Cette animation visualise la simulation de trafic multi-classes basée sur le modèle ARZ (Aw-Rascle-Zhang) dans le quartier de Victoria Island à Lagos, Nigeria.

---

## 🎨 Palette de Couleurs

### Véhicules (Trails animés)

| Type | Couleur | Code RGB | Hex | Visuel |
|------|---------|----------|-----|--------|
| **Motos** 🏍️ | Orange vif | `[241, 148, 54]` | `#F19436` | 🟠 |
| **Voitures** 🚗 | Bleu ciel | `[52, 152, 219]` | `#3498DB` | 🔵 |

**Pourquoi ces couleurs ?**
- **Orange** : Couleur chaude, très visible, représente l'agilité des motos
- **Bleu** : Couleur froide, contraste avec l'orange, représente les véhicules plus lourds

### Feux de Signalisation

| État | Couleur | Code RGB | Signification |
|------|---------|----------|---------------|
| 🟢 **Vert** | Vert émeraude | `[39, 174, 96]` | Passage autorisé |
| 🟡 **Jaune** | Jaune soleil | `[241, 196, 15]` | Attention, transition |
| 🔴 **Rouge** | Rouge corail | `[231, 76, 60]` | Arrêt obligatoire |

**Cycle des feux** : 10s vert → 3s jaune → reste rouge (total ~25s par cycle)

### Infrastructure Routière

| Élément | Couleur | Code RGB | Description |
|---------|---------|----------|-------------|
| **Routes** | Gris ardoise | `[90, 100, 120]` | Chaussée principale |
| **Lignes centrales** | Gris clair | `[180, 190, 210]` | Marquage au sol pointillé |
| **Poteaux feux** | Gris foncé | `[80, 80, 90]` | Support des feux |

---

## 📐 Paramètres Techniques

### Trails (Trajectoires des véhicules)

| Paramètre | Motos | Voitures | Explication |
|-----------|-------|----------|-------------|
| `widthMinPixels` | 8 px | 10 px | Épaisseur minimale du trait |
| `trailLength` | 80 | 100 | Longueur de la "queue" (unités de temps) |
| `opacity` | 1.0 | 1.0 | Opacité (100% = couleur pleine) |
| `fadeTrail` | true | true | Dégradé progressif vers la transparence |

**Interprétation visuelle** :
- Plus le trail est long, plus on voit le "parcours récent" du véhicule
- Le fadeTrail crée un effet de mouvement fluide
- Les voitures ont des trails plus épais car elles sont plus grandes physiquement

### Vue de la carte

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `longitude` | 3.4205 | Centre de Victoria Island |
| `latitude` | 6.4295 | Lagos, Nigeria |
| `zoom` | 15 | Niveau de détail quartier |
| `pitch` | 45° | Inclinaison 3D |
| `bearing` | -15° | Rotation de la carte |

---

## 🗺️ Options de Style de Carte (Basemaps CARTO)

### Styles disponibles

| Style | URL | Description | Noms de rues |
|-------|-----|-------------|--------------|
| **Voyager** (gris coloré) | `voyager-gl-style` | Carte colorée, fond gris | ✅ Oui (noir) |
| **Positron** (clair) | `positron-gl-style` | Fond blanc/gris très clair | ✅ Oui (noir) |
| **Dark Matter** (sombre) | `dark-matter-gl-style` | Fond noir/gris foncé | ✅ Oui (blanc) |
| Dark Matter No Labels | `dark-matter-nolabels-gl-style` | Fond noir sans texte | ❌ Non |

### URLs complètes

```javascript
// Gris coloré avec noms de rues (RECOMMANDÉ pour présentation jour)
'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'

// Fond sombre avec noms de rues BLANCS (RECOMMANDÉ pour présentation sombre)
'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json'

// Fond très clair
'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
```

---

## 🔧 Comment modifier les couleurs

### Changer la couleur des motos

Dans `traffic_realistic.html`, trouver la section `trips-motos` :

```javascript
new TripsLayer({
    id: 'trips-motos',
    // ...
    getColor: [241, 148, 54],  // ← Modifier ici (R, G, B)
    // ...
})
```

### Changer la couleur des voitures

```javascript
new TripsLayer({
    id: 'trips-cars',
    // ...
    getColor: [52, 152, 219],  // ← Modifier ici (R, G, B)
    // ...
})
```

### Convertir Hex → RGB

| Hex | RGB |
|-----|-----|
| `#FF5733` | `[255, 87, 51]` |
| `#3498DB` | `[52, 152, 219]` |
| `#E74C3C` | `[231, 76, 60]` |

---

## 🎯 Conseils de Présentation

### Pour une salle éclairée (jour)
- Utiliser **Voyager** (fond gris coloré)
- Les noms de rues seront en noir, bien lisibles
- Couleurs vives recommandées pour les véhicules

### Pour une salle sombre / projection
- Utiliser **Dark Matter** (fond noir)
- Les noms de rues seront en BLANC automatiquement
- Les couleurs vives ressortiront bien sur le fond sombre

### Pour un écran de téléphone/tablette
- Utiliser **Positron** (fond blanc)
- Meilleur contraste en plein soleil

---

## 📊 Données de simulation

### Routes simulées
- **32 segments** de route dans Victoria Island
- Chaque segment : 2 voies, largeur 6m

### Véhicules
- **Motos** : Trajectoires rapides, comportement agile
- **Voitures** : Trajectoires plus lentes, respect des feux

### Feux de signalisation
- **4 intersections** contrôlées
- Cycle synchronisé mais décalé entre intersections

---

## 🐛 Dépannage

### Les trails sont invisibles
- Vérifier `widthMinPixels` (minimum 6-8)
- Vérifier `opacity` (doit être > 0.5)
- Vérifier que les données `tripsMotoData` et `tripsCarsData` ne sont pas vides

### Les noms de rues ne s'affichent pas
- Vérifier que vous utilisez un style AVEC labels :
  - ✅ `voyager-gl-style` 
  - ✅ `dark-matter-gl-style`
  - ❌ `dark-matter-nolabels-gl-style`

### Les couleurs ne ressortent pas
- Sur fond clair → utiliser des couleurs saturées
- Sur fond sombre → éviter le noir et les gris foncés

### Le cache pose problème
- Faire Ctrl+Shift+R (hard refresh)
- Ou ouvrir en navigation privée

---

## 📚 Références

- [deck.gl TripsLayer](https://deck.gl/docs/api-reference/geo-layers/trips-layer)
- [CARTO Basemaps](https://github.com/CartoDB/basemap-styles)
- [Modèle ARZ](https://en.wikipedia.org/wiki/Aw%E2%80%93Rascle%E2%80%93Zhang_model)
