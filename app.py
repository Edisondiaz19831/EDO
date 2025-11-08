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


@app.route("/cuerda-masa-variable", methods=["GET", "POST"])
def cuerda_masa_variable():
    # Valores por defecto (puedes ajustarlos)
    g_default = 9.8
    L_default = 1.0
    m_default = 0.5
    x0_default = 0.10
    v0_default = 0.01

    # Cargamos valores del formulario si viene POST
    if request.method == "POST":
        try:
            g = float(request.form.get("g", g_default))
        except (TypeError, ValueError):
            g = g_default

        try:
            L = float(request.form.get("L", L_default))
        except (TypeError, ValueError):
            L = L_default

        try:
            x0 = float(request.form.get("x0", x0_default))
        except (TypeError, ValueError):
            x0 = x0_default

        try:
            v0 = float(request.form.get("v0", v0_default))
        except (TypeError, ValueError):
            v0 = v0_default

        # Punto donde quiero evaluar v(x):
        try:
            x_eval = float(request.form.get("x_eval", x0))
        except (TypeError, ValueError):
            x_eval = x0

    else:
        g = g_default
        L = L_default
        x0 = x0_default
        v0 = v0_default
        x_eval = x0

    # Calculamos v(x_eval) usando la solución analítica,
    # solo si los datos tienen sentido
    v_eval = None
    valido = False
    msg_error = None

    try:
        if g >= 0 and L > 0 and x_eval >= x0:
            # v(x)^2 = v0^2 + (g/L)(x^2 - x0^2)
            inside = v0**2 + (g / L) * (x_eval**2 - x0**2)
            if inside >= 0:
                v_eval = math.sqrt(inside)
                valido = True
            else:
                msg_error = "Con esos valores, la expresión dentro de la raíz es negativa."
        else:
            msg_error = "Verifica que L>0 y que x ≥ x₀."
    except Exception as e:
        msg_error = f"Error en el cálculo: {e}"

    return render_template(
        "cuerda_masa_variable.html",
        g=g,
        L=L,
        x0=x0,
        v0=v0,
        x_eval=x_eval,
        v_eval=v_eval,
        valido=valido,
        msg_error=msg_error,
    )

@app.route("/cuerda-masa-variable-codigo")
def cuerda_masa_variable_codigo():
    return render_template("cuerda_masa_variable_codigo.html")
@app.route("/cuerda-enrollada", methods=["GET"])
def cuerda_enrollada():
    # si quieres podrías pasar defaults, pero aquí todo se maneja en el front
    return render_template("cuerda_enrollada.html")

@app.route("/oscilador-amortiguado", methods=["GET"])
def oscilador_amortiguado():
    # Valores por defecto como en el cuaderno
    k = 50.0
    m = 0.5
    b = 0.5
    F0 = 10.0  # no se usa aquí porque F_ext = 0 en esta sección
    Gamma = b / m
    omega_0 = (k / m) ** 0.5
    x0 = 10.0
    v0 = 0.0

    return render_template(
        "oscilador_amortiguado.html",
        k=k, m=m, b=b, F0=F0,
        Gamma=Gamma, omega_0=omega_0,
        x0=x0, v0=v0
    )

@app.route("/oscilador-forzado", methods=["GET"])
def oscilador_forzado():
    # Mismos parámetros base que el profe
    k = 50.0
    m = 0.5
    b = 0.5
    F0 = 70.0
    omega_f = 30.0

    Gamma = b / m
    omega_0 = (k / m) ** 0.5
    x0 = 10.0
    v0 = 0.0

    return render_template(
        "oscilador_forzado.html",
        k=k, m=m, b=b,
        F0=F0, omega_f=omega_f,
        Gamma=Gamma, omega_0=omega_0,
        x0=x0, v0=v0
    )

@app.route("/globo-cuerda", methods=["GET"])
def globo_cuerda():
    # Parámetros por defecto (los del notebook)
    V_g = 0.002      # m^3  volumen del globo
    mu = 0.01        # kg/m masa lineal de la cuerda
    rho_a = 1.2      # kg/m^3 densidad aire
    rho_He = 0.18    # kg/m^3 densidad helio
    b = 0.01         # N·s/m rozamiento
    x0 = 0.0         # m   longitud inicial de cuerda levantada
    v0 = 0.0         # m/s velocidad inicial

    return render_template(
        "globo_cuerda.html",
        V_g=V_g,
        mu=mu,
        rho_a=rho_a,
        rho_He=rho_He,
        b=b,
        x0=x0,
        v0=v0
    )

@app.route("/tanque-oscilador", methods=["GET"])
def tanque_oscilador():
    # Valores base razonables
    A = 0.20      # m^2 área del tanque
    a = 1e-4      # m^2 área del orificio
    rho = 1000.0  # kg/m^3 (agua)
    M = 5.0       # kg masa tanque + soporte
    k = 200.0     # N/m constante del resorte
    c = 2.0       # N·s/m amortiguador
    h0 = 1.0      # m altura inicial del agua
    x0 = 0.0      # m elongación inicial
    v0 = 0.0      # m/s velocidad inicial

    return render_template(
        "tanque_oscilador.html",
        A=A, a=a, rho=rho, M=M, k=k, c=c,
        h0=h0, x0=x0, v0=v0
    )

@app.route("/modelo-sida", methods=["GET", "POST"])
def modelo_sida():
    # -----------------------------
    # Valores por defecto
    # -----------------------------
    # Población inicial
    N0_default = 1000
    x0_default = 990   # susceptibles
    y0_default = 10    # infectados sin tratamiento
    z0_default = 0     # infectados con tratamiento

    # Parámetros epidemiológicos (valores ilustrativos)
    c_default      = 1.0     # contactos promedio por unidad de tiempo
    beta1_default  = 0.30    # prob contagio con infectado sin tratar
    beta2_default  = 0.05    # prob contagio con infectado tratado
    mu_default     = 0.0001  # muerte natural
    delta_default  = 0.01    # muerte por SIDA sin tratamiento
    tau_default    = 0.10    # paso a tratamiento
    d_default      = 0.005   # muerte en tratados

    # Tiempo de simulación
    T_default  = 365.0       # días
    dt_default = 1.0         # paso (día)

    # -----------------------------
    # Leer datos del formulario
    # -----------------------------
    if request.method == "POST":
        def get_float(name, default):
            try:
                return float(request.form.get(name, default))
            except (TypeError, ValueError):
                return default

        x0 = get_float("x0", x0_default)
        y0 = get_float("y0", y0_default)
        z0 = get_float("z0", z0_default)

        c     = get_float("c", c_default)
        beta1 = get_float("beta1", beta1_default)
        beta2 = get_float("beta2", beta2_default)
        mu    = get_float("mu", mu_default)
        delta = get_float("delta", delta_default)
        tau   = get_float("tau", tau_default)
        d     = get_float("d", d_default)

        T  = get_float("T", T_default)
        dt = get_float("dt", dt_default)
    else:
        x0, y0, z0 = x0_default, y0_default, z0_default
        c, beta1, beta2 = c_default, beta1_default, beta2_default
        mu, delta, tau, d = mu_default, delta_default, tau_default, d_default
        T, dt = T_default, dt_default

    # Asegurar cosas razonables
    if T <= 0:
        T = T_default
    if dt <= 0:
        dt = dt_default

    # -----------------------------
    # Simulación numérica (Euler)
    # -----------------------------
    t_vals = []
    x_vals = []
    y_vals = []
    z_vals = []

    x = max(x0, 0.0)
    y = max(y0, 0.0)
    z = max(z0, 0.0)

    steps = int(T / dt)

    for n in range(steps + 1):
        t = n * dt
        t_vals.append(t)
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)

        N = x + y + z
        if N <= 0:
            break  # se extinguió la población

        # Ecuaciones del modelo:
        # dx/dt = -μ x - c β1 (y/N) x - c β2 (z/N) x
        # dy/dt = c β1 (y/N) x + c β2 (z/N) x - μ y - δ y - τ y
        # dz/dt = τ y - μ z - d z

        dxdt = -mu * x - c * beta1 * (y / N) * x - c * beta2 * (z / N) * x
        dydt = (
            c * beta1 * (y / N) * x
            + c * beta2 * (z / N) * x
            - mu * y
            - delta * y
            - tau * y
        )
        dzdt = tau * y - mu * z - d * z

        # Paso de Euler
        x_new = x + dxdt * dt
        y_new = y + dydt * dt
        z_new = z + dzdt * dt

        # Evitar negativos por error numérico
        x = max(x_new, 0.0)
        y = max(y_new, 0.0)
        z = max(z_new, 0.0)

    # -----------------------------
    # Renderizar
    # -----------------------------
    return render_template(
        "modelo_sida.html",
        # parámetros y CI para rellenar el formulario
        x0=x0, y0=y0, z0=z0,
        c=c, beta1=beta1, beta2=beta2,
        mu=mu, delta=delta, tau=tau, d=d,
        T=T, dt=dt,
        # datos de serie para la gráfica
        t_vals=t_vals,
        x_vals=x_vals,
        y_vals=y_vals,
        z_vals=z_vals,
    )


if __name__ == "__main__":
    app.run(debug=True)