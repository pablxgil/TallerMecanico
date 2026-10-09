# Evaluación de Archify

## Hallazgo

La coincidencia técnica relevante es el proyecto `tt-a1i/archify`: un skill y renderizador Node.js que transforma una representación JSON de arquitectura, flujos y secuencias en HTML/SVG. No es una librería de tiempo de ejecución para Vue/FastAPI ni una necesidad de producción de TallerMecanico.

## Decisión

No se instala Archify en esta entrega. Incorporarlo añadiría una herramienta de autoría específica de agentes, sin necesidad operativa comprobada ni beneficio sobre Mermaid para documentación versionada. Mermaid permite revisión por pull request, visualización directa en GitHub y no modifica el stack de ejecución.

## Revisión futura

Puede evaluarse Archify como herramienta de documentación opcional en un entorno de desarrollo aislado si se requiere exportar diagramas HTML/SVG interactivos. No debe ejecutarse en el contenedor del frontend ni del backend sin una decisión explícita.
