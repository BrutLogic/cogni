.# Installation

## Prerequisites
- Python 3.8+
- pip
- git

## Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cogni.git
cd cogni
```

2. Install using pip:
```bash
pip install -e .
```

3. Verify installation:
```bash
python -c "import cogni; print(cogni.__version__)"
```

## Development Setup

For development, you'll also want to install test dependencies:

```bash
pip install -r requirements.txt
```

Run tests to verify everything is working:
```bash
pytest tests/
```
