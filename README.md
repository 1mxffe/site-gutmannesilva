# Site institucional — Gutmann & Silva Advogados Associados

Site estático (HTML + CSS + JS puro, sem dependências) gerado a partir da copy
aprovada no Notion ("Copy do Site — Gutmann & Silva Advogados Associados").

## Estrutura

| Arquivo | Página |
|---|---|
| `index.html` | Home |
| `escritorio.html` | O Escritório |
| `areas.html` | Áreas de Atuação (visão geral) |
| `area-*.html` | Empresarial, Tributário, Trabalhista, Cível, Família & Sucessões, Previdenciário |
| `blog.html` | Blog, com filtro pelas 6 áreas (`blog.html#tributario` abre já filtrado) |
| `equipe.html` | Sócios |
| `contato.html` | Contato + newsletter |
| `assets/styles.css`, `assets/main.js` | Estilo e comportamento compartilhados |

## Como editar

As páginas `.html` são **geradas** — edite `build.py` e rode:

```sh
python3 build.py
```

- **Formulários**: preencha `FORM_ENDPOINT` e `NEWSLETTER_ENDPOINT` em `build.py`
  com a URL que recebe os envios (a mesma usada no site atual). Enquanto
  vazios, o formulário orienta o visitante a usar os canais diretos.
- **Artigos do blog**: adicione entradas em `POSTS` (`build.py`). Cada artigo
  ganha página própria (`blog-<slug>.html`), aparece no filtro da área e
  termina com o CTA padrão "Precisa de orientação sobre este tema? Fale com
  nossa equipe." Estrutura: título claro e sem sensacionalismo, introdução,
  corpo sem prometer resultado, fechamento com CTA da área.

## Identidade visual

- Navy `#0E1F30` (fundo predominante), azul `#2C6196` (CTAs e destaques),
  branco e cinzas levemente azulados; `#8EB2D8` (tom claro do azul) nos
  números sobre fundo escuro, para manter contraste legível.
- Títulos em Newsreader (serifada, com destaque em itálico), texto em Figtree — ambas via Google Fonts.
- Linguagem visual inspirada em hlc.com: botões retos com seta ↗, rótulos com fio vertical, painéis em degradê com fios horizontais, cards com seta no canto, mega menu de áreas, menu lateral e abas na linha do tempo.

## Publicação (Vercel)

Importe este repositório na Vercel com Framework Preset **Other**, sem Build
Command e com o Output Directory padrão (raiz). Cada push na `main` publica o site.
