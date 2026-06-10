from __future__ import annotations

import json
import math
import textwrap
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.narutoonline.shop"
SITE_NAME = "Now Fakes"
TODAY = date(2026, 6, 10).isoformat()
ASSET_VERSION = "v20260610-seo-pagespeed"

WHATSAPP_ORDER = "https://wa.me/555384469263?text=Ol%C3%A1%21%20Quero%20fakes%20para%20Naruto%20Online%20e%20raspadinha."
WHATSAPP_GROUP = "https://chat.whatsapp.com/DGnnI9FYjaYGhU9y8veNuG"
DISCORD_URL = "https://discord.gg/UzGRDUgUwv"
FACEBOOK_URL = "https://facebook.com/groups/narutoonlinetrocas"
OFFICIAL_NARUTO_URL = "https://naruto.narutowebgame.com/pt/"


def clean(text: str) -> str:
    return textwrap.dedent(text).strip()


def write_file(relative_path: str, content: str) -> None:
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean(content) + "\n", encoding="utf-8", newline="\n")


def site_url(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return BASE_URL + path


def json_ld(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def asset_url(path: str) -> str:
    return site_url(path)


def local_asset(path: str) -> str:
    return f"{path}?v={ASSET_VERSION}"


def resize_webp(source: str, target: str, max_width: int, quality: int = 82) -> tuple[int, int]:
    src = ROOT / source
    dst = ROOT / target
    with Image.open(src) as image:
        image.load()
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "A" in image.mode else "RGB")
        width, height = image.size
        if width > max_width:
            new_height = math.floor(height * (max_width / width))
            image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        image.save(dst, "WEBP", quality=quality, method=6)
        return image.size


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, font_obj: ImageFont.ImageFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        next_line = f"{line} {word}".strip()
        bbox = draw.textbbox((0, 0), next_line, font=font_obj)
        if bbox[2] - bbox[0] <= max_width or not line:
            line = next_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def create_social_preview() -> None:
    target = ROOT / "now-fakes-social.webp"
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), "#050505")
    draw = ImageDraw.Draw(image)
    for y in range(height):
        red = int(10 + (y / height) * 45)
        draw.line((0, y, width, y), fill=(red, 8, 10))
    draw.rectangle((0, 0, width, height), outline="#e30613", width=8)

    logo_path = ROOT / "now-fakes-logo.webp"
    if logo_path.exists():
        with Image.open(logo_path) as logo:
            logo = logo.convert("RGBA").resize((250, 250), Image.Resampling.LANCZOS)
            image.paste(logo, (82, 188), logo)

    title_font = font(60, bold=True)
    subtitle_font = font(34, bold=False)
    kicker_font = font(28, bold=True)
    draw.text((388, 108), "NOW FAKES", fill="#ffffff", font=kicker_font)
    title_lines = wrap_text(draw, "Fakes para Naruto Online e raspadinha", 690, title_font)
    y = 165
    for line in title_lines[:3]:
        draw.text((388, y), line, fill="#ffffff", font=title_font)
        y += 68
    subtitle = "Pacotes, suporte e downloads para quem joga Naruto Online."
    for line in wrap_text(draw, subtitle, 690, subtitle_font)[:2]:
        draw.text((388, y + 8), line, fill="#fca5a5", font=subtitle_font)
        y += 42
    draw.rounded_rectangle((388, 492, 820, 552), radius=8, fill="#166534")
    draw.text((414, 506), "Pedido via WhatsApp", fill="#ffffff", font=font(28, bold=True))
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target, "WEBP", quality=86, method=6)


def build_assets() -> dict[str, tuple[int, int]]:
    sizes = {
        "/now-fakes-logo.webp": resize_webp("logosakai.avif", "now-fakes-logo.webp", 320, 86),
        "/now-fakes-logo-160.webp": resize_webp("logosakai.avif", "now-fakes-logo-160.webp", 160, 86),
        "/precos-br-1400.webp": resize_webp("Preços BR.png", "precos-br-1400.webp", 1400, 80),
        "/precos-br-thumb.webp": resize_webp("Preços BR.png", "precos-br-thumb.webp", 520, 72),
        "/precos-na-1400.webp": resize_webp("Preços NA.png", "precos-na-1400.webp", 1400, 80),
        "/precos-na-thumb.webp": resize_webp("Preços NA.png", "precos-na-thumb.webp", 520, 72),
        "/servicos-br-1400.webp": resize_webp("ServicosBR.jpg", "servicos-br-1400.webp", 1400, 82),
        "/servicos-br-thumb.webp": resize_webp("ServicosBR.jpg", "servicos-br-thumb.webp", 520, 74),
        "/servicos-na-1400.webp": resize_webp("ServicosNA.jpg", "servicos-na-1400.webp", 1400, 82),
        "/servicos-na-thumb.webp": resize_webp("ServicosNA.jpg", "servicos-na-thumb.webp", 520, 74),
        "/promo-fakes-br.webp": resize_webp("PROMO1.jpg", "promo-fakes-br.webp", 1400, 82),
        "/promo-fakes-br-thumb.webp": resize_webp("PROMO1.jpg", "promo-fakes-br-thumb.webp", 520, 74),
        "/promo-fakes-na.webp": resize_webp("PROMO2.jpg", "promo-fakes-na.webp", 1400, 82),
        "/promo-fakes-na-thumb.webp": resize_webp("PROMO2.jpg", "promo-fakes-na-thumb.webp", 520, 74),
    }
    create_social_preview()
    sizes["/now-fakes-social.webp"] = (1200, 630)
    return sizes


NAV_ITEMS = [
    ("Início", "/"),
    ("Fakes para raspadinha", "/#fakes-raspadinha"),
    ("Preços", "/#precos"),
    ("Jogar Naruto Online", "/jogar-naruto-online/"),
    ("Launcher", "/download-launcher-fakes/"),
    ("Sobre", "/sobre-nos/"),
]


def header() -> str:
    nav = "".join(f'<a href="{href}">{label}</a>' for label, href in NAV_ITEMS)
    return f"""
    <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
    <header class="site-header" id="topo">
      <div class="site-header__inner">
        <a class="brand" href="/" aria-label="Now Fakes - página inicial">
          <img src="{local_asset('/now-fakes-logo-160.webp')}" alt="Logo Now Fakes Naruto Online" width="160" height="160" fetchpriority="high" decoding="async">
          <span class="brand__text">
            <strong>Now Fakes</strong>
            <small>Naruto Online</small>
          </span>
        </a>
        <nav class="main-nav" aria-label="Navegação principal">
          {nav}
        </nav>
      </div>
    </header>
    """


def footer() -> str:
    return f"""
    <footer id="universal-footer" class="universal-footer" aria-label="Links institucionais">
      <div class="universal-footer__inner">
        <div class="universal-footer__hero">
          <span class="universal-footer__eyebrow">Links rápidos</span>
          <strong class="universal-footer__title">Now Fakes para Naruto Online</strong>
          <p class="universal-footer__text">Fakes para raspadinha, pedidos por região, downloads oficiais e suporte para jogar Naruto Online.</p>
          <a class="universal-footer__cta" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Falar no WhatsApp</a>
        </div>
        <div class="universal-footer__grid">
          <nav class="universal-footer__column" aria-label="Principal" data-label="Principal">
            <a class="universal-footer__link" href="/">Início</a>
            <a class="universal-footer__link" href="/jogar-naruto-online/">Jogar Naruto Online</a>
            <a class="universal-footer__link" href="/#fakes-raspadinha">Fakes para raspadinha</a>
            <a class="universal-footer__link" href="/#precos">Preços e serviços</a>
            <a class="universal-footer__link" href="/#faq">Perguntas frequentes</a>
          </nav>
          <nav class="universal-footer__column" aria-label="Downloads" data-label="Downloads">
            <a class="universal-footer__link" href="/download-launcher-fakes/">Launcher de Fakes</a>
            <a class="universal-footer__link" href="/download-launcher-trainer/">Launcher + Trainer</a>
          </nav>
          <nav class="universal-footer__column" aria-label="Suporte" data-label="Suporte">
            <a class="universal-footer__link" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Pedido no WhatsApp</a>
            <a class="universal-footer__link" href="{WHATSAPP_GROUP}" target="_blank" rel="noopener noreferrer">Grupo WhatsApp</a>
            <a class="universal-footer__link" href="{DISCORD_URL}" target="_blank" rel="noopener noreferrer">Comunidade no Discord</a>
          </nav>
          <nav class="universal-footer__column" aria-label="Institucional" data-label="Institucional">
            <a class="universal-footer__link" href="/sobre-nos/">Sobre a Now Fakes</a>
            <a class="universal-footer__link" href="/sitemap.xml">Sitemap XML</a>
            <a class="universal-footer__link" href="/robots.txt">Robots.txt</a>
          </nav>
        </div>
        <div class="universal-footer__bottom">
          <div class="universal-footer__socials" aria-label="Redes sociais">
            <a class="universal-footer__social-link universal-footer__social-link--whatsapp" href="{WHATSAPP_GROUP}" target="_blank" rel="noopener noreferrer" aria-label="Grupo WhatsApp">WA</a>
            <a class="universal-footer__social-link universal-footer__social-link--discord" href="{DISCORD_URL}" target="_blank" rel="noopener noreferrer" aria-label="Discord">DC</a>
            <a class="universal-footer__social-link universal-footer__social-link--facebook" href="{FACEBOOK_URL}" target="_blank" rel="noopener noreferrer" aria-label="Facebook">f</a>
          </div>
          <p class="universal-footer__copyline">Now Fakes - Atendimento oficial - 2026 - Todos os direitos reservados</p>
        </div>
      </div>
    </footer>
    """


def theme_button() -> str:
    return """
    <button id="theme-toggle" class="theme-toggle" type="button" aria-label="Alternar tema" aria-pressed="true" title="Alternar tema">
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path class="theme-toggle__path" d="M20.99 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 20.99 12.79Z"></path>
      </svg>
    </button>
    """


def modal_markup() -> str:
    return """
    <div id="image-modal" class="image-modal" hidden>
      <div class="image-modal__backdrop" data-modal-close></div>
      <div class="image-modal__dialog" role="dialog" aria-modal="true" aria-label="Imagem ampliada">
        <button class="image-modal__close" type="button" data-modal-close aria-label="Fechar imagem">×</button>
        <div id="image-modal-frame" class="image-modal__frame"></div>
      </div>
    </div>
    """


def whatsapp_float() -> str:
    return f"""
    <a id="whatsapp-float" class="whatsapp-float" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer" aria-label="Chamar a Now Fakes no WhatsApp" title="Chamar no WhatsApp">
      <span aria-hidden="true">WA</span>
    </a>
    """


def build_page(
    *,
    page_id: str,
    path: str,
    title: str,
    description: str,
    main: str,
    schema: dict,
    keywords: list[str],
    image: str = "/now-fakes-social.webp",
    robots: str = "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1",
    extra_script_src: str | None = None,
) -> str:
    canonical = site_url(path)
    image_abs = asset_url(image)
    keywords_content = ", ".join(keywords)
    theme_prepaint = """(function(){try{var r=document.documentElement,t="dark";try{t=localStorage.getItem("theme")||t}catch(e){}if(t!=="dark"&&t!=="light")t="dark";r.setAttribute("data-theme",t);r.style.colorScheme=t}catch(e){}})();"""
    extra_script_tag = f'\n      <script src="{local_asset(extra_script_src)}" defer></script>' if extra_script_src else ""
    return f"""<!DOCTYPE html>
    <html lang="pt-BR" data-page="{escape(page_id)}" data-theme="dark">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script id="nowfakes-theme-prepaint">{theme_prepaint}</script>
      <title>{escape(title)}</title>
      <meta name="title" content="{escape(title)}">
      <meta name="description" content="{escape(description)}">
      <meta name="keywords" content="{escape(keywords_content)}">
      <meta name="robots" content="{escape(robots)}">
      <meta name="author" content="Now Fakes Oficial">
      <meta name="publisher" content="Now Fakes">
      <meta name="theme-color" content="#E30613">
      <meta name="referrer" content="strict-origin-when-cross-origin">
      <link rel="canonical" href="{canonical}">
      <link rel="alternate" hreflang="pt-BR" href="{canonical}">
      <link rel="alternate" hreflang="x-default" href="{canonical}">
      <link rel="icon" type="image/webp" href="{local_asset('/now-fakes-logo-160.webp')}">
      <link rel="apple-touch-icon" href="{local_asset('/now-fakes-logo-160.webp')}">
      <link rel="preload" as="image" href="{local_asset('/now-fakes-logo-160.webp')}" type="image/webp" fetchpriority="high">
      <link rel="image_src" href="{image_abs}">
      <meta property="og:site_name" content="Now Fakes">
      <meta property="og:title" content="{escape(title)}">
      <meta property="og:description" content="{escape(description)}">
      <meta property="og:type" content="website">
      <meta property="og:locale" content="pt_BR">
      <meta property="og:url" content="{canonical}">
      <meta property="og:image" content="{image_abs}">
      <meta property="og:image:secure_url" content="{image_abs}">
      <meta property="og:image:type" content="image/webp">
      <meta property="og:image:width" content="1200">
      <meta property="og:image:height" content="630">
      <meta property="og:image:alt" content="{escape(title)}">
      <meta name="twitter:card" content="summary_large_image">
      <meta name="twitter:title" content="{escape(title)}">
      <meta name="twitter:description" content="{escape(description)}">
      <meta name="twitter:image" content="{image_abs}">
      <meta name="twitter:image:alt" content="{escape(title)}">
      <link rel="stylesheet" href="{local_asset('/styles.css')}">
      <script type="application/ld+json">{json_ld(schema)}</script>
      <script src="{local_asset('/script.js')}" defer></script>{extra_script_tag}
    </head>
    <body>
      <div class="site-shell">
        {header()}
        <main id="conteudo">
          {main}
        </main>
        {footer()}
      </div>
      {theme_button()}
      {whatsapp_float()}
      {modal_markup()}
    </body>
    </html>"""


def home_main(sizes: dict[str, tuple[int, int]]) -> str:
    gallery = [
        ("/precos-br-1400.webp", "/precos-br-thumb.webp", "Tabela de preços BR para fakes Naruto Online", "Tabela BR", "Pacotes de fakes para Naruto Online em real, com quantidade, nível e prazo para combinar o pedido."),
        ("/servicos-br-1400.webp", "/servicos-br-thumb.webp", "Tabela de serviços BR para Naruto Online", "Serviços BR", "Serviços extras para quem joga Naruto Online: fakes, apoio em eventos, amizade e organização por servidor."),
        ("/precos-na-1400.webp", "/precos-na-thumb.webp", "Tabela de preços NA para fakes Naruto Online", "Tabela NA", "Pacotes em dólar para Naruto Online NA, úteis para quem precisa de fakes por região ou servidor."),
        ("/servicos-na-1400.webp", "/servicos-na-thumb.webp", "Tabela de serviços NA para Naruto Online", "Serviços NA", "Serviços complementares para contas, eventos e rotina de Naruto Online na região NA."),
        ("/promo-fakes-br.webp", "/promo-fakes-br-thumb.webp", "Promoção de fakes para raspadinha no Naruto Online", "Promo BR", "Ofertas de fakes para raspadinha no Naruto Online com atendimento direto e conferência antes da entrega."),
        ("/promo-fakes-na.webp", "/promo-fakes-na-thumb.webp", "Oferta internacional de fakes para Naruto Online", "Promo NA", "Oferta para jogadores da região NA que buscam fakes para Naruto Online com suporte organizado."),
    ]
    gallery_cards = []
    for full_src, thumb_src, alt, title, text in gallery:
        width, height = sizes[thumb_src]
        gallery_cards.append(
            f"""
            <article class="media-card">
              <button class="media-card__image" type="button" data-modal-image="{local_asset(full_src)}" data-modal-alt="{escape(alt)}">
                <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" data-src="{local_asset(thumb_src)}" alt="{escape(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async" fetchpriority="low">
              </button>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
            """
        )

    return f"""
    <section class="hero hero--home">
      <div class="hero__content">
        <span class="section-kicker">Naruto Online, Sakai e raspadinha</span>
        <h1>Fakes para raspadinha no Naruto Online e fakes para Naruto Online com pedido organizado</h1>
        <p>Compre fakes para Naruto Online com atendimento direto, entrega combinada por região e suporte para quem quer jogar Naruto Online, participar de eventos e preparar contas para raspadinha.</p>
        <div class="hero-actions" aria-label="Ações principais">
          <a class="btn btn--primary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Pedir fakes no WhatsApp</a>
          <a class="btn btn--secondary" href="{DISCORD_URL}" target="_blank" rel="noopener noreferrer">Entrar no Discord</a>
        </div>
        <ul class="trust-list" aria-label="Diferenciais da Now Fakes">
          <li>Pacotes para BR, NA e servidores informados no pedido.</li>
          <li>Fakes nível 30 ou nível 40, com bônus combinado antes da entrega.</li>
          <li>Atendimento para raspadinha, eventos, amizade e rotina de Naruto Online.</li>
        </ul>
      </div>
      <aside class="offer-panel" aria-label="Oferta principal">
        <img src="{local_asset('/now-fakes-logo-160.webp')}" alt="Now Fakes Naruto Online" width="160" height="160" decoding="async">
        <strong>Oferta em destaque</strong>
        <p>200 fakes nível 40 para Naruto Online a partir de R$76 no BR ou US$17 na NA, com até 10% de bônus conforme o pedido.</p>
        <a class="btn btn--compact" href="#precos">Ver tabelas</a>
      </aside>
    </section>

    <section id="fakes-raspadinha" class="section-band">
      <div class="section-heading">
        <span class="section-kicker">Busca principal</span>
        <h2>Fakes para raspadinha no Naruto Online</h2>
        <p>Esta página foi estruturada para responder direto a quem procura fakes para raspadinha no Naruto Online, fakes para Naruto Online e formas práticas de jogar Naruto Online com contas organizadas por região.</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card">
          <h3>Fakes para raspadinha</h3>
          <p>Pacotes pensados para eventos de raspadinha, com quantidade definida, nível combinado e entrega em lista clara para facilitar o uso.</p>
        </article>
        <article class="feature-card">
          <h3>Fakes para Naruto Online</h3>
          <p>Contas preparadas para jogadores que precisam de volume, organização e suporte antes de fechar um pacote maior.</p>
        </article>
        <article class="feature-card">
          <h3>Jogar Naruto Online</h3>
          <p>Guia rápido para entrar no Naruto Online oficial, entender servidores, classes, launcher e organizar sua rotina de contas.</p>
          <a class="text-link" href="/jogar-naruto-online/">Abrir guia para jogar Naruto Online</a>
        </article>
      </div>
    </section>

    <section id="jogar-naruto-online" class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Naruto Online oficial</span>
        <h2>Jogar Naruto Online no navegador, com conta, servidor e launcher</h2>
        <p>O site oficial reúne registro, login, lista de servidores, notícias, eventos, tutorial, imagens, fórum e central de download. A Now Fakes organiza um guia simples para quem quer jogar Naruto Online e usar fakes com menos confusão.</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card">
          <h3>Registro e login</h3>
          <p>Crie ou acesse sua conta pelo portal oficial antes de escolher servidor, classe e rotina de jogo.</p>
        </article>
        <article class="feature-card">
          <h3>Servidores e eventos</h3>
          <p>Acompanhe aberturas de servidores, anúncios e eventos no site oficial para decidir onde usar suas fakes.</p>
        </article>
        <article class="feature-card">
          <h3>Classes e tutorial</h3>
          <p>Compare classes como Lâmina das Trevas, Olho das Chamas, Dançarina dos Ventos, Garra das Águas e Punho de Pedra.</p>
        </article>
      </div>
      <div class="section-actions">
        <a class="btn btn--primary" href="/jogar-naruto-online/">Ver guia completo</a>
        <a class="btn btn--secondary" href="{OFFICIAL_NARUTO_URL}" target="_blank" rel="noopener noreferrer">Abrir site oficial</a>
      </div>
    </section>

    <section id="precos" class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Preços e serviços</span>
        <h2>Tabelas de fakes, raspadinha e serviços Naruto Online</h2>
        <p>Abra as imagens para ver os valores em detalhe. Os nomes dos arquivos foram normalizados em WebP para carregar melhor e evitar quebra de imagem no servidor.</p>
      </div>
      <div class="media-gallery" data-gallery>
        <div class="gallery-track" data-gallery-track>
          {"".join(gallery_cards)}
        </div>
        <div class="gallery-controls">
          <button type="button" class="icon-button" data-gallery-prev aria-label="Tabela anterior">‹</button>
          <button type="button" class="icon-button" data-gallery-next aria-label="Próxima tabela">›</button>
        </div>
      </div>
    </section>

    <section id="como-pedir" class="section-band">
      <div class="section-heading">
        <span class="section-kicker">Pedido simples</span>
        <h2>Como comprar fakes para Naruto Online</h2>
      </div>
      <div class="steps">
        <article class="step-card">
          <span>1</span>
          <h3>Informe objetivo e região</h3>
          <p>Diga se quer fakes para raspadinha, evento, amizade ou outro uso, além da região e servidor do Naruto Online.</p>
        </article>
        <article class="step-card">
          <span>2</span>
          <h3>Confirme quantidade e nível</h3>
          <p>Escolha a quantidade de fakes, nível desejado, prazo e forma de receber a lista.</p>
        </article>
        <article class="step-card">
          <span>3</span>
          <h3>Receba suporte até a entrega</h3>
          <p>O atendimento acompanha o pedido e orienta sobre downloads, conferência e organização das fakes.</p>
        </article>
      </div>
    </section>

    <section id="downloads" class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Downloads oficiais</span>
        <h2>Ferramentas para fakes e Naruto Online</h2>
      </div>
      <div class="download-grid">
        <article class="download-card">
          <h3>Launcher de Fakes</h3>
          <p>Gerencie fakes, verifique níveis e organize várias contas em uma rotina mais simples.</p>
          <a class="btn btn--secondary" href="/download-launcher-fakes/">Abrir download</a>
        </article>
        <article class="download-card">
          <h3>Launcher Lite + Trainer</h3>
          <p>Página dedicada ao Launcher Lite Blue, tutorial e download oficial informado pela Now Fakes.</p>
          <a class="btn btn--secondary" href="/download-launcher-trainer/">Abrir download</a>
        </article>
      </div>
    </section>

    <section id="pedido-whatsapp" class="section-band">
      <div class="conversion-strip">
        <div>
          <span class="section-kicker">Conversão rápida</span>
          <h2>Quer fakes para Naruto Online sem perder tempo?</h2>
          <p>Envie servidor, região, quantidade e objetivo do pedido. O atendimento já responde com prazo, forma de pagamento e melhor pacote para raspadinha ou rotina de jogo.</p>
        </div>
        <a class="btn btn--primary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Pedir orçamento no WhatsApp</a>
      </div>
    </section>

    <section id="faq" class="section-band">
      <div class="section-heading">
        <span class="section-kicker">FAQ SEO</span>
        <h2>Perguntas frequentes sobre fakes Naruto Online</h2>
      </div>
      <div class="faq-list">
        <details open>
          <summary>O que são fakes para raspadinha no Naruto Online?</summary>
          <p>São contas auxiliares organizadas para participar de ações, eventos e rotinas de raspadinha no Naruto Online, conforme a região e o servidor informados pelo jogador.</p>
        </details>
        <details>
          <summary>A Now Fakes vende fakes para Naruto Online BR e NA?</summary>
          <p>Sim. A página mostra tabelas para BR e NA, além de suporte por WhatsApp ou Discord para confirmar servidor, quantidade, nível e prazo.</p>
        </details>
        <details>
          <summary>Como faço para jogar Naruto Online com suporte da Now Fakes?</summary>
          <p>Use os links de download e fale com o atendimento para organizar fakes, launcher e rotina de contas.</p>
        </details>
        <details>
          <summary>Qual é o prazo de entrega das fakes?</summary>
          <p>O prazo depende do nível e da quantidade. Como referência, fakes nível 30 costumam ter prazo menor que fakes nível 40, sempre confirmado no atendimento.</p>
        </details>
      </div>
    </section>

    <section id="avaliacoes" class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Prova social</span>
        <h2>Avaliações de clientes Now Fakes</h2>
      </div>
      <div class="testimonial-grid">
        <article class="testimonial-card">
          <h3>Lucas Fernandes</h3>
          <p>Recebi fakes extras e consegui organizar melhor meus eventos no Naruto Online. Atendimento rápido e pedido entregue antes do combinado.</p>
          <span>5/5</span>
        </article>
        <article class="testimonial-card">
          <h3>Gustavo Silva</h3>
          <p>O launcher facilitou minha rotina com fakes e o suporte ajudou na conferência da lista. Vou continuar comprando.</p>
          <span>5/5</span>
        </article>
        <article class="testimonial-card">
          <h3>Ana Costa</h3>
          <p>Comprei fakes para minha conta e recebi orientação clara sobre prazo, pagamento e entrega. Recomendo para Naruto Online.</p>
          <span>5/5</span>
        </article>
      </div>
    </section>
    """


def home_schema() -> dict:
    faqs = [
        ("O que são fakes para raspadinha no Naruto Online?", "São contas auxiliares organizadas para participar de ações, eventos e rotinas de raspadinha no Naruto Online, conforme a região e o servidor informados pelo jogador."),
        ("A Now Fakes vende fakes para Naruto Online BR e NA?", "Sim. A Now Fakes informa tabelas para BR e NA e confirma servidor, quantidade, nível e prazo por WhatsApp ou Discord."),
        ("Como faço para jogar Naruto Online com suporte da Now Fakes?", "Use os links de download e fale com o atendimento para organizar fakes, launcher e rotina de contas."),
        ("Qual é o prazo de entrega das fakes?", "O prazo depende do nível e da quantidade. Fakes nível 30 costumam ter prazo menor que fakes nível 40, sempre confirmado no atendimento."),
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": BASE_URL + "/",
                "inLanguage": "pt-BR",
            },
            {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": BASE_URL + "/",
                "logo": asset_url("/now-fakes-logo.webp"),
                "image": asset_url("/now-fakes-social.webp"),
                "sameAs": [DISCORD_URL, FACEBOOK_URL],
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "contactType": "sales",
                        "areaServed": ["BR", "NA"],
                        "availableLanguage": ["pt-BR", "en"],
                        "url": WHATSAPP_ORDER,
                    }
                ],
            },
            {
                "@type": "WebPage",
                "name": "Fakes para Naruto Online e raspadinha | Now Fakes",
                "url": BASE_URL + "/",
                "description": "Fakes para raspadinha no Naruto Online, fakes para Naruto Online e suporte para jogar Naruto Online com atendimento via WhatsApp e Discord.",
                "inLanguage": "pt-BR",
                "primaryImageOfPage": {"@type": "ImageObject", "url": asset_url("/now-fakes-social.webp"), "width": 1200, "height": 630},
                "keywords": ["fakes para raspadinha no Naruto Online", "fakes para Naruto Online", "jogar Naruto Online", "Sakai Naruto Online", "Now Fakes"],
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
            },
            {
                "@type": "Service",
                "name": "Fakes para raspadinha no Naruto Online",
                "serviceType": "Fakes para Naruto Online",
                "url": BASE_URL + "/#fakes-raspadinha",
                "provider": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
                "areaServed": ["BR", "NA"],
                "description": "Pacotes de fakes para Naruto Online, raspadinha, eventos e organização por servidor.",
                "offers": {"@type": "AggregateOffer", "priceCurrency": "BRL", "lowPrice": "76", "availability": "https://schema.org/InStock"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
                    for question, answer in faqs
                ],
            },
        ],
    }


def download_page(kind: str) -> tuple[str, str, str, dict, list[str]]:
    if kind == "fakes":
        title = "Download Launcher de Fakes para Naruto Online | Now Fakes"
        description = "Baixe o Launcher de Fakes da Now Fakes para gerenciar fakes no Naruto Online, verificar níveis, alterar senhas e organizar várias contas com mais facilidade."
        main = f"""
        <section class="hero hero--subpage">
          <div class="hero__content">
            <span class="section-kicker">Download seguro</span>
            <h1>Launcher de Fakes para Naruto Online</h1>
            <p>Ferramenta para organizar fakes no Naruto Online, verificar nível, alterar senha e usar várias contas com menos retrabalho.</p>
            <div class="hero-actions">
              <a class="btn btn--primary" href="https://www.mediafire.com/file/onyf8kgup7if5ov/Launcher_de_Fakes.zip/file" target="_blank" rel="noopener noreferrer">Baixar via MediaFire</a>
              <a class="btn btn--secondary" href="https://mega.nz/file/65QAXKrJ#bHjaVM84CdTUO2a_4So5CfW0X63j1jJKz_Vs2-cp6uY" target="_blank" rel="noopener noreferrer">Baixar via Mega</a>
            </div>
          </div>
        </section>
        <section class="section-band">
          <div class="section-heading">
            <span class="section-kicker">Funcionalidades</span>
            <h2>O que o Launcher de Fakes ajuda a fazer</h2>
          </div>
          <div class="feature-grid">
            <article class="feature-card"><h3>Gerenciar fakes</h3><p>Organize contas de Naruto Online em um fluxo único, com foco em velocidade e conferência.</p></article>
            <article class="feature-card"><h3>Verificar níveis</h3><p>Confira o nível das fakes antes de usar em raspadinha, evento ou rotina de jogo.</p></article>
            <article class="feature-card"><h3>Usar várias contas</h3><p>Facilite a abertura e acompanhamento de várias fakes na mesma rotina.</p></article>
          </div>
        </section>
        <section class="section-band section-band--alt">
          <div class="section-heading">
            <span class="section-kicker">Tutorial</span>
            <h2>Como usar o Launcher de Fakes</h2>
          </div>
          <div class="video-frame">
            <button class="video-placeholder" type="button" data-video-id="jKODmrmb3gw" data-video-title="Tutorial do Launcher de Fakes para Naruto Online">
              <span>Tutorial do Launcher de Fakes</span>
              <strong>Carregar vídeo</strong>
            </button>
          </div>
        </section>
        """
        schema_name = "Launcher de Fakes - Now Fakes"
        download_urls = [
            "https://www.mediafire.com/file/onyf8kgup7if5ov/Launcher_de_Fakes.zip/file",
            "https://mega.nz/file/65QAXKrJ#bHjaVM84CdTUO2a_4So5CfW0X63j1jJKz_Vs2-cp6uY",
        ]
        keywords = ["download launcher de fakes", "launcher de fakes Naruto Online", "gerenciar fakes Naruto Online", "fakes para Naruto Online"]
    else:
        title = "Launcher Lite Blue + Trainer para Naruto Online | Now Fakes"
        description = "Baixe o Launcher Lite Blue + Trainer para Naruto Online pela Now Fakes, com tutorial, link oficial e orientação para uso no Windows."
        main = f"""
        <section class="hero hero--subpage">
          <div class="hero__content">
            <span class="section-kicker">Launcher Lite Blue</span>
            <h1>Launcher Lite Blue + Trainer para Naruto Online</h1>
            <p>Página oficial da Now Fakes para acessar o Launcher Lite Blue + Trainer, tutorial e download informado para Naruto Online.</p>
            <div class="hero-actions">
              <a class="btn btn--primary" href="https://mega.nz/folder/ulhwQBhL#-VFoZGaHiC5F9fSnYJA3-Q" target="_blank" rel="noopener noreferrer">Baixar Launcher Lite + Trainer</a>
              <a class="btn btn--secondary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Tirar dúvida no WhatsApp</a>
            </div>
          </div>
        </section>
        <section class="section-band">
          <div class="section-heading">
            <span class="section-kicker">Antes de baixar</span>
            <h2>Orientações para Windows e Naruto Online</h2>
          </div>
          <div class="feature-grid">
            <article class="feature-card"><h3>Use links oficiais</h3><p>Baixe apenas pelos links desta página e confirme com o suporte se tiver dúvida sobre a origem do arquivo.</p></article>
            <article class="feature-card"><h3>Confira o tutorial</h3><p>Assista ao vídeo antes de executar o Launcher Lite Blue para entender o fluxo e evitar erro de uso.</p></article>
            <article class="feature-card"><h3>Suporte Now Fakes</h3><p>Fale com o atendimento caso o Windows bloqueie o arquivo ou o jogo não abra como esperado.</p></article>
          </div>
        </section>
        <section class="section-band section-band--alt">
          <div class="section-heading">
            <span class="section-kicker">Vídeo</span>
            <h2>Tutorial do Launcher Lite Blue + Trainer</h2>
          </div>
          <div class="video-frame">
            <button class="video-placeholder" type="button" data-video-id="MOoeSYd4mOM" data-video-title="Tutorial do Launcher Lite Blue + Trainer para Naruto Online">
              <span>Tutorial do Launcher Lite Blue + Trainer</span>
              <strong>Carregar vídeo</strong>
            </button>
          </div>
        </section>
        """
        schema_name = "Launcher Lite Blue + Trainer - Now Fakes"
        download_urls = ["https://mega.nz/folder/ulhwQBhL#-VFoZGaHiC5F9fSnYJA3-Q"]
        keywords = ["Launcher Lite Blue Naruto Online", "Trainer Naruto Online", "download launcher Naruto Online", "jogar Naruto Online"]

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "name": schema_name,
                "applicationCategory": "GameApplication",
                "operatingSystem": "Windows",
                "downloadUrl": download_urls,
                "author": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
                "description": description,
            },
            {
                "@type": "WebPage",
                "name": title,
                "url": site_url(f"/download-launcher-{kind}/" if kind == "fakes" else "/download-launcher-trainer/"),
                "description": description,
                "inLanguage": "pt-BR",
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
            },
        ],
    }
    return title, description, main, schema, keywords


def goku_main() -> str:
    return f"""
    <section class="hero hero--subpage">
      <div class="hero__content">
        <span class="section-kicker">Pedido por formulário</span>
        <h1>Goku Fakes para Naruto Online</h1>
        <p>Solicite fakes para Naruto Online informando quantidade, servidor, região e se deseja apoio para amizade ou raspadinha.</p>
      </div>
    </section>
    <section class="section-band">
      <div class="form-layout">
        <div class="section-heading section-heading--left">
          <span class="section-kicker">Pedido rápido</span>
          <h2>Enviar pedido de fakes no WhatsApp</h2>
          <p>Preencha os dados e a mensagem será montada automaticamente para atendimento do Goku Fakes.</p>
        </div>
        <form class="request-form" id="goku-fakes-form">
          <label for="qtdFakes">Quantidade de fakes</label>
          <input type="number" id="qtdFakes" name="qtdFakes" min="1" required inputmode="numeric">
          <label for="servidor">Servidor</label>
          <input type="text" id="servidor" name="servidor" required autocomplete="off">
          <label for="regiao">Região</label>
          <input type="text" id="regiao" name="regiao" required autocomplete="off">
          <label class="check-row" for="amizade">
            <input type="checkbox" id="amizade" name="amizade">
            <span>Adicionar amizade</span>
          </label>
          <label class="check-row" for="raspadinha">
            <input type="checkbox" id="raspadinha" name="raspadinha">
            <span>Fakes para raspadinha</span>
          </label>
          <button class="btn btn--primary" type="submit">Enviar pedido via WhatsApp</button>
        </form>
      </div>
    </section>
    <section class="section-band section-band--alt">
      <div class="feature-grid">
        <article class="feature-card"><h3>Pedido detalhado</h3><p>A mensagem já inclui quantidade, servidor, região, amizade e raspadinha.</p></article>
        <article class="feature-card"><h3>Foco em Naruto Online</h3><p>O formulário usa linguagem direta para jogadores que precisam de fakes para Naruto Online.</p></article>
        <article class="feature-card"><h3>Atendimento externo</h3><p>O pedido abre no WhatsApp informado para o Goku Fakes.</p></article>
      </div>
    </section>
    """


def divulgador_main() -> str:
    return """
    <section class="hero hero--subpage">
      <div class="hero__content">
        <span class="section-kicker">Ferramenta de apoio</span>
        <h1>Divulgador Naruto Online para criar contas e abrir servidor</h1>
        <p>Gere código de conta, copie nicks de apoio e abra links de cadastro, login e servidor em poucos cliques.</p>
      </div>
    </section>
    <section class="section-band">
      <div class="tool-layout" id="divulgador-tool">
        <div class="section-heading section-heading--left">
          <span class="section-kicker">Macro</span>
          <h2>Gerador rápido de links Naruto Online</h2>
          <p>Digite um código ou deixe vazio para gerar automaticamente. O código completo é copiado com região e servidor.</p>
        </div>
        <div class="tool-panel">
          <label for="codigoInput">Código base</label>
          <input type="text" id="codigoInput" placeholder="Digite um código ou deixe vazio" autocomplete="off">
          <div class="tool-actions" aria-label="Ações do divulgador">
            <button type="button" class="tool-button tool-button--red" data-divulgador-action="gerar">Gerar conta</button>
            <button type="button" class="tool-button tool-button--green" data-divulgador-action="nick1">Copiar nick 1</button>
            <button type="button" class="tool-button tool-button--green" data-divulgador-action="nick2">Copiar nick 2</button>
            <button type="button" class="tool-button tool-button--green" data-divulgador-action="nick3">Copiar nick 3</button>
            <button type="button" class="tool-button tool-button--green" data-divulgador-action="nick4">Copiar nick 4</button>
            <button type="button" class="tool-button tool-button--orange" data-divulgador-action="recall">Abrir recall</button>
          </div>
          <div class="generated-links" aria-live="polite">
            <div id="registroLink"></div>
            <div id="loginLink"></div>
            <div id="gameLink"></div>
          </div>
        </div>
      </div>
    </section>
    """


def about_main() -> str:
    return f"""
    <section class="hero hero--subpage">
      <div class="hero__content">
        <span class="section-kicker">Sobre a Now Fakes</span>
        <h1>Atendimento para fakes, raspadinha e Naruto Online</h1>
        <p>A Now Fakes reúne pacotes de fakes para Naruto Online, suporte para raspadinha, links de download e ferramentas para quem joga Naruto Online com rotina de várias contas.</p>
        <div class="hero-actions">
          <a class="btn btn--primary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Falar com atendimento</a>
          <a class="btn btn--secondary" href="/#precos">Ver preços</a>
        </div>
      </div>
    </section>
    <section class="section-band">
      <div class="feature-grid">
        <article class="feature-card"><h3>Foco no jogador</h3><p>Conteúdo direto para quem busca fakes para Naruto Online, jogar Naruto Online e organizar contas por servidor.</p></article>
        <article class="feature-card"><h3>SEO limpo</h3><p>O site usa canonicals, sitemap, dados estruturados e páginas internas alinhadas ao mesmo tema visual.</p></article>
        <article class="feature-card"><h3>Suporte centralizado</h3><p>WhatsApp, Discord e páginas de download ficam no mesmo footer e navegação.</p></article>
      </div>
    </section>
    """


def jogar_naruto_online_main() -> str:
    return f"""
    <section class="hero hero--subpage">
      <div class="hero__content">
        <span class="section-kicker">Guia independente</span>
        <h1>Jogar Naruto Online oficial: registro, servidores, launcher e classes</h1>
        <p>Guia rápido para quem quer jogar Naruto Online no navegador, encontrar o site oficial, entender a escolha de servidor e organizar fakes para eventos, raspadinha e rotina de jogo.</p>
        <div class="hero-actions">
          <a class="btn btn--primary" href="{OFFICIAL_NARUTO_URL}" target="_blank" rel="noopener noreferrer">Abrir Naruto Online oficial</a>
          <a class="btn btn--secondary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Pedir fakes no WhatsApp</a>
        </div>
      </div>
    </section>

    <section class="section-band">
      <div class="section-heading">
        <span class="section-kicker">Jogo do Naruto</span>
        <h2>O que procurar no site oficial do Naruto Online</h2>
        <p>O portal oficial do Naruto Online em português concentra áreas importantes para jogadores: notícias, eventos, anúncios, tutorial, iniciante, informações, imagens, fórum, SAC, launcher, registro, login e seleção de servidores.</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card">
          <h3>Registro e entrada rápida</h3>
          <p>Use o portal oficial para criar conta, recuperar senha, fazer login e escolher um servidor ativo antes de começar a jogar.</p>
        </article>
        <article class="feature-card">
          <h3>Servidores novos</h3>
          <p>Acompanhe anúncios e aberturas de servidores para decidir onde vale iniciar uma conta principal ou organizar fakes auxiliares.</p>
        </article>
        <article class="feature-card">
          <h3>Launcher e suporte</h3>
          <p>Consulte a central de download e os canais oficiais quando precisar de launcher, tutorial ou atendimento do próprio jogo.</p>
        </article>
      </div>
    </section>

    <section class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Classes Naruto Online</span>
        <h2>Classes para começar no Naruto Online</h2>
        <p>Antes de jogar Naruto Online, compare o estilo de cada classe. A escolha muda sua rotina de batalha, suporte e organização em eventos.</p>
      </div>
      <div class="feature-grid">
        <article class="feature-card"><h3>Lâmina das Trevas</h3><p>Classe ligada a espada e ninjutsu de relâmpago, boa para quem prefere pressão ofensiva.</p></article>
        <article class="feature-card"><h3>Olho das Chamas</h3><p>Classe de fogo e genjutsu, indicada para estratégias de controle e dano constante.</p></article>
        <article class="feature-card"><h3>Dançarina dos Ventos</h3><p>Classe de vento, útil para ataques em área e combinações rápidas com ninjas de suporte.</p></article>
        <article class="feature-card"><h3>Garra das Águas</h3><p>Classe com cura, veneno e estilo água, interessante para formações mais defensivas.</p></article>
        <article class="feature-card"><h3>Punho de Pedra</h3><p>Classe de terra e taijutsu, focada em resistência, defesa e presença na linha de frente.</p></article>
        <article class="feature-card"><h3>Fakes e eventos</h3><p>Depois de definir servidor e objetivo, a Now Fakes ajuda a organizar fakes para raspadinha, eventos e rotina de contas.</p></article>
      </div>
    </section>

    <section class="section-band">
      <div class="conversion-strip">
        <div>
          <span class="section-kicker">SEO + conversão</span>
          <h2>Quer jogar Naruto Online e preparar fakes para eventos?</h2>
          <p>Entre no site oficial para registro e servidor. Depois fale com a Now Fakes para combinar quantidade, nível, região e prazo das fakes.</p>
        </div>
        <a class="btn btn--primary" href="{WHATSAPP_ORDER}" target="_blank" rel="noopener noreferrer">Organizar fakes agora</a>
      </div>
    </section>

    <section class="section-band section-band--alt">
      <div class="section-heading">
        <span class="section-kicker">Perguntas frequentes</span>
        <h2>FAQ sobre jogar Naruto Online</h2>
      </div>
      <div class="faq-list">
        <details open>
          <summary>Onde jogar Naruto Online oficial?</summary>
          <p>O acesso deve ser feito pelo portal oficial em português, onde ficam registro, login, notícias, eventos, tutoriais, suporte e servidores.</p>
        </details>
        <details>
          <summary>O Naruto Online roda no navegador?</summary>
          <p>O portal oficial apresenta o jogo como RPG online para navegador e também mantém uma área de launcher e download para jogadores.</p>
        </details>
        <details>
          <summary>Fakes ajudam em que parte do Naruto Online?</summary>
          <p>Fakes podem ajudar em organização de eventos, raspadinha, testes por servidor e rotina de contas, sempre conforme o objetivo do jogador.</p>
        </details>
      </div>
    </section>
    """


def jogar_naruto_online_schema() -> dict:
    title = "Jogar Naruto Online Oficial: Registro, Launcher e Classes | Now Fakes"
    description = "Guia para jogar Naruto Online oficial em português, acessar registro, servidores, launcher, tutorial, classes e organizar fakes para eventos."
    faqs = [
        ("Onde jogar Naruto Online oficial?", "O acesso deve ser feito pelo portal oficial em português, onde ficam registro, login, notícias, eventos, tutoriais, suporte e servidores."),
        ("O Naruto Online roda no navegador?", "O portal oficial apresenta o jogo como RPG online para navegador e também mantém uma área de launcher e download para jogadores."),
        ("Fakes ajudam em que parte do Naruto Online?", "Fakes podem ajudar em organização de eventos, raspadinha, testes por servidor e rotina de contas, conforme o objetivo do jogador."),
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": title,
                "url": site_url("/jogar-naruto-online/"),
                "description": description,
                "inLanguage": "pt-BR",
                "about": {"@type": "VideoGame", "name": "Naruto Online", "url": OFFICIAL_NARUTO_URL},
                "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": BASE_URL + "/"},
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Jogar Naruto Online", "item": site_url("/jogar-naruto-online/")},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer}}
                    for question, answer in faqs
                ],
            },
        ],
    }


def generic_schema(title: str, description: str, path: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "name": title,
                "url": site_url(path),
                "description": description,
                "inLanguage": "pt-BR",
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE_URL + "/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": title, "item": site_url(path)},
                ],
            },
        ],
    }


def build_css() -> str:
    return """
    :root {
      --font-body: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, Arial, sans-serif;
      --red: #e30613;
      --red-dark: #8f0610;
      --gold: #ffd700;
      --green: #166534;
      --ink: #111827;
      --muted: #4b5563;
      --page: #f5f5f7;
      --surface: #ffffff;
      --surface-alt: #f8fafc;
      --line: rgba(227, 6, 19, 0.14);
      --shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
      --radius: 8px;
      color-scheme: light;
    }

    html[data-theme="dark"] {
      --ink: #f9fafb;
      --muted: #cbd5e1;
      --page: #090909;
      --surface: #151515;
      --surface-alt: #1f2937;
      --line: rgba(255, 255, 255, 0.12);
      --shadow: 0 14px 30px rgba(0, 0, 0, 0.28);
      color-scheme: dark;
    }

    *, *::before, *::after {
      box-sizing: border-box;
      letter-spacing: 0;
    }

    html {
      scroll-behavior: smooth;
      scrollbar-gutter: stable;
      -webkit-text-size-adjust: 100%;
      text-size-adjust: 100%;
    }

    body {
      margin: 0;
      font-family: var(--font-body);
      background: var(--page);
      color: var(--ink);
      line-height: 1.5;
      overflow-x: hidden;
    }

    img, iframe {
      max-width: 100%;
    }

    img {
      height: auto;
      display: block;
    }

    a {
      color: inherit;
    }

    a:focus-visible, button:focus-visible, input:focus-visible, summary:focus-visible {
      outline: 3px solid var(--gold);
      outline-offset: 3px;
    }

    .skip-link {
      position: absolute;
      left: 12px;
      top: 12px;
      z-index: 2000;
      transform: translateY(-160%);
      padding: 10px 14px;
      border-radius: var(--radius);
      background: #111;
      color: #fff;
      font-weight: 800;
      text-decoration: none;
    }

    .skip-link:focus {
      transform: translateY(0);
    }

    .site-shell {
      width: min(100%, 1240px);
      margin: 0 auto;
      background: var(--surface);
      min-height: 100vh;
      border-inline: 1px solid var(--line);
    }

    .site-header {
      background: linear-gradient(135deg, #43111c 0%, #1a0811 56%, #070405 100%);
      color: #fff;
      border-bottom: 3px solid var(--red);
    }

    .site-header__inner {
      min-height: 92px;
      padding: 14px 24px;
      display: grid;
      grid-template-columns: auto 1fr;
      align-items: center;
      gap: 18px;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
      color: #fff;
      text-decoration: none;
    }

    .brand img {
      width: 70px;
      height: 70px;
      object-fit: contain;
    }

    .brand__text {
      display: grid;
      line-height: 1.1;
      min-width: 0;
    }

    .brand__text strong {
      font-size: 1.25rem;
      font-weight: 900;
    }

    .brand__text small {
      color: rgba(255, 255, 255, 0.82);
      font-size: 0.9rem;
      font-weight: 700;
    }

    .main-nav {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 8px;
    }

    .main-nav a {
      min-height: 38px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 12px;
      border-radius: 999px;
      color: #fff;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 800;
      border: 1px solid rgba(255, 255, 255, 0.14);
      background: rgba(255, 255, 255, 0.06);
    }

    .main-nav a:hover {
      background: rgba(227, 6, 19, 0.38);
    }

    .hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(260px, 340px);
      gap: 28px;
      align-items: center;
      padding: 52px 28px;
      min-height: 420px;
      color: #fff;
      background:
        radial-gradient(circle at 82% 20%, rgba(227, 6, 19, 0.2), transparent 34%),
        linear-gradient(135deg, #43111c 0%, #1a0811 56%, #070405 100%);
      border-bottom: 1px solid var(--line);
    }

    .hero--subpage {
      grid-template-columns: 1fr;
      min-height: 300px;
    }

    .hero__content {
      width: min(100%, 820px);
      display: grid;
      gap: 18px;
    }

    .section-kicker {
      width: fit-content;
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(227, 6, 19, 0.16);
      color: #fecaca;
      border: 1px solid rgba(255, 255, 255, 0.14);
      font-size: 0.78rem;
      font-weight: 900;
      text-transform: uppercase;
    }

    .section-band .section-kicker {
      color: var(--red-dark);
      background: rgba(227, 6, 19, 0.08);
      border-color: rgba(227, 6, 19, 0.14);
    }

    html[data-theme="dark"] .section-band .section-kicker {
      color: #fecaca;
      background: rgba(227, 6, 19, 0.16);
      border-color: rgba(227, 6, 19, 0.28);
    }

    h1, h2, h3, p {
      margin-top: 0;
    }

    h1 {
      max-width: 20ch;
      margin-bottom: 0;
      font-size: 2.65rem;
      line-height: 1.08;
      font-weight: 900;
    }

    h2 {
      margin-bottom: 0;
      color: var(--ink);
      font-size: 1.85rem;
      line-height: 1.15;
      font-weight: 900;
    }

    h3 {
      margin-bottom: 6px;
      color: var(--ink);
      font-size: 1.18rem;
      line-height: 1.2;
      font-weight: 900;
    }

    .hero p {
      max-width: 68ch;
      margin-bottom: 0;
      color: rgba(255, 255, 255, 0.88);
      font-size: 1.08rem;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }

    .btn {
      min-height: 46px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 12px 16px;
      border: 0;
      border-radius: 999px;
      text-decoration: none;
      text-align: center;
      font-size: 0.95rem;
      font-weight: 900;
      line-height: 1.15;
      cursor: pointer;
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
      white-space: normal;
    }

    .btn--primary {
      background: linear-gradient(135deg, var(--red), var(--red-dark));
      color: #fff;
    }

    .btn--secondary {
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--line);
    }

    .btn--compact {
      min-height: 40px;
      padding-inline: 14px;
      background: #fff;
      color: #111827;
    }

    .trust-list {
      display: grid;
      gap: 8px;
      margin: 2px 0 0;
      padding: 0;
      list-style: none;
    }

    .trust-list li {
      position: relative;
      padding-left: 18px;
      color: rgba(255, 255, 255, 0.86);
    }

    .trust-list li::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0.65em;
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: var(--red);
    }

    .offer-panel {
      display: grid;
      gap: 12px;
      align-content: start;
      padding: 18px;
      border-radius: var(--radius);
      border: 1px solid rgba(255, 255, 255, 0.18);
      background: rgba(10, 10, 10, 0.72);
      box-shadow: var(--shadow);
    }

    .offer-panel img {
      width: 132px;
      height: 132px;
      object-fit: contain;
    }

    .offer-panel strong {
      font-size: 1.2rem;
    }

    .offer-panel p {
      margin: 0;
      color: rgba(255, 255, 255, 0.84);
    }

    .section-band {
      padding: 42px 28px;
      background: var(--surface);
    }

    .section-band--alt {
      background: var(--surface-alt);
    }

    .section-heading {
      width: min(100%, 860px);
      margin: 0 auto 22px;
      display: grid;
      justify-items: center;
      text-align: center;
      gap: 10px;
    }

    .section-heading--left {
      justify-items: start;
      text-align: left;
      margin: 0;
    }

    .section-heading p {
      max-width: 72ch;
      margin: 0;
      color: var(--muted);
    }

    .feature-grid, .download-grid, .testimonial-grid, .steps {
      width: min(100%, 1080px);
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .download-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .feature-card, .download-card, .testimonial-card, .step-card, .media-card {
      min-width: 0;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      box-shadow: var(--shadow);
    }

    .feature-card p, .download-card p, .testimonial-card p, .step-card p, .media-card p {
      margin-bottom: 0;
      color: var(--muted);
    }

    .text-link {
      width: fit-content;
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      margin-top: 12px;
      color: var(--red);
      font-weight: 900;
      text-decoration: none;
    }

    .text-link:hover {
      text-decoration: underline;
    }

    .section-actions {
      width: min(100%, 1080px);
      margin: 18px auto 0;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
    }

    .conversion-strip {
      width: min(100%, 980px);
      margin: 0 auto;
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 18px;
      align-items: center;
      padding: 20px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: linear-gradient(135deg, rgba(227, 6, 19, 0.16), var(--surface));
      box-shadow: var(--shadow);
    }

    .conversion-strip h2 {
      margin: 8px 0;
    }

    .conversion-strip p {
      margin: 0;
      color: var(--muted);
    }

    .step-card span {
      width: 34px;
      height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 12px;
      border-radius: 999px;
      background: var(--red);
      color: #fff;
      font-weight: 900;
    }

    .download-card {
      display: grid;
      gap: 10px;
      align-content: start;
    }

    .media-gallery {
      position: relative;
      width: min(100%, 1120px);
      margin: 0 auto;
    }

    .gallery-track {
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: minmax(280px, 360px);
      gap: 14px;
      overflow-x: auto;
      scroll-snap-type: x proximity;
      padding: 4px 4px 12px;
      scrollbar-width: thin;
    }

    .media-card {
      scroll-snap-align: start;
      display: grid;
      gap: 12px;
      align-content: start;
    }

    .media-card__image {
      width: 100%;
      aspect-ratio: 16 / 10;
      overflow: hidden;
      border: 0;
      border-radius: var(--radius);
      padding: 0;
      background: #111;
      cursor: zoom-in;
    }

    .media-card__image img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      background: #111;
      opacity: 1;
    }

    .media-card__image img[data-src] {
      opacity: 0;
    }

    .media-card__image img.is-loaded {
      opacity: 1;
    }

    .gallery-controls {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin-top: 12px;
    }

    .icon-button {
      width: 44px;
      height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--ink);
      font-size: 1.8rem;
      line-height: 1;
      cursor: pointer;
    }

    .faq-list {
      width: min(100%, 920px);
      margin: 0 auto;
      display: grid;
      gap: 10px;
    }

    details {
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      box-shadow: var(--shadow);
      overflow: hidden;
    }

    summary {
      min-height: 54px;
      padding: 16px;
      cursor: pointer;
      font-weight: 900;
    }

    details p {
      margin: 0;
      padding: 0 16px 16px;
      color: var(--muted);
    }

    .testimonial-card span {
      display: inline-flex;
      margin-top: 12px;
      color: var(--red);
      font-weight: 900;
    }

    .video-frame {
      width: min(100%, 920px);
      margin: 0 auto;
      aspect-ratio: 16 / 9;
      border-radius: var(--radius);
      overflow: hidden;
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      background: #111;
    }

    .video-frame iframe {
      width: 100%;
      height: 100%;
      display: block;
      border: 0;
    }

    .video-placeholder {
      width: 100%;
      height: 100%;
      display: grid;
      place-items: center;
      gap: 10px;
      padding: 20px;
      border: 0;
      background:
        radial-gradient(circle at 50% 28%, rgba(227, 6, 19, 0.2), transparent 34%),
        linear-gradient(135deg, #111827, #050505);
      color: #fff;
      text-align: center;
      cursor: pointer;
      font: inherit;
    }

    .video-placeholder span {
      font-weight: 900;
      font-size: 1.15rem;
    }

    .video-placeholder strong {
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 16px;
      border-radius: 999px;
      background: var(--red);
      color: #fff;
      font-size: 0.92rem;
    }

    .form-layout, .tool-layout {
      width: min(100%, 980px);
      margin: 0 auto;
      display: grid;
      grid-template-columns: minmax(0, 0.9fr) minmax(320px, 1.1fr);
      gap: 24px;
      align-items: start;
    }

    .request-form, .tool-panel {
      display: grid;
      gap: 10px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--surface);
      box-shadow: var(--shadow);
    }

    label {
      font-weight: 800;
      color: var(--ink);
    }

    input[type="text"], input[type="number"] {
      width: 100%;
      min-height: 44px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 0 12px;
      background: var(--surface-alt);
      color: var(--ink);
      font: inherit;
    }

    .check-row {
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 38px;
    }

    .check-row input {
      width: 18px;
      height: 18px;
      accent-color: var(--red);
    }

    .tool-actions {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }

    .tool-button {
      min-height: 42px;
      border: 0;
      border-radius: var(--radius);
      color: #fff;
      font-weight: 900;
      cursor: pointer;
    }

    .tool-button--red { background: #b91c1c; }
    .tool-button--green { background: #166534; }
    .tool-button--orange { background: #c2410c; }

    .generated-links {
      display: grid;
      gap: 8px;
      min-height: 54px;
      padding-top: 8px;
    }

    .generated-links a {
      min-height: 40px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 8px 10px;
      border-radius: var(--radius);
      background: var(--surface-alt);
      border: 1px solid var(--line);
      font-weight: 900;
      text-decoration: none;
    }

    .theme-toggle {
      position: fixed;
      top: 14px;
      right: 14px;
      z-index: 1200;
      width: 46px;
      height: 46px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: color-mix(in srgb, var(--surface) 92%, transparent);
      color: var(--ink);
      box-shadow: var(--shadow);
      cursor: pointer;
    }

    .theme-toggle svg {
      width: 20px;
      height: 20px;
      display: block;
      fill: none;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }

    .whatsapp-float {
      position: fixed;
      right: 14px;
      bottom: 14px;
      z-index: 1200;
      width: 52px;
      height: 52px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      background: #25d366;
      color: #fff;
      text-decoration: none;
      font-weight: 900;
      box-shadow: var(--shadow);
    }

    .universal-footer {
      display: block;
      width: 100%;
      clear: both;
      padding: 10px 15px 24px;
      background: var(--surface);
    }

    .universal-footer__inner {
      width: min(100%, 1200px);
      margin: 0 auto;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: linear-gradient(180deg, var(--surface), var(--surface-alt));
      box-shadow: var(--shadow);
      display: grid;
      gap: 14px;
      overflow: hidden;
    }

    .universal-footer__hero {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 6px 16px;
      align-items: center;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--line);
    }

    .universal-footer__eyebrow, .universal-footer__column::before {
      color: var(--red);
      font-size: 0.76rem;
      font-weight: 900;
      text-transform: uppercase;
    }

    .universal-footer__title {
      color: var(--ink);
      font-size: 1.25rem;
      line-height: 1.12;
    }

    .universal-footer__text, .universal-footer__copyline {
      margin: 0;
      color: var(--muted);
    }

    .universal-footer__cta {
      grid-column: 2;
      grid-row: 1 / 4;
      align-self: center;
      min-height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 14px;
      border-radius: 999px;
      background: var(--green);
      color: #fff;
      text-decoration: none;
      font-weight: 900;
      white-space: nowrap;
    }

    .universal-footer__grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
    }

    .universal-footer__column {
      display: grid;
      gap: 6px;
      align-content: start;
      min-width: 0;
      padding: 10px;
      border-radius: var(--radius);
      background: color-mix(in srgb, var(--surface) 72%, transparent);
      border: 1px solid var(--line);
    }

    .universal-footer__column::before {
      content: attr(data-label);
      display: block;
      margin-bottom: 2px;
    }

    .universal-footer__link {
      width: fit-content;
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      color: var(--ink);
      font-weight: 800;
      text-decoration: none;
      overflow-wrap: anywhere;
    }

    .universal-footer__link::before {
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: var(--red);
      box-shadow: 0 0 0 3px rgba(227, 6, 19, 0.08);
      flex: 0 0 auto;
    }

    .universal-footer__bottom {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px 16px;
    }

    .universal-footer__socials {
      display: inline-flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }

    .universal-footer__social-link {
      width: 44px;
      height: 44px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 999px;
      color: #fff;
      text-decoration: none;
      font-weight: 900;
      font-size: 0.8rem;
    }

    .universal-footer__social-link--whatsapp { background: #15803d; }
    .universal-footer__social-link--discord { background: #4f46e5; }
    .universal-footer__social-link--facebook { background: #1d4ed8; font-size: 1.35rem; }

    .image-modal[hidden] {
      display: none;
    }

    .image-modal {
      position: fixed;
      inset: 0;
      z-index: 2400;
      display: grid;
      place-items: center;
      padding: 18px;
    }

    .image-modal__backdrop {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.82);
    }

    .image-modal__dialog {
      position: relative;
      z-index: 1;
      width: min(100%, 1120px);
      max-height: 90vh;
      overflow: auto;
      border-radius: var(--radius);
      background: #111;
      border: 1px solid rgba(255, 255, 255, 0.14);
      box-shadow: 0 28px 80px rgba(0, 0, 0, 0.5);
    }

    .image-modal__dialog img {
      width: 100%;
      height: auto;
      object-fit: contain;
    }

    .image-modal__close {
      position: sticky;
      top: 8px;
      left: calc(100% - 52px);
      width: 44px;
      height: 44px;
      margin: 8px 8px -52px auto;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 0;
      border-radius: 999px;
      background: #b91c1c;
      color: #fff;
      font-size: 1.7rem;
      line-height: 1;
      cursor: pointer;
      z-index: 2;
    }

    @media (max-width: 900px) {
      .site-header__inner {
        grid-template-columns: 1fr;
      }

      .main-nav {
        justify-content: flex-start;
        overflow-x: auto;
        flex-wrap: nowrap;
        padding-bottom: 4px;
      }

      .main-nav a {
        flex: 0 0 auto;
      }

      .hero {
        grid-template-columns: 1fr;
      }

      .feature-grid, .download-grid, .testimonial-grid, .steps {
        grid-template-columns: 1fr;
      }

      .conversion-strip {
        grid-template-columns: 1fr;
      }

      .form-layout, .tool-layout {
        grid-template-columns: 1fr;
      }

      .universal-footer__grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 640px) {
      .site-shell {
        border-inline: 0;
      }

      .site-header__inner {
        padding: 12px 12px 14px;
      }

      .brand img {
        width: 56px;
        height: 56px;
      }

      h1 {
        max-width: 100%;
        font-size: 1.9rem;
      }

      h2 {
        font-size: 1.5rem;
      }

      .hero, .section-band {
        padding-inline: 14px;
      }

      .hero {
        min-height: auto;
        padding-block: 34px;
      }

      .hero--home {
        gap: 12px;
        padding-block: 24px;
      }

      .hero__content {
        gap: 12px;
      }

      .hero--home h1 {
        font-size: 1.55rem;
        line-height: 1.08;
      }

      .hero p {
        font-size: 0.98rem;
        line-height: 1.45;
      }

      .hero-actions {
        gap: 8px;
      }

      .btn {
        min-height: 42px;
        padding: 10px 13px;
        font-size: 0.88rem;
      }

      .trust-list {
        display: none;
      }

      .offer-panel {
        grid-template-columns: 56px 1fr;
        align-items: center;
        gap: 8px 10px;
        padding: 14px;
      }

      .offer-panel img {
        width: 56px;
        height: 56px;
        grid-row: 1 / span 3;
      }

      .offer-panel strong {
        font-size: 1rem;
      }

      .offer-panel p {
        font-size: 0.82rem;
        line-height: 1.35;
      }

      .offer-panel .btn {
        grid-column: 1 / -1;
        min-height: 36px;
      }

      .gallery-track {
        grid-auto-columns: minmax(260px, 86vw);
      }

      .tool-actions {
        grid-template-columns: 1fr;
      }

      .theme-toggle {
        top: 10px;
        right: 10px;
      }

      .universal-footer {
        padding: 10px;
      }

      .universal-footer__inner {
        padding: 14px;
      }

      .universal-footer__hero {
        grid-template-columns: 1fr;
      }

      .universal-footer__cta {
        grid-column: 1;
        grid-row: auto;
        width: 100%;
      }

      .universal-footer__grid {
        grid-template-columns: 1fr;
      }

      .universal-footer__bottom {
        display: grid;
        justify-items: start;
      }
    }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation: none !important;
        transition: none !important;
        scroll-behavior: auto !important;
      }
    }
    """


def build_js() -> str:
    return """
    (function () {
      "use strict";

      var sunPath = "M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10ZM12 1v3M12 20v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M1 12h3M20 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12";
      var moonPath = "M20.99 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 20.99 12.79Z";

      function setTheme(theme, persist) {
        var root = document.documentElement;
        theme = theme === "light" ? "light" : "dark";
        root.setAttribute("data-theme", theme);
        root.style.colorScheme = theme;
        if (persist) {
          try {
            localStorage.setItem("theme", theme);
          } catch (error) {}
        }
        var button = document.getElementById("theme-toggle");
        if (!button) return;
        button.setAttribute("aria-pressed", String(theme === "dark"));
        var path = button.querySelector(".theme-toggle__path");
        if (path) path.setAttribute("d", theme === "dark" ? moonPath : sunPath);
      }

      function initTheme() {
        var current = document.documentElement.getAttribute("data-theme") || "dark";
        setTheme(current, false);
        var button = document.getElementById("theme-toggle");
        if (!button) return;
        button.addEventListener("click", function () {
          var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
          setTheme(next, true);
        });
      }

      function initGallery() {
        document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
          var track = gallery.querySelector("[data-gallery-track]");
          if (!track) return;
          var amount = function () {
            return Math.max(280, Math.floor(track.clientWidth * 0.82));
          };
          var prev = gallery.querySelector("[data-gallery-prev]");
          var next = gallery.querySelector("[data-gallery-next]");
          if (prev) prev.addEventListener("click", function () { track.scrollBy({ left: -amount(), behavior: "smooth" }); });
          if (next) next.addEventListener("click", function () { track.scrollBy({ left: amount(), behavior: "smooth" }); });
        });
      }

      function initDeferredImages() {
        var images = Array.prototype.slice.call(document.querySelectorAll("img[data-src]"));
        if (!images.length) return;

        function loadImage(img) {
          if (!img || !img.dataset || !img.dataset.src) return;
          var src = img.dataset.src;
          delete img.dataset.src;
          img.addEventListener("load", function () {
            img.classList.add("is-loaded");
          }, { once: true });
          img.src = src;
          if (img.complete) img.classList.add("is-loaded");
        }

        if (!("IntersectionObserver" in window)) {
          setTimeout(function () {
            images.forEach(loadImage);
          }, 1200);
          return;
        }

        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            observer.unobserve(entry.target);
            loadImage(entry.target);
          });
        }, { rootMargin: "80px 0px", threshold: 0.01 });

        images.forEach(function (img) {
          observer.observe(img);
        });
      }

      function initVideoPlaceholders() {
        document.addEventListener("click", function (event) {
          var button = event.target.closest && event.target.closest(".video-placeholder[data-video-id]");
          if (!button) return;
          var videoId = button.getAttribute("data-video-id");
          var title = button.getAttribute("data-video-title") || "Vídeo tutorial";
          if (!videoId) return;
          var iframe = document.createElement("iframe");
          iframe.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(videoId) + "?autoplay=1&rel=0";
          iframe.title = title;
          iframe.loading = "lazy";
          iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
          iframe.allowFullscreen = true;
          button.replaceWith(iframe);
        });
      }

      function initImageModal() {
        var modal = document.getElementById("image-modal");
        var frame = document.getElementById("image-modal-frame");
        if (!modal || !frame) return;

        function close() {
          modal.hidden = true;
          frame.textContent = "";
          document.body.style.overflow = "";
        }

        document.addEventListener("click", function (event) {
          var opener = event.target.closest && event.target.closest("[data-modal-image]");
          if (opener) {
            var image = document.createElement("img");
            image.src = opener.getAttribute("data-modal-image");
            image.alt = opener.getAttribute("data-modal-alt") || "Imagem ampliada";
            image.width = 1200;
            image.height = 720;
            image.loading = "lazy";
            frame.replaceChildren(image);
            modal.hidden = false;
            document.body.style.overflow = "hidden";
          }
          if (event.target.closest && event.target.closest("[data-modal-close]")) {
            close();
          }
        });

        document.addEventListener("keydown", function (event) {
          if (event.key === "Escape" && !modal.hidden) close();
        });
      }

      document.addEventListener("DOMContentLoaded", function () {
        initTheme();
        initGallery();
        initDeferredImages();
        initVideoPlaceholders();
        initImageModal();
      });
    })();
    """


def build_hidden_tools_js() -> str:
    return """
    (function () {
      "use strict";

      function initGokuForm() {
        var form = document.getElementById("goku-fakes-form");
        if (!form) return;
        form.addEventListener("submit", function (event) {
          event.preventDefault();
          var qtd = document.getElementById("qtdFakes").value;
          var servidor = document.getElementById("servidor").value;
          var regiao = document.getElementById("regiao").value;
          var amizade = document.getElementById("amizade").checked ? "Sim" : "Não";
          var raspadinha = document.getElementById("raspadinha").checked ? "Sim" : "Não";
          var mensagem = "Olá! Quero solicitar " + qtd + " fake(s) no servidor " + servidor + ", região " + regiao + ". Serviço de adicionar amizade: " + amizade + ". Deseja mandar raspadinha: " + raspadinha + ".";
          window.open("https://wa.me/5521984295108?text=" + encodeURIComponent(mensagem), "_blank", "noopener,noreferrer");
        });
      }

      var servidores = [
        ["pt", "5"], ["pt", "20"], ["pt", "37"], ["pt", "61"], ["pt", "86"], ["pt", "121"], ["pt", "148"], ["pt", "184"],
        ["pt", "221"], ["pt", "250"], ["pt", "302"], ["pt", "332"], ["pt", "373"], ["pt", "413"], ["pt", "458"], ["pt", "503"],
        ["pt", "548"], ["pt", "593"], ["pt", "638"], ["pt", "653"], ["pt", "668"], ["pt", "683"], ["pt", "688"], ["pt", "693"],
        ["pt", "698"], ["pt", "713"], ["pt", "718"], ["pt", "728"], ["pt", "738"], ["pt", "743"], ["pt", "753"], ["pt", "758"],
        ["pt", "773"], ["pt", "778"], ["pt", "783"], ["pt", "788"], ["pt", "793"], ["pt", "798"], ["pt", "799"], ["pt", "800"],
        ["pt", "801"], ["pt", "802"], ["pt", "803"], ["pt", "804"], ["pt", "805"], ["pt", "806"], ["pt", "807"], ["pt", "808"],
        ["pt", "809"], ["pt", "810"], ["pt", "811"]
      ];

      function generateRandomCode(length) {
        var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        var code = "";
        for (var i = 0; i < length; i += 1) {
          code += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return code;
      }

      function copyText(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          return navigator.clipboard.writeText(text).then(function () { return true; }).catch(function () { return false; });
        }
        var textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.style.position = "fixed";
        textarea.style.opacity = "0";
        document.body.appendChild(textarea);
        textarea.select();
        var ok = false;
        try {
          ok = document.execCommand("copy");
        } catch (error) {
          ok = false;
        }
        document.body.removeChild(textarea);
        return Promise.resolve(ok);
      }

      function setLink(id, href, label, action) {
        var slot = document.getElementById(id);
        if (!slot) return;
        if (action === "popup") {
          slot.innerHTML = '<button class="tool-button tool-button--orange" type="button" data-open-popup="' + href + '">' + label + "</button>";
        } else {
          slot.innerHTML = '<a href="' + href + '" target="_blank" rel="noopener noreferrer">' + label + "</a>";
        }
      }

      function initDivulgador() {
        var tool = document.getElementById("divulgador-tool");
        if (!tool) return;
        var nicks = {
          nick1: "Kaze´Vex",
          nick2: "S130-Kazu",
          nick3: "S702-KhaLiL",
          nick4: "S773-Neljjz"
        };

        tool.addEventListener("click", function (event) {
          var popup = event.target.closest && event.target.closest("[data-open-popup]");
          if (popup) {
            window.open(popup.getAttribute("data-open-popup"), "_blank", "width=800,height=600,noopener,noreferrer");
            return;
          }

          var button = event.target.closest && event.target.closest("[data-divulgador-action]");
          if (!button) return;
          var action = button.getAttribute("data-divulgador-action");
          if (nicks[action]) {
            copyText(nicks[action]).then(function () {
              var oldText = button.textContent;
              button.textContent = "Nick copiado";
              setTimeout(function () { button.textContent = oldText; }, 1200);
            });
            return;
          }
          if (action === "recall") {
            window.open("https://narutorecall.oasgames.com/pt/return", "_blank", "width=800,height=600,noopener,noreferrer");
            return;
          }
          if (action !== "gerar") return;

          var input = document.getElementById("codigoInput");
          var codigo = input && input.value ? input.value.trim() : generateRandomCode(12);
          var servidor = servidores[Math.floor(Math.random() * servidores.length)];
          var codigoCompleto = codigo + "|" + servidor[1] + "|" + servidor[0];
          copyText(codigoCompleto);
          var registro = "https://passport.narutowebgame.com/index.php?m=register&email=" + encodeURIComponent(codigoCompleto) + "&pwd=080808";
          var login = "https://passport.narutowebgame.com/index.php?m=login&email=" + encodeURIComponent(codigoCompleto) + "&pwd=080808";
          var jogo = "https://naruto.narutowebgame.com/" + servidor[0] + "/serverlist/s" + servidor[1] + "?leftbar_collapse=yes&logintype=4";
          setLink("registroLink", registro, "Abrir cadastro gerado");
          setLink("loginLink", login, "Abrir login gerado");
          setLink("gameLink", jogo, "Abrir servidor " + servidor[1], "popup");
        });
      }

      document.addEventListener("DOMContentLoaded", function () {
        initGokuForm();
        initDivulgador();
      });
    })();
    """


def build_sitemap(paths: list[str]) -> str:
    urls = []
    for path in paths:
        priority = "1.0" if path == "/" else "0.82"
        urls.append(
            f"""
            <url>
              <loc>{site_url(path)}</loc>
              <lastmod>{TODAY}</lastmod>
              <changefreq>weekly</changefreq>
              <priority>{priority}</priority>
            </url>
            """
        )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      {"".join(urls)}
    </urlset>
    """


def main() -> None:
    sizes = build_assets()

    pages = [
        {
            "page_id": "home",
            "path": "/",
            "file": "index.html",
            "title": "Fakes para Naruto Online e Raspadinha | Now Fakes",
            "description": "Fakes para raspadinha no Naruto Online, fakes para Naruto Online e suporte para jogar Naruto Online com entrega organizada, WhatsApp e Discord.",
            "main": home_main(sizes),
            "schema": home_schema(),
            "keywords": ["fakes para raspadinha no Naruto Online", "fakes para Naruto Online", "jogar Naruto Online", "Sakai Naruto Online", "comprar fakes Naruto Online", "Now Fakes"],
            "indexed": True,
        }
    ]

    for kind, file_path, path in [
        ("fakes", "download-launcher-fakes/index.html", "/download-launcher-fakes/"),
        ("trainer", "download-launcher-trainer/index.html", "/download-launcher-trainer/"),
    ]:
        title, description, main_html, schema, keywords = download_page(kind)
        pages.append({"page_id": f"download-{kind}", "path": path, "file": file_path, "title": title, "description": description, "main": main_html, "schema": schema, "keywords": keywords, "indexed": True})

    jogar_title = "Jogar Naruto Online Oficial: Registro, Launcher e Classes | Now Fakes"
    jogar_description = "Guia para jogar Naruto Online oficial em português, acessar registro, servidores, launcher, tutorial, classes e organizar fakes para eventos."
    pages.append({
        "page_id": "jogar-naruto-online",
        "path": "/jogar-naruto-online/",
        "file": "jogar-naruto-online/index.html",
        "title": jogar_title,
        "description": jogar_description,
        "main": jogar_naruto_online_main(),
        "schema": jogar_naruto_online_schema(),
        "keywords": ["jogar Naruto Online", "Naruto Online oficial", "Jogo do Naruto", "RPG Naruto Online", "launcher Naruto Online", "classes Naruto Online"],
        "indexed": True,
    })

    goku_title = "Goku Fakes para Naruto Online e Raspadinha | Now Fakes"
    goku_description = "Formulário Goku Fakes para pedir fakes de Naruto Online por quantidade, servidor, região, amizade e raspadinha via WhatsApp."
    pages.append({
        "page_id": "gokufakes",
        "path": "/gokufakes/",
        "file": "gokufakes/index.html",
        "title": goku_title,
        "description": goku_description,
        "main": goku_main(),
        "schema": generic_schema(goku_title, goku_description, "/gokufakes/"),
        "keywords": ["Goku Fakes", "fakes para Naruto Online", "fakes para raspadinha", "pedido de fakes Naruto Online"],
        "indexed": False,
    })

    divulgador_title = "Divulgador Naruto Online e Macro de Contas | Now Fakes"
    divulgador_description = "Ferramenta divulgador para Naruto Online com geração de código, links de cadastro, login, servidor e cópia rápida de nicks."
    pages.append({
        "page_id": "divulgador",
        "path": "/divulgador/",
        "file": "divulgador/index.html",
        "title": divulgador_title,
        "description": divulgador_description,
        "main": divulgador_main(),
        "schema": generic_schema(divulgador_title, divulgador_description, "/divulgador/"),
        "keywords": ["divulgador Naruto Online", "macro criação de contas Naruto Online", "jogar Naruto Online", "fakes Naruto Online"],
        "indexed": False,
    })

    about_title = "Sobre a Now Fakes | Fakes para Naruto Online"
    about_description = "Conheça a Now Fakes, atendimento para fakes de Naruto Online, raspadinha, downloads e suporte para jogadores BR e NA."
    pages.append({
        "page_id": "sobre",
        "path": "/sobre-nos/",
        "file": "sobre-nos/index.html",
        "title": about_title,
        "description": about_description,
        "main": about_main(),
        "schema": generic_schema(about_title, about_description, "/sobre-nos/"),
        "keywords": ["Now Fakes", "sobre Now Fakes", "fakes Naruto Online", "fakes para raspadinha Naruto Online"],
        "indexed": True,
    })

    for page in pages:
        write_file(
            page["file"],
            build_page(
                page_id=page["page_id"],
                path=page["path"],
                title=page["title"],
                description=page["description"],
                main=page["main"],
                schema=page["schema"],
                keywords=page["keywords"],
                robots="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" if page.get("indexed", True) else "noindex,nofollow,noarchive",
                extra_script_src="/hidden-tools.js" if not page.get("indexed", True) else None,
            ),
        )

    write_file("styles.css", build_css())
    write_file("script.js", build_js())
    write_file("hidden-tools.js", build_hidden_tools_js())
    write_file(
        "robots.txt",
        f"""
        User-agent: *
        Allow: /

        Sitemap: {BASE_URL}/sitemap.xml
        """,
    )
    write_file(
        "llms.txt",
        f"""
        # Now Fakes

        Now Fakes é um site em português para jogadores de Naruto Online que procuram fakes para raspadinha no Naruto Online, fakes para Naruto Online, downloads de launcher e suporte por WhatsApp ou Discord.

        URL principal: {BASE_URL}/
        Principais páginas: /, /jogar-naruto-online/, /download-launcher-fakes/, /download-launcher-trainer/, /sobre-nos/
        Contato comercial: {WHATSAPP_ORDER}
        """,
    )
    write_file("sitemap.xml", build_sitemap([page["path"] for page in pages if page.get("indexed", True)]))
    write_file(
        "_redirects",
        """
        https://nowfakes.netlify.app/* https://www.narutoonline.shop/:splat 301!
        https://nowfakes7.netlify.app/* https://www.narutoonline.shop/:splat 301!
        /download-launcher-fakes /download-launcher-fakes/ 301
        /download-launcher-trainer /download-launcher-trainer/ 301
        /jogar-naruto-online /jogar-naruto-online/ 301
        /gokufakes /gokufakes/ 301
        /divulgador /divulgador/ 301
        /sobre-nos /sobre-nos/ 301
        /logo.png /now-fakes-logo.webp 301!
        /logosakai.avif /now-fakes-logo.webp 301!
        /Pre%C3%A7os%20BR.png /precos-br-1400.webp 301!
        /Pre%C3%A7os%20NA.png /precos-na-1400.webp 301!
        /ServicosBR.jpg /servicos-br-1400.webp 301!
        /ServicosNA.jpg /servicos-na-1400.webp 301!
        /servicosbr.jpg /servicos-br-1400.webp 301!
        /servicosna.jpg /servicos-na-1400.webp 301!
        /PROMO1.jpg /promo-fakes-br.webp 301!
        /PROMO2.jpg /promo-fakes-na.webp 301!
        /promo1.jpg /promo-fakes-br.webp 301!
        /promo2.jpg /promo-fakes-na.webp 301!
        """,
    )
    write_file(
        "_headers",
        """
        /*
          X-Content-Type-Options: nosniff
          Referrer-Policy: strict-origin-when-cross-origin
          Permissions-Policy: camera=(), microphone=(), geolocation=()

        /*.html
          Cache-Control: public, max-age=0, must-revalidate

        /styles.css
          Cache-Control: public, max-age=31536000, immutable

        /script.js
          Cache-Control: public, max-age=31536000, immutable

        /hidden-tools.js
          Cache-Control: public, max-age=31536000, immutable

        /*.webp
          Cache-Control: public, max-age=31536000, immutable

        /sitemap.xml
          Content-Type: application/xml; charset=utf-8
          Cache-Control: public, max-age=3600

        /robots.txt
          Content-Type: text/plain; charset=utf-8
          Cache-Control: public, max-age=3600

        /gokufakes/*
          X-Robots-Tag: noindex, nofollow, noarchive

        /divulgador/*
          X-Robots-Tag: noindex, nofollow, noarchive
        """,
    )
    write_file(
        ".netlifyignore",
        """
        # Source assets kept for local regeneration. Optimized WebP files are deployed instead.
        logo.png
        logosakai.avif
        Preços BR.png
        Preços NA.png
        ServicosBR.jpg
        ServicosNA.jpg
        PROMO1.jpg
        PROMO2.jpg

        # Local build tooling is not needed in the static deploy.
        tools/
        """,
    )

    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".txt", ".xml", ""}:
            try:
                data = path.read_bytes()
            except OSError:
                continue
            if data.startswith(b"\xef\xbb\xbf"):
                path.write_bytes(data[3:])

    print("Site reconstruído em UTF-8 sem BOM.")
    for page in pages:
        print(f"- {page['file']}")


if __name__ == "__main__":
    main()
