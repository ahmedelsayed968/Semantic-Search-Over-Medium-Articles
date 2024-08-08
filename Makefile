.PHONY: package-manager

package-manager:
	chmod +x scripts/package_manager.sh
	sudo ./scripts/package_manager.sh

.PHONY: dep
dep:
	pip install -r requirements.txt

.PHONY: run-app
run-app:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 5000