// Canonical site chrome — triple-majority variant (auburn-township-oh/firewood-delivery):
// header CTA #quick-quote no-icon (62 pages), 529-char footer (88), '13 NE Ohio cities' utility bar (99).
// active-nav neutralized (re-added per page in Base); per-page JSON-LD excluded. Rendered via set:html.
export const HEADER_CHROME = `<div class="utility-bar">
<div class="container">
<div class="left">
<span><i class="fa-solid fa-phone"></i> <a href="tel:+14402948002">(440) 294-8002</a></span>
<span><i class="fa-solid fa-clock"></i> Extended hours · 24/7 emergency line</span>
<span><i class="fa-solid fa-tree"></i> Free estimates in 40-mile radius</span>
</div>
<div class="right"><a href="/service-areas/"><i class="fa-solid fa-map-pin"></i> Auburn Twp HQ — 13 NE Ohio cities</a></div>
</div>
</div>
<header class="header">
<div class="container">
<a class="header-logo" href="/"><img alt="Roubic Tree &amp; Landscape LLC" src="/brand_assets/ROUBIC TREE all BLUE.png"/></a>
<nav aria-label="Main navigation" class="nav">
<div class="nav-item has-mega">
<a href="/services/">Services</a>
<div class="mega mega-services" role="menu">
<div class="mega-cols">
<div class="mega-col">
<h4>Tree Removal</h4>
<ul>
<li><a class="hub-link" href="/services/tree-removal/">All Tree Removal →</a></li>
<li><a href="/services/tree-removal/residential-tree-removal/">Residential Removal</a></li>
<li><a href="/services/tree-removal/commercial-tree-removal/">Commercial Removal</a></li>
<li><a href="/services/tree-removal/emergency-tree-removal/">Emergency Removal</a></li>
<li><a href="/services/tree-removal/large-tree-removal/">Large-Tree Removal</a></li>
<li><a href="/services/tree-removal/dangerous-dead-tree-removal/">Dangerous/Dead Tree</a></li>
</ul>
</div>
<div class="mega-col">
<h4>Trimming &amp; Pruning</h4>
<ul>
<li><a class="hub-link" href="/services/tree-trimming-pruning/">All Trimming &amp; Pruning →</a></li>
<li><a href="/services/tree-trimming-pruning/crown-reduction/">Crown Reduction</a></li>
<li><a href="/services/tree-trimming-pruning/crown-thinning/">Crown Thinning</a></li>
<li><a href="/services/tree-trimming-pruning/deadwood-removal/">Deadwood Removal</a></li>
<li><a href="/services/tree-trimming-pruning/oak-tree-care/">Oak Tree Care</a></li>
<li><a href="/services/tree-trimming-pruning/maple-tree-maintenance/">Maple Maintenance</a></li>
</ul>
</div>
<div class="mega-col">
<h4>Grinding &amp; Clearing</h4>
<ul>
<li><a class="hub-link" href="/services/stump-grinding/">Stump Grinding →</a></li>
<li><a href="/services/stump-grinding/commercial-stump-grinding/">Commercial Grinding</a></li>
<li><a class="hub-link" href="/services/land-clearing/">Land Clearing →</a></li>
<li><a href="/services/land-clearing/lot-clearing/">Lot Clearing</a></li>
<li><a href="/services/land-clearing/brush-clearing/">Brush Clearing</a></li>
</ul>
</div>
</div>
</div>
</div>
<div class="nav-item has-mega">
<a href="/service-areas/">Service Areas</a>
<div class="mega" role="menu">
<div class="mega-cols">
<div class="mega-col">
<h4>Tier 1 — Priority Response</h4>
<ul>
<li><a href="/auburn-township-oh/">Auburn Township (HQ)</a></li>
<li><a href="/pepper-pike-oh/">Pepper Pike</a></li>
<li><a href="/chagrin-falls-oh/">Chagrin Falls</a></li>
<li><a href="/moreland-hills-oh/">Moreland Hills</a></li>
<li><a href="/solon-oh/">Solon</a></li>
</ul>
</div>
<div class="mega-col">
<h4>Tier 2 — 2-day</h4>
<ul>
<li><a href="/gates-mills-oh/">Gates Mills</a></li>
<li><a href="/beachwood-oh/">Beachwood</a></li>
<li><a href="/orange-oh/">Orange</a></li>
<li><a href="/bainbridge-township-oh/">Bainbridge Twp</a></li>
<li><a href="/shaker-heights-oh/">Shaker Heights</a></li>
</ul>
</div>
<div class="mega-col">
<h4>Tier 3</h4>
<ul>
<li><a href="/chesterland-oh/">Chesterland</a></li>
<li><a href="/mayfield-oh/">Mayfield</a></li>
<li><a href="/south-russell-oh/">South Russell</a></li>
<li><a class="hub-link" href="/service-areas/">All Service Areas →</a></li>
</ul>
</div>
</div>
</div>
</div>
<div class="nav-item has-mega">
<a href="/resources/">Resources</a>
<div class="mega" role="menu">
<div class="mega-cols" style="grid-template-columns: 1fr 1fr">
<div class="mega-col">
<h4>Guides</h4>
<ul>
<li><a class="hub-link" href="/blog/">Blog →</a></li>
<li><a href="/tree-service-cost-guide/">Tree Service Cost Guide</a></li>
<li><a href="/tree-removal-cost-guide/">Tree Removal Calculator</a></li>
<li><a href="/when-to-remove-tree/">When to Remove a Tree</a></li>
</ul>
</div>
<div class="mega-col">
<h4>Reference</h4>
<ul>
<li><a href="/storm-preparation-checklist/">Storm Preparation</a></li>
<li><a href="/arborist-guide/">Arborist's Guide</a></li>
<li><a href="/ohio-tree-species-guide/">Ohio Tree Species</a></li>
</ul>
</div>
</div>
</div>
</div>
<div class="nav-item"><a href="/about/">About</a></div>
<div class="nav-item"><a href="/contact/">Contact</a></div>
</nav>
<div class="header-cta">
<a class="header-phone" href="tel:+14402948002"><i class="fa-solid fa-phone"></i><span>(440) 294-8002</span></a>
<a class="btn btn-primary" data-shine="true" href="#quick-quote"><span>Get a Free Estimate</span></a>
<button class="mobile-toggle" onclick="document.getElementById('mobileMenu').classList.add('open')"><i class="fa-solid fa-bars"></i></button>
</div>
</div>
</header>
<div class="mobile-menu" id="mobileMenu">
<button aria-label="Close menu" class="mobile-menu-close" onclick="document.getElementById('mobileMenu').classList.remove('open')">
<i class="fa-solid fa-times"></i>
</button>
<details>
<summary>Services</summary>
<ul>
<li><a href="/services/tree-removal/">Tree Removal</a></li>
<li><a href="/services/tree-trimming-pruning/">Trimming &amp; Pruning</a></li>
<li><a href="/services/stump-grinding/">Stump Grinding</a></li>
<li><a href="/services/land-clearing/">Land Clearing</a></li>
<li><a href="/services/storm-damage-emergency/">Storm Damage &amp; Emergency</a></li>
<li><a href="/services/firewood-delivery/">Firewood Delivery</a></li>
</ul>
</details>
<details>
<summary>Service Areas</summary>
<ul>
<li><a href="/auburn-township-oh/">Auburn Township (HQ)</a></li>
<li><a href="/pepper-pike-oh/">Pepper Pike</a></li>
<li><a href="/chagrin-falls-oh/">Chagrin Falls</a></li>
<li><a href="/moreland-hills-oh/">Moreland Hills</a></li>
<li><a href="/solon-oh/">Solon</a></li>
<li><a href="/service-areas/">All 13 Cities →</a></li>
</ul>
</details>
<details>
<summary>Resources</summary>
<ul>
<li><a href="/blog/">Blog</a></li>
<li><a href="/tree-service-cost-guide/">Cost Guides</a></li>
<li><a href="/storm-preparation-checklist/">Storm Prep</a></li>
</ul>
</details>
<a href="/about/">About</a>
<a href="/contact/">Contact</a>
<div class="mobile-menu-ctas">
<a class="btn btn-secondary" href="tel:+14402948002" style="justify-content: center"><i class="fa-solid fa-phone"></i> Call (440) 294-8002</a>
<a class="btn btn-primary" data-shine="true" href="/contact/" style="justify-content: center"><span>Get a Free Estimate</span></a>
</div>
</div>`;

export const FOOTER_CHROME = `<footer class="footer">
<div class="container">
<div class="footer-top">
<div class="footer-brand">
<img alt="Roubic Tree &amp; Landscape LLC" src="/brand_assets/ROUBIC TREE ALL WHITE.png"/>
<p>Family-owned NE Ohio tree service since 1982. Two generations. One Auburn Township yard.</p>
<div class="footer-social">
<a aria-label="Facebook" href="#"><i class="fa-brands fa-facebook-f"></i></a>
<a aria-label="Instagram" href="#"><i class="fa-brands fa-instagram"></i></a>
<a aria-label="Google" href="#"><i class="fa-brands fa-google"></i></a>
<a aria-label="Angi" href="#"><i class="fa-solid fa-star"></i></a>
</div>
</div>
<div><h4>Services</h4><ul><li><a href="/services/tree-removal/">Tree Removal</a></li><li><a href="/services/tree-trimming-pruning/">Trimming</a></li><li><a href="/services/stump-grinding/">Stump Grinding</a></li><li><a href="/services/land-clearing/">Land Clearing</a></li><li><a href="/services/storm-damage-emergency/">Storm Damage</a></li><li><a href="/services/firewood-delivery/">Firewood</a></li></ul></div>
<div><h4>Service Areas</h4><ul><li><a href="/auburn-township-oh/">Auburn Township</a></li><li><a href="/pepper-pike-oh/">Pepper Pike</a></li><li><a href="/chagrin-falls-oh/">Chagrin Falls</a></li><li><a href="/moreland-hills-oh/">Moreland Hills</a></li><li><a href="/solon-oh/">Solon</a></li><li><a href="/service-areas/">All 13 Cities →</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/why-choose-us/">Why Choose Us</a></li><li><a href="/resources/">Resources</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul></div>
<div>
<h4>Contact</h4>
<ul class="footer-contact">
<li><i class="fa-solid fa-map-pin"></i>10840 Taylor May Rd<br/>Auburn Township, OH 44023</li>
<li><i class="fa-solid fa-phone"></i><a href="tel:+14402948002">(440) 294-8002</a></li>
<li><i class="fa-solid fa-clock"></i>Mon–Fri 7a–6p · 24/7 emergency</li>
</ul>
<div class="footer-cta"><a class="btn btn-primary" data-shine="true" href="#quick-quote"><span>Get a Free Estimate</span></a></div>
</div>
</div>
<div class="footer-bottom">
<div>© 1982–2026 Roubic Tree &amp; Landscape LLC · <a href="/privacy-policy/">Privacy</a> · <a href="/terms-and-conditions/">Terms</a> · <a href="/sitemap.xml">Sitemap</a></div>
<div class="powered">Powered by <strong>Efficiency Boss</strong></div>
</div>
</div>
</footer>
<div class="mobilebar">
<a class="btn btn-secondary" href="tel:+14402948002"><i class="fa-solid fa-phone"></i> Call Now</a>
<a class="btn btn-primary" data-shine="true" href="#quick-quote"><i class="fa-solid fa-calendar-check"></i><span>Get Estimate</span></a>
</div>
<div aria-modal="true" class="ghl-modal" id="ghlModal" role="dialog">
<div class="ghl-modal-inner">
<div class="ghl-modal-head">
<div><h3>Free Auburn Township Firewood Quote</h3><p>Aaron responds within 1 business day</p></div>
<button class="ghl-modal-close" onclick="closeGhlModal()" type="button"><i class="fa-solid fa-xmark"></i></button>
</div>
<div class="ghl-modal-body" id="ghlModalBody"></div>
</div>
</div>
<script>
  (function () {
    var modal = document.getElementById('ghlModal'), body = document.getElementById('ghlModalBody'), loaded = false;
    window.openGhlModal = function () {
      if (!loaded) {
        var f = document.createElement('iframe');
        f.src = 'https://link.efficiencyboss.com/widget/form/rBDRY0U64itnSpm4WsLU';
        f.title = 'Roubic Tree Website Form';
        body.appendChild(f);
        var s = document.createElement('script');
        s.src = 'https://link.efficiencyboss.com/js/form_embed.js';
        document.body.appendChild(s);
        loaded = true;
      }
      modal.classList.add('open'); document.body.classList.add('modal-open');
    };
    window.closeGhlModal = function () { modal.classList.remove('open'); document.body.classList.remove('modal-open') };
    modal.addEventListener('click', function (e) { if (e.target === modal) closeGhlModal() });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && modal.classList.contains('open')) closeGhlModal() });
    document.querySelectorAll('a[href="#quick-quote"], a[href$="#quick-quote"]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); openGhlModal() });
    });
  })();
</script>
<script data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js" data-widget-id="669159d923552246a5c498f8" src="https://widgets.leadconnectorhq.com/loader.js"></script>
<script>
/* v8.3 Mobile navigation contract — split-button accordion, one hub open at a time */
(function(){
  var hamburger = document.querySelector('.nav-hamburger, .mobile-toggle');
  var drawer = document.getElementById('mobile-drawer') || document.querySelector('.mobile-menu');
  if (hamburger && drawer) {
    hamburger.addEventListener('click', function(){
      var open = hamburger.getAttribute('aria-expanded') === 'true';
      hamburger.setAttribute('aria-expanded', String(!open));
      drawer.classList.toggle('open', !open);
    });
  }
  document.querySelectorAll('.submenu-toggle').forEach(function(btn){
    btn.addEventListener('click', function(){
      var item = btn.closest('.menu-item');
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.menu-item.open').forEach(function(openItem){
        if (openItem !== item) {
          openItem.classList.remove('open');
          var otherToggle = openItem.querySelector('.submenu-toggle');
          if (otherToggle) otherToggle.setAttribute('aria-expanded', 'false');
        }
      });
      item.classList.toggle('open', !wasOpen);
      btn.setAttribute('aria-expanded', String(!wasOpen));
    });
  });
})();
</script>`;
