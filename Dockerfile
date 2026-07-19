FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN python -m pip install .
ENTRYPOINT ["python", "-m", "leakloom.cli"]
CMD ["analyze", "--gitleaks", "examples/gitleaks.json", "--trivy", "examples/trivy.json", "--git-log", "examples/git-log.json", "--artifacts", "examples/artifacts.json", "--workspace", "examples/current", "--html", "/tmp/report.html", "--json", "/tmp/report.json"]
