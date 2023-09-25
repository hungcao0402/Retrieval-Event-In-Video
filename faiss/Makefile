build_image:
	docker build -f deployment/Dockerfile -t faiss:latest .
faiss_up:
	bash deployment/deploy.sh run_faiss data/config.yaml 8051
