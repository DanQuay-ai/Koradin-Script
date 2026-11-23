const source: LexicalModelSource = {
  format: 'trie-1.0',
  sources: ['wordlist.tsv'],
  // each Kɔradin sign is one "word": break text into syllables so suggestions offer the family of the onset being typed
  wordBreaker: function (text: string) {
    const spans = [];
    const re = /(kp|gb|ky|tw|gy|dw|kw|hy|hw|ny|ni|my|ts|dz|[hwypbktdjgszfvrlnm])?[aeɛiouɔ]|[hwypbktdjgszfvrlnm]{1,2}$/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      if (!m[0]) { re.lastIndex++; continue; }
      spans.push({ start: m.index, end: m.index + m[0].length, length: m[0].length, text: m[0] });
    }
    return spans;
  },
  languageUsesCasing: false,
};
export default source;
