# Comandos Git Útiles (Cheatsheet)

## Ramas
git branch                  # Listar ramas locales
git branch -a                # Listar todas (incluidas remotas)
git checkout -b nombre-rama  # Crear y cambiar a rama
git switch -c nombre-rama    # Alternativa moderna

## Commits
git status
git add .
git commit -m "tipo: descripción"
git log --oneline --graph    # Ver historial bonito

## Sincronización
git pull origin main
git push origin nombre-rama
git fetch --all

## Merge
git checkout main
git merge nombre-rama
git branch -d nombre-rama    # Eliminar rama local

## Stash (guardar cambios temporales)
git stash push -m "descripción"
git stash list
git stash pop

## Convención de Commits
feat: nueva funcionalidad
fix: corrección de bug
docs: documentación
style: formato, espacios, puntos y comas (no afecta código)
refactor: refactorización de código
test: agregar o corregir tests
chore: tareas de mantenimiento, configuración
