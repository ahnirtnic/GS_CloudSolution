from flask import Flask, render_template
import pandas as pd
import chardet
import os

app = Flask(__name__)

# Caminho interno do CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "br_datahackers_state_data_microdados.csv")

def detect_encoding(path, nbytes=10000):
    """Detecta a codificação do CSV."""
    with open(path, "rb") as f:
        raw = f.read(nbytes)
    result = chardet.detect(raw)
    return result.get("encoding", "utf-8")

def load_csv(path):
    """Carrega CSV com detecção automática de encoding e separador."""
    encoding = detect_encoding(path)

    sample = open(path, encoding=encoding).read(2000)
    sep = "," if sample.count(",") >= sample.count(";") else ";"

    df = pd.read_csv(path, encoding=encoding, sep=sep)
    return df

@app.route("/")
def index():
    try:
        df = load_csv(CSV_PATH)
        table_html = df.head(200).to_html(
            classes="table table-striped", index=False
        )
        return render_template(
            "index.html",
            table_html=table_html,
            rows=len(df),
            columns=list(df.columns)
        )
    except Exception as e:
        return f"Erro ao carregar CSV: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
