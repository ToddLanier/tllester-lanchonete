# tllester-lanchonete

## Project: Lanchonete

This project consists in a Hugo static-generated website that is pre-populated with migrated content (posts, pages, images, files, etc..) from about a half dozen individual Wordpress blogs, all originally located under the domain `lanchonete.org`.

### Running Pagefind

`alias hs='rm -rf public && npx -y pagefind --site public --serve`

`npm_config_yes=true npx pagefind --site "public" --output-subdir ../static/pagefind`

```bash
npm_config_yes=true npx pagefind --site "public" --output-subdir ../static/pagefind
hugo server
```

### Language Detection (Geolocation)

On the **homepage only**, the site automatically redirects visitors to their preferred language version using a three-step waterfall:

1. **Stored preference** (`localStorage` key `lanchonete-lang`) — checked first on every visit. Set by prior detection or by manually clicking a language button.
2. **Browser locale** (`navigator.language`) — if it starts with `pt`, the visitor goes straight to the Portuguese version with no external API call.
3. **IP geolocation** ([ipapi.co](https://ipapi.co), free tier) — used only when the browser locale is non-PT. Redirects to PT for visitors in Lusophone countries (BR, PT, AO, MZ, CV, GW, ST, TL, MO), EN otherwise.

If the API is unreachable, a non-PT browser defaults to EN.

Manual language switching via the language-switcher widget always wins on subsequent visits (writes to `localStorage`).

**Hugo URL structure:** Portuguese at `/`, English at `/en/`.
