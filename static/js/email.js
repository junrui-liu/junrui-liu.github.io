// Reveal-on-hover email obfuscation.
// HTML scrapers see only the placeholder text; headless JS without simulated
// hovers also can't trigger reveal. After one hover (or touchstart on mobile),
// the span's contents are swapped for a mailto: link.
//
// To swap in a new email:
//   1. Compute the key hex from the passphrase below:
//        KEY_HEX=$(echo -n "<PASSPHRASE>" | shasum -a 256 | awk '{print $1}')
//        IV_HEX=$(echo -n '0123456789abcdef' | xxd -p -c 256)
//   2. Encrypt:
//        echo -n "<your@email.tld>" | openssl enc -aes-256-cbc -K "$KEY_HEX" -iv "$IV_HEX" -base64 -A
//   3. Paste the output into the `data-cipher` attribute on the <span class="email">.
(function () {
  // The passphrase can be any length — it's hashed to a 32-byte AES-256 key.
  const PASSPHRASE = 'Loremipsumdolorsitamet/consecteturadipiscing';

  const stoa = (s) => new TextEncoder().encode(s).buffer;
  const atos = (b) => new TextDecoder().decode(b);
  const b64ToA = (s) => new Uint8Array([...atob(s)].map(c => c.charCodeAt(0))).buffer;
  const iv = stoa('0123456789abcdef');

  let keyPromise;
  function getKey() {
    if (!keyPromise) {
      keyPromise = crypto.subtle.digest('SHA-256', stoa(PASSPHRASE))
        .then((hash) => crypto.subtle.importKey('raw', hash, 'AES-CBC', false, ['decrypt']));
    }
    return keyPromise;
  }

  async function decrypt(data) {
    const k = await getKey();
    return atos(await crypto.subtle.decrypt({ name: 'AES-CBC', iv }, k, b64ToA(data)));
  }

  function wire(n) {
    let addr = '';
    const reveal = async () => {
      if (!addr) addr = await decrypt(n.dataset.cipher);
      n.innerHTML = `<a href="mailto:${addr}">${addr}</a>`;
      n.removeEventListener('mouseover', reveal);
      n.removeEventListener('touchstart', reveal);
      n.removeEventListener('focus', reveal);
    };
    n.addEventListener('mouseover', reveal);
    n.addEventListener('touchstart', reveal);
    n.addEventListener('focus', reveal);
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('span.email[data-cipher]').forEach(wire);
  });
})();
