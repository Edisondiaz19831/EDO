from flask import Flask, render_template, request, url_for
import math

app = Flask(__name__)

G_DEF = 9.8

@app.route("/", methods=["GET", "POST"])
def index():
    g = G_DEF
    h = None
    v = None
    if request.method == "POST":
        try:
            g = float(request.form.get("g", g))
        except (TypeError, ValueError):
            g = G_DEF
        try:
            h = float(request.form.get("h", ""))
            if h >= 0 and g >= 0:
                v = math.sqrt(2 * g * h)
        except (TypeError, ValueError):
            h, v = None, None
    return render_template("index.html", g=g, h=h, v=v)

@app.route("/continuidad")
def continuidad():
    return render_template("continuidad.html")

# ... resto de imports y rutas
@app.route("/integracion", methods=["GET", "POST"])
def integracion():
    # valores por defecto razonables
    A  = 0.20   # m^2  (área del tanque)
    a  = 1e-4   # m^2  (área del orificio)
    g  = 9.8    # m/s^2
    h0 = 1.0    # m    (altura inicial)

    T = None
    if request.method == "POST":
        try:
            A  = float(request.form.get("A", A))
            a  = float(request.form.get("a", a))
            g  = float(request.form.get("g", g))
            h0 = float(request.form.get("h0", h0))
            if A > 0 and a > 0 and g >= 0 and h0 >= 0:
                k = (a/A) * math.sqrt(2*g)
                T = (2*math.sqrt(h0))/k  # equivalente a (A/a)*sqrt(2*h0/g)
        except (TypeError, ValueError):
            T = None

    return render_template("integracion.html", A=A, a=a, g=g, h0=h0, T=T)

@app.route("/modelo-lineal", methods=["GET"])
def modelo_lineal():
    # Si quieres pasar valores por defecto desde el servidor, puedes,
    # pero el template ya trae defaults del lado del cliente.
    return render_template("integracion_lineal.html")

@app.route("/metodo_analiticoc")
def metodo_analiticoc():
    return render_template("metodo_analiticoc.html")

@app.route("/metodo_numericoc")
def metodo_numericoc():
    return render_template("metodo_numericoc.html")

@app.route("/barrido-area")
def barrido_area():
    return render_template("barrido_area.html")
@app.route("/cono-perfecto-analitico")
def cono_perfecto_analitico():
    return render_template("cono_perfecto_analitico.html")

@app.route("/cono-perfecto-numerico")
def cono_perfecto_numerico():
    return render_template("cono_perfecto_numerico.html")

@app.route("/cono-truncado-analitico")
def cono_truncado_analitico():
    return render_template("cono_truncado_analitico.html")

@app.route("/cono-truncado-numerico")
def cono_truncado_numerico():
    return render_template("cono_truncado_numerico.html")
@app.route("/barrido-areac")
def barrido_areac():
    return render_template("barrido_areac.html")
    
if __name__ == "__main__":
    app.run(debug=True)