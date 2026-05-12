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
