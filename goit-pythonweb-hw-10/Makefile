ENTRYPOINT = main.py

add:
	git add .

commit:
	git commit -m "${name}"
push:
	git push origin main

compose:
	docker compose up -d

autogenerate:
	alembic revision --autogenerate -m "${name}"

head:
	alembic upgrade head

dev:
	fastapi dev main.py