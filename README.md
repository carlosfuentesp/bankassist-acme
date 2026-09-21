# BankAssist ACME

POC end-to-end de un asistente grounded para analistas autorizados de cobranza.
Combina hechos estructurados obtenidos con Genie, política vigente recuperada con
AI Search y una evaluación determinista antes de pedir al foundation model que
redacte la respuesta final.

```text
CSV -> Bronze -> Silver -> Gold -> Genie ---------+
                                                    +-> BankAssist -> respuesta
Markdown -> parse -> chunks -> AI Search ----------+
```

BankAssist únicamente determina si un cliente cumple condiciones para ser
evaluado. Nunca aprueba acuerdos de pago.

## Componentes

- `src/ingestion`, `src/transformations`: Lakeflow Declarative Pipelines.
- `src/documents`: ingestión, parsing, chunking y publicación documental.
- `src/agents/bankassist`: orquestación Genie + AI Search, reglas y guardrails.
- `src/app`: chatbot para Databricks Apps.
- `resources`: pipelines, AI Search, App y workflow de preparación end-to-end.
- `tests/unit`: límites y resultados de CUST-001, CUST-002 y CUST-003.

## Resultados esperados del caso principal

| Cliente | Resultado |
|---|---|
| CUST-001 | No iniciar un acuerdo: tiene una promesa activa. |
| CUST-002 | Cumple condiciones para evaluación humana. |
| CUST-003 | No cumple: tuvo un acuerdo dentro de los 90 días anteriores. |

La ventana usa `snapshot_date`, no la fecha del sistema. Exactamente 90 días aún
está dentro de la ventana; el cliente pasa la condición desde el día 91.


## Getting started

Choose how you want to work on this project:

(a) Directly in your Databricks workspace, see
    https://docs.databricks.com/dev-tools/bundles/workspace.

(b) Locally with an IDE like Cursor or VS Code, see
    https://docs.databricks.com/dev-tools/vscode-ext.html.

(c) With command line tools, see https://docs.databricks.com/dev-tools/cli/databricks-cli.html

If you're developing with an IDE, dependencies for this project should be installed using uv:

*  Make sure you have the UV package manager installed.
   It's an alternative to tools like pip: https://docs.astral.sh/uv/getting-started/installation/.
*  Run `uv sync --dev` to install the project's dependencies.


# Using this project using the CLI

The Databricks workspace and IDE extensions provide a graphical interface for working
with this project. It's also possible to interact with it directly using the CLI:

1. Authenticate to your Databricks workspace, if you have not done so already:
    ```
    $ databricks configure
    ```

2. To deploy a development copy of this project, type:
    ```
    $ databricks bundle deploy --target dev
    ```
    (Note that "dev" is the default target, so the `--target` parameter
    is optional here.)

    This deploys everything that's defined for this project.

3. Similarly, to deploy a production copy, type:
   ```
   $ databricks bundle deploy --target prod
   ```

4. To run a job or pipeline, use the "run" command:
   ```
   $ databricks bundle run
   ```

5. Para ejecutar las pruebas locales:
    ```
    $ uv sync --dev
    $ uv run pytest
    ```

6. Para ejecutar el flujo completo en Databricks:

    ```
    databricks bundle deploy -t dev --profile <perfil>
    databricks bundle run bankassist_end_to_end -t dev --profile <perfil>
    databricks bundle run bankassist_app -t dev --profile <perfil>
    ```

El workflow prepara las capas Bronze/Silver/Gold, procesa las políticas y publica
la tabla fuente del índice. La App consume únicamente cuatro dependencias de
runtime: Genie, AI Search, Foundation Model y el SQL Warehouse de Genie.
