# Kɔradin and Unicode

Kɔradin is not yet in Unicode. Today the fonts show Kɔradin by turning Latin text into signs; text copied elsewhere stays Latin. Unicode encoding would let Kɔradin be stored and exchanged as its own text.

## What reviewers look for

Unicode's Script Encoding Working Group and UC Berkeley's Script Encoding Initiative (SEI) check, for a newly invented script:

1. **Use by people other than the creator**, in running text, over several years.
2. **A frozen repertoire:** the set of signs and their rules no longer change.
3. **A need for plain-text interchange:** people need to send Kɔradin as text, not images.
4. **A documented proposal**, usually prepared with SEI or SIL researchers.

Popularity alone is not the bar. Toto (2015) was encoded in 2021 with a small, unified community and a locked 31-character set. The Adinkra Alphabet has had proposals on hold since 2020 for lack of evidence of sustained use.

## Kɔradin's case

- **Design:** a featural syllabary fitted to Akan syllable structure (CV, labiovelars, clusters, nasal finals), not a letter-for-letter cipher of Latin.
- **Age:** created 2021.
- **Tools:** OpenType fonts, Keyman keyboard (desktop and phone), type tester, this public repository with dated history.

## Roadmap

### Phase 1: freeze and document (now to early 2027)
- [ ] Settle the remaining orthography rules from the Fante, Nzema, Ahanta dialect review.
- [ ] Freeze the sign repertoire: version 1.0 of the chart, with names and sound values.
- [ ] Publish a Kɔradin Standard (PDF): signs, nasal rules, cluster rules, punctuation, sort order.
- [ ] Choose the font licence (SIL OFL recommended) and publish Keyman keyboard to keyman.com.

### Phase 2: public use (2027 onward)
- [ ] A Twi/Fante to Kɔradin converter on neoakan.com, with copy as image and sticker.
- [ ] Running text: bilingual folktales, essays, dialogues, a primer (print with ISBN).
- [ ] Third parties: educators and writers using Kɔradin in their own publications, with at least one full paragraph of Kɔradin text.
- [ ] Learners posting Kɔradin sentences; a public wall or community space.

### Phase 3: researchers and proposal
- [ ] Entries on ScriptSource (SIL) and Omniglot.
- [ ] Contact SEI (Deborah Anderson) with the Standard, the evidence dossier and this repository.
- [ ] Preliminary proposal, co-written with SEI or SIL.

## Evidence dossier

Every item in `unicode-evidence/` gets: date, author (independent user or Merankron), context, the Kɔradin text with Latin Akan and English, and a Wayback Machine link (web.archive.org) taken on the day it goes live.

| Folder | What goes in |
|---|---|
| `01_independent_users` | Posts, messages and exercises written by people other than Ntirikwaamaa |
| `02_third_party_articles` | Articles, lessons and mentions on sites Merankron does not own |
| `03_published_texts` | Books, PDFs, primers and long-form texts |
| `04_interchange_pain` | Cases where Kɔradin breaks without Unicode (boxes, Latin fallback, images instead of text) |
