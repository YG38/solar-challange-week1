# Solar Challenge Week 1

This project analyzes solar energy data from multiple countries to compare solar potential and identify key differences.

## Project Structure

```
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/solar-challenge-week1.git
   cd solar-challenge-week1
   ```

2. **Create and activate a conda environment**
   ```bash
   # Create a new conda environment
   conda create -n solar python=3.9
   conda activate solar
   
   # Or use an existing environment
   conda activate myenv
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package in development mode**
   ```bash
   pip install -e .
   ```

## Running the Analysis

1. **Jupyter Notebooks**
   ```bash
   jupyter notebook
   ```
   Then open the notebook in the `notebooks/` directory.

2. **Running tests**
   ```bash
   pytest
   ```

## Contributing

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

3. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
