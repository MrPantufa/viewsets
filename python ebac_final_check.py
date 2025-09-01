# ebac_final_check.py
# Verifica estrutura, roda migrate/check/test, confere endpoints e faz E2E idempotente.

import os, sys, re, uuid, subprocess, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent
MANAGE = ROOT / "manage.py"

def die(msg, code=1):
    print(f"[ERRO] {msg}")
    sys.exit(code)

def run(cmd, log=None):
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=str(ROOT), text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout)
    if log:
        (ROOT / log).write_text(p.stdout, encoding="utf-8")
    return p.returncode

def detect_settings():
    txt = MANAGE.read_text(encoding="utf-8")
    m = re.search(r"DJANGO_SETTINGS_MODULE['\"]\s*,\s*['\"]([^'\"\s]+)['\"]", txt)
    if not m:
        die("Não achei DJANGO_SETTINGS_MODULE no manage.py", 2)
    return m.group(1)

def check_structure():
    ok = True
    if not MANAGE.exists():
        print(" - manage.py ausente"); ok = False
    if not (ROOT / "portfolio").exists():
        print(" - app 'portfolio' ausente"); ok = False
    vdir = ROOT / "portfolio" / "views"
    modular = all((vdir / x).exists() for x in
        ["__init__.py","tags.py","technologies.py","projects.py",
         "project_links.py","experiences.py","educations.py"])
    if modular:
        print(" + ViewSets modularizados (portfolio/views/*)")
    else:
        if (ROOT / "portfolio" / "views.py").exists():
            print(" ! ViewSets ainda centralizados em portfolio/views.py (ok para rodar, mas desalinhado ao feedback)")
        else:
            print(" - Nenhum views.py encontrado"); ok = False
    if not (ROOT / "pyproject.toml").exists():
        print(" ! pyproject.toml (Poetry) ausente (requisito do feedback)")
    return ok

def main():
    if not check_structure():
        die("Estrutura básica ausente")

    # Detecta settings pelo manage.py (sem depender de variáveis externas)
    settings = detect_settings()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)
    sys.path.insert(0, str(ROOT))

    # Migrate + check
    if run([sys.executable, "manage.py", "migrate", "--noinput"]) != 0:
        die("migrate falhou")
    if run([sys.executable, "manage.py", "check"]) != 0:
        die("django check falhou")

    # Testes do app
    if run([sys.executable, "manage.py", "test", "portfolio", "-v", "2"], log=".test-output.txt") != 0:
        die("Testes falharam (ver .test-output.txt)")

    # Endpoints + E2E com Client
    import django
    django.setup()
    from django.urls import reverse, NoReverseMatch
    from django.test import Client

    names = ["tag-list","technology-list","project-list","projectlink-list","experience-list","education-list"]
    c = Client()
    missing = []
    for nm in names:
        try:
            path = reverse(nm)
        except NoReverseMatch:
            missing.append(nm); continue
        r = c.get(path)
        print("GET", path, r.status_code)
        if r.status_code != 200:
            missing.append(nm)

    if missing:
        die(f"Endpoints ausentes/sem 200: {', '.join(missing)}", 3)

    # E2E idempotente (evita unicidade)
    def post(urlname, payload, expect=201):
        url = reverse(urlname)
        resp = c.post(url, data=json.dumps(payload), content_type="application/json")
        print("POST", url, "->", resp.status_code)
        if resp.status_code != expect:
            print(resp.content[:300])
            return False, None
        return True, resp.json()

    def patch(url, payload, expect=200):
        resp = c.patch(url, data=json.dumps(payload), content_type="application/json")
        return (resp.status_code == expect, (resp.json() if resp.content else None))

    suf = uuid.uuid4().hex[:8]
    ok, tag  = post("tag-list", {"name": f"web-{suf}"})
    ok2, tech = post("technology-list", {"name": f"django-{suf}"})
    if not (ok and ok2):
        die("Falha criando tag/technology", 4)

    payload = {
        "title": f"Site A {suf}", "slug": f"site-a-{suf}", "description": "desc",
        "started_at": "2024-01-01", "finished_at": "2024-01-31", "is_active": True,
        "tags": [tag["id"]], "technologies": [tech["id"]],
        "links": [{"label":"repo","url":"https://ex.com"},
                  {"label":"live","url":"https://ex2.com"}]
    }
    ok, proj = post("project-list", payload, 201)
    if not ok:
        die("Falha criando projeto com links", 5)

    assert len(proj.get("links", [])) == 2, "Projeto deve retornar 2 links"
    assert len(set(l["label"] for l in proj["links"])) == 2, "Labels de links devem ser únicas"
    assert len(proj.get("tags", [])) == 1 and len(proj.get("technologies", [])) == 1

    # validações 400
    ok, _ = post("project-list",
                 {"title":"X","slug": f"x-{suf}","started_at":"2024-05-02","finished_at":"2024-01-01"},
                 expect=400)
    assert ok, "Project com datas ruins deveria falhar (400)"
    ok, _ = post("experience-list",
                 {"role":"Dev","company":"ACME","started_at":"2025-01-10","finished_at":"2024-01-01"},
                 expect=400)
    assert ok, "Experience inválida deveria falhar (400)"
    ok, _ = post("education-list",
                 {"course":"CS","institution":"Uni","started_at":"2025-01-10","finished_at":"2024-01-01"},
                 expect=400)
    assert ok, "Education inválida deveria falhar (400)"

    # PATCH no projeto
    from django.urls import reverse
    detail = reverse("project-detail", args=[proj["id"]])
    ok, pj2 = patch(detail, {"title": f"Site A v2 {suf}"}, 200)
    assert ok and pj2.get("title") == f"Site A v2 {suf}", "PATCH project não atualizou o título"

    print("\n[OK] Tudo certo: Estrutura + migrate/check + testes + endpoints + E2E.")
    sys.exit(0)

if __name__ == "__main__":
    main()
