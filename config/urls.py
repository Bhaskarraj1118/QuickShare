
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def sitemap_xml(request):
    site_url = request.build_absolute_uri('/')

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{site_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>'''

    return HttpResponse(xml, content_type='application/xml')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clipboard.urls')),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
]
