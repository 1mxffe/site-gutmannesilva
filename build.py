#!/usr/bin/env python3
"""Gera o site estático do Gutmann & Silva Advogados Associados.

Uso:
    python3 site/build.py                 # grava as páginas .html em site/
    python3 site/build.py --preview DIR   # variante para pré-visualização como Artifact

Toda a copy vem do documento "Copy do Site — Gutmann & Silva Advogados
Associados" (Notion). Não reescreva textos aqui sem que a copy aprovada mude.
"""

import argparse
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Endpoint que recebe o POST dos formulários (ex.: Formspree, RD Station,
# script próprio). Vazio = formulário exibe aviso para usar os canais diretos.
FORM_ENDPOINT = ""
NEWSLETTER_ENDPOINT = ""

FONTS = ("https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500"
         "&family=Figtree:wght@400;500;600&display=swap")

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
           "%3Crect width='64' height='64' fill='%230E1F30'/%3E%3Ctext x='32' y='43' font-family='Georgia,serif' "
           "font-size='30' font-weight='700' text-anchor='middle' fill='%238EB2D8'%3EG%26S%3C/text%3E%3C/svg%3E")

CONTATO = {
    "telefone": "(41) 3081-3679",
    "telefone_href": "tel:+554130813679",
    "whatsapp": "+55 41 8814-1335",
    "whatsapp_href": "https://wa.me/554188141335",
    "email": "contato@gutmannesilva.com.br",
    "endereco": "Rua João Ângelo Cordeiro, 272 — São Pedro, São José dos Pinhais/PR — CEP 83005-570",
}

AREAS = [
    {
        "slug": "empresarial",
        "nome": "Empresarial",
        "titulo": "Direito Empresarial",
        "meta_titulo": "Direito Empresarial | Gutmann & Silva Advogados",
        "meta_desc": "Assessoria em Direito Empresarial: constituição societária, contratos, governança corporativa e operações de M&A no Paraná, São Paulo e Santa Catarina.",
        "resumo": "Assessoria jurídica contínua para empresas em constituição societária, contratos, governança e operações do dia a dia do negócio.",
        "abertura": "Empresas em qualquer estágio — da constituição à expansão — enfrentam decisões jurídicas que impactam diretamente sua operação. A equipe de Direito Empresarial do Gutmann & Silva acompanha esse dia a dia, oferecendo orientação sobre estrutura societária, contratos e governança.",
        "itens": [
            "Constituição e reestruturação societária",
            "Elaboração e revisão de contratos empresariais",
            "Governança corporativa e acordos de sócios",
            "Assessoria em operações de compra, venda e fusão de empresas",
            "Consultoria jurídica preventiva para rotina operacional",
        ],
        "fechamento": "Se sua empresa precisa de uma avaliação jurídica sobre um contrato, uma decisão societária ou a estruturação de uma operação, fale com nossa equipe de Direito Empresarial.",
        "cta": "Falar com a equipe Empresarial",
    },
    {
        "slug": "tributario",
        "nome": "Tributário",
        "titulo": "Direito Tributário",
        "meta_titulo": "Direito Tributário | Gutmann & Silva Advogados",
        "meta_desc": "Planejamento tributário, análise de enquadramento fiscal e orientação sobre isenção de Imposto de Renda para aposentados e pensionistas.",
        "resumo": "Planejamento e orientação tributária para pessoas físicas e jurídicas, incluindo análise de enquadramento e regimes especiais.",
        "abertura": "A carga tributária brasileira é complexa e está em constante mudança. A equipe de Direito Tributário do Gutmann & Silva acompanha essas mudanças para orientar pessoas físicas e jurídicas sobre enquadramento, regimes especiais e oportunidades legais de organização fiscal.",
        "itens": [
            "Planejamento tributário para empresas e pessoas físicas",
            "Análise de enquadramento e regime tributário",
            "Orientação sobre isenções e benefícios fiscais previstos em lei",
            "Consultoria em obrigações acessórias e rotina fiscal",
            "Representação em processos administrativos tributários",
        ],
        "destaque": {
            "titulo": "Isenção de Imposto de Renda para aposentados, pensionistas e portadores de doença grave",
            "texto": "A legislação prevê isenção de Imposto de Renda para pessoas nessas condições. Nossa equipe orienta sobre os requisitos legais e o processo de reconhecimento desse direito junto aos órgãos competentes.",
            "cta": "Entenda se você tem direito à isenção",
        },
        "fechamento": "Fale com a equipe de Direito Tributário para entender melhor o enquadramento fiscal da sua empresa ou situação pessoal.",
        "cta": "Falar com a equipe Tributária",
    },
    {
        "slug": "trabalhista",
        "nome": "Trabalhista",
        "titulo": "Direito Trabalhista",
        "meta_titulo": "Direito Trabalhista | Gutmann & Silva Advogados",
        "meta_desc": "Consultoria trabalhista preventiva e representação em processos trabalhistas para empresas e pessoas físicas no Paraná, São Paulo e Santa Catarina.",
        "resumo": "Consultoria preventiva e representação em Direito do Trabalho, tanto para empregadores quanto para pessoas físicas.",
        "abertura": "As relações de trabalho envolvem obrigações e direitos que mudam com frequência na legislação e na jurisprudência. A equipe de Direito Trabalhista do Gutmann & Silva assessora tanto empresas na gestão de suas obrigações quanto pessoas físicas em questões relacionadas ao vínculo de trabalho.",
        "itens": [
            "Consultoria trabalhista preventiva para empresas",
            "Elaboração de políticas internas e contratos de trabalho",
            "Representação em processos trabalhistas",
            "Orientação sobre rescisões, verbas e direitos trabalhistas",
            "Due diligence trabalhista em operações societárias",
        ],
        "fechamento": "Converse com a equipe de Direito Trabalhista para entender como organizar ou revisar sua situação trabalhista.",
        "cta": "Falar com a equipe Trabalhista",
    },
    {
        "slug": "civel",
        "nome": "Cível",
        "titulo": "Direito Cível",
        "meta_titulo": "Direito Cível | Gutmann & Silva Advogados",
        "meta_desc": "Assessoria em contratos civis, responsabilidade civil, questões imobiliárias e cobranças no Paraná, São Paulo e Santa Catarina.",
        "resumo": "Atuação em contratos, responsabilidade civil, questões imobiliárias e demais relações regidas pelo Direito Civil.",
        "abertura": "O Direito Civil está presente em praticamente todas as relações pessoais e comerciais — de um contrato de locação a uma disputa sobre responsabilidade civil. A equipe Cível do Gutmann & Silva orienta clientes nessas situações com atenção aos detalhes que fazem diferença em cada caso.",
        "itens": [
            "Elaboração e revisão de contratos civis",
            "Questões imobiliárias e de posse",
            "Responsabilidade civil e reparação de danos",
            "Cobranças e negociação de dívidas",
            "Representação em processos cíveis",
        ],
        "fechamento": "Se você precisa de orientação sobre um contrato, uma questão imobiliária ou qualquer outra relação civil, fale com nossa equipe.",
        "cta": "Falar com a equipe Cível",
    },
    {
        "slug": "familia-sucessoes",
        "nome": "Família & Sucessões",
        "titulo": "Família & Sucessões",
        "meta_titulo": "Família & Sucessões | Gutmann & Silva Advogados",
        "meta_desc": "Planejamento sucessório, inventários, partilhas e divórcios conduzidos com discrição no Paraná, São Paulo e Santa Catarina.",
        "resumo": "Orientação em planejamento sucessório, inventários, partilhas e questões de direito de família, com a discrição que o tema exige.",
        "abertura": "Questões de família e sucessão exigem, além de conhecimento técnico, sensibilidade para lidar com momentos delicados da vida de cada cliente. A equipe de Família & Sucessões do Gutmann & Silva conduz esses processos com discrição e clareza sobre cada etapa.",
        "itens": [
            "Planejamento sucessório e organização patrimonial",
            "Inventários judiciais e extrajudiciais",
            "Partilha de bens",
            "Divórcios e questões de guarda e pensão",
            "Elaboração de testamentos e doações",
        ],
        "fechamento": "Nossa equipe está disponível para conversar, com a discrição necessária, sobre planejamento sucessório ou qualquer questão de família.",
        "cta": "Falar com a equipe de Família & Sucessões",
    },
    {
        "slug": "previdenciario",
        "nome": "Previdenciário",
        "titulo": "Direito Previdenciário",
        "meta_titulo": "Direito Previdenciário | Gutmann & Silva Advogados",
        "meta_desc": "Análise de benefícios do INSS, revisão de aposentadorias e orientação sobre isenção fiscal para aposentados e pensionistas.",
        "resumo": "Análise de direitos previdenciários, benefícios e questões relacionadas ao INSS, incluindo situações de isenção fiscal.",
        "abertura": "Entender os próprios direitos previdenciários nem sempre é simples diante das constantes mudanças na legislação do INSS. A equipe Previdenciária do Gutmann & Silva orienta clientes na análise de benefícios e no reconhecimento de direitos previstos em lei.",
        "itens": [
            "Análise de tempo de contribuição e planejamento de aposentadoria",
            "Revisão e concessão de benefícios do INSS",
            "Orientação sobre isenções fiscais para aposentados e pensionistas",
            "Representação em processos administrativos e judiciais previdenciários",
        ],
        "fechamento": "Fale com a equipe de Direito Previdenciário para entender melhor seus direitos junto ao INSS.",
        "cta": "Falar com a equipe Previdenciária",
    },
]

# Artigos do blog. Cada artigo segue a estrutura da copy: título claro e sem
# sensacionalismo, introdução, corpo em linguagem acessível (sem prometer
# resultado) e fechamento com CTA para a equipe da área. Exemplo:
#   {"slug": "isencao-ir-doenca-grave", "area": "tributario",
#    "titulo": "...", "resumo": "...", "data": "2026-10-01",
#    "corpo": "<p>...</p><h2>...</h2><p>...</p>"}
POSTS = []

# Nomes de arquivo por página (o preview troca a home por inicio.html)
HOME = "index.html"
CURRENT = ' aria-current="page"'


ARROW = ('<svg class="ico" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5" '
         'fill="none" stroke="currentColor" stroke-width="1.6"/></svg>')


def e(text):
    return html.escape(text, quote=True)


def area_href(a):
    return f"area-{a['slug']}.html"


def btn(label, href, kind="primary", extra=""):
    return f'<a class="btn btn--{kind}" href="{href}"{extra}><span>{e(label)}</span>{ARROW}</a>'


def eyebrow(text):
    return f'<p class="eyebrow">{e(text)}</p>'


def head(title, desc):
    return f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/styles.css">"""


def logo(cls=""):
    return f"""<a class="logo {cls}" href="{HOME}" aria-label="Gutmann &amp; Silva Advogados Associados — página inicial">
  <span class="logo__line">Gutmann &amp; Silva</span>
  <span class="logo__line logo__line--sub">Advogados Associados<i class="logo__sq" aria-hidden="true"></i></span>
</a>"""


def header(active):
    def cur(key):
        return CURRENT if key == active else ""

    areas_current = active == "areas" or active.startswith("area-")
    mega = "\n".join(
        f'<li><a href="{area_href(a)}"{cur("area-" + a["slug"])}><span>{e(a["nome"])}</span>{ARROW}</a></li>'
        for a in AREAS
    )
    panel_areas = "\n".join(f'<li><a href="{area_href(a)}">{e(a["nome"])}</a></li>' for a in AREAS)
    return f"""<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    {logo()}
    <nav class="nav" aria-label="Principal">
      <ul class="nav__list">
        <li><a class="nav__link" href="{HOME}"{cur("home")}>Home</a></li>
        <li><a class="nav__link" href="escritorio.html"{cur("escritorio")}>O Escritório</a></li>
        <li class="has-mega{' is-current' if areas_current else ''}">
          <button class="nav__link" type="button" aria-expanded="false" aria-controls="mega-areas">Áreas de Atuação <span class="chev" aria-hidden="true"></span></button>
          <div class="mega" id="mega-areas">
            <div class="wrap mega__inner">
              <div class="mega__intro">
                <p class="mega__title">Áreas de Atuação</p>
                {btn("Ver todas as áreas em detalhe", "areas.html", "outline-light")}
              </div>
              <ul class="mega__list">{mega}</ul>
            </div>
          </div>
        </li>
        <li><a class="nav__link" href="blog.html"{cur("blog")}>Blog</a></li>
        <li><a class="nav__link" href="equipe.html"{cur("equipe")}>Equipe</a></li>
      </ul>
      {btn("Contato", "contato.html", "primary", cur("contato"))}
    </nav>
    <button class="burger" type="button" aria-expanded="false" aria-controls="painel" aria-label="Abrir menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="panel" id="painel" hidden>
  <div class="panel__inner">
    <button class="panel__close" type="button" aria-label="Fechar menu"><span></span><span></span></button>
    <ul class="panel__main">
      <li><a href="{HOME}">Home</a></li>
      <li><a href="escritorio.html">O Escritório</a></li>
      <li><a href="areas.html">Áreas de Atuação</a><ul class="panel__sub">{panel_areas}</ul></li>
      <li><a href="blog.html">Blog</a></li>
      <li><a href="equipe.html">Equipe</a></li>
      <li><a href="contato.html">Contato</a></li>
    </ul>
    <div class="panel__contact">
      <p>{CONTATO['telefone']}</p>
      <p>{CONTATO['email']}</p>
    </div>
  </div>
</div>"""


def footer():
    areas = "\n".join(f'<li><a href="{area_href(a)}">{e(a["nome"])}</a></li>' for a in AREAS)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer__brand">{logo("logo--xl")}</div>
    <div class="footer__grid">
      <div class="footer__col">
        <h2>Escritório</h2>
        <ul>
          <li><a href="escritorio.html">O Escritório</a></li>
          <li><a href="equipe.html">Equipe</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="contato.html">Contato</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h2>Áreas de Atuação</h2>
        <ul>{areas}</ul>
      </div>
      <div class="footer__col">
        <h2>Contato</h2>
        <ul>
          <li><a href="{CONTATO['telefone_href']}">{CONTATO['telefone']}</a></li>
          <li>WhatsApp <a href="{CONTATO['whatsapp_href']}" target="_blank" rel="noopener">{CONTATO['whatsapp']}</a></li>
          <li><a href="mailto:{CONTATO['email']}">{CONTATO['email']}</a></li>
        </ul>
      </div>
      <div class="footer__col">
        <h2>Endereço</h2>
        <address>{e(CONTATO['endereco'])}</address>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© 2026 Gutmann &amp; Silva Advogados Associados</span>
      <span>OAB/PR · OAB/SP · OAB/SC</span>
    </div>
  </div>
</footer>
<script src="assets/main.js"></script>"""


def document(title, desc, active, main, fragment=False):
    body = f"""{header(active)}
<main id="conteudo">
{main}
</main>
{footer()}"""
    if fragment:
        # Página principal do Artifact: o publicador acrescenta doctype/head.
        return f"{head(title, desc)}\n{body}\n"
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head(title, desc)}
</head>
<body>
{body}
</body>
</html>
"""


def crumbs(*items):
    li = []
    for label, href in items:
        li.append(f'<li><a href="{href}">{e(label)}</a></li>' if href else f'<li aria-current="page">{e(label)}</li>')
    return f'<ol class="crumbs" aria-label="Você está em">{"".join(li)}</ol>'


def photo_panel(src, alt, inner="", extra=""):
    """Painel com foto real (assets/img/<src>.jpg). `inner` fica sobre a foto (ex.: o ano 1994)."""
    return (f'<div class="lines lines--photo {extra}">'
            f'<img src="assets/img/{src}.jpg" alt="{e(alt)}" decoding="async">{inner}</div>')


def page_hero(crumb_items, title_html, lead=None, panel_html="", photo=None):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    if photo:
        panel = photo_panel(*photo, inner=panel_html)
    else:
        panel = f'<div class="lines" aria-hidden="true">{panel_html}</div>'
    return f"""<section class="page-hero">
  <div class="page-hero__grid">
    <div class="page-hero__text">
      {crumbs(*crumb_items)}
      <h1>{title_html}</h1>
      {lead_html}
    </div>
    {panel}
  </div>
</section>"""


def cta_final():
    return f"""<section class="cta-band">
  <div class="wrap cta-band__inner">
    <h2>Precisa de orientação jurídica <em>especializada?</em></h2>
    <div class="cta-band__side">
      <p>Entre em contato com o Gutmann &amp; Silva e converse com uma equipe preparada para entender sua situação antes de indicar qualquer caminho.</p>
      {btn("Fale conosco", "contato.html", "light")}
    </div>
  </div>
</section>"""


def area_tiles(exclude=None):
    return "\n".join(
        f"""<a class="tile" href="{area_href(a)}">
  <h3>{e(a['nome'])}</h3>
  <p>{e(a['resumo'])}</p>
  <span class="tile__go" aria-hidden="true">{ARROW}</span>
</a>"""
        for a in AREAS if a is not exclude
    )


# ---------------------------------------------------------------- páginas

def page_home():
    main = f"""<section class="hero">
  <div class="hero__grid">
    <div class="hero__text">
      <h1>Três décadas de trajetória. Uma equipe que cresceu junto com <em>quem confiou nela.</em></h1>
      <div class="hero__side">
        <p>Desde 1994, o Gutmann &amp; Silva assessora empresas e famílias com uma equipe que hoje reúne mais de 30 profissionais, atuando em Direito Empresarial, Tributário, Trabalhista, Cível, Família &amp; Sucessões e Previdenciário — com sede no Paraná e atuação registrada também em São Paulo e Santa Catarina.</p>
        <div class="actions">
          {btn("Fale com o escritório", "contato.html")}
          {btn("Conheça nossa história", "escritorio.html", "outline-light")}
        </div>
      </div>
    </div>
    {photo_panel("fachada", "Fachada do escritório Gutmann &amp; Silva em São José dos Pinhais", '<span class="lines__year" aria-hidden="true">1994</span>', "lines--hero")}
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="statement">
      {eyebrow("Desde 1994")}
      <div class="statement__body">
        <h2 class="h-statement">30 anos não se constroem — se acumulam, <em>um cliente de cada vez</em></h2>
        <div class="cols-2">
          <p>Fundado em 1994, o Gutmann &amp; Silva é hoje um dos escritórios mais consolidados do Paraná, com uma trajetória construída quase inteiramente por indicação e relacionamento de longo prazo — a prova mais concreta de que confiança, no Direito, se conquista com o tempo. Nossa atuação nasceu no Paraná e, ao longo de três décadas, se estendeu a São Paulo e Santa Catarina, sempre mantendo o mesmo princípio: entender o negócio ou a situação do cliente antes de indicar qualquer caminho jurídico.</p>
          <p>Hoje somos mais de 28 advogados e advogadas organizados por área de especialização.</p>
        </div>
      </div>
    </div>
    <ul class="figures">
      <li><strong>30</strong><span>anos de história (desde 1994)</span></li>
      <li><strong>30+</strong><span>profissionais</span></li>
      <li><strong>3</strong><span>estados de atuação: Paraná, São Paulo e Santa Catarina</span></li>
    </ul>
  </div>
</section>

<section class="section section--gradient">
  <div class="wrap">
    <div class="statement statement--dark">
      {eyebrow("O que fazemos")}
      <h2>Áreas de <em>Atuação</em></h2>
    </div>
    <div class="tiles">{area_tiles()}</div>
    <div class="row-end">{btn("Ver todas as áreas em detalhe", "areas.html")}</div>
  </div>
</section>

<section class="spot">
  <div class="spot__text">
    {eyebrow("Presença")}
    <h2>Onde <em>atuamos</em></h2>
    <p>O Gutmann &amp; Silva tem sede em São José dos Pinhais, no Paraná, e atua com registros ativos nas seccionais da OAB de três estados:</p>
    <p class="muted">Essa presença em três estados permite acompanhar clientes com operações que ultrapassam fronteiras estaduais, mantendo o mesmo padrão de atendimento em qualquer frente.</p>
  </div>
  <div class="spot__visual">
    <ul class="states">
      <li class="is-hq"><span class="states__code" aria-hidden="true">PR</span><strong>Paraná (OAB/PR)</strong><span>sede do escritório</span></li>
      <li><span class="states__code" aria-hidden="true">SP</span><strong>São Paulo (OAB/SP)</strong></li>
      <li><span class="states__code" aria-hidden="true">SC</span><strong>Santa Catarina (OAB/SC)</strong></li>
    </ul>
  </div>
</section>

<section class="section section--sky">
  <div class="wrap">
    <div class="statement">
      {eyebrow("Reconhecimentos")}
      <div class="statement__body">
        <h2>Reconhecimentos</h2>
        <p class="lead-dark">Ao longo de nossa trajetória, o Gutmann &amp; Silva foi reconhecido por instituições e pela comunidade que atende:</p>
      </div>
    </div>
    <ul class="cards">
      <li class="card"><span class="card__kicker">Prêmio</span><p>Eleito Melhor Escritório de Advocacia do Ano em São José dos Pinhais em 2022, 2024 e 2025</p></li>
      <li class="card"><span class="card__kicker">Homenagem</span><p>Homenageado pela Assembleia Legislativa do Paraná</p></li>
      <li class="card"><span class="card__kicker">Google</span><p>Nota 4,9 no Google, com 139 avaliações</p></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="statement statement--dark">
      {eyebrow("Trajetória")}
      <h2>Por que escolher um escritório com <em>trajetória</em></h2>
    </div>
    <ul class="reasons">
      <li><h3>Histórico consolidado.</h3><p>Mais de três décadas de atuação contínua no mercado jurídico paranaense e nacional.</p></li>
      <li><h3>Equipe multidisciplinar.</h3><p>Profissionais dedicados a áreas específicas do Direito, permitindo profundidade técnica em cada frente.</p></li>
      <li><h3>Presença em três estados.</h3><p>Registro em três seccionais da OAB (PR, SP e SC), acompanhando clientes com operações em mais de um estado.</p></li>
      <li><h3>Relacionamento de longo prazo.</h3><p>Construímos vínculos duradouros com empresas e famílias, entendendo cada fase de sua trajetória.</p></li>
    </ul>
  </div>
</section>

{cta_final()}"""
    return ("Gutmann & Silva Advogados | 30 Anos em São José dos Pinhais/PR",
            "Escritório de advocacia full-service há 30 anos, com atuação em Empresarial, Tributário, Trabalhista, Cível, Família & Sucessões e Previdenciário no Paraná, São Paulo e Santa Catarina.",
            "home", main)


NOTAB = ' tabindex="-1"'


def page_escritorio():
    hist = [
        ("1994", "1994", "Fundação do escritório no Paraná, com foco em atendimento próximo a empresas e famílias."),
        ("anos", "Ao longo dos anos", "Expansão da atuação para São Paulo e Santa Catarina, com novos registros na OAB/SP e OAB/SC, e estruturação das áreas de especialização (Empresarial, Tributário, Trabalhista, Cível, Família &amp; Sucessões e Previdenciário), com a equipe crescendo para os atuais 30+ profissionais."),
        ("premios", "2022, 2024 e 2025", "Eleito Melhor Escritório de Advocacia do Ano em São José dos Pinhais."),
        ("hoje", "Hoje", "30 anos de história, presença em três estados e reconhecimento consolidado no mercado jurídico paranaense."),
    ]
    tabs = "".join(
        f'<button class="tabs__tab" type="button" role="tab" id="tab-{k}" aria-controls="painel-{k}" aria-selected="{"true" if i == 0 else "false"}"{"" if i == 0 else NOTAB}>{label}</button>'
        for i, (k, label, _) in enumerate(hist)
    )
    panels = "".join(
        f'<div class="tabs__panel" role="tabpanel" id="painel-{k}" aria-labelledby="tab-{k}"{"" if i == 0 else " hidden"}><strong>{label}</strong><p>{text}</p></div>'
        for i, (k, label, text) in enumerate(hist)
    )
    main = f"""{page_hero((("Home", HOME), ("O Escritório", None)), "Sobre o <em>Gutmann &amp; Silva</em>",
        "Fundado em 1994, o Gutmann &amp; Silva Advogados Associados nasceu no Paraná com um propósito simples: oferecer assessoria jurídica séria, próxima e tecnicamente sólida para empresas e famílias. Ao longo de três décadas, esse propósito não mudou — o que mudou foi o tamanho da equipe e a amplitude das áreas que passamos a atender.",
        '<span class="lines__year" aria-hidden="true">1994</span>',
        photo=("recepcao", "Recepção do escritório Gutmann &amp; Silva"))}

<section class="section section--sand">
  <div class="wrap statement">
    {eyebrow("Nossa trajetória")}
    <div class="statement__body">
      <h2 class="h-statement">Nossa <em>trajetória</em></h2>
      <div class="cols-2">
        <p>O escritório começou com uma atuação mais concentrada e, com o tempo, estruturou departamentos dedicados às áreas Empresarial, Cível, Trabalhista, Tributária, de Família &amp; Sucessões e Previdenciária. Essa especialização por área permite que cada cliente seja atendido por profissionais com domínio técnico específico sobre o tema em questão, sem perder a visão integrada que um escritório de porte médio consegue oferecer.</p>
        <p>Hoje, com sede em São José dos Pinhais, no Paraná, e registros ativos nas seccionais da OAB do Paraná, São Paulo e Santa Catarina, o Gutmann &amp; Silva atende clientes com operações que ultrapassam as fronteiras estaduais, mantendo o mesmo padrão de atendimento em qualquer frente.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="h-accent">Nossa história</h2>
    <div class="tabs" data-tabs>
      <div class="tabs__list" role="tablist" aria-label="Nossa história">{tabs}</div>
      {panels}
    </div>
  </div>
</section>

<section class="section section--white">
  <div class="wrap">
    <h2 class="h-accent">Nosso espaço</h2>
    <div class="gallery">
      <figure><img src="assets/img/sala-reuniao-4.jpg" alt="Sala de reuniões com mesa e cadeiras estofadas" loading="lazy" decoding="async"></figure>
      <figure><img src="assets/img/sala-espera.jpg" alt="Sala de espera do escritório" loading="lazy" decoding="async"></figure>
      <figure><img src="assets/img/sala-reuniao-2.jpg" alt="Sala de reuniões com a identidade do escritório" loading="lazy" decoding="async"></figure>
      <figure><img src="assets/img/fachada-portao.jpg" alt="Entrada do escritório em São José dos Pinhais" loading="lazy" decoding="async"></figure>
    </div>
  </div>
</section>

<section class="section section--sky">
  <div class="wrap">
    <div class="statement">
      {eyebrow("Propósito")}
      <h2>Missão, visão e <em>valores</em></h2>
    </div>
    <div class="mvv">
      <div class="card"><span class="card__kicker">Propósito</span><p>Proporcionar verdadeira proteção jurídica e apresentar soluções que gerem segurança e credibilidade além do esperado.</p></div>
      <div class="card"><span class="card__kicker">Visão</span><p>Solucionar conflitos, construir relacionamentos de confiança e proporcionar um impacto positivo que torne o ambiente jurídico mais justo para todos.</p></div>
      <div class="card card--dark"><span class="card__kicker">Valores</span>
        <ul class="values"><li>Ética</li><li>União</li><li>Comprometimento</li><li>Inovação</li><li>Respeito</li><li>Comunicação</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap duo">
    <div class="duo__text">
      <h2 class="h-accent">Como trabalhamos</h2>
      <p class="big">Antes de qualquer indicação jurídica, buscamos entender o contexto completo do cliente — seja uma empresa em expansão, uma família organizando sua sucessão ou um profissional com uma dúvida trabalhista ou previdenciária. Essa etapa de escuta é o que orienta cada estratégia que construímos.</p>
    </div>
    <div class="box">
      <h2>Compromisso ético</h2>
      <p>Atuamos em conformidade com o Código de Ética e Disciplina da OAB e com as normas que regulam a publicidade da advocacia no Brasil. Nossa comunicação busca informar, nunca prometer resultados ou comparar nossa atuação com a de outros profissionais.</p>
    </div>
  </div>
</section>

{cta_final()}"""
    return ("Sobre o Gutmann & Silva | 30 Anos de Advocacia no Paraná",
            "Conheça a história, a missão e os valores do Gutmann & Silva Advogados Associados, fundado em 1994 e atuante em Paraná, São Paulo e Santa Catarina.",
            "escritorio", main)


def page_areas():
    main = f"""{page_hero((("Home", HOME), ("Áreas de Atuação", None)), "Áreas de <em>Atuação</em>", photo=("sala-reuniao-3", "Sala de reuniões do escritório Gutmann &amp; Silva"))}
<section class="section section--gradient">
  <div class="wrap"><div class="tiles">{area_tiles()}</div></div>
</section>
{cta_final()}"""
    return ("Áreas de Atuação | Gutmann & Silva Advogados",
            "Escritório de advocacia full-service há 30 anos, com atuação em Empresarial, Tributário, Trabalhista, Cível, Família & Sucessões e Previdenciário no Paraná, São Paulo e Santa Catarina.",
            "areas", main)


def page_area(a):
    itens = "\n".join(f"<li>{e(i)}</li>" for i in a["itens"])
    destaque = ""
    if a.get("destaque"):
        d = a["destaque"]
        destaque = f"""<section class="section section--sky">
  <div class="wrap statement">
    {eyebrow("Destaque")}
    <div class="statement__body">
      <h2 class="h-statement">{e(d['titulo'])}</h2>
      <p class="lead-dark">{e(d['texto'])}</p>
      <div class="actions">{btn(d['cta'], "contato.html")}</div>
    </div>
  </div>
</section>"""
    main = f"""{page_hero((("Home", HOME), ("Áreas de Atuação", "areas.html"), (a["titulo"], None)), e(a['titulo']), e(a['abertura']),
        photo=("area-" + a["slug"], "Ilustração da área de " + a["nome"]))}
<section class="section">
  <div class="wrap practice">
    <div>
      <h2 class="h-accent">O que fazemos nesta área</h2>
      <ul class="services">{itens}</ul>
    </div>
    <div class="box box--sticky">
      <p>{e(a['fechamento'])}</p>
      {btn(a['cta'], "contato.html", "outline-dark")}
    </div>
  </div>
</section>
{destaque}
<section class="section section--sand">
  <div class="wrap">
    <div class="statement">
      {eyebrow("Áreas de Atuação")}
      <h2>Áreas de <em>Atuação</em></h2>
    </div>
    <div class="tiles tiles--light">{area_tiles(exclude=a)}</div>
  </div>
</section>"""
    return (a["meta_titulo"], a["meta_desc"], "area-" + a["slug"], main)


def page_blog():
    area_by_slug = {a["slug"]: a for a in AREAS}
    chips = ['<button class="chip" type="button" data-filter="todas" aria-pressed="true">Todas</button>'] + [
        f'<button class="chip" type="button" data-filter="{a["slug"]}" aria-pressed="false">{e(a["nome"])}</button>'
        for a in AREAS
    ]
    cards = "\n".join(
        f"""<a class="post" href="blog-{p['slug']}.html" data-category="{p['area']}">
  <span class="tag">{e(area_by_slug[p['area']]['nome'])}</span>
  <h3>{e(p['titulo'])}</h3>
  <p>{e(p['resumo'])}</p>
</a>"""
        for p in sorted(POSTS, key=lambda p: p["data"], reverse=True)
    )
    main = f"""{page_hero((("Home", HOME), ("Blog", None)), "Blog <em>Gutmann &amp; Silva</em>",
        "Reunimos aqui orientações e atualizações sobre as áreas em que atuamos, organizadas para ajudar empresas e pessoas físicas a entender melhor seus direitos e obrigações. Nosso conteúdo é informativo — não substitui uma consulta jurídica personalizada.",
        photo=("sala-espera", "Sala de espera do escritório Gutmann &amp; Silva"))}
<section class="section section--white">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Categorias do blog">{''.join(chips)}</div>
    <div class="posts">{cards}</div>
    <p class="empty" data-empty{'' if not POSTS else ' hidden'}>Nenhum artigo publicado nesta categoria até o momento.</p>
  </div>
</section>"""
    return ("Blog Jurídico | Gutmann & Silva Advogados",
            "Conteúdo jurídico sobre Direito Empresarial, Tributário, Trabalhista, Cível, Família & Sucessões e Previdenciário, direto de quem atua nessas áreas há 30 anos.",
            "blog", main)


def page_post(p):
    a = next(x for x in AREAS if x["slug"] == p["area"])
    main = f"""{page_hero((("Home", HOME), ("Blog", "blog.html"), (a["nome"], f"blog.html#{a['slug']}")), e(p['titulo']), photo=("area-" + a["slug"], "Ilustração da área de " + a["nome"]))}
<section class="section section--white">
  <div class="wrap">
    <article class="article">{p['corpo']}</article>
    <div class="box article-cta">
      <p>Precisa de orientação sobre este tema? Fale com nossa equipe.</p>
      {btn(a['cta'], "contato.html", "outline-dark")}
    </div>
  </div>
</section>"""
    return (f"{p['titulo']} | Gutmann & Silva Advogados", p["resumo"], "blog", main)


def partner(img, name, role, bio, regs):
    chips = "".join(f"<li>{r}</li>" for r in regs)
    return f"""<article class="partner">
  <div class="partner__photo"><img src="assets/img/{img}.jpg" alt="Retrato de {name}" loading="lazy" decoding="async"></div>
  <div class="partner__band"><h2>{name}</h2><span>{role}</span></div>
  <div class="partner__body">
    <p>{bio}</p>
    <ul class="oab"><li class="oab__label">Registros:</li>{chips}</ul>
  </div>
</article>"""


def page_equipe():
    main = f"""{page_hero((("Home", HOME), ("Equipe", None)), "Nossa <em>Equipe</em>",
        "O Gutmann &amp; Silva reúne mais de 30 profissionais organizados por área de especialização, com registro na OAB em três estados: Paraná, São Paulo e Santa Catarina. À frente da condução jurídica, institucional e empresarial do escritório estão nossos sócios.",
        photo=("sala-reuniao-1", "Sala de reuniões do escritório Gutmann &amp; Silva"))}
<section class="section section--white">
  <div class="wrap partners">
    {partner("celso-gutmann", "Celso Fernando Gutmann", "Sócio fundador", "Formado pela PUC/PR (1995). Atua em Direito Cível, Trabalhista e Empresarial, com especialização em Direito Empresarial e Civil.", ["OAB/PR 21.713", "OAB/SP 402.027"])}
    {partner("cristiano-silva", "Cristiano da Silva", "Sócio", "Graduado pela PUC/PR (2011), pós-graduado em Direito Civil e Processo Civil pela UNICURITIBA (2014), com atuação também em Legislação Tributária.", ["OAB/PR 60.125", "OAB/SP 401.811"])}
  </div>
</section>
{cta_final()}"""
    return ("Nossa Equipe | Gutmann & Silva Advogados",
            "Conheça os sócios fundadores do Gutmann & Silva Advogados Associados, à frente do escritório há 30 anos.",
            "equipe", main)


def page_contato():
    c = CONTATO
    main = f"""{page_hero((("Home", HOME), ("Contato", None)), "Fale com o <em>Gutmann &amp; Silva</em>",
        "Estamos à disposição para entender sua situação e indicar o melhor caminho jurídico. Preencha o formulário abaixo ou utilize um dos canais de contato direto.",
        photo=("fachada-portao", "Entrada do escritório Gutmann &amp; Silva"))}
<section class="section section--white" id="formulario">
  <div class="wrap contact">
    <form class="form" data-form data-endpoint="{e(FORM_ENDPOINT)}" data-success="Mensagem enviada." novalidate>
      <div class="form__row">
        <div class="field"><label for="nome">Nome</label><input id="nome" name="nome" type="text" autocomplete="name" required></div>
        <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="field"><label for="telefone">Telefone</label><input id="telefone" name="telefone" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="mensagem">Mensagem</label><textarea id="mensagem" name="mensagem" required></textarea></div>
      <p class="form__note">Ao enviar este formulário, você concorda em ser contatado pela nossa equipe. Suas informações não serão compartilhadas com terceiros.</p>
      <p class="form__status" role="status" hidden></p>
      <button class="btn btn--primary" type="submit"><span>Enviar mensagem</span>{ARROW}</button>
    </form>
    <dl class="channels">
      <div class="channel"><dt>Telefone</dt><dd><a href="{c['telefone_href']}">{c['telefone']}</a></dd></div>
      <div class="channel"><dt>WhatsApp</dt><dd><a href="{c['whatsapp_href']}" target="_blank" rel="noopener">{c['whatsapp']}</a></dd></div>
      <div class="channel"><dt>E-mail</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd></div>
      <div class="channel"><dt>Endereço</dt><dd>{e(c['endereco'])}</dd></div>
    </dl>
  </div>
</section>
<section class="section section--sky">
  <div class="wrap newsletter">
    <div>
      <h2>Fique por <em>dentro</em></h2>
      <p class="lead-dark">Cadastre-se para receber atualizações jurídicas relevantes para sua empresa ou sua família, direto na sua caixa de entrada.</p>
    </div>
    <form class="newsletter__form" data-form data-endpoint="{e(NEWSLETTER_ENDPOINT)}" data-success="Inscrição realizada." novalidate>
      <div class="newsletter__row">
        <div class="field"><label for="news-email">E-mail</label><input id="news-email" name="email" type="email" autocomplete="email" required></div>
        <button class="btn btn--primary" type="submit"><span>Inscrever-se</span>{ARROW}</button>
      </div>
      <p class="form__status" role="status" hidden></p>
    </form>
  </div>
</section>"""
    return ("Contato | Gutmann & Silva Advogados",
            "Fale com o Gutmann & Silva Advogados Associados em São José dos Pinhais/PR. Atendimento por telefone, WhatsApp, e-mail ou formulário.",
            "contato", main)


def build(out: Path, preview: bool):
    global HOME
    HOME = "inicio.html" if preview else "index.html"
    pages = {
        HOME: page_home(),
        "escritorio.html": page_escritorio(),
        "areas.html": page_areas(),
        "blog.html": page_blog(),
        "equipe.html": page_equipe(),
        "contato.html": page_contato(),
    }
    for a in AREAS:
        pages[area_href(a)] = page_area(a)
    for p in POSTS:
        pages[f"blog-{p['slug']}.html"] = page_post(p)

    out.mkdir(parents=True, exist_ok=True)
    for name, (title, desc, active, main) in pages.items():
        (out / name).write_text(document(title, desc, active, main), encoding="utf-8")
    if preview:
        title, desc, active, main = pages[HOME]
        (out / "preview.html").write_text(document(title, desc, active, main, fragment=True), encoding="utf-8")
    return sorted(pages)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", metavar="DIR", help="gera variante para Artifact em DIR")
    args = ap.parse_args()
    if args.preview:
        names = build(Path(args.preview), preview=True)
    else:
        names = build(ROOT, preview=False)
    print("\n".join(names))
