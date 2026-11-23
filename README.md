# Kɔradin

Kɔradin is a featural syllabary for the Akan languages (Twi, Fante, Akuapem, Bono and related varieties), created in 2021 by **Ntirikwaamaa** and developed within **Merankron**, the platform of the Neo-Akan movement ([neoakan.com](https://neoakan.com)).

## Merankron mission

Merankron works for the revival and unity of the Akan people through nine principles, set out in the [Merankron Manifesto](merankron-manifesto.pdf):

1. Unite Akan identity across the groups descended from Bonoman, Adanseman, Mankesim and Koromanti.
2. Use an Akan calendar and keep indigenous festivals at the heart of communal life.
3. Use Akan names as first names and Akan dialects in higher education.
4. **Use an Akan script** as the primary tool for writing Akan, so that a child could learn any field, aerospace engineering included, entirely in Akan.
5. Wear Akan-inspired dress in daily life, not only for ceremonies.
6. Produce and consume locally.
7. Modernise without losing the Akan essence.
8. Strengthen Nton, Asafo and Abusua structures.
9. Create art, architecture and music rooted in Akan values.

Kɔradin is principle 4 in practice.

## How the script works

- **Syllabic signs:** each sign is a consonant radical (onset) joined to a vowel form. Seven vowels: a e ɛ i o ɔ u.
- **Onset families:** single consonants (p b t d k g s z f v h r l n m w y), labiovelars (kp gb), and Akan clusters (ky gy hy tw dw kw hw ny my). One family shares one radical.
- **Nasals:** a nasal mark before an opening syllable (n-, m-, ng-), and a mark under the sign for a closing nasal (-n, -m, -ng).
- **Consonant clusters (CRV):** fra, bra, tra and similar take a filler vowel, ɔ before back vowels and ɛ before front vowels: fra → fɔ-ra.
- **Fante:** ts and dz are written with the t and d families (dzidzi → di-di).
- **Codas:** a consonant closing a syllable before another sign takes the same filler (dawurbɔ → da-wu-rɔ-bɔ). A final consonant takes ɛ (tsitsir → ti-ti-rɛ, bayir → ba-yi-rɛ).
- **Lone w:** written with the ɔ sign (asɛmpɔw → a-sɛm-pɔ-ɔ, gyinabew → gyi-na-be-ɔ).
- **Lone ts / dz:** written like t / d with the filler (tstsew → tɛ-te-ɔ, pɛrpɛrdzi → pɛ-rɛ-pɛ-rɛ-di).
- **Elision:** write elided forms in full (n'asɛm → ne asɛm or no asɛm).
- **Filler choice:** ɔ or ɛ by default; some words take the echo vowel instead (mbra → m-ba-ra). These are listed word by word in the Kɔradin Standard.
- **Doubled nasals:** mm before a consonant is written once, as a closing mark (yɛmmpɛ → yɛm-pɛ). Before a vowel the opening mark stays (mma → m-ma).

See `specimens/syllable-chart.png` for every sign.

## Planned (Kɔradin orthography)

Kɔradin will get its own orthography rather than mirroring Latin Akan spelling:

- **Spelling by sound, not by Latin:** asɛmpɔw is a-sɛm-pɔ-ɔ for now and will become a-sɛm-pɔ-o. Latin homographs can be told apart in Kɔradin, and the reverse also holds (mbra's spelling stays open).
- **Reduplication sign:** one mark after a sign means "say it again": ntomtom → n-tom + sign, ahwɛhwɛ → a-hwɛ + sign.
- **Elision:** written in full (n'asɛm → ne asɛm / no asɛm). Reference: Abakah (2004), *Elision in Fante* (`references/`).

## Contents

| Folder | What |
|---|---|
| `fonts/` | Sakyira Text (regular) and Sakyira Display (bold slanted), OpenType fonts that turn typed Latin Akan into Kɔradin signs |
| `keyman/` | Kɔradin (Sakyira) keyboard for Keyman on Windows, macOS, Linux, iOS and Android, with an adaptive phone layout (one key per family) |
| `specimens/` | Syllable chart and specimens |
| `standard/` | Kɔradin Standard v1.0 (PDF and source) |
| `UNICODE.md` | The path to Unicode encoding and how evidence is collected |
| `unicode-evidence/` | Dated evidence of Kɔradin in use |

## Typing Kɔradin

Install a font and type Akan in Latin letters: `sakyira`, `akwaaba`, `mfantse`. On keyboards without ɛ and ɔ, the Keyman keyboard types ɛ with X and ɔ with C.

## Credit and licence

Script and fonts © 2026 Ntirikwaamaa, Merankron. Fonts are licensed under the SIL Open Font License 1.1 (see `OFL.txt`).
