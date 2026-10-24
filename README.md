# Datheon Python Tasks

A beginner-friendly Python portfolio containing four console/utility projects.

## Projects

1. **Hangman Word Guessing Game** — letter-by-letter guessing, six incorrect attempts, ASCII stages, and duplicate-guess protection.
2. **Stock Portfolio Performance Tracker** — fetches quotes with `yfinance`, calculates portfolio value and P/L, and appends timestamped snapshots to CSV.
3. **Automated File Organizer & Cleanup Utility** — organizes files by extension and offers a dry-run mode before making changes.
4. **Rule-Based Interactive Terminal Assistant** — menu-driven chatbot with simple intent recognition.

## Requirements

- Python 3.10 or newer recommended.
- Tasks 1, 3, and 4 use only the Python standard library.
- Task 2 uses `yfinance` for market quotes.

Install the optional Task 2 dependency:

```bash
python -m pip install -r task2_stock_tracker/requirements.txt
```

## Run each task

From the repository root:

```bash
python task1_hangman/hangman.py
python task2_stock_tracker/stock_tracker.py
python task3_file_organizer/file_organizer.py
python task4_terminal_assistant/assistant.py
```

### Task 2 usage

Edit `HOLDINGS` near the top of `stock_tracker.py` to match your own tickers and share quantities. The included holdings are examples, not investment recommendations. Quote availability depends on the data provider and internet access. The program writes snapshots to `portfolio_log.csv` in the current working directory.

### Task 3 safety

The organizer defaults to **dry-run mode** so you can review proposed moves first. Set `DRY_RUN = False` only after checking the source folder and preview. It does not delete files; it sorts files into folders by extension.

## GitHub upload

1. Create a new **public** repository on GitHub, e.g. `datheon-python-tasks`.
2. Extract this ZIP and open the extracted folder in VS Code.
3. Open the VS Code terminal in the repository root and run:

```bash
git init
git add .
git commit -m "Add four Datheon Python tasks"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/datheon-python-tasks.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not upload passwords, API keys, or private data.
