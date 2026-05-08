# Docker Usage

Mega Fintrade Quant Engine supports Docker runtime packaging for repeatable Python-based testing and analytics pipeline execution.

Docker is an additional runtime option. It does not replace the normal local Python virtual environment workflow.

The Docker setup allows the project to:

- Build a clean Python runtime image
- Install dependencies from `requirements.txt`
- Run the full `pytest` test suite inside Docker
- Run the analytics pipeline inside Docker
- Read processed C++ market engine outputs from `data/processed/`
- Write generated Java backend import files to `data/output/`
- Keep generated reports under `reports/`
- Make the project easier to run across macOS, Windows, Linux, GitHub Actions, and future cloud environments

---

## Docker Files

Docker-related files:

| File | Purpose |
|---|---|
| `Dockerfile` | Builds the Python quant engine image |
| `.dockerignore` | Keeps Docker build context clean |
| `docker-compose.yml` | Provides repeatable commands for tests and pipeline execution |
| `docs/docker-usage.md` | Documents Docker usage |

---

## Docker vs Python Virtual Environment

This project supports two development/runtime styles.

| Method | Purpose |
|---|---|
| `.venv` | Local Python development and quick testing |
| Docker | Portable test and runtime environment |

A Python virtual environment isolates Python packages on the local machine.

Docker isolates the Python runtime, operating system environment, installed dependencies, working directory, and execution command.

For local development, use:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 -m pytest
    python3 -m src.run_pipeline

For portable runtime testing, use:

    docker compose run --rm quant-engine-tests
    docker compose run --rm quant-engine-pipeline

Docker is the recommended option when you want to prove the project runs in a clean environment without relying on local Python installation details.

---

## Runtime Paths

The analytics pipeline uses these paths inside the container:

| Container path | Purpose |
|---|---|
| `/app/data/processed/cleaned_market_data.csv` | Cleaned market data from Project 3 C++ market engine |
| `/app/data/processed/daily_returns.csv` | Daily returns from Project 3 C++ market engine |
| `/app/data/output/strategy_signals.csv` | Strategy signals for Project 1 Java backend |
| `/app/data/output/backtest_results.csv` | Backtest results for Project 1 Java backend |
| `/app/data/output/risk_metrics.csv` | Risk metrics for Project 1 Java backend |
| `/app/data/output/portfolio_equity_curve.csv` | Portfolio equity curve for Project 1 Java backend |
| `/app/reports/` | Report and future chart output location |

Docker Compose mounts local folders into the container:

    ./data:/app/data
    ./reports:/app/reports

This means the container reads and writes directly through the local project folders.

Generated output files remain available after the container exits.

---

## Required Input Files

Before running the analytics pipeline, make sure these files exist:

    data/processed/cleaned_market_data.csv
    data/processed/daily_returns.csv

These files are produced by:

    mega-fintrade-market-engine-cpp

If Project 3 is stored beside Project 2 in the same parent folder, you can copy the files with:

    cp ../mega-fintrade-market-engine-cpp/data/output/cleaned_market_data.csv data/processed/cleaned_market_data.csv
    cp ../mega-fintrade-market-engine-cpp/data/output/daily_returns.csv data/processed/daily_returns.csv

If your repositories are stored in a different layout, adjust the relative path.

Also make sure the output and report folders exist:

    mkdir -p data/processed data/output reports

---

## Build Docker Image

From the project root, run:

    docker build -t mega-fintrade-quant-engine .

Expected image name:

    mega-fintrade-quant-engine:latest

Confirm the image exists:

    docker images | grep mega-fintrade-quant-engine

The image uses:

    python:3.12-slim

During the image build, Docker installs dependencies from:

    requirements.txt

Current main dependencies:

    pandas
    numpy
    yfinance
    matplotlib
    pytest

---

## Build Without Docker Cache

Use this when you want to confirm the image can be built from a clean state:

    docker build --no-cache -t mega-fintrade-quant-engine .

This takes longer because Python dependencies are installed again from scratch.

---

## Run Tests Inside Docker

Recommended Docker Compose command:

    docker compose run --rm quant-engine-tests

This runs:

    python -m pytest

inside the container.

Expected result:

    all tests pass

Direct Docker alternative:

    docker run --rm mega-fintrade-quant-engine python -m pytest

The Compose command is preferred because it matches the project’s documented runtime workflow.

---

## Run Analytics Pipeline Inside Docker

Recommended Docker Compose command:

    docker compose run --rm quant-engine-pipeline

This runs:

    python -m src.run_pipeline

inside the container.

Expected behavior:

- Read `data/processed/cleaned_market_data.csv`
- Read `data/processed/daily_returns.csv`
- Generate strategy signals
- Run backtests
- Calculate risk metrics
- Generate portfolio equity curve
- Write output CSV files to `data/output/`

Direct Docker alternative for macOS/Linux shell:

    docker run --rm \
      -v "$(pwd)/data:/app/data" \
      -v "$(pwd)/reports:/app/reports" \
      mega-fintrade-quant-engine python -m src.run_pipeline

For cross-platform documentation and normal use, prefer Docker Compose because volume syntax is simpler and more consistent.

---

## Verify Output Files

After running the pipeline, check:

    ls -lh data/output

Expected output files:

    strategy_signals.csv
    backtest_results.csv
    risk_metrics.csv
    portfolio_equity_curve.csv

Preview each file:

    head data/output/strategy_signals.csv
    head data/output/backtest_results.csv
    head data/output/risk_metrics.csv
    head data/output/portfolio_equity_curve.csv

Check line counts:

    wc -l data/output/strategy_signals.csv
    wc -l data/output/backtest_results.csv
    wc -l data/output/risk_metrics.csv
    wc -l data/output/portfolio_equity_curve.csv

Each file should normally contain more than one line because the first line is the header.

---

## Output Files for Java Backend

Project 2 generates these files for Project 1:

| File | Project 1 purpose |
|---|---|
| `data/output/strategy_signals.csv` | Strategy signal import |
| `data/output/backtest_results.csv` | Backtest result import |
| `data/output/risk_metrics.csv` | Risk metric import |
| `data/output/portfolio_equity_curve.csv` | Portfolio equity curve import |

These files are consumed by:

    mega-fintrade-backend-java

The Docker pipeline should produce the same output files as the local Python pipeline.

---

## Docker Compose Services

The Compose file defines these services:

| Service | Purpose |
|---|---|
| `quant-engine-tests` | Runs the pytest test suite |
| `quant-engine-pipeline` | Runs the analytics pipeline |

Common commands:

    docker compose run --rm quant-engine-tests
    docker compose run --rm quant-engine-pipeline

Clean up temporary Compose containers:

    docker compose down

---

## Local Python Workflow Still Works

Docker should not replace the local Python workflow.

Local setup:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Local tests:

    python3 -m pytest

Local pipeline:

    python3 -m src.run_pipeline

Docker is an additional packaging and reproducibility option.

---

## Cross-Platform Notes

Docker is practical for:

- macOS
- Windows
- Linux
- GitHub Actions
- future cloud deployment

Mobile devices such as iOS and Android are not normal Docker runtime targets.

For mobile usage, the correct design is:

    Run the Dockerized service on a computer, server, or cloud environment.
    Access dashboards or APIs from the mobile browser if needed.

For this Python quant engine, Docker is meant for development, CI, and backend runtime portability.

---

## Git Status Warning

Running the pipeline may generate or update files under:

    data/output/
    reports/

Do not automatically commit generated runtime files unless they are intentionally maintained as sample outputs.

Docker packaging files that should be committed:

    Dockerfile
    .dockerignore
    docker-compose.yml
    docs/docker-usage.md

---

## Troubleshooting

### Docker build fails during dependency installation

Run:

    docker build -t mega-fintrade-quant-engine .

Check the first Python or pip error.

Common causes:

- `requirements.txt` contains a package that cannot be installed
- Network connection issue during pip install
- Python version incompatibility
- Docker Desktop is not running

---

### Tests fail inside Docker

Run:

    docker compose run --rm quant-engine-tests

Common causes:

- Missing test data
- Import path issue
- Missing dependency
- Test depends on local-only files
- Test depends on live internet data

Tests should ideally be deterministic and should not depend on live market-data downloads.

---

### Pipeline cannot find processed input files

The pipeline requires:

    data/processed/cleaned_market_data.csv
    data/processed/daily_returns.csv

Check:

    ls -lh data/processed

If missing, copy Project 3 outputs:

    cp ../mega-fintrade-market-engine-cpp/data/output/cleaned_market_data.csv data/processed/cleaned_market_data.csv
    cp ../mega-fintrade-market-engine-cpp/data/output/daily_returns.csv data/processed/daily_returns.csv

Then rerun:

    docker compose run --rm quant-engine-pipeline

---

### Output files are not generated

Run:

    docker compose run --rm quant-engine-pipeline

Then check:

    ls -lh data/output

If files are missing, inspect the pipeline error output.

Also confirm that:

    data/processed/cleaned_market_data.csv
    data/processed/daily_returns.csv

exist and contain valid data.

---

### Reports are not generated

The `reports/` folder is mounted for future chart/report outputs.

If the current pipeline does not generate reports, an empty `reports/` folder is acceptable.

---

## Clean Docker Rebuild

Use this when Docker behavior seems stale:

    docker compose down
    docker build --no-cache -t mega-fintrade-quant-engine .
    docker compose run --rm quant-engine-tests
    docker compose run --rm quant-engine-pipeline

---

## Docker Design Notes

Docker design principles:

- Keep the local Python `.venv` workflow unchanged.
- Use Docker for portable test and runtime execution.
- Use `python:3.12-slim` as a clean Python runtime base.
- Install dependencies from `requirements.txt`.
- Mount `data/` so pipeline input and output files stay on the host.
- Mount `reports/` so reports remain on the host.
- Keep generated runtime files out of the image.
- Prefer Docker Compose commands for cross-platform usability.
- Keep Docker usage suitable for portfolio demonstration and future CI enhancement.