---
layout: default
---

# URL Debug Page

This page helps debug the correct URLs for the notebooks.

## Collection URLs to try:

1. **Using site.baseurl**: [Fine-tuning notebook]({{ site.baseurl }}/notebooks/01-basic-fine-tuning/)
2. **Using relative_url**: [Fine-tuning notebook]({{ '/notebooks/01-basic-fine-tuning/' | relative_url }})
3. **Direct relative**: [Fine-tuning notebook](./notebooks/01-basic-fine-tuning/)
4. **Collection item**: {% for notebook in site.notebooks %}{% if notebook.name == '01-basic-fine-tuning.md' %}[{{ notebook.title }}]({{ notebook.url | relative_url }}){% endif %}{% endfor %}

## All available notebooks:

{% for notebook in site.notebooks %}
- **[{{ notebook.title }}]({{ notebook.url | relative_url }})** ({{ notebook.difficulty }})
{% endfor %}

## Collection info:
- Collection name: {{ site.collections.notebooks.label }}
- Permalink: {{ site.collections.notebooks.permalink }}

---

**Note:** This is a debug page to help find the correct URLs. Once you find the working link format, you can update the home page accordingly.
