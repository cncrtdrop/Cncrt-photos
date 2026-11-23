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
- 25/11 : 215 Eden Park 19h31 · 216 Maison du Jersey 19h54
Après publication : `python3 mark_online.py src dst ref url [repub]` si la ligne existe dans l'Excel ; sinon créer la ligne (copier le style de la dernière ligne, formules Marge et Jours en ligne) + ligne Journal.

## Colis
Tous les colis vendus ont été envoyés (confirmé par Guillaume le 23/11 21h39). Ne plus lister de colis sans vérifier sur Vinted.

## Vestiaire Collective
CONNECTÉ (23/11 22h10) dans le **Chrome du HP via l'extension Claude in Chrome** (connexion Google). Le navigateur intégré de l'app Claude NE MARCHE PAS pour Vestiaire (boutons morts, pop-up Google bloquée) : ne pas l'utiliser pour Vestiaire.
À faire : regarder les prix (filtre vendus à trouver ; la recherche ?sold=1 ne filtre pas) pour Avirex, Boss, Guess ; proposer ; mettre l'Avirex et sans doute le blazer Boss. Repère 23/11 : blousons Avirex cuir en vente ~150-500 € (prix affichés, frais acheteur compris). Défauts acceptés s'ils sont déclarés. Frais Vestiaire : <75 € → 12 € + 3 € ; ≥75 € → 17 % + 3 %. Dès qu'une plateforme vend, retirer l'annonce de l'autre.

## Astuces techniques
- Navigateur intégré : si le panneau fait ~449 px, `resize_window` 1024x768 puis recharger ; remettre preset "desktop" AVANT de rendre la main à Guillaume (sinon ses clics ne marchent plus).
- Juste après publication, Vinted peut bloquer « Modifier/Supprimer » (vérification automatique, `can_edit=false` dans l'API) : ça peut durer de quelques minutes à quelques jours, ne pas insister.
- Excel : stager le fichier du HP, éditer avec openpyxl, enregistrer sous un NOUVEAU nom dans /mnt/user-data/outputs/, commit avec expectedMtimeMs du staging.
- Économiser la limite : pas de captures d'écran inutiles, JS + find refs, un message final court à Guillaume.
