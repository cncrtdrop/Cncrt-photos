# État CNCRT DROP — mis à jour le 23/11/2026 21h35

À lire au début de chaque nouvelle conversation (avec la compétence vinted-cncrt-drop).

## Publiées le 23/11
- 150 Benetton (republication) — items/10943578051
- 192 Levi's réversible (republication) — items/10943898841
- 213 Avirex A-2 1992, 89,24 € — items/10944836534 (Guillaume a mis lui-même la photo de dos en 1re)
- 209 Gotcha aztèque, 25,24 € — items/10944875388
- 187 Petrol Industries (republication), 5,24 € — items/10944908292
Excel à jour (dernière version commitée : Inventaire_v20261123d).

## À publier (détails complets dans a_publier.json)
- 24/11 : 214 Landers 19h24 · 210 John Baner 19h37 · 130bis Nike (republication) 19h58 · 211 Guess 20h14 · 212 Hugo Boss 20h39
- 25/11 : 215 Eden Park 19h31 · 216 Maison du Jersey 19h54 · 005 Diesel (republication, supprimer l'ancienne annonce 10503011538 juste avant) 20h17
Après publication : `python3 mark_online.py src dst ref url [repub]` si la ligne existe dans l'Excel ; sinon créer la ligne (copier le style de la dernière ligne, formules Marge et Jours en ligne) + ligne Journal.

## Colis
Tous les colis vendus ont été envoyés (confirmé par Guillaume le 23/11 21h39). Ne plus lister de colis sans vérifier sur Vinted.

## Vestiaire Collective
Connecté dans le **Chrome du HP via l'extension Claude in Chrome** (connexion Google). Le navigateur intégré de l'app Claude NE MARCHE PAS pour Vestiaire. Les captures d'écran Chrome peuvent planter (HP capot fermé) : tout faire en JS/find. Procédure + fonctions : `_vinted/vestiaire_helpers.js`. Recherche prix : API POST https://search.vestiairecollective.com/v1/product/search (filtre `sold:["1"]` = vendus), à lancer depuis une page de recherche Vestiaire.
Règle Guillaume : se caler sur les prix Vestiaire en comparant ce qui est comparable (état, matière, modèle). Dès qu'une plateforme vend, retirer l'annonce de l'autre.

### Déjà en vente par Guillaume AVANT le 23/11 (profil https://fr.vestiairecollective.com/profile/36155053/) — TOUJOURS vérifier ce profil avant de déposer
- Palace sweat M 64 € (réf 169) · Pas de Mer sweat laine L 94 € (réf 045) · Diesel blouson S 79 € (réf 005)
- Déjà vendus sur Vestiaire : 2 articles (Palace, Versace)

### Déposées le 23/11 (en vérification Vestiaire, mail à Guillaume)
- 213 Avirex A-2 1992 coton, état Correct, 139 € (net 111,20) — product_id 74154550 — aussi sur Vinted 89,24
- 212 Blazer Hugo Boss velours, Très bon état, IT 52, 79 € (net ~64) — product_id 74154624 — Vinted prévu 24/11
- 211 Veste Guess velours côtelé noire L, 59 € (net 44) — product_id 74154667 — Vinted prévu 24/11

### À déposer le 24/11 : `_vinted/vestiaire_a_publier.json` (188 Schott, 006 Lacoste, 189 Tommy ; photos vc188/vc006/vc189 ; 005 Diesel retiré : déjà en ligne)

### Écartés (pas rentables après 15 € de frais ou pas de demande) : Stüssy x Nike 140, Kulte, Magenta, Lancel 205, Diesel 022.

## Astuces techniques
- Navigateur intégré : si le panneau fait ~449 px, `resize_window` 1024x768 puis recharger ; remettre preset "desktop" AVANT de rendre la main à Guillaume (sinon ses clics ne marchent plus).
- Juste après publication, Vinted peut bloquer « Modifier/Supprimer » (vérification automatique, `can_edit=false` dans l'API) : ça peut durer de quelques minutes à quelques jours, ne pas insister.
- Excel : stager le fichier du HP, éditer avec openpyxl, enregistrer sous un NOUVEAU nom dans /mnt/user-data/outputs/, commit avec expectedMtimeMs du staging.
- Économiser la limite : pas de captures d'écran inutiles, JS + find refs, un message final court à Guillaume.
