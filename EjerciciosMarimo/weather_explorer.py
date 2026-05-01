import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import requests
    from pathlib import Path

    return Path, mo, pd, px, requests


@app.cell
def _(mo):
    mo.md(r"""
    # Explorador Meteorologico

    Datos historicos de temperatura y precipitacion para cuatro ciudades europeas,
    obtenidos de [Open-Meteo](https://open-meteo.com/) — API gratuita y sin clave de acceso.

    Selecciona una ciudad y un periodo. Por defecto se usan **datos locales predescargados**;
    activa el interruptor para consultar la **API en tiempo real** (requiere conexion a internet).
    """)
    return


@app.cell
def _(mo):
    city_select = mo.ui.dropdown(
        options={"Madrid": "madrid", "Barcelona": "barcelona", "Paris": "paris", "Londres": "london"},
        value="Madrid",
        label="Ciudad",
    )
    period_select = mo.ui.dropdown(
        options=["Enero-Abril 2025", "Julio-Octubre 2024", "Todo 2024"],
        value="Enero-Abril 2025",
        label="Periodo",
    )
    use_api = mo.ui.switch(label="Usar API en tiempo real")
    mo.hstack([city_select, period_select, use_api], gap=2, justify="start")
    return city_select, period_select, use_api


@app.cell
def _(Path, city_select, mo, pd, period_select, requests, use_api):
    _CITIES = {
        "madrid":    {"lat": 40.4165,  "lon": -3.70256, "tz": "Europe/Madrid"},
        "barcelona": {"lat": 41.3888,  "lon":  2.15899, "tz": "Europe/Madrid"},
        "paris":     {"lat": 48.85341, "lon":  2.3488,  "tz": "Europe/Paris"},
        "london":    {"lat": 51.50853, "lon": -0.12574, "tz": "Europe/London"},
    }
    _PERIODS = {
        "Enero-Abril 2025":   ("2025-01-01", "2025-04-30"),
        "Julio-Octubre 2024": ("2024-07-01", "2024-10-31"),
        "Todo 2024":          ("2024-01-01", "2024-12-31"),
    }

    _city = city_select.value
    _start, _end = _PERIODS[period_select.value]

    _DATA_DIR = Path(__file__).parent / "data"

    if use_api.value:
        _info = _CITIES[_city]
        _url = (
            "https://archive-api.open-meteo.com/v1/archive"
            f"?latitude={_info['lat']}&longitude={_info['lon']}"
            f"&start_date={_start}&end_date={_end}"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone={_info['tz']}"
        )
        _resp = requests.get(_url, timeout=15)
        _resp.raise_for_status()
        _raw = _resp.json()["daily"]
        df = pd.DataFrame(_raw).rename(columns={
            "time":               "fecha",
            "temperature_2m_max": "temp_max",
            "temperature_2m_min": "temp_min",
            "precipitation_sum":  "precip_mm",
        })
    else:
        _file = _DATA_DIR / f"{_city}_weather.csv"
        if not _file.exists():
            mo.stop(
                True,
                mo.callout(
                    mo.md(f"Fichero local no encontrado: `{_file.name}`\n\n"
                          "Activa *Usar API en tiempo real* para descargar los datos."),
                    kind="danger",
                ),
            )
        _all = pd.read_csv(_file)
        df = _all[(_all["fecha"] >= _start) & (_all["fecha"] <= _end)].copy()

    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.dropna().reset_index(drop=True)
    return (df,)


@app.cell
def _(df, mo):
    _n = len(df)
    _start_d = df["fecha"].min().date() if _n else "-"
    _end_d = df["fecha"].max().date() if _n else "-"
    mo.md(
        f"**{_n} registros cargados** &nbsp;|&nbsp; "
        f"{_start_d} &rarr; {_end_d}"
    )
    return


@app.cell
def _(df, mo):
    _stats = (
        df[["temp_max", "temp_min", "precip_mm"]]
        .describe()
        .round(2)
        .reset_index()
        .rename(columns={"index": "estadistico", "temp_max": "temp_max (C)",
                         "temp_min": "temp_min (C)", "precip_mm": "precip (mm)"})
    )
    mo.md("## Resumen estadistico"), mo.ui.table(_stats)
    return


@app.cell
def _(city_select, df, px):
    _city_label = city_select.value.title()
    _fig = px.line(
        df,
        x="fecha",
        y=["temp_max", "temp_min"],
        title=f"Temperatura diaria — {_city_label}",
        labels={"value": "Temperatura (C)", "variable": "", "fecha": "Fecha"},
        color_discrete_map={"temp_max": "#e74c3c", "temp_min": "#3498db"},
    )
    _fig.update_layout(hovermode="x unified", legend_title_text="")
    _fig.for_each_trace(lambda t: t.update(
        name="Max" if t.name == "temp_max" else "Min"
    ))
    _fig
    return


@app.cell
def _(city_select, df, px):
    _city_label = city_select.value.title()
    _fig = px.bar(
        df,
        x="fecha",
        y="precip_mm",
        title=f"Precipitacion diaria — {_city_label}",
        color="precip_mm",
        color_continuous_scale="Blues",
        labels={"precip_mm": "Precipitacion (mm)", "fecha": "Fecha"},
    )
    _fig
    return


@app.cell
def _(df, mo):
    mo.md("## Tabla de datos"), mo.ui.table(df, pagination=True, page_size=15)
    return


if __name__ == "__main__":
    app.run()
