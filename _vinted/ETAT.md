# État CNCRT DROP — mis à jour le 24/11/2026 20h45 (publications du soir)

À lire au début de chaque nouvelle conversation (avec la compétence vinted-cncrt-drop).

## Publiées le 24/11
- 214 Landers, 19,24 € — items/10956839884 (marque perso « Landers », absente de la liste Vinted)
- 210 John Baner, 14,24 € — items/10957014380
- 130bis Nike (republication), 3,24 € — items/10957279594
- 211 Guess, 24,24 € — items/10957522301
- 212 Hugo Boss, 34,24 € — items/10957883318 (marque Vinted « Hugo Boss »)
Excel à jour (dernière version commitée : Inventaire_v20261124b).

## Publiées le 23/11
- 150 Benetton (republication) — items/10943578051
- 192 Levi's réversible (republication) — items/10943898841
- 213 Avirex A-2 1992, 89,24 € — items/10944836534 (Guillaume a mis lui-même la photo de dos en 1re)
- 209 Gotcha aztèque, 25,24 € — items/10944875388
- 187 Petrol Industries (republication), 5,24 € — items/10944908292

## Passe quotidienne 24/11 (5 actions ; veille 6)
- Vente : 203 Survêtement Adidas Originals 35,24 € (bordereau envoyé) → colis à envoyer ; **à retirer de Vestiaire (id 74171192)** — signalé à Guillaume.
- Baisse : 182 Maillot FC Porto 15,24 → 13,24.
- Suppressions (photos sauvegardées dans 004r, 106r, 160r, 196r ; dans a_publier.json) : 004 Hélas, 106 Adidas 14 ans, 160 Reebok, 196 Lot hoodies rap.
- Prix changés par Guillaume constatés (respecter) : 150 5,24 · 198 19,24 · 143 19,24 · 189 17,24 · 169 49,24 · 083 15,24 (remonté).
- Ne pas re-baisser avant 1/12 : 182 ; avant 29-30/11 : 002 004 049 066 075 097 109 096 144.

## À publier (détails complets dans a_publier.json)
- 25/11 : 215 Eden Park 19h31 · 216 Maison du Jersey 19h54 · 005 Diesel (republication, supprimer l'ancienne annonce 10503011538 juste avant) 20h17 · 004 Hélas (republication, photos 004r) 20h36 · 160 Reebok (republication, 160r) 20h52
- 26/11 : 196 Lot 3 hoodies rap (196r) 19h28 · 106 Veste Adidas 14 ans (106r, prix 7,24 < achat+2 : à confirmer) 19h49
Après publication : `python3 mark_online.py src dst ref url [repub]` si la ligne existe dans l'Excel ; sinon créer la ligne (copier le style de la dernière ligne, formules Marge et Jours en ligne) + ligne Journal.

## Colis
À envoyer : 203 Survêtement Adidas Originals (vendu 35,24 €, bordereau envoyé — vu 24/11). Les autres ventes sont expédiées (vérifié 24/11).

## Vestiaire Collective
Connecté dans le **Chrome du HP via l'extension Claude in Chrome** (connexion Google). Le navigateur intégré de l'app Claude NE MARCHE PAS pour Vestiaire. Les captures d'écran Chrome peuvent planter (HP capot fermé) : tout faire en JS/find. Procédure + fonctions : `_vinted/vestiaire_helpers.js`. Mode femme : catégories différentes (21 Vestes, 611 Blousons, 20 Manteaux > Doudoune, 56 Pulls & Gilets) et norme de taille par défaut FR → choisir « International » (valeur 5). Recherche prix : API POST https://search.vestiairecollective.com/v1/product/search (filtre `sold:["1"]` = vendus), à lancer depuis une page de recherche Vestiaire.
Règle Guillaume : se caler sur les prix Vestiaire en comparant ce qui est comparable (état, matière, modèle). Dès qu'une plateforme vend, retirer l'annonce de l'autre.

### Déjà en vente par Guillaume AVANT le 23/11 (profil https://fr.vestiairecollective.com/profile/36155053/) — TOUJOURS vérifier ce profil avant de déposer
- Palace sweat M 64 € (réf 169) · Pas de Mer sweat laine L 94 € (réf 045) · Diesel blouson S 79 € (réf 005)
- Déjà vendus sur Vestiaire : 2 articles (Palace, Versace)

### Déposées le 23/11 (en vérification Vestiaire, mail à Guillaume)
- 213 Avirex A-2 1992 coton, état Correct, 139 € (net 111,20) — product_id 74154550 — aussi sur Vinted 89,24
- 212 Blazer Hugo Boss velours VERT KAKI FONCÉ, Très bon état, IT 52, 79 € (net 63,20) — product_id 74156436 (redéposé le 23/11 23h30 ; l'ancien 74154624 en « marron » retiré, accord de Guillaume). Une fois en ligne, Vestiaire ne permet que d'ajouter des photos / baisser le prix / retirer. — Vinted prévu 24/11
- 211 Veste Guess velours côtelé noire L, 59 € (net 44) — product_id 74154667 — Vinted prévu 24/11

### Déposées le 24/11 (en vérification Vestiaire)
- 188 Doudoune Schott Utah vert L, Très bon état, 75 € (net 60) — product_id 74170892 (similaires vendus 56-69 €)
- 006 Sweat Lacoste Devanlay vert XS, Très bon état, 51 € (net 36) — product_id 74170948 (similaires 25-38 €)
- 189 Doudoune Tommy Hilfiger noire M (femme, Manteaux > Doudoune), Bon état, 45 € (net 30) — product_id 74171022 (similaires 37-52 €, reco 44)
- 145 Gilet Adidas West Germany bleu M vintage, polyamide 70 %, Très bon état, 59 € (net 44) — product_id 74171077 (similaires 43-55 €)
- 075 Coupe-vent Adidas Ventex bleu M vintage (femme, Vestes > Blouson), Bon état, 47 € (net 32) — product_id 74171142 (similaires 33-47 €)
- 203 Survêtement Adidas Originals noir L (Veste), Très bon état, 69 € (net 54) — product_id 74171192 (vestes seules vendues 54-78 €)
Excel à jour pour ces 6 dépôts (24/11). **203 VENDU sur Vinted le 23/11 → retirer de Vestiaire (74171192).**
Rappel : dès qu'un article se vend sur une plateforme, retirer l'annonce de l'autre (tous sont aussi sur Vinted).

### Écartés (pas rentables après 15 € de frais ou pas de demande) : Stüssy x Nike 140, Kulte, Magenta, Lancel 205, Diesel 022.

## Astuces techniques
- Navigateur intégré : après chaque navigation, refaire une mini-capture (scale 0.1) avant de cliquer par coordonnées (sinon erreur « no screenshot dimensions »).
- Navigateur intégré : si le panneau fait ~449 px, `resize_window` 1024x768 puis recharger ; remettre preset "desktop" AVANT de rendre la main à Guillaume (sinon ses clics ne marchent plus).
- Juste après publication, Vinted peut bloquer « Modifier/Supprimer » (vérification automatique, `can_edit=false` dans l'API) : ça peut durer de quelques minutes à quelques jours, ne pas insister.
- Excel : stager le fichier du HP, éditer avec openpyxl, enregistrer sous un NOUVEAU nom dans /mnt/user-data/outputs/, commit avec expectedMtimeMs du staging.
- Économiser la limite : pas de captures d'écran inutiles, JS + find refs, un message final court à Guillaume.
