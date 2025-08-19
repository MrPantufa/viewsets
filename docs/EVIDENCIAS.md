# Exercício EBAC — ViewSets + DRF

- ViewSets criados: Tag, Technology, Project, ProjectLink, Experience, Education  
- Rotas registradas com DefaultRouter em `/api/`
- Testes: 12 passando  
  - CRUD de Tag (APITestCase)
  - Criação de Project com links aninhados + M2M
  - Validações de datas (Project/Experience/Education)

## Como rodar
pip install -r requirements.txt
python manage.py migrate
python manage.py test portfolio -v 2
python manage.py runserver  # http://127.0.0.1:8000/api/
