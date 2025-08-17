# another placeholder copied from previosu assignment-- fix this


# Define variables for the image name and tag
API_IMAGE := sentiment-api 
MONITOR_IMAGE := monitoring-app
create-volume:
	@docker volume inspect sentiment-logs >/dev/null 2>&1 || docker volume create sentiment-logs
build-api:
	@echo "Building Docker image: $(API_IMAGE)"
	docker build -t $(API_IMAGE) ./api

# run-api: create-volume
# 	@echo "Running Docker container..."
# 	docker run --rm -p 8000:8000 -v sentiment-logs:/logs $(API_IMAGE)
run-api:
	docker run --rm -p 8000:8000 -v "$(PWD)/logs:/logs" $(API_IMAGE)

build-monitor:
	@echo "Building Docker image: $(MONITOR_IMAGE)"
	docker build -t $(MONITOR_IMAGE) ./monitoring

# run-monitor: create-volume
# 	@echo "Running Docker container..."
# 	docker run --rm -p 8501:8501 -v sentiment-logs:/logs $(MONITOR_IMAGE)
run-monitor:
	docker run --rm -p 8501:8501 -v "$(PWD)/logs:/logs" $(MONITOR_IMAGE)


clean:
	@echo "Removing Docker images: $(API_IMAGE) $(MONITOR_IMAGE)"
	docker rmi $(API_IMAGE) $(MONITOR_IMAGE) || true

rebuild: clean build-api build-monitor

help:
	@echo "Available commands:"
	@echo "  make build-api    - Build the API Docker image"
	@echo "  make run-api      - Run the API Docker container"
	@echo "  make build-monitor   - Build the monitoring Docker image"
	@echo "  make run-monitor      - Run the monitoring Docker container"
	@echo "  make clean    - Remove the Docker image"
	@echo "  make rebuild  - Clean and rebuild both images"
