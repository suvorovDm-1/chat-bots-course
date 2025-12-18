VENV_DIR = .venv
ACTIVATE_VENV := . $(VENV_DIR)/bin/activate

# Имя volume

TELEGRAM_BOT_IMAGE=sdmitrii/pizza-bot-repo
TELEGRAM_BOT_CONTAINER=telegram_pizza_bot

# Автоматически загружаем переменные из .env
include .env
export $(shell sed 's/=.*//' .env)

$(VENV_DIR):
	python3 -m venv $(VENV_DIR)
	$(ACTIVATE_VENV) && pip install --upgrade pip
	$(ACTIVATE_VENV) && pip install --requirement requirements.txt

install: $(VENV_DIR)

# Run black formatter
black: $(VENV_DIR)
	$(ACTIVATE_VENV) && black .

# Run ruff linter
ruff: $(VENV_DIR)
	$(ACTIVATE_VENV) && ruff check .

# Run all tests (includes black, ruff, and pytest)
test: black ruff

telegram_bot_build:
	docker build \
	  -t $(TELEGRAM_BOT_IMAGE) \
	  --platform linux/amd64,linux/arm64 \
	  -f Dockerfile \
	  .

telegram_bot_start:
	docker run -d \
	  --name $(TELEGRAM_BOT_CONTAINER) \
	  --restart unless-stopped \
	  -e TELEGRAM_TOKEN="$(TELEGRAM_TOKEN)" \
	  $(TELEGRAM_BOT_IMAGE)

telegram_bot_stop:
	docker stop $(TELEGRAM_BOT_CONTAINER)
	docker rm $(TELEGRAM_BOT_CONTAINER)

telegram_bot_push:
	docker push $(TELEGRAM_BOT_IMAGE)

logs:
	docker logs -f $(BOT_CONTAINER)