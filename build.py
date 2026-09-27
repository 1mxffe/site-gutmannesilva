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

FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700"
         "&family=Source+Sans+3:wght@400;500;600&display=swap")

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


def e(text):
    return html.escape(text, quote=True)


def area_href(a):
    return f"area-{a['slug']}.html"


def head(title, desc):
    return f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/styles.css">"""


def header(active):
    def cur(key):
        return ' aria-current="page"' if key == active else ""

    areas_current = active == "areas" or active.startswith("area-")
    sub = "\n".join(
        f'<li><a href="{area_href(a)}"{cur("area-" + a["slug"])}>{e(a["nome"])}</a></li>' for a in AREAS
    )
    return f"""<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="{HOME}" aria-label="Gutmann &amp; Silva Advogados Associados — página inicial">
      <span class="brand__name">Gutmann <span>&amp;</span> Silva</span>
      <span class="brand__tag">Advogados Associados</span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    <nav class="nav" id="menu" aria-label="Principal">
      <ul class="nav__list">
        <li><a class="nav__link" href="{HOME}"{cur("home")}>Home</a></li>
        <li><a class="nav__link" href="escritorio.html"{cur("escritorio")}>O Escritório</a></li>
        <li class="nav__item--has-sub{' nav__item--current' if areas_current else ''}">
          <button class="nav__link" type="button" aria-expanded="false" aria-controls="submenu-areas">Áreas de Atuação <span class="chev" aria-hidden="true"></span></button>
          <ul class="submenu" id="submenu-areas">
            {sub}
            <li class="submenu__all"><a href="areas.html"{cur("areas")}>Todas as áreas</a></li>
          </ul>
        </li>
        <li><a class="nav__link" href="blog.html"{cur("blog")}>Blog</a></li>
        <li><a class="nav__link" href="equipe.html"{cur("equipe")}>Equipe</a></li>
        <li><a class="btn btn--primary nav__cta" href="contato.html"{cur("contato")}>Contato</a></li>
      </ul>
    </nav>
  </div>
</header>"""


def footer():
    areas = "\n".join(f'<li><a href="{area_href(a)}">{e(a["nome"])}</a></li>' for a in AREAS)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__col">
        <a class="brand" href="{HOME}">
          <span class="brand__name">Gutmann <span>&amp;</span> Silva</span>
          <span class="brand__tag">Advogados Associados</span>
        </a>
        <address>{e(CONTATO['endereco'])}</address>
      </div>
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
          <li>Telefone: <a href="{CONTATO['telefone_href']}">{CONTATO['telefone']}</a></li>
          <li>WhatsApp: <a href="{CONTATO['whatsapp_href']}" target="_blank" rel="noopener">{CONTATO['whatsapp']}</a></li>
          <li>E-mail: <a href="mailto:{CONTATO['email']}">{CONTATO['email']}</a></li>
        </ul>
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


def cta_final():
    return """<section class="cta-band">
  <div class="wrap">
    <div class="cta-band__text">
      <h2>Precisa de orientação jurídica especializada?</h2>
      <p>Entre em contato com o Gutmann &amp; Silva e converse com uma equipe preparada para entender sua situação antes de indicar qualquer caminho.</p>
    </div>
    <a class="btn btn--light" href="contato.html">Fale conosco</a>
  </div>
</section>"""


def area_cards():
    cards = "\n".join(
        f"""<a class="area-card" href="{area_href(a)}">
  <h3>{e(a['nome'])}</h3>
  <p>{e(a['resumo'])}</p>
  <span class="area-card__go" aria-hidden="true">→</span>
</a>"""
        for a in AREAS
    )
    return f'<div class="areas">{cards}</div>'


# ---------------------------------------------------------------- páginas

def page_home():
    main = f"""<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__text">
      <h1>Três décadas de trajetória. Uma equipe que cresceu junto com quem confiou nela.</h1>
      <p class="lead">Desde 1994, o Gutmann &amp; Silva assessora empresas e famílias com uma equipe que hoje reúne mais de 30 profissionais, atuando em Direito Empresarial, Tributário, Trabalhista, Cível, Família &amp; Sucessões e Previdenciário — com sede no Paraná e atuação registrada também em São Paulo e Santa Catarina.</p>
      <div class="actions">
        <a class="btn btn--primary" href="contato.html">Fale com o escritório</a>
        <a class="btn btn--ghost" href="escritorio.html">Conheça nossa história</a>
      </div>
    </div>
    <div class="hero__mark" aria-hidden="true">
      <span class="hero__since">Desde</span>
      <span class="hero__year">1994</span>
      <span class="hero__states">PR · SP · SC</span>
    </div>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    <div class="split">
      <h2>30 anos não se constroem — se acumulam, um cliente de cada vez</h2>
      <div class="prose">
        <p>Fundado em 1994, o Gutmann &amp; Silva é hoje um dos escritórios mais consolidados do Paraná, com uma trajetória construída quase inteiramente por indicação e relacionamento de longo prazo — a prova mais concreta de que confiança, no Direito, se conquista com o tempo. Nossa atuação nasceu no Paraná e, ao longo de três décadas, se estendeu a São Paulo e Santa Catarina, sempre mantendo o mesmo princípio: entender o negócio ou a situação do cliente antes de indicar qualquer caminho jurídico.</p>
        <p>Hoje somos mais de 28 advogados e advogadas organizados por área de especialização.</p>
      </div>
    </div>
    <ul class="stats">
      <li><span class="stats__num">30</span><span class="stats__label">anos de história (desde 1994)</span></li>
      <li><span class="stats__num">30+</span><span class="stats__label">profissionais</span></li>
      <li><span class="stats__num">3</span><span class="stats__label">estados de atuação: Paraná, São Paulo e Santa Catarina</span></li>
    </ul>
  </div>
</section>

<section class="section section--light">
  <div class="wrap">
    <div class="section__head">
      <h2>Onde atuamos</h2>
      <p class="lead">O Gutmann &amp; Silva tem sede em São José dos Pinhais, no Paraná, e atua com registros ativos nas seccionais da OAB de três estados:</p>
    </div>
    <ul class="states">
      <li class="is-hq"><span class="states__code" aria-hidden="true">PR</span><strong>Paraná (OAB/PR)</strong><span>sede do escritório</span></li>
      <li><span class="states__code" aria-hidden="true">SP</span><strong>São Paulo (OAB/SP)</strong></li>
      <li><span class="states__code" aria-hidden="true">SC</span><strong>Santa Catarina (OAB/SC)</strong></li>
    </ul>
    <p>Essa presença em três estados permite acompanhar clientes com operações que ultrapassam fronteiras estaduais, mantendo o mesmo padrão de atendimento em qualquer frente.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <h2>Reconhecimentos</h2>
      <p class="lead">Ao longo de nossa trajetória, o Gutmann &amp; Silva foi reconhecido por instituições e pela comunidade que atende:</p>
    </div>
    <ul class="honors">
      <li><span class="honors__mark" aria-hidden="true"></span>Eleito Melhor Escritório de Advocacia do Ano em São José dos Pinhais em 2022, 2024 e 2025</li>
      <li><span class="honors__mark" aria-hidden="true"></span>Homenageado pela Assembleia Legislativa do Paraná</li>
      <li><span class="honors__mark" aria-hidden="true"></span>Nota 4,9 no Google, com 139 avaliações</li>
    </ul>
  </div>
</section>

<section class="section section--light">
  <div class="wrap">
    <div class="section__head">
      <h2>Áreas de Atuação</h2>
    </div>
    {area_cards()}
    <p class="block-cta"><a class="link-arrow" href="areas.html">Ver todas as áreas em detalhe →</a></p>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    <div class="section__head">
      <h2>Por que escolher um escritório com trajetória</h2>
    </div>
    <ul class="reasons">
      <li><strong>Histórico consolidado.</strong><span>Mais de três décadas de atuação contínua no mercado jurídico paranaense e nacional.</span></li>
      <li><strong>Equipe multidisciplinar.</strong><span>Profissionais dedicados a áreas específicas do Direito, permitindo profundidade técnica em cada frente.</span></li>
      <li><strong>Presença em três estados.</strong><span>Registro em três seccionais da OAB (PR, SP e SC), acompanhando clientes com operações em mais de um estado.</span></li>
      <li><strong>Relacionamento de longo prazo.</strong><span>Construímos vínculos duradouros com empresas e famílias, entendendo cada fase de sua trajetória.</span></li>
    </ul>
  </div>
</section>

{cta_final()}"""
    return ("Gutmann & Silva Advogados | 30 Anos em São José dos Pinhais/PR",
            "Escritório de advocacia full-service há 30 anos, com atuação em Empresarial, Tributário, Trabalhista, Cível, Família & Sucessões e Previdenciário no Paraná, São Paulo e Santa Catarina.",
            "home", main)


def page_escritorio():
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("O Escritório", None))}
    <h1>Sobre o Gutmann &amp; Silva</h1>
    <p class="lead">Fundado em 1994, o Gutmann &amp; Silva Advogados Associados nasceu no Paraná com um propósito simples: oferecer assessoria jurídica séria, próxima e tecnicamente sólida para empresas e famílias. Ao longo de três décadas, esse propósito não mudou — o que mudou foi o tamanho da equipe e a amplitude das áreas que passamos a atender.</p>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap split">
    <h2>Nossa trajetória</h2>
    <div class="prose">
      <p>O escritório começou com uma atuação mais concentrada e, com o tempo, estruturou departamentos dedicados às áreas Empresarial, Cível, Trabalhista, Tributária, de Família &amp; Sucessões e Previdenciária. Essa especialização por área permite que cada cliente seja atendido por profissionais com domínio técnico específico sobre o tema em questão, sem perder a visão integrada que um escritório de porte médio consegue oferecer.</p>
      <p>Hoje, com sede em São José dos Pinhais, no Paraná, e registros ativos nas seccionais da OAB do Paraná, São Paulo e Santa Catarina, o Gutmann &amp; Silva atende clientes com operações que ultrapassam as fronteiras estaduais, mantendo o mesmo padrão de atendimento em qualquer frente.</p>
    </div>
  </div>
</section>

<section class="section section--light">
  <div class="wrap split">
    <h2>Nossa história</h2>
    <ol class="timeline">
      <li><span class="timeline__when">1994</span><p>Fundação do escritório no Paraná, com foco em atendimento próximo a empresas e famílias.</p></li>
      <li><span class="timeline__when">Ao longo dos anos</span><p>Expansão da atuação para São Paulo e Santa Catarina, com novos registros na OAB/SP e OAB/SC, e estruturação das áreas de especialização (Empresarial, Tributário, Trabalhista, Cível, Família &amp; Sucessões e Previdenciário), com a equipe crescendo para os atuais 30+ profissionais.</p></li>
      <li><span class="timeline__when">2022, 2024 e 2025</span><p>Eleito Melhor Escritório de Advocacia do Ano em São José dos Pinhais.</p></li>
      <li><span class="timeline__when">Hoje</span><p>30 anos de história, presença em três estados e reconhecimento consolidado no mercado jurídico paranaense.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head"><h2>Missão, visão e valores</h2></div>
    <div class="pillars">
      <div class="pillar"><span class="label">Propósito</span><p>Proporcionar verdadeira proteção jurídica e apresentar soluções que gerem segurança e credibilidade além do esperado.</p></div>
      <div class="pillar"><span class="label">Visão</span><p>Solucionar conflitos, construir relacionamentos de confiança e proporcionar um impacto positivo que torne o ambiente jurídico mais justo para todos.</p></div>
    </div>
    <ul class="values" aria-label="Valores">
      <li class="values__label label">Valores</li>
      <li>Ética</li><li>União</li><li>Comprometimento</li><li>Inovação</li><li>Respeito</li><li>Comunicação</li>
    </ul>
  </div>
</section>

<section class="section section--light">
  <div class="wrap stack">
    <div class="split">
      <h2>Como trabalhamos</h2>
      <div class="prose"><p>Antes de qualquer indicação jurídica, buscamos entender o contexto completo do cliente — seja uma empresa em expansão, uma família organizando sua sucessão ou um profissional com uma dúvida trabalhista ou previdenciária. Essa etapa de escuta é o que orienta cada estratégia que construímos.</p></div>
    </div>
    <div class="ethics">
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
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Áreas de Atuação", None))}
    <h1>Áreas de Atuação</h1>
  </div>
</section>
<section class="section section--light">
  <div class="wrap">{area_cards()}</div>
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
        destaque = f"""<div class="highlight">
        <span class="label">Destaque</span>
        <h3>{e(d['titulo'])}</h3>
        <p>{e(d['texto'])}</p>
        <div class="actions"><a class="btn btn--primary" href="contato.html">{e(d['cta'])}</a></div>
      </div>"""
    aside = "\n".join(
        f'<li><a href="{area_href(o)}"{CURRENT if o is a else ""}>{e(o["nome"])}</a></li>' for o in AREAS
    )
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Áreas de Atuação", "areas.html"), (a["titulo"], None))}
    <h1>{e(a['titulo'])}</h1>
    <p class="lead">{e(a['abertura'])}</p>
  </div>
</section>
<section class="section section--light">
  <div class="wrap area-layout">
    <div class="area-main">
      <div>
        <h2>O que fazemos nesta área</h2>
        <ul class="services">{itens}</ul>
      </div>
      {destaque}
      <div class="closing">
        <p>{e(a['fechamento'])}</p>
        <div class="actions"><a class="btn btn--primary" href="contato.html">{e(a['cta'])}</a></div>
      </div>
    </div>
    <nav class="aside-nav" aria-label="Áreas de Atuação">
      <span class="label">Áreas de Atuação</span>
      <ul>{aside}</ul>
    </nav>
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
        f"""<a class="post-card" href="blog-{p['slug']}.html" data-category="{p['area']}">
  <span class="label">{e(area_by_slug[p['area']]['nome'])}</span>
  <h3>{e(p['titulo'])}</h3>
  <p>{e(p['resumo'])}</p>
</a>"""
        for p in sorted(POSTS, key=lambda p: p["data"], reverse=True)
    )
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Blog", None))}
    <h1>Blog Gutmann &amp; Silva</h1>
    <p class="lead">Reunimos aqui orientações e atualizações sobre as áreas em que atuamos, organizadas para ajudar empresas e pessoas físicas a entender melhor seus direitos e obrigações. Nosso conteúdo é informativo — não substitui uma consulta jurídica personalizada.</p>
  </div>
</section>
<section class="section section--light">
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
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Blog", "blog.html"), (a["nome"], f"blog.html#{a['slug']}"))}
    <h1>{e(p['titulo'])}</h1>
  </div>
</section>
<section class="section section--light">
  <div class="wrap">
    <article class="article">{p['corpo']}</article>
    <div class="article-cta">
      <p>Precisa de orientação sobre este tema? Fale com nossa equipe.</p>
      <a class="btn btn--primary" href="contato.html">{e(a['cta'])}</a>
    </div>
  </div>
</section>"""
    return (f"{p['titulo']} | Gutmann & Silva Advogados", p["resumo"], "blog", main)


def page_equipe():
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Equipe", None))}
    <h1>Nossa Equipe</h1>
    <p class="lead">O Gutmann &amp; Silva reúne mais de 30 profissionais organizados por área de especialização, com registro na OAB em três estados: Paraná, São Paulo e Santa Catarina. À frente da condução jurídica, institucional e empresarial do escritório estão nossos sócios.</p>
  </div>
</section>
<section class="section section--light">
  <div class="wrap partners">
    <article class="partner">
      <div class="partner__monogram" aria-hidden="true">CG</div>
      <div class="partner__body">
        <h2>Celso Fernando Gutmann</h2>
        <span class="partner__role">Sócio fundador</span>
        <p>Formado pela PUC/PR (1995). Atua em Direito Cível, Trabalhista e Empresarial, com especialização em Direito Empresarial e Civil.</p>
        <ul class="oab"><li class="oab__label">Registros:</li><li>OAB/PR 21.713</li><li>OAB/SP 402.027</li></ul>
      </div>
    </article>
    <article class="partner">
      <div class="partner__monogram" aria-hidden="true">CS</div>
      <div class="partner__body">
        <h2>Cristiano da Silva</h2>
        <span class="partner__role">Sócio</span>
        <p>Graduado pela PUC/PR (2011), pós-graduado em Direito Civil e Processo Civil pela UNICURITIBA (2014), com atuação também em Legislação Tributária.</p>
        <ul class="oab"><li class="oab__label">Registros:</li><li>OAB/PR 60.125</li><li>OAB/SP 401.811</li></ul>
      </div>
    </article>
  </div>
</section>
{cta_final()}"""
    return ("Nossa Equipe | Gutmann & Silva Advogados",
            "Conheça os sócios fundadores do Gutmann & Silva Advogados Associados, à frente do escritório há 30 anos.",
            "equipe", main)


def page_contato():
    c = CONTATO
    main = f"""<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", HOME), ("Contato", None))}
    <h1>Fale com o Gutmann &amp; Silva</h1>
    <p class="lead">Estamos à disposição para entender sua situação e indicar o melhor caminho jurídico. Preencha o formulário abaixo ou utilize um dos canais de contato direto.</p>
  </div>
</section>
<section class="section section--light" id="formulario">
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
      <button class="btn btn--primary" type="submit">Enviar mensagem</button>
    </form>
    <dl class="channels">
      <div class="channel"><dt>Telefone</dt><dd><a href="{c['telefone_href']}">{c['telefone']}</a></dd></div>
      <div class="channel"><dt>WhatsApp</dt><dd><a href="{c['whatsapp_href']}" target="_blank" rel="noopener">{c['whatsapp']}</a></dd></div>
      <div class="channel"><dt>E-mail</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd></div>
      <div class="channel"><dt>Endereço</dt><dd>{e(c['endereco'])}</dd></div>
    </dl>
  </div>
</section>
<section class="section section--deep">
  <div class="wrap newsletter">
    <div class="stack">
      <h2>Fique por dentro</h2>
      <p class="lead">Cadastre-se para receber atualizações jurídicas relevantes para sua empresa ou sua família, direto na sua caixa de entrada.</p>
    </div>
    <form class="newsletter__form" data-form data-endpoint="{e(NEWSLETTER_ENDPOINT)}" data-success="Inscrição realizada." novalidate>
      <div class="newsletter__row">
        <div class="field"><label for="news-email">E-mail</label><input id="news-email" name="email" type="email" autocomplete="email" required></div>
        <button class="btn btn--primary" type="submit">Inscrever-se</button>
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
