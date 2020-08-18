set -e

FILE=${1:-"."}
EXTRA_ARG_BLACK=$2

echo -e "\033[1m\nRunning Format and checks on ${FILE}\033[0m"

echo -e "\033[1m\nRunning Black...\033[0m"
pipenv run black "$FILE"

echo -e "\033[1m\nRunning MyPy...\033[0m"
pipenv run mypy "$FILE"

echo -e "\033[1m\nRunning Flake8...\033[0m"
pipenv run flake8 "$FILE"

echo -e "\033[1m\nRunning Bandit...\033[0m"
pipenv run bandit -r --ini=".bandit" "$FILE"

if [ "$FILE" == "." ]; then
  echo -e "\033[1m\nRunning PyTest...\033[0m"
  pipenv run pytest

  echo -e "\033[1m\Checking migrations...\033[0m"
  pipenv run python manage.py makemigrations --check --dry-run
fi


echo -e "\033[1;32m\nFormat and checks successfully passed!\033[0m"