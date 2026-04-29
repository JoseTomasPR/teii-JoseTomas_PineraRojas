# Tecnologías Específicas en Ingeniería Informática • Developer's Guide Vol. 2

- [Tecnologías Específicas en Ingeniería Informática • Developer's Guide Vol. 2](#tecnologías-específicas-en-ingeniería-informática--developers-guide-vol-2)
  - [Calidad de código Python](#calidad-de-código-python)
    - [Documentación del código](#documentación-del-código)
      - [¿Por qué es importante documentar el código?](#por-qué-es-importante-documentar-el-código)
      - [¿Qué se debe documentar en el código?](#qué-se-debe-documentar-en-el-código)
      - [¿Cómo se debe documentar el código?](#cómo-se-debe-documentar-el-código)
      - [¿Qué formato deben tener los *docstrings*?](#qué-formato-deben-tener-los-docstrings)
      - [¿Cómo se muestra la ayuda de las clases, paquetes, subpaquetes y módulos?](#cómo-se-muestra-la-ayuda-de-las-clases-paquetes-subpaquetes-y-módulos)
    - [Estilo del código, *linting* y *type hinting*](#estilo-del-código-linting-y-type-hinting)
      - [PEP8 — *Style Guide for Python Code*](#pep8--style-guide-for-python-code)
      - [*Linting* con `flake8`](#linting-con-flake8)
      - [*Static type checking* con `mypy`](#static-type-checking-con-mypy)
      - [*Linting* y *type hinting* con Visual Studio Code](#linting-y-type-hinting-con-visual-studio-code)
        - [Configuración de `flake8` y `mypy`](#configuración-de-flake8-y-mypy)
    - [Ejercicio 1](#ejercicio-1)
    - [*Unit Testing* con *Mocking*](#unit-testing-con-mocking)
      - [Escribir y ejecutar tests unitarios con `pytest`](#escribir-y-ejecutar-tests-unitarios-con-pytest)
      - [El módulo `unittest.mock`](#el-módulo-unittestmock)
    - [Ejercicio 2](#ejercicio-2)
    - [Depuración y *profiling* en Python](#depuración-y-profiling-en-python)
      - [El módulo `pdb`](#el-módulo-pdb)
      - [El módulo `timeit`](#el-módulo-timeit)
      - [El módulo `time`](#el-módulo-time)
      - [El módulo `cProfile`](#el-módulo-cprofile)
      - [El módulo `tracemalloc`](#el-módulo-tracemalloc)
  - [Referencias](#referencias)
    - [Documentación](#documentación)
    - [Estilo, *linting* y *type hinting*](#estilo-linting-y-type-hinting)
    - [*Unit testing* y *mocking*](#unit-testing-y-mocking)
    - [Depuración y *profiling*](#depuración-y-profiling)

## Calidad de código Python

En cualquier lenguaje de programación, no sólo en Python, el código de calidad:

- Hace lo que se supone que debe hacer eficientemente.
- No presenta defectos, errores o problemas.
- Es fácil de leer, mantener y extender.

Para cumplir los requisitos anteriores, el código se debería escribir y
documentar de manera homogénea, y validar lo más frecuentemente posible de
manera automática. En las siguientes secciones, hablaremos de cómo documentar el
código Python, cómo escribirlo siguiendo un estilo homogéneo estandarizado, cómo
probarlo exhaustivamente de manera sistemática y, para terminar, cómo analizar
su rendimiento.

### Documentación del código

#### ¿Por qué es importante documentar el código?

> “Code is more often read than written.” — Guido van Rossum

El desarrollo de software es una tarea de equipo que progresa de manera gradual.
Por ello, con frecuencia tendremos que revisar código escrito por nosotros
mismos o por otros miembros del equipo algún tiempo después de la última
modificación.

> “It doesn’t matter how good your software is, because if the documentation is
> not good enough, people will not use it.“ — Daniele Procida

En el [*Python Package Index* (PyPi)](https://pypi.org/) se pueden encontrar
miles de paquetes Python que implementan funcionalidad de lo más variopinta. Si
algo tienen en común los más populares es, normalmente, la buena calidad de su
documentación.

#### ¿Qué se debe documentar en el código?

> “Code tells you how; Comments tell you why.” — Jeff Atwood

La mejor forma de documentar el código es escribirlo de manera que sea legible y
autoexplicativo, por ejemplo, utilizando nombres de variables y funciones
descriptivas. No obstante, siempre habrá secciones del código de especial interés:

- Fragmentos de código cuyo objetivo o funcionamiento no se pueda deducir
  fácilmente leyendo el código.
- Algoritmos:
  - Si son conocidos, siempre se debería explicar por qué se usa uno en
    particular y no otras alternativas.
  - Si se trata de un algoritmo propio, especialmente si es complejo, resulta
    aconsejable detallar cómo funciona.
- Errores, deficiencias o funcionalidad no implementada. Se suelen marcar con
  etiquetas como `BUG`, `FIXME` o `TODO`.

#### ¿Cómo se debe documentar el código?

El código Python se documenta con ***docstrings*** que no son más que texto
delimitado por triples comillas dobles (`"""`):

- Las **clases** se documentan con un *docstring* a continuación de la
  definición de la clase y otro por método, con una descripción detallada y
  precisa de cambios de estado del objeto, parámetros, valor devuelto y
  excepciones creadas.
- Los **paquetes y subpaquetes** se documentan con un *docstring* en el archivo
  `__init__py`.
- Los **módulos** se documentan con un *docstring* al principio del archivo
  antes de los *imports*.

Más adelante veremos cómo el *type hinting* también contribuye a documentar el código.

#### ¿Qué formato deben tener los *docstrings*?

Existen varios formatos estandarizados. Para más detalles, véase [Docstring
Formats](https://realpython.com/documenting-python-code/#docstring-formats).
Aunque su uso no es obligatorio, sí que es recomendable, especialmente en
proyectos grandes. El uso de un formato estandarizado posibilita el uso de
herramientas de generación automática de documentación como, por ejemplo,
[Sphinx](https://www.sphinx-doc.org/en/master/).

#### ¿Cómo se muestra la ayuda de las clases, paquetes, subpaquetes y módulos?

Para ilustrar como mostrar la ayuda a partir de los *docstrings* que documentan
el código, usaremos el paquete `teii`:

```bash
$ python3
>>> import teii.finance
>>> help(teii.finance)
...
```

### Estilo del código, *linting* y *type hinting*

> "Readability counts.” — The Zen of Python

Cuando un componente software lo escribe un equipo de varios desarrolladores, el
estilo del código tiende a ser heterogéneo, lo que va en contra de la
legibilidad. Para evitarlo, suele seguirse una guía de estilo. En el caso de
Python existe un estándar comúnmente aceptado, que pertenece a la lista de
*Python Enhancement Proposals*, denominado PEP 8.

#### PEP8 — *Style Guide for Python Code*

PEP 8, también conocido como PEP8 o PEP-8, es un documento que describe un
conjunto de convenciones y buenas prácticas para escribir código Python. Escrito
en 2001 por Guido van Rossum, Barry Warsaw, and Nick Coghlan, su objetivo
principal es mejorar la legibilidad y homogeneidad del código Python. Entre
otras cosas, el estándar incluye:

- Nombres de las clases, métodos/funciones y atributos/variables.
- Formato de los *docstrings* usados para comentar el código.
- Varios aspectos relativos al formato del código.

#### *Linting* con `flake8`

Un *linter* es una herramienta que analiza el código en busca de errores:

- Lógicos: Errores o estructuras potencialmente erróneas.
- Estilísticos: Normalmente, no conforme al estándar PEP 8.
  
En Python hay multitud de opciones. En nuestro caso, vamos a usar `flake8` que
engloba otros *linters* y es fácil de configurar. `flake8` analiza el código en
busca de ambos tipos de errores. Uno de sus *linters*, `pycodestyle`, comprueba
que se cumplan algunas de las convenciones de PEP 8. Para más información,
véanse las referencias relativas a estilo, *linting* y *type hinting*.

Tras la ejecución del análisis, `flake8` crea una lista de errores con un
código. Por ejemplo:

```bash
$ python3 -m flake8 /path/to/src/hello.py
Configuracion/src/hello.py:4:1: E305 expected 2 blank lines after class or function definition, found 1
Configuracion/src/hello.py:5:11: W292 no newline at end of **file**
```

`flake8` se puede configurar mediante la línea de órdenes o en los archivos
`.flake8` o `tox.ini` (si se usa `tox`).

:pushpin: El estándar PEP 8 prescribe que la longitud de una línea de código
Python no debería ser nunca mayor que **79** caracteres. Con la entrada
`max-line-length = 120` en nuestro archivo `tox.ini` ampliamos la longitud
máxima a 120 caracteres. Alternativamente, podríamos haber hecho lo mismo
incluyendo `--max-line-length=120` en la línea de órdenes.

Para ejecutar `flake8` sobre el paquete `teii`:

```bash
$ python3 -m flake8 teii
```

#### *Static type checking* con `mypy`

`mypy` es un *linter* que realiza una comprobación estática de tipos (*static
type checking*) del código Python, es decir, sin ejecutar el código. Esto
implica que siempre podemos ignorar los errores encontrados por `mypy` y
considerarlos avisos (*warnings*). No obstante, si ejecutamos `mypy` sobre un
código sin anotaciones de tipos (*type annotations* o *type hints*),
probablemente no indicará error alguno, porque `mypy` requiere que el
desarrollador incluya dichas anotaciones.

Por ejemplo, dado el *script* `greeting.py`:

```python
# greeting.py
def greeting(name):
    return f"Hello {name}"

def farewell(name):
    return f"Bye {name}"

greeting("Bob")
greeting(b'Alice')
greeting(3)

farewell("Bob")
farewell(b'Alice')
farewell(3)
```

Si añadimos anotaciones de tipos a la función `greeting()`:

```python
# greeting.py con type hints
def greeting(name: str) -> str:
    return f"Hello {name}"
```

La ejecución de `mypy` señalará como incorrectas aquellas llamadas con tipos que
no sean una cadena:

```bash
$ python3 -m mypy greeting.py 
greeting.py:9: error: Argument 1 to "greeting" has incompatible type "bytes"; expected "str"  [arg-type]
greeting.py:10: error: Argument 1 to "greeting" has incompatible type "int"; expected "str"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
```

:pushpin: `mypy` ignorará las llamadas a la función `farewell()` que no tienen
anotaciones, a no ser que añadamos `--disallow-untyped-defs`. Además, con
`--ignore-missing-imports`, se obvian los errores de los paquetes importados sin
anotaciones.

Para ejecutar `mypy` sobre el paquete `teii.finance`:

```bash
$ python3 -m mypy -p teii.finance [-v] [--ignore-missing-imports]
```

#### *Linting* y *type hinting* con Visual Studio Code

Ejecutar los *linters* con frecuencia es muy útil pues elimina los errores
lógicos o estilísticos a medida que se escribe el código. Muchos IDEs permiten
ejecutarlos de manera transparente. Veamos como usar `flake8` y `mypy` desde
Visual Studio Code.

##### Configuración de `flake8` y `mypy`

<!-- markdownlint-disable MD013 -->
| Menú                                      | Acción                                                       |
| ----------------------------------------- | ------------------------------------------------------------ |
| Ver : Paleta de comandos (`Ctrl+Mayús+P`) | Preferencias: Abrir configuración del área de trabajo (JSON) |
<!-- markdownlint-enable MD013 -->

Añade las siguientes líneas al archivo `settings.json` creado durante el paso
anterior:

```json
{
    "flake8.args": [
      "--max-line-length=120"
    ],

    "mypy-type-checker.args": [
        "--ignore-missing-imports",
        "--check-untyped-defs"
    ],
    "mypy-type-checker.reportingScope": "workspace",
    "mypy-type-checker.severity": {
        "error": "Warning",
        "note": "Information"
    },
}
```

### Ejercicio 1

Soluciona los problemas identificados por `flake8` y `mypy` en `example.py`, `hello.py` y
`greeting.py`.

### *Unit Testing* con *Mocking*

> "Errors should never pass silently. Unless explicitly silenced." — The Zen of Python

#### Escribir y ejecutar tests unitarios con `pytest`

Los tests unitarios (en inglés, *unit tests*) son tests que se ejecutan de
manera sistemática para garantizar que los diferentes componentes de una
aplicación se ajustan al diseño y funcionan de la manera deseada. El módulo
`pytest` es un *framework* para *unit testing* muy flexible y potente que
facilita el diseño y ejecución de dichas pruebas.

Para ejecutar los tests unitarios del paquete `teii`:

```bash
$ python3 -m pytest -rA -v --cov teii --cov-report term-missing tests/finance
```

Cuando tecleamos el comando anterior, `pytest` busca todas las funciones cuyo
nombre empieza por `test` (cada una de ellas es un test unitario) en todos los
archivos `.py` del directorio `tests`, las ejecuta una a una y muestra un
resumen. El nombre asignado a cada una de esas funciones es arbitrario pero
debería ser representativo del tipo de prueba realizada.

Por ejemplo, el test `test_constructor_success()` en `test_timeseries.py`:

```python
def test_constructor_success(api_key_str, mocked_response):
    TimeSeriesFinanceClient("NVDA", api_key_str)
```

se limita a crear un objeto de la clase `TimeSeriesFinanceClient()` y comprobar
que no se produce ningún error. Si se generase alguna excepción, el test
unitario fallaría.

Los tests unitarios deben comprobar no sólo el funcionamiento normal del código,
sino también las condiciones de error.

Por ejemplo, el test `test_constructor_failure_invalid_api_key()` en
`test_timeseries.py`:

```python
def test_constructor_failure_invalid_api_key():
    with pytest.raises(FinanceClientInvalidAPIKey):   # captura la excepción
        TimeSeriesFinanceClient("NVDA")
```

comprueba que cuando no se especifica la *API key* (su valor por defecto es
`None`), el constructor de la clase `TimeSeriesFinanceClient()` genera una
excepción `FinanceClientInvalidAPIKey`.

Los parámetros que aparecen en cada test unitario son *fixtures*. Una *fixture*
es una función que proporciona datos o estado a los tests unitarios. Las
*fixtures* se definen en un archivo `conftest.py`. Cada test unitario que
depende de una *fixture* tiene que incluirla como un argumento. Los recursos que
proporciona una *fixture* se crean la primera vez que un test unitario que
depende de ella es ejecutado y se destruyen dependiendo de su ámbito o *scope*:

- `function`: La *fixture* se destruye al final del test (ámbito por defecto).
- `module`: La *fixture* se destruye tras ejecutar el último test del módulo.
- `package`: La *fixture* se destruye tras ejecutar el último test del paquete.
- `session`: La *fixture* se destruye tras ejecutar el último test de la sesión.

En el directorio `tests/` del paquete `teii` hay dos archivos `conftest.py`:

- `tests/conftest.py`: Genérico para todos los subpaquetes de `teii`.
- `tests/finance/conftest.py`: Específico para el subpaquete `teii.finance`.

La *fixture* `sandbox_root_path()` definida en `tests/conftest.py` hace que,
durante la ejecución de un test, el directorio de trabajo actual sea un
directorio temporal creado por `pytest`. Si un test dependiese de esta *fixture*,
los archivos que crease durante su ejecución quedarían en ese directorio
temporal, que en Linux suele estar dentro de `/tmp` (aunque depende de la
configuración del sistema). Esta *fixture* depende de la *fixture* proporcionada
por `pytest` `tmp_path` (que crea el directorio temporal), así como de `monkeypatch`,
también proporcionada por `pytest`, que permite modificar temporalmente el
entorno del test. Por ejemplo, puede cambiar el directorio actual, una variable de
entorno o sustituir una función por una versión simulada. Cuando el test
termina, `pytest` deshace automáticamente esos cambios para que no afecten a los
demás tests.

La *fixture* `api_key_str()` definida en `tests/finance/conftest.py`  es una
cadena de caracteres que representa una *API key*. 

El propósito de las demás *fixtures* se explicará en la siguiente sección.

También es posible ejecutar los tests unitarios del paquete `teii` en Visual
Studio Code:

`Visual Studio Code • Testing : Configure Python Tests : pytest`

(Seleccionando después 'tests/' como directorio de testing).

Esta secuencia de acciones es equivalente a añadir las siguientes líneas al
archivo `settings.json`:

```json
{
    ...
    "python.testing.pytestArgs": [
        "${workspaceFolder}/tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true,
}
```

#### El módulo `unittest.mock`

Cuando se ejecuta un test unitario, tenemos que cerciorarnos de que su salida es
la esperada. Para poder hacerlo, es necesario saber de antemano qué resultado va
a devolver la función o método objeto del test unitario. Si el test unitario
tiene alguna dependencia externa, por ejemplo, una base de datos o una interfaz
HTTP, el resultado devuelto por dicha función o método podría cambiar con el
tiempo. Además, si esa dependencia no está disponible, el test podría fallar por
motivos ajenos al código objeto del test unitario. Este escenario es bastante
frecuente por lo que en lugar de utilizar directamente esas dependencias
externas, se suele utilizar la técnica de *mocking* consistente en emular su
comportamiento, pero haciendo que éste sea determinista. De esta forma se
garantiza que el comportamiento de los tests unitarios también lo sea.

Por ejemplo, el método `_query_api()` de la clase `FinanceClient()` realiza una
consulta a una interfaz HTTP. Por defecto, dicha interfaz devuelve un resultado
consistente en diversos datos bursátiles de un *ticker*. En consecuencia, si
ejecutamos dicho método con una semana de diferencia, los valores devueltos no
serán los mismos.

Para hacer que la interfaz HTTP devuelva siempre los mismos valores,
independientemente de la fecha, la *fixture* `mocked_requests()` crea un objeto
`requests`, de la clase `Mock()`  del paquete `unittest.mock`, que manipularemos
para que tenga los mismos atributos que el módulo `requests`. En particular, el
método `requests.get()`. Con `requests.get.side_effect` indicamos que cuando se
ejecute `requests.get()` se realice en su lugar una llamada a `mocked_get()`. El
método `mocked_get()` crea un objeto `response` de la clase `Mock()` del paquete
`unittest.mock`, el cual modificaremos para que tenga los mismos atributos y
métodos que un objeto de la clase `requests.Response()` devuelto por
`requests.get()`. En concreto, el atributo `status_code` y el método `json()`.
Al asignar `200` a `status_code`, indicamos que la consulta ha tenido éxito. 
Haciendo uso de `importlib.resources`, se devuelve el contenido del archivo de
datos `TIME_SERIES_WEEKLY_ADJUSTED.NVDA.json`, si en la URL se incluye el
ticker NVDA o se genera una excepción en caso contrario, sin acceder a la
interfaz HTTP. El contenido de dicho archivo fue obtenido y verificado
previamente en un Jupyter Notebook.

```python
@fixture(scope='package')
def mocked_requests():
    def mocked_get(url):
        response = mock.Mock()
        response.status_code = 200
        if 'NVDA' in url:
            json_filename = 'TIME_SERIES_WEEKLY_ADJUSTED.NVDA.json'
        else:
            raise ValueError('Ticker no soportado')
        json_resource = resources.files('teii.finance.data').joinpath(json_filename)
        json_data = json.loads(json_resource.read_text(encoding='utf-8'))
        response.json.return_value = json_data
        return response

    # This fixture does not return a value: it patches teii.finance.finance.requests
    # with a local mock to avoid real HTTP calls and keep tests deterministic.
    mocked_requests = mock.Mock()
    mocked_requests.get.side_effect = mocked_get
    teii.finance.finance.requests = mocked_requests
```

:warning: Téngase en cuenta que, por simplicidad, sólo hemos usado la
funcionalidad básica de `pytest` y `unittest.mock` en el diseño de los tests
unitarios del paquete `teii`. Es posible realizar tests mucho más sofisticados y
con  entradas distintas.

Por último, las *fixtures* `pandas_series_NVDA_prices()` y
`pandas_series_NVDA_prices_filtered()` declaradas en `tests/finance/conftest.py`
devuelven el resultado esperado de los tests `test_weekly_price_no_dates()` y
`test_weekly_price_dates()`, respectivamente, obtenidos y verificados
previamente en un Jupyter Notebook.

### Ejercicio 2

Modifica el test unitario `test_constructor_success()` para que use el ticker de
Apple. Verifica que el test finaliza con éxito.

### Depuración y *profiling* en Python

Para depurar código Python, lo más práctico es emplear el depurador integrado de
Visual Studio Code. No obstante, también es posible utilizar el módulo `pdb` que
forma parte de la biblioteca estándar de Python.

#### El módulo `pdb`

El módulo `pdb` ofrece una funcionalidad básica similar a `gdb`. Por ejemplo:

```bash
$ python3 -m pdb example.py
> /path/to/example.py(1)<module>()
-> """ Ejemplo de uso del paquete teii. """

(Pdb) break main
Breakpoint 1 at /path/to/example.py:34

(Pdb) continue
> /path/to/example.py(37)main()
-> logger = setup_logging(logging.WARNING)

(Pdb) ll
 34 B def main():
 35  """ Muestra como usar teii-finance. """
 36  
 37  ->  logger = setup_logging(logging.WARNING)
 38
 39      logger.info("Inicio")
 ...

(Pdb) return
--Return--
> /path/to/example.py(66)main()->None
-> logger.info("Fin")

(Pdb) quit
```

#### El módulo `timeit`

El módulo `timeit` se usa para medir cuánto tiempo tardan en ejecutarse
pequeños fragmentos de código. Por ejemplo:

```bash
$ python3 -m timeit '"-".join([str(n) for n in range(10000)])'
```

:pushpin: En un Jupyter Notebook, también se puede medir cuánto tiempo tarda una
celda en evaluarse incluyendo `%%timeit`.

#### El módulo `time`

El módulo `time` proporciona varias funciones para medir el tiempo:

- [`perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter):
  Devuelve el valor en segundos de un contador hardware.
- [`process_time()`](https://docs.python.org/3/library/time.html#time.process_time):
  Devuelve el tiempo en segundos del proceso (*syscalls* + CPU).
- [`time()`](https://docs.python.org/3/library/time.html#time.time): Devuelve el
  valor en segundos desde *epoch* (January 1, 1970, 00:00:00 -UTC-).

Con `perf_counter()` el punto de referencia es indefinido, es decir, sólo la diferencia
entre dos llamadas tiene sentido; en `process_time()` no se incluye el tiempo
que el proceso está suspendido; y `time()` tiene una resolución de segundos.

En [PEP 418](https://www.python.org/dev/peps/pep-0418/#rationale), se recomienda
usar `perf_counter()` o `process_time()` para hacer *benchmarking* y *profiling*.

En el siguiente ejemplo, se usa `perf_counter()` para medir el tiempo de
ejecución de `TimeSeriesFinanceClient()`:

```python
    try:
        import time
        tic = time.perf_counter()
        tf_client = tf.TimeSeriesFinanceClient(ticker,
                                               my_alpha_vantage_api_key,
                                               logging_level=logging.WARNING)
        toc = time.perf_counter()
        print(f"Tiempo de creación de TimeSeriesFinanceClient: {toc - tic:0.6f} segundos")
```

#### El módulo `cProfile`

El módulo `cProfile` genera estadísticas que describen la frecuencia y tiempo de
ejecución de las diferentes partes de un *script*. Emplear este módulo suele ser
una buena estrategia para encontrar **cuellos de botella** en nuestro código.

En el siguiente ejemplo, se usa `cProfile` para caracterizar el rendimiento del
*script* `example.py`:

<!-- markdownlint-disable MD013-->
```bash
$ python3 -m cProfile -o example.prof example.py
$ python3 -m pstats example.prof
example.prof% help
example.prof% strip
example.prof% sort tottime   # ordena por columna 'totime'
example.prof% stats 10       # muestra los primeros 10 valores

         1254874 function calls (1233251 primitive calls) in 2.055 seconds

   Ordered by: internal time
   List reduced from 5095 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       41    0.602    0.015    0.602    0.015 {method 'read' of '_ssl._SSLSocket' objects}
      697    0.103    0.000    0.103    0.000 {built-in method marshal.loads}
     6793    0.071    0.000    0.123    0.000 inspect.py:625(cleandoc)
        1    0.052    0.052    0.052    0.052 {method 'load_verify_locations' of '_ssl._SSLContext' objects}
1998/1885    0.041    0.000    0.554    0.000 {built-in method builtins.__build_class__}
    96/93    0.040    0.000    0.045    0.000 {built-in method _imp.create_dynamic}
        1    0.035    0.035    0.036    0.036 xml.py:1(<module>)
     9329    0.024    0.000    0.024    0.000 {method 'search' of 're.Pattern' objects}
     3228    0.024    0.000    0.024    0.000 {built-in method posix.stat}
      429    0.022    0.000    0.022    0.000 {built-in method builtins.dir}
example.prof% quit
```
<!-- markdownlint-emable MD013-->

:warning: Para realizar el *profiling*, se comentó la línea `plt.show()` que
muestra la ventana con la gráfica y, por tanto, mide el tiempo que el usuario
tarda en cerrar la ventana. Además, el nivel de severidad tanto del *script*
como del paquete `teii` se estableció a `WARNING`. Las operaciones de E/S suelen
ser operaciones muy lentas que pueden distorsionar las medidas.

El significado de las columnas en la tabla del ejemplo anterior es el siguiente:

- `ncalls` es el número de llamadas.
- `tottime` es el tiempo total en segundos, excluyendo el tiempo de las llamadas
  a sub-funciones.
- `percall` es el cociente entre `tottime` y `ncalls`.
- `cumtime` es el tiempo total en segundos, incluyendo el tiempo de las llamadas
  a sub-funciones.
- `percall` es el cociente entre `cumtime` y `ncalls`.
- `filename:lineno(function)` es el archivo:línea y función.

Analizando la tabla del ejemplo anterior, puede deducirse fácilmente que el
**cuello de botella en `example.py`** son las operaciones de lectura del
*socket* en el método `_query_api()` que se invoca en el constructor de la clase
`TimeSeriesFinanceClient()`. En otros casos, podría no resultar evidente dónde
están los cuellos de botella ya que `cProfile` sólo nos dice en qué funciones se
consume la mayor parte del tiempo. Si es así, tendríamos que recurrir a otros
*profilers*, como [`line_profiler`](https://pypi.org/project/line-profiler/),
que atribuyen el tiempo de ejecución a líneas del código en lugar de a funciones.

#### El módulo `tracemalloc`

El módulo `tracemalloc` permite identificar los bloques de memoria reservados
atribuyéndolos a líneas código fuente.

En el siguiente ejemplo, se usa `tracemalloc` para caracterizar el uso de
memoria de `TimeSeriesFinanceClient()`:

```python
    try:
        import tracemalloc
        tracemalloc.start()
        tf_client = tf.TimeSeriesFinanceClient(ticker,
                                               my_alpha_vantage_api_key,
                                               logging_level=logging.WARNING)
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        for stat in snapshot.statistics('lineno')[:5]:
            frame = stat.traceback[0]
            avg = stat.size / stat.count if stat.count else 0
            print(f"{frame.filename.split('/')[-1] + ':' + str(frame.lineno):50} "
                  f"size = {stat.size:7} bytes     count = {stat.count:5}    avg = {avg:6.1f} bytes")
```

Si ejecutamos `example.py` después de realizar los cambios anteriores:

<!-- markdownlint-disable MD013-->
```bash
# Salida de logging (default stderr) enviada a /dev/null, para ver sólo salida tracemalloc:
$ python3 example.py 2> /dev/null 
❯ python example.py 2> /dev/null 
decoder.py:353                                     size = 1054742 bytes     count = 13808    avg =   76.4 bytes
take.py:157                                        size =   78120 bytes     count =    21    avg = 3720.0 bytes
encoder.py:258                                     size =   77867 bytes     count =  1387    avg =   56.1 bytes
<frozen abc>:123                                   size =   23417 bytes     count =   278    avg =   84.2 bytes
<frozen importlib._bootstrap_external>:729         size =   13421 bytes     count =    99    avg =  135.6 bytes
```
<!-- markdownlint-enable MD013-->

comprobaremos que el procesamiento de la respuesta en formato JSON de la
interfaz HTTP y su manipulación con `pandas` son los principales responsables
del consumo de memoria de `example.py`.

## Referencias

### Documentación

- [Real Python • Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/)

### Estilo, *linting* y *type hinting*

- [Real Python • Python Code Quality: Tools & Best Practices](https://realpython.com/python-code-quality/)
- [Python Documentation • PEP0 — Index of Python Enhancement Proposals (PEPs)](https://www.python.org/dev/peps/)
- [Python Documentation • PEP8 — Style Guide for Python Code](https://pep8.org/)
- [Flake8: Your Tool For Style Guide Enforcement](https://flake8.pycqa.org/en/stable/index.html)
  - [Configuring Flake8](https://flake8.pycqa.org/en/stable/user/configuration.html)
  - [Error/Violation Codes](https://flake8.pycqa.org/en/stable/user/error-codes.html)
- [Real Python • How to Write Beautiful Python Code With PEP 8](https://realpython.com/python-pep8/)
- [Mypy](http://mypy-lang.org/)
  - [Getting started](https://mypy.readthedocs.io/en/stable/getting_started.html)
  - [Type hints cheat sheet (Python 3)](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
  - [Missing type hints for third party library](https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-type-hints-for-third-party-library)
- [Linting Python in Visual Studio Code](https://code.visualstudio.com/docs/python/linting)

### *Unit testing* y *mocking*

- [Unit testing](https://en.wikipedia.org/wiki/Unit_testing)
- [The `pytest` framework](https://docs.pytest.org/)
- [Real Python • Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)
- [Real Python • Understanding the Python Mock Object Library](https://realpython.com/python-mock-library/)

### Depuración y *profiling*

- [Python Documentation • Debugging and Profiling](https://docs.python.org/3.11/library/debug.html)
  - [`pdb` — The Python Debugger](https://docs.python.org/3.11/library/pdb.html)
  - [`timeit` — Measure execution time of small code snippets](https://docs.python.org/3.11/library/timeit.html)
  - [`time` — Time access and conversions](https://docs.python.org/3.11/library/time.html)
  - [The Python Profilers](https://docs.python.org/3.11/library/profile.html)
  - [`trace` — Trace or track Python statement execution](https://docs.python.org/3.11/library/trace.html)
  - [`tracemalloc` — Trace memory allocations](https://docs.python.org/3.11/library/tracemalloc.html)
- [Real Python • Python Debugging With Pdb](https://realpython.com/python-debugging-pdb/)
- [Real Python • Python Timer Functions: Three Ways to Monitor Your Code](https://realpython.com/python-timer/)
