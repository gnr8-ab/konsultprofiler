

{{ slogan }}
{{ summary }}

Expertis
{% for expertis in expertise %} · {{ expertis }} {% endfor %}
 
Urval av Uppdrag
{% for assignment in assignments %}
{{ assignment.main_role }}{% if assignment.other_roles and assignment.other_roles|length > 0 %} ({{ assignment.other_roles | join(', ') }}){% endif %}
{{ assignment.client }} ({{ assignment.period }})
{{ assignment.description }}

{% endfor %}

Utbildning
{% for education in educations %}  {{ education.institution }},  {{ education.focus }} ({{ education.period }}) {% endfor %}
Språk
{% for lang in languages %}  {{ lang.language }},  {{ lang.level }} {% endfor %}
Teknisk Kompetens
Teknologier	Metoder	Verktyg
{% for technology in technologies %} {{technology }}
{% endfor %}	{% for method in methods %} {{method }}
{% endfor %}	{% for tool in tools %} {{tool }}
{% endfor %}
Certifieringar
{% for certification in certifications %} {{ certification }} {% endfor %}
Kontaktuppgifter
E-post: {{ email }}
Telefon: {{ phone }}
Ort: {{ location }}


