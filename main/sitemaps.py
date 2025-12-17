from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "tariffs",
            "contacts",
            "about",
            "why",
            "how",
            "documentation",
            "consumer",
            "contract_docs",
            "start",
            "complaints",
            "documentation_overview",
            "appeals",
        ]

    def location(self, item):
        return reverse(item)
