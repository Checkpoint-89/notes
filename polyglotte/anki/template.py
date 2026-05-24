FRONT_TEMPLATE_DE_FR = """\
<div class="word">{{Mot DE}}</div>
{{#Exemple DE}}<hr><div class="example">{{Exemple DE}}</div>{{/Exemple DE}}
"""

BACK_TEMPLATE_DE_FR = """\
{{FrontSide}}
<hr id="answer">
<div class="translation">{{Traduction FR}}</div>
{{#Exemple FR}}<div class="example fr">{{Exemple FR}}</div>{{/Exemple FR}}
"""

FRONT_TEMPLATE_FR_DE = (
    '<div class="translation">{{Traduction FR}}</div>'
    '{{#Exemple FR}}<hr><div class="example fr">{{Exemple FR}}</div>{{/Exemple FR}}'
)

BACK_TEMPLATE_FR_DE = (
    "{{FrontSide}}"
    '<hr id="answer">'
    '<div class="word">{{Mot DE}}</div>'
    '{{#Exemple DE}}<div class="example">{{Exemple DE}}</div>{{/Exemple DE}}'
)

CSS_LIGHT = """\
.card {
  font-family: "Georgia", serif;
  font-size: 20px;
  text-align: center;
  color: #1a1a2e;
  background: #f9f6f0;
}
.word {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}
.example {
  font-style: italic;
  color: #555;
  font-size: 17px;
}
.translation {
  font-size: 24px;
  font-weight: bold;
  margin: 12px 0 6px;
  color: #16213e;
}
.fr {
  color: #444;
}
hr { border-color: #ccc; }
"""

CSS_DARK = """\
.card {
  font-family: "Georgia", serif;
  font-size: 20px;
  text-align: center;
  color: #e0d8c8;
  background: #1e1e2e;
}
.word {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #fdf6e3;
}
.example {
  font-style: italic;
  color: #c8bfa8;
  font-size: 17px;
}
.translation {
  font-size: 24px;
  font-weight: bold;
  margin: 12px 0 6px;
  color: #f5ead5;
}
.fr {
  color: #bdb5a0;
}
hr { border-color: #45475a; }
"""
