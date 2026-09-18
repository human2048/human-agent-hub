\# Plano del Sistema - CyberNiche Lab (`human-agent-hub`)



\## 1. Visión General

\- \*\*Propósito:\*\* Web-app ultraligera de catálogo digital y despacho directo a WhatsApp.

\- \*\*Costo Operativo:\*\* $0 USD (GitHub Pages / Vercel).

\- \*\*Filosofía:\*\* Local-first, Vanilla JS sin dependencias, carga < 1s.



\## 2. Stack Tecnológico

\- \*\*Frontend UI:\*\* HTML5 Semántico, CSS3 personalizado (`cyber-ui.css`), JavaScript ES6+ nativo.

\- \*\*Persistencia de Datos:\*\* `data/menu-matrix.json` (catálogo) y `LocalStorage` (canasta).

\- \*\*SEO Local:\*\* Marcado `JSON-LD` (Schema.org `Restaurant` / `LocalBusiness`), OpenGraph.

\- \*\*Integración:\*\* API `https://wa.me/` con formateo mediante `encodeURIComponent`.



\## 3. Estructura del Repositorio

cyberniche-lab/

├── index.html               # Portal de entrada / Vitrina SEO local

├── menu-viewer.html         # Visor interactivo del catálogo

├── data/

│   └── menu-matrix.json     # Matriz de oferta, precios y configuración

├── css/

│   └── cyber-ui.css         # Capa visual y diseño responsivo

├── js/

│   ├── menu-engine.js       # Motor de renderizado del catálogo

│   ├── order-basket.js      # Gestor de canasta de compras

│   └── wa-dispatcher.js     # Despachador formateador para WhatsApp

├── docs/

│   └── system-blueprint.md  # Plano arquitectónico del sistema

└── README.md                # Documentación general del proyecto



\## 4. Contrato de Datos (`data/menu-matrix.json`)

```json

{

&#x20; "merchant": {

&#x20;   "name": "Comercio Ejemplo",

&#x20;   "whatsapp\_phone": "573000000000",

&#x20;   "currency": "COP",

&#x20;   "city": "Bogotá"

&#x20; },

&#x20; "categories": \[

&#x20;   {

&#x20;     "id": "cat-1",

&#x20;     "name": "Especialidades",

&#x20;     "products": \[

&#x20;       {

&#x20;         "id": "prod-101",

&#x20;         "name": "Producto Demo",

&#x20;         "description": "Descripción optimizada para conversión",

&#x20;         "price": 25000,

&#x20;         "image\_url": "assets/img/demo.jpg"

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ]

}

