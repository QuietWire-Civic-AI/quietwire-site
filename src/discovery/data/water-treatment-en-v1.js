window.QW_DISCOVERY_SURVEY = {
  "schema": "quietwire.discovery.survey",
  "schema_version": "1.0",
  "survey_id": "water-treatment-en",
  "survey_version": "1.0.0-candidate",
  "title": "QuietWire Discovery — Water Treatment Operations",
  "subtitle": "ERPNext + Canonical Attestation Platform",
  "language": "en",
  "question_count": 333,
  "quick_question_ids": [
    "01.1",
    "01.2",
    "01.7",
    "01.8",
    "01.9",
    "01.10",
    "02.2",
    "02.8",
    "02.9",
    "21.1",
    "23.3",
    "23.4",
    "23.14",
    "26.5",
    "30.2",
    "30.6",
    "30.7"
  ],
  "roles": {
    "executive": {
      "label": "Owner or executive",
      "description": "Scope, priorities, authority, risk, and investment decisions."
    },
    "operations": {
      "label": "Operations",
      "description": "How work moves through teams, sites, equipment, and customers."
    },
    "sales": {
      "label": "Sales and customer relationships",
      "description": "Leads, pricing, quotations, contracts, and communication."
    },
    "field": {
      "label": "Field service and engineering",
      "description": "Site surveys, installation, service visits, and equipment evidence."
    },
    "inventory": {
      "label": "Inventory and purchasing",
      "description": "Items, warehouses, suppliers, quality, and replenishment."
    },
    "finance": {
      "label": "Finance",
      "description": "Accounting, invoicing, collection, profitability, and financial controls."
    },
    "technology": {
      "label": "Technology",
      "description": "Data, integration, architecture, security, and operating systems."
    },
    "governance": {
      "label": "Governance and assurance",
      "description": "Authority, evidence, privacy, models, workflows, and human review."
    },
    "service": {
      "label": "Customer service",
      "description": "Issues, SLAs, escalations, warranty, and satisfaction."
    },
    "quality": {
      "label": "Quality and compliance",
      "description": "Standards, inspection, calibration, non-conformity, and safety."
    }
  },
  "areas": {
    "strategy": "Company and project scope",
    "people": "People and authority",
    "customers": "Customers and relationships",
    "sales": "Sales and contracting",
    "field": "Field work and installation",
    "products": "Products and services",
    "equipment": "Equipment lifecycle",
    "inventory": "Inventory and purchasing",
    "quality": "Quality and warranty",
    "maintenance": "Maintenance and service",
    "finance": "Finance and accounting",
    "digital": "Website and digital channels",
    "reporting": "Reports and indicators",
    "data": "Data and migration",
    "integrations": "Integrations",
    "cap": "CAP and AI use cases",
    "privacy": "Privacy and security",
    "ai-governance": "Model governance",
    "technology": "Technical architecture",
    "workflow": "Workflows and approvals",
    "pilot": "Pilot and acceptance",
    "operations": "Operations",
    "contracts": "Contracts",
    "procurement": "Procurement",
    "service": "Customer service",
    "accounting": "Accounting",
    "migration": "Migration",
    "security": "Security",
    "risk": "Risk",
    "compliance": "Compliance"
  },
  "sections": [
    {
      "id": "01",
      "title": "Company profile and project scope",
      "description": "Define the organization, the present operating environment, and the first outcomes that matter.",
      "roles": [
        "executive",
        "operations",
        "technology"
      ],
      "areas": [
        "strategy",
        "operations"
      ],
      "questions": [
        {
          "id": "01.1",
          "prompt": "What are the company’s legal name and trading name, and where does it operate?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "01.2",
          "prompt": "Which activities does the company perform: equipment sales, spare parts, installation, maintenance, recurring contracts, rental, assembly, importing, e-commerce, or other work?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "01.3",
          "prompt": "Which customer sectors does the company serve—B2C, B2B, B2G—and what approximate share comes from each?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "01.4",
          "prompt": "How many branches, warehouses, retail locations, service centres, field teams, and mobile technician vehicles exist?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "01.5",
          "prompt": "How many users are expected in the first phase and after twelve months?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "01.6",
          "prompt": "What systems are currently used for sales, customer management, inventory, maintenance, accounting, customer service, field operations, and reporting?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "01.7",
          "prompt": "What are the three most costly, disruptive, or frustrating problems in the current operation?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "01.8",
          "prompt": "What measurable results must ERPNext achieve in the first ninety days?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "01.9",
          "prompt": "What measurable results must CAP achieve in the first ninety days?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "01.10",
          "prompt": "Is the desired implementation complete from the beginning or phased, and what is the minimum acceptable first phase?",
          "response_type": "decision with explanation",
          "priority": "critical"
        }
      ]
    },
    {
      "id": "02",
      "title": "Organization, users, roles, and permissions",
      "description": "Map people, authority, visibility, ownership, and audit requirements.",
      "roles": [
        "executive",
        "operations",
        "governance",
        "technology"
      ],
      "areas": [
        "people",
        "governance"
      ],
      "questions": [
        {
          "id": "02.1",
          "prompt": "Which departments and teams currently exist?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "02.2",
          "prompt": "Who has final decision authority for pricing, discounts, purchasing, inventory release, warranty, returns, case closure, debt write-off, compensation, and replacement?",
          "response_type": "roles / owners",
          "priority": "critical"
        },
        {
          "id": "02.3",
          "prompt": "Which roles require daily access to ERPNext?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "02.4",
          "prompt": "Will technicians and sales representatives use mobile devices, and do they require temporary offline capability?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "02.5",
          "prompt": "Which data must not be visible to each role or external contractor?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "02.6",
          "prompt": "Do permissions vary by branch, city, warehouse, sales region, customer category, company, or legal entity?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "02.7",
          "prompt": "Which transactions require multi-stage approval, and what stages, thresholds, roles, and escalation conditions apply?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "02.8",
          "prompt": "Who owns operational data in ERPNext, and who owns evidence, recommendations, model runs, and attestations in CAP?",
          "response_type": "roles / owners",
          "priority": "critical"
        },
        {
          "id": "02.9",
          "prompt": "Who reviews CAP recommendations and may accept, reject, override, or escalate them?",
          "response_type": "roles / owners",
          "priority": "critical"
        },
        {
          "id": "02.10",
          "prompt": "Is a complete audit record required for viewing, creating, editing, approving, rejecting, exporting, deleting, and overriding, and how long must it be retained?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "03",
      "title": "Customers, sites, and addresses",
      "description": "Describe customer categories, locations, contacts, consent, and duplicate-control rules.",
      "roles": [
        "executive",
        "sales",
        "operations",
        "governance"
      ],
      "areas": [
        "customers",
        "sales"
      ],
      "questions": [
        {
          "id": "03.1",
          "prompt": "Which customer types must be represented?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.2",
          "prompt": "Can one customer have multiple installation or service locations?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.3",
          "prompt": "Which customer fields are mandatory?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.4",
          "prompt": "Must billing party, installation location, service location, delivery location, primary contact, and technical contact be represented separately?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.5",
          "prompt": "Should the system store GPS coordinates, access instructions, parking, entry times, security requirements, and site contacts?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.6",
          "prompt": "Are customers classified by commercial value, risk, region, water type, equipment type, service level, contract type, or payment behaviour?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.7",
          "prompt": "Are credit limits or payment terms different by customer or customer group?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.8",
          "prompt": "Must consent be recorded for marketing, data sharing, data analysis, AI-assisted processing, and contact channels?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.9",
          "prompt": "What matching rules should prevent duplicate customer records across channels?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "03.10",
          "prompt": "Should family members or employees of an institutional customer be linked to the primary customer record?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "04",
      "title": "Leads and customer relationship management",
      "description": "Understand how leads arrive, move, close, and receive human or CAP support.",
      "roles": [
        "sales",
        "executive",
        "operations"
      ],
      "areas": [
        "sales",
        "customers"
      ],
      "questions": [
        {
          "id": "04.1",
          "prompt": "Through which channels do leads arrive?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "04.2",
          "prompt": "What are the current sales stages from first contact to closure?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.3",
          "prompt": "What information must be collected in a Lead before it becomes an Opportunity or Customer?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.4",
          "prompt": "Should leads be assigned automatically by city, product, customer size, representative, industry, customer type, workload, or territory?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.5",
          "prompt": "What is the acceptable response time for each lead channel?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.6",
          "prompt": "Which standardized reasons should be used when an opportunity is lost?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.7",
          "prompt": "Should calls, visits, messages, files, photographs, and other interactions be stored in the customer timeline?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.8",
          "prompt": "Are sales targets and commissions used, and how are commissions calculated?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.9",
          "prompt": "Which sales and pipeline reports are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "04.10",
          "prompt": "What should CAP do in the sales process, such as lead scoring, close probability, next-action support, summarization, or neglected-lead detection?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "05",
      "title": "Site survey and water-quality assessment",
      "description": "Capture field evidence, measurements, risks, recommendation boundaries, and escalation.",
      "roles": [
        "operations",
        "field",
        "quality",
        "technology"
      ],
      "areas": [
        "field",
        "quality"
      ],
      "questions": [
        {
          "id": "05.1",
          "prompt": "Is a site survey performed before sale or installation, and who performs it?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "05.2",
          "prompt": "Which water sources are encountered?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.3",
          "prompt": "Which measurements are currently collected?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.4",
          "prompt": "Are measurements taken with field devices, laboratories, or both, and what device, calibration, laboratory, report, and sample details must be stored?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.5",
          "prompt": "Which consumption and site variables must be collected?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.6",
          "prompt": "Should the survey include photographs or video of the site, pipework, water source, electrical panel, installation space, drainage, and access route?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.7",
          "prompt": "Which installation risks or constraints must be recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.8",
          "prompt": "Who approves the site-survey result and technical recommendation?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "05.9",
          "prompt": "Should a quotation be generated automatically from the survey result?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.10",
          "prompt": "Should CAP recommend the treatment system, stages, components, replacement intervals, conditions, reasons, and confidence, and what boundaries apply?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "05.11",
          "prompt": "Under which conditions must CAP refuse to recommend and escalate to an engineer or laboratory?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "06",
      "title": "Product and service master data",
      "description": "Define items, variants, bundles, serials, batches, compatibility, services, and technical fields.",
      "roles": [
        "operations",
        "inventory",
        "field",
        "technology"
      ],
      "areas": [
        "products",
        "inventory"
      ],
      "questions": [
        {
          "id": "06.1",
          "prompt": "What are the main product groups?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.2",
          "prompt": "Is each system sold as a finished unit, component collection, configured package, custom-built system, or manufactured item?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.3",
          "prompt": "Which Item Variant attributes are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.4",
          "prompt": "Should a packaged system be represented as a Product Bundle, Bill of Materials assembly, manufactured item, configured project package, or another design?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.5",
          "prompt": "Should replaceable components be recorded as separate Items?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.6",
          "prompt": "Which Items require Serial Numbers, Batch Numbers, expiry dates, manufacturing dates, or warranty identifiers?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "06.7",
          "prompt": "Which manufacturer, barcode, QR, model, specification, certificate, image, origin, and compatibility fields are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.8",
          "prompt": "Which units of measure and packaging types are used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.9",
          "prompt": "Are compatible alternatives available, and under what rules may a technician substitute a component?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.10",
          "prompt": "Which components are mandatory or optional for each model?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.11",
          "prompt": "Do warranties and replacement intervals vary by item, model, supplier, water type, usage, or region?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "06.12",
          "prompt": "Which services should be represented as non-stock Items?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "06.13",
          "prompt": "Which additional technical fields are required for each Item?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "07",
      "title": "Pricing, quotations, and discounts",
      "description": "Define price lists, cost logic, approvals, validity, service pricing, and CAP boundaries.",
      "roles": [
        "sales",
        "finance",
        "executive"
      ],
      "areas": [
        "sales",
        "finance"
      ],
      "questions": [
        {
          "id": "07.1",
          "prompt": "How many Price Lists are required, and what kinds?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "07.2",
          "prompt": "Does the listed price include installation, delivery, tax, commissioning, survey, and consumables, or are these separate?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "07.3",
          "prompt": "Do prices vary by city, distance, floor, access, complexity, customer category, or urgency?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "07.4",
          "prompt": "Are quantity discounts, package offers, free Items, coupons, promotions, or seasonal pricing used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "07.5",
          "prompt": "What is the maximum discount for each role, and when is approval required?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "07.6",
          "prompt": "Do quotations expire, and what booking, reservation, and advance-payment conditions apply?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "07.7",
          "prompt": "Are prices linked to purchase cost, landed cost, minimum margin, replacement cost, or market price?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "07.8",
          "prompt": "Should the system prevent sales below cost, minimum margin, or an approved floor price?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "07.9",
          "prompt": "How are maintenance contracts, subscriptions, and recurring replacements priced?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "07.10",
          "prompt": "Should CAP detect risky margins, recommend pricing, estimate price sensitivity, detect unusual discounting, or identify missing costs, and what limits apply?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "08",
      "title": "Quotations, orders, and contracting",
      "description": "Map templates, signatures, mixed orders, payments, inventory reservations, projects, and changes.",
      "roles": [
        "sales",
        "finance",
        "operations"
      ],
      "areas": [
        "sales",
        "contracts"
      ],
      "questions": [
        {
          "id": "08.1",
          "prompt": "Are different quotation templates required by customer sector, product type, or project type?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.2",
          "prompt": "Which specifications, performance, exclusions, warranty, payment, delivery, duration, maintenance, and assumption elements must appear in a quotation?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "08.3",
          "prompt": "Is electronic signature or approval by link required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.4",
          "prompt": "Can one order include equipment, parts, services, installation, recurring visits, and subscriptions?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.5",
          "prompt": "Is an advance payment required before confirming the Sales Order, and what percentage?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "08.6",
          "prompt": "Must the customer’s purchase order or formal request be attached?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.7",
          "prompt": "Can inventory be reserved before payment, and for how long?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.8",
          "prompt": "Do large orders require Projects, Tasks, or Milestones?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "08.9",
          "prompt": "Should an installation plan or Maintenance Schedule be created automatically after order confirmation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "08.10",
          "prompt": "What rules apply to cancelling or changing an order after reservation, preparation, or dispatch?",
          "response_type": "open response",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "09",
      "title": "Delivery, installation, and commissioning",
      "description": "Define scheduling, technician evidence, material movement, completion states, and commissioning.",
      "roles": [
        "operations",
        "field",
        "inventory"
      ],
      "areas": [
        "field",
        "operations"
      ],
      "questions": [
        {
          "id": "09.1",
          "prompt": "Who creates installation appointments and assigns technicians or teams?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "09.2",
          "prompt": "Is scheduling based on region, skill, equipment, parts, customer availability, travel, workload, or priority?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.3",
          "prompt": "Are service windows used, and is urgent service available at an additional charge?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.4",
          "prompt": "Which fields must appear on the installation work order?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.5",
          "prompt": "Which pre-departure, arrival, safety, commissioning, and handover checklists are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.6",
          "prompt": "Must technicians scan the QR code or Serial Number for every installed system and component?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.7",
          "prompt": "Must technicians record components consumed, returned, damaged, transferred, and vehicle inventory changes?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.8",
          "prompt": "Which before-and-after photographs, signatures, readings, times, and test evidence are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.9",
          "prompt": "What constitutes a completed installation, and what partial, blocked, or failed states are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.10",
          "prompt": "When is the Delivery Note created, and can delivery occur without installation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.11",
          "prompt": "Should warranty and replacement schedules activate automatically at installation completion?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "09.12",
          "prompt": "What should CAP do in scheduling, routing, duration estimation, parts warnings, abnormal-result detection, or repeat-visit prediction?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "10",
      "title": "Installed equipment and lifecycle tracking",
      "description": "Create the durable record of equipment, configuration, readings, transfers, replacements, and predictions.",
      "roles": [
        "operations",
        "field",
        "quality",
        "technology"
      ],
      "areas": [
        "equipment",
        "maintenance"
      ],
      "questions": [
        {
          "id": "10.1",
          "prompt": "What should be the primary record for each installed system?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.2",
          "prompt": "Should each installed system link to customer, site, components, contract, warranty, maintenance, and installation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.3",
          "prompt": "Can configuration change over time, and how should additions, removals, and substitutions be recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.4",
          "prompt": "Which commissioning data must be stored?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.5",
          "prompt": "Should consumption, operating hours, flow, pressure, IoT, temperature, and alarm history be retained?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.6",
          "prompt": "What is the replacement interval for each component, and what variables determine it?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.7",
          "prompt": "Can equipment be transferred between locations, customers, or legal entities, and what approval is required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.8",
          "prompt": "How are complete replacement, return, refurbishment, resale, disposal, scrap, and supplier return handled?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.9",
          "prompt": "Should the system create a unified equipment timeline from purchase through disposal?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "10.10",
          "prompt": "Should CAP predict component failure or replacement dates, and what confidence level is required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "11",
      "title": "Inventory and warehouses",
      "description": "Map physical and logical warehouses, stock rules, counts, reservations, valuation, and forecasts.",
      "roles": [
        "inventory",
        "operations",
        "finance"
      ],
      "areas": [
        "inventory",
        "operations"
      ],
      "questions": [
        {
          "id": "11.1",
          "prompt": "Which physical and logical Warehouses are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.2",
          "prompt": "Should each technician vehicle be a separate Warehouse?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.3",
          "prompt": "Which Items are critical and must not run out?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.4",
          "prompt": "What Reorder Level, Safety Stock, Lead Time, minimum quantity, and maximum stock values apply, and is current data reliable?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.5",
          "prompt": "Are recurring transfers performed between Warehouses, and who approves them?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "11.6",
          "prompt": "Is counting performed using barcode or QR, and how often?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.7",
          "prompt": "How are variances, damage, theft, expiry, loss, quality failure, and unknown movement recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.8",
          "prompt": "Is inventory reserved for specific orders, contracts, customers, or projects?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.9",
          "prompt": "Must cartridges, chemicals, or consumables be tracked by Batch and expiry?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.10",
          "prompt": "Which valuation or issue policies are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.11",
          "prompt": "Which actual, projected, reserved, slow-moving, fast-moving, near-reorder, expiry, and accuracy reports are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "11.12",
          "prompt": "What should CAP do in demand forecasting, replenishment, anomaly detection, stock distribution, excess stock, or shortage prediction?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "12",
      "title": "Procurement and suppliers",
      "description": "Define supplier records, sourcing, approvals, import costs, inspections, claims, and CAP support.",
      "roles": [
        "inventory",
        "finance",
        "operations"
      ],
      "areas": [
        "procurement",
        "inventory"
      ],
      "questions": [
        {
          "id": "12.1",
          "prompt": "Which supplier types are used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.2",
          "prompt": "Which supplier identity, tax, currency, payment, contact, bank, certification, lead-time, and warranty data is mandatory?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.3",
          "prompt": "Are Requests for Quotation sent to multiple suppliers?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.4",
          "prompt": "Which supplier-selection criteria are used, and how should they be weighted?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.5",
          "prompt": "What approval limits apply to Material Requests, RFQs, and Purchase Orders?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "12.6",
          "prompt": "Is procurement local, international, or both, and what shipment, customs, freight, insurance, duty, landed-cost, and delay data is required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.7",
          "prompt": "Is quality inspection performed on receipt, and what outcomes are possible?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.8",
          "prompt": "Are Batch and Serial Numbers supplied by the vendor or generated internally?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.9",
          "prompt": "How are supplier claims handled for defective or returned components?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.10",
          "prompt": "Are price agreements, Blanket Orders, minimum quantities, volume commitments, or exclusivity arrangements used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "12.11",
          "prompt": "What should CAP do in supplier evaluation, delay prediction, supplier recommendation, price or quality change detection, or unusual purchasing detection?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "13",
      "title": "Quality and technical compliance",
      "description": "Define standards, inspections, non-conformities, calibration, evidence, indicators, and pattern detection.",
      "roles": [
        "quality",
        "operations",
        "field",
        "governance"
      ],
      "areas": [
        "quality",
        "compliance"
      ],
      "questions": [
        {
          "id": "13.1",
          "prompt": "Which standards, certifications, licences, and regulatory requirements apply?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "13.2",
          "prompt": "Are Quality Inspection Templates required for each equipment or component type?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.3",
          "prompt": "Which inspections are required on receipt, before and after installation, after maintenance, before handover, and after repair?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.4",
          "prompt": "Who may accept or reject an inspection result?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "13.5",
          "prompt": "How are non-conformities, corrective actions, and preventive actions recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.6",
          "prompt": "Are TDS, pH, pressure, flow, and other measuring devices calibrated regularly?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.7",
          "prompt": "Must calibration-certificate numbers and expiry dates be tracked?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.8",
          "prompt": "Are retained samples or laboratory reports linked to a Batch, site, customer, or installed system?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.9",
          "prompt": "Which quality indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "13.10",
          "prompt": "Should CAP detect defect patterns by supplier, Batch, technician, model, region, water type, or installation method?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "14",
      "title": "Warranty, claims, and returns",
      "description": "Map warranty periods, start points, invalidation, claims, costs, replacements, returns, and misuse signals.",
      "roles": [
        "operations",
        "field",
        "finance",
        "quality"
      ],
      "areas": [
        "warranty",
        "service"
      ],
      "questions": [
        {
          "id": "14.1",
          "prompt": "What is the warranty period for each equipment type, component, and service?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.2",
          "prompt": "When does warranty begin?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "14.3",
          "prompt": "What invalidates warranty?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "14.4",
          "prompt": "Is warranty linked to the Serial Number?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.5",
          "prompt": "What are the steps in a Warranty Claim from opening through decision and closure?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.6",
          "prompt": "Who pays for site visit, component, labour, transport, laboratory analysis, and replacement in each scenario?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "14.7",
          "prompt": "Is approval required before replacing a component or complete system, and what limits apply?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.8",
          "prompt": "How is a replaced component recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.9",
          "prompt": "What is the return and replacement policy during the allowable return period?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "14.10",
          "prompt": "Should CAP identify possible misuse, repeated claims, unusual warranty behaviour, fraud indicators, or product-quality patterns, and by what criteria?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "15",
      "title": "Preventive maintenance, contracts, and subscriptions",
      "description": "Define service products, intervals, schedules, visit content, tiers, billing, renewal, reminders, and CAP support.",
      "roles": [
        "operations",
        "field",
        "sales",
        "finance"
      ],
      "areas": [
        "maintenance",
        "contracts"
      ],
      "questions": [
        {
          "id": "15.1",
          "prompt": "Which service types are offered?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.2",
          "prompt": "Is maintenance sold as an individual visit, Annual Maintenance Contract, Subscription Plan, usage-based service, warranty service, or other form?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.3",
          "prompt": "What service or replacement intervals are used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.4",
          "prompt": "Do intervals vary by water type, usage, equipment model, or customer category?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "15.5",
          "prompt": "What should automatically create a Maintenance Schedule?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.6",
          "prompt": "What checklist is required for each visit type?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.7",
          "prompt": "Which materials, tools, and components are expected for each visit type?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.8",
          "prompt": "Are contract tiers such as Gold, Silver, and Bronze offered, and what differs?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.9",
          "prompt": "Do contracts include specific components, visit limits, response commitments, exclusions, labour limits, distance limits, or emergency service?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "15.10",
          "prompt": "How is service invoiced?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.11",
          "prompt": "How are renewal, suspension, freezing, cancellation, and reactivation handled?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.12",
          "prompt": "Should automatic reminders be sent to customers and technicians, through which channels, and when?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "15.13",
          "prompt": "Should CAP personalize replacement intervals, predict non-renewal, recommend retention offers, detect missed visits, or identify likely service failure, and what limits apply?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "16",
      "title": "Customer service, issues, and service-level agreements",
      "description": "Map intake channels, issue types, priorities, SLAs, escalation, customer access, CAP support, and human-only decisions.",
      "roles": [
        "service",
        "operations",
        "sales",
        "governance"
      ],
      "areas": [
        "service",
        "customers"
      ],
      "questions": [
        {
          "id": "16.1",
          "prompt": "Through which channels are service issues received?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.2",
          "prompt": "Which Issue types are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.3",
          "prompt": "What priority levels and criteria are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.4",
          "prompt": "What response and resolution targets apply to each priority or customer category?",
          "response_type": "ranked priorities",
          "priority": "standard"
        },
        {
          "id": "16.5",
          "prompt": "Which conditions pause the SLA clock?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "16.6",
          "prompt": "How does escalation work, and who receives alerts when breach is approaching?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "16.7",
          "prompt": "Should an Issue automatically link to customer, site, equipment, Serial Number, contract, previous visits, warranty, and installation history?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.8",
          "prompt": "Does the employee need a summarized timeline before responding?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "16.9",
          "prompt": "Is customer satisfaction measured after closure, and by which measure?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.10",
          "prompt": "May customers open and track Issues and upload photographs through the Customer Portal?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.11",
          "prompt": "What should CAP do in classification, summarization, solution suggestion, repetition detection, SLA prediction, sentiment, or missing-evidence detection?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "16.12",
          "prompt": "Which decisions must remain entirely human and never be executed by CAP?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "17",
      "title": "Technician management and field operations",
      "description": "Define skills, shifts, teams, assets, time, task acceptance, closure evidence, quality review, KPIs, and recommendations.",
      "roles": [
        "field",
        "operations",
        "service"
      ],
      "areas": [
        "field",
        "people"
      ],
      "questions": [
        {
          "id": "17.1",
          "prompt": "Which skills, licences, certifications, and equipment authorizations does each technician possess?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "17.2",
          "prompt": "What working hours, shifts, leave rules, and service territories apply?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "17.3",
          "prompt": "Are multi-technician teams used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.4",
          "prompt": "Must vehicles, tools, and mobile inventory be tracked?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.5",
          "prompt": "Should travel, labour, and waiting time be recorded separately?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.6",
          "prompt": "Are different labour rates used for overtime, emergencies, or distant locations?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.7",
          "prompt": "Must technicians accept or reject assigned tasks and provide a reason?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.8",
          "prompt": "Which evidence is mandatory before a technician may close a visit?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.9",
          "prompt": "How is technician work reviewed, and how are repeat visits and quality failures handled?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.10",
          "prompt": "Which technician performance indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "17.11",
          "prompt": "Should CAP recommend the technician, appointment time, and route, and explain the factors behind the recommendation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "18",
      "title": "Invoicing, collection, and accounting",
      "description": "Define currencies, taxes, integrations, invoice timing, payments, debt, commissions, credits, profitability, and financial alerts.",
      "roles": [
        "finance",
        "executive",
        "sales"
      ],
      "areas": [
        "finance",
        "accounting"
      ],
      "questions": [
        {
          "id": "18.1",
          "prompt": "Which currencies are used, and are multi-currency transactions required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.2",
          "prompt": "Which taxes and fees apply by country, sector, product, or service?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "18.3",
          "prompt": "Is integration required with electronic invoicing, payment providers, banks, point-of-sale, tax authority, or other systems?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "18.4",
          "prompt": "When is the Sales Invoice created?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.5",
          "prompt": "Are partial invoices, milestone payments, retentions, or staged payments required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.6",
          "prompt": "Which payment methods are accepted?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.7",
          "prompt": "How is a Payment Entry linked to Sales Orders, Sales Invoices, advances, contracts, installments, and credit notes?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.8",
          "prompt": "What policies govern debt, collection, reminders, suspension, and service stoppage?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "18.9",
          "prompt": "Are commissions linked to actual collection?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.10",
          "prompt": "How are Credit Notes, returns, rebates, and later discounts handled?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.11",
          "prompt": "Which profitability dimensions are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "18.12",
          "prompt": "Should CAP predict late payment or detect unusual financial transactions, and what boundaries apply?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "19",
      "title": "Website, online store, and digital channels",
      "description": "Map public channels, stock and pricing display, scheduling, portals, campaigns, automation, and content approval.",
      "roles": [
        "sales",
        "marketing",
        "technology",
        "service"
      ],
      "areas": [
        "digital",
        "sales"
      ],
      "questions": [
        {
          "id": "19.1",
          "prompt": "Is there an existing website or online store, and which platform is used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.2",
          "prompt": "Does the website display actual stock, estimated stock, branch availability, or no stock information?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "19.3",
          "prompt": "Can customers schedule site surveys, installation, maintenance, laboratory analysis, or consultation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.4",
          "prompt": "Are prices public, or must customers request a quotation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.5",
          "prompt": "Should online orders create Sales Orders automatically?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.6",
          "prompt": "Is a distributor portal or login-based special pricing required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.7",
          "prompt": "Should the Customer Portal display orders, invoices, deliveries, issues, contracts, maintenance, installed equipment, and warranty?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.8",
          "prompt": "Which marketing channels should be linked to Lead source and campaign?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.9",
          "prompt": "Are automatic messages sent through email, WhatsApp, or SMS, and for which events?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "19.10",
          "prompt": "Should CAP generate personalized content or messages, and what approval is required before sending?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "20",
      "title": "Reports and dashboards",
      "description": "Define report audiences, operational indicators, CAP presentation, proactive alerts, and export authority.",
      "roles": [
        "executive",
        "operations",
        "sales",
        "inventory",
        "finance",
        "service",
        "quality"
      ],
      "areas": [
        "reporting",
        "governance"
      ],
      "questions": [
        {
          "id": "20.1",
          "prompt": "Who uses reports?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "20.2",
          "prompt": "Which management indicators are required daily, weekly, and monthly?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.3",
          "prompt": "Which sales indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.4",
          "prompt": "Which operational indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.5",
          "prompt": "Which inventory indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.6",
          "prompt": "Which service indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.7",
          "prompt": "Which contract indicators are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.8",
          "prompt": "Which profitability measures are required by business dimension?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.9",
          "prompt": "Are proactive alert reports required in addition to historical reports?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "20.10",
          "prompt": "How should CAP outputs present score, reason, confidence, factors, evidence, action, owner, deadline, and escalation?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "20.11",
          "prompt": "Who may download or export reports containing personal, financial, or confidential data?",
          "response_type": "roles / owners",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "21",
      "title": "Existing data, migration, and cleansing",
      "description": "Inventory sources, scale, history, identifiers, quality, merge authority, files, minimization, and acceptance.",
      "roles": [
        "technology",
        "operations",
        "finance",
        "governance"
      ],
      "areas": [
        "data",
        "migration"
      ],
      "questions": [
        {
          "id": "21.1",
          "prompt": "What are the current data sources?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "21.2",
          "prompt": "Approximately how many customers, Items, suppliers, invoices, orders, installed systems, Issues, contracts, and attachments exist?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "21.3",
          "prompt": "What is the earliest date that must be migrated?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.4",
          "prompt": "Should migration include detailed history, opening balances, open transactions, master data, or selected history?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.5",
          "prompt": "Are there customer, Item, Serial Number, or document identifiers that must be preserved?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.6",
          "prompt": "What level of duplication, missing data, or error is expected?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.7",
          "prompt": "Who has authority to merge or reject duplicate records?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "21.8",
          "prompt": "Are photographs, contracts, laboratory reports, certificates, or other files required to be linked?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.9",
          "prompt": "Must old data be deleted, masked, anonymized, or excluded before being sent to CAP?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "21.10",
          "prompt": "What are the migration acceptance criteria?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "22",
      "title": "External integrations",
      "description": "Identify connected systems, credentials, frequencies, devices, identity, criticality, recovery, and ownership.",
      "roles": [
        "technology",
        "operations",
        "finance"
      ],
      "areas": [
        "integrations",
        "technology"
      ],
      "questions": [
        {
          "id": "22.1",
          "prompt": "Which systems must be integrated?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.2",
          "prompt": "Are APIs available, and who owns credentials, contracts, and access rights?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "22.3",
          "prompt": "Must sensor or meter readings be imported in real time, periodically, on demand, or manually?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.4",
          "prompt": "Which barcode, QR, label, point-of-sale, measurement, mobile, or other hardware must be integrated?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.5",
          "prompt": "Is Single Sign-On or Active Directory required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.6",
          "prompt": "Must ERPNext integrate with an existing accounting system instead of using ERPNext Accounting fully?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.7",
          "prompt": "Which integrations are business-critical and would stop operations if unavailable?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.8",
          "prompt": "What retry, alert, reconciliation, and exception process is required when an integration fails?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "22.9",
          "prompt": "Who monitors integration logs and errors?",
          "response_type": "roles / owners",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "23",
      "title": "CAP role and artificial-intelligence use cases",
      "description": "Define CAP correctly, select use cases, bind outputs to evidence, set confidence thresholds, and prohibit unsafe actions.",
      "roles": [
        "executive",
        "governance",
        "technology",
        "operations"
      ],
      "areas": [
        "cap",
        "ai-governance"
      ],
      "questions": [
        {
          "id": "23.1",
          "prompt": "Confirm the formal operating name: Canonical Attestation Platform — CAP.",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "23.2",
          "prompt": "Is ERPNext the System of Record for operational business transactions?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.3",
          "prompt": "What actions may CAP perform: read, analyse, recommend, summarize, draft, create tasks or alerts, propose updates, or execute only after approval?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "23.4",
          "prompt": "What are the first five CAP use cases, ranked by priority?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "23.5",
          "prompt": "For each use case, what decision is improved, who owns it, what harm could an error cause, and what evidence is required?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "23.6",
          "prompt": "Which ERPNext DocTypes and fields are required for each use case?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.7",
          "prompt": "Which additional files, messages, photographs, sensors, maps, laboratory data, or external sources are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.8",
          "prompt": "What form should each CAP output take?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.9",
          "prompt": "What minimum confidence is required before display, and when must an output be hidden, qualified, or escalated?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.10",
          "prompt": "Must CAP show the evidence, records, sources, and factors supporting its output?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "23.11",
          "prompt": "Must every model run record inputs, source IDs, model, version, configuration, output, confidence, time, human decision, and final action?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "23.12",
          "prompt": "How should acceptance, rejection, override, and reasons be recorded?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.13",
          "prompt": "Are CAP outputs advisory only, or may CAP execute after explicit human approval?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "23.14",
          "prompt": "Which actions are prohibited for CAP?",
          "response_type": "decision with explanation",
          "priority": "critical"
        }
      ]
    },
    {
      "id": "24",
      "title": "Data flow from ERPNext to CAP",
      "description": "Define the event contract, minimization, provenance, ordering, identity, replay, authentication, and forbidden data.",
      "roles": [
        "technology",
        "governance",
        "operations"
      ],
      "areas": [
        "cap",
        "integrations",
        "data"
      ],
      "questions": [
        {
          "id": "24.1",
          "prompt": "Which ERPNext DocTypes should be sent during the first phase?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.2",
          "prompt": "Should transfer use Webhooks, REST polling, scheduled export, event stream, or a combination?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.3",
          "prompt": "Which events are important for each DocType?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.4",
          "prompt": "Should the complete record or selected fields only be transmitted?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.5",
          "prompt": "Should attachments and photographs be transmitted, or only secure references and access permissions?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.6",
          "prompt": "How are correlation_id, source_id, company, branch, tenant, record version, source system, and actor identity defined?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.7",
          "prompt": "Must event order, previous versions, or a cryptographic hash chain be preserved?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.8",
          "prompt": "How should CAP handle duplicate, retried, late, out-of-order, or partial events?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.9",
          "prompt": "Is an initial historical backfill required, and what period and record types are included?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.10",
          "prompt": "What is the maximum acceptable delay between an ERPNext event and arrival in CAP?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.11",
          "prompt": "What Dead Letter Queue, error log, retry, and reprocessing mechanism is required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.12",
          "prompt": "How is webhook signature or API identity verified?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "24.13",
          "prompt": "Will a dedicated least-privilege API user be used?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "24.14",
          "prompt": "Which data must never be sent to CAP?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "25",
      "title": "Returning CAP outputs to ERPNext",
      "description": "Define where outputs appear, immutable result records, lifecycle, authority, versioning, customer release, and evaluation.",
      "roles": [
        "technology",
        "governance",
        "operations"
      ],
      "areas": [
        "cap",
        "integrations"
      ],
      "questions": [
        {
          "id": "25.1",
          "prompt": "Where should CAP outputs appear in ERPNext?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.2",
          "prompt": "Should custom DocTypes such as CAP Model Run, Recommendation, Insight, Attestation, and Review Decision be created?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.3",
          "prompt": "Which type, source, score, confidence, explanation, evidence, action, status, owner, expiry, model version, and source version fields are mandatory?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "25.4",
          "prompt": "Can one recommendation link to multiple ERPNext records?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.5",
          "prompt": "Must the original CAP result remain immutable while later human decisions are added separately?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.6",
          "prompt": "Which recommendation lifecycle states are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.7",
          "prompt": "Who may accept or reject each recommendation type?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "25.8",
          "prompt": "Does acceptance create a draft transaction, actual transaction, task, notification, or no automated object?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "25.9",
          "prompt": "How is a revised, withdrawn, or superseded recommendation handled when data or model output changes?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "25.10",
          "prompt": "May CAP results be sent to customers, and who approves wording before release?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "25.11",
          "prompt": "Which measures are required to evaluate CAP accuracy and commercial value?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "26",
      "title": "Data governance, privacy, and security",
      "description": "Classify data, define lawful use, hosting, model boundaries, masking, retention, rights, encryption, secrets, review, incidents, and separation.",
      "roles": [
        "governance",
        "technology",
        "executive"
      ],
      "areas": [
        "privacy",
        "security"
      ],
      "questions": [
        {
          "id": "26.1",
          "prompt": "How is data classified?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.2",
          "prompt": "Which personal data is collected, and for what purpose?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.3",
          "prompt": "What legal basis or customer consent permits AI-assisted analysis?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "26.4",
          "prompt": "Where must ERPNext, CAP, and backups be hosted?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.5",
          "prompt": "Is transmission of data to external or cloud models prohibited?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "26.6",
          "prompt": "Must personal identifiers be masked or tokenized before processing?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.7",
          "prompt": "What retention period applies to each data type, and when must it be deleted, anonymized, or archived?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.8",
          "prompt": "Do customers have rights to access, correction, deletion, objection, restriction, or portability?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "26.9",
          "prompt": "What encryption is required in transit, at rest, in backups, on mobile devices, and in exports?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.10",
          "prompt": "How are API keys, passwords, private keys, and other secrets managed, and who may access them?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "26.11",
          "prompt": "How frequently are permissions, login records, and exports reviewed?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.12",
          "prompt": "What is the incident-response plan for leaks, breaches, incorrect model data, unauthorized export, compromised accounts, or incorrect recommendations?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "26.13",
          "prompt": "Must data for companies, branches, or institutional customers be separated logically or physically?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "27",
      "title": "Model governance and human risk",
      "description": "Approve models, test them, measure them, understand error cost and bias, prevent invention, monitor drift, and retain human control.",
      "roles": [
        "governance",
        "technology",
        "executive",
        "quality"
      ],
      "areas": [
        "ai-governance",
        "risk"
      ],
      "questions": [
        {
          "id": "27.1",
          "prompt": "Which models and providers are permitted, and are local models available?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "27.2",
          "prompt": "Who approves adding or updating a model?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "27.3",
          "prompt": "Must a model be tested on historical data before production use?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "27.4",
          "prompt": "Which acceptance measures apply to each use case?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "27.5",
          "prompt": "What error rate is acceptable, and what are the costs of false positives and false negatives?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "27.6",
          "prompt": "Could customer groups, regions, languages, or conditions be affected by biased data?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "27.7",
          "prompt": "How will CAP be prevented from inventing technical specifications, unsupported claims, or nonexistent evidence?",
          "response_type": "open response",
          "priority": "critical"
        },
        {
          "id": "27.8",
          "prompt": "Must users review the supporting source before accepting a sensitive recommendation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "27.9",
          "prompt": "How will model drift be detected over time?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "27.10",
          "prompt": "What is the immediate kill-switch process for disabling a model and returning to manual operation?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "27.11",
          "prompt": "Who reviews samples, rejected recommendations, overrides, and feedback, and how frequently?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "27.12",
          "prompt": "Is a documented decision record required showing inputs, outputs, evidence, and human approval?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "28",
      "title": "Technical architecture and operations",
      "description": "Choose deployment architecture, environments, availability, scale, recovery, monitoring, RACI, customization, and localization.",
      "roles": [
        "technology",
        "operations",
        "governance"
      ],
      "areas": [
        "technology",
        "operations"
      ],
      "questions": [
        {
          "id": "28.1",
          "prompt": "Which Frappe and ERPNext versions are targeted, and what hosting model will be used?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.2",
          "prompt": "Will CAP operate in the same environment, as a separate service, on a local QWOS node, in a hybrid architecture, or another form?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "28.3",
          "prompt": "Which development, test, staging, production, disaster-recovery, and training environments are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.4",
          "prompt": "What operating hours and uptime are required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.5",
          "prompt": "What daily transaction, record, event, attachment, model-run, user, and API-call volume is expected?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.6",
          "prompt": "What backup, recovery, RTO, and RPO requirements apply?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "28.7",
          "prompt": "Is unified monitoring required for logs, metrics, alerts, security, integrations, model performance, and backups?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.8",
          "prompt": "Who is responsible for operations, updates, security, backups, support, model governance, and incident response?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "28.9",
          "prompt": "Is High Availability or a disaster-recovery site required?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.10",
          "prompt": "How will customizations be managed so ERPNext upgrades remain safe?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "28.11",
          "prompt": "Is a dedicated Frappe application required instead of scattered Client Scripts and manual customization?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "28.12",
          "prompt": "What Arabic, English, printing, localization, and right-to-left requirements apply?",
          "response_type": "open response",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "29",
      "title": "Workflows, approvals, and exceptions",
      "description": "Formalize states, transitions, thresholds, exceptions, post-submit changes, automation, CAP influence, priority, and overrides.",
      "roles": [
        "executive",
        "operations",
        "governance",
        "technology"
      ],
      "areas": [
        "workflow",
        "governance"
      ],
      "questions": [
        {
          "id": "29.1",
          "prompt": "Which transactions require formal Workflow control?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "29.2",
          "prompt": "What are the states for each Workflow, and who may move a record between states?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "29.3",
          "prompt": "What approval limits apply by value, discount, quantity, cost, margin, risk, or customer category?",
          "response_type": "open response",
          "priority": "standard"
        },
        {
          "id": "29.4",
          "prompt": "Which emergency exceptions are permitted, and how must they be documented?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "29.5",
          "prompt": "May records be changed after Submit, and who approves cancellation or amendment?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "29.6",
          "prompt": "Which events should automatically create a ToDo, Notification, Escalation, review request, approval request, or incident record?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "29.7",
          "prompt": "Are CAP recommendations a mandatory condition, advisory information, review trigger, risk indicator, or prohibited from affecting Workflow automatically?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "29.8",
          "prompt": "What takes priority when a CAP recommendation conflicts with manager decision, policy, contract, regulation, or safety rule?",
          "response_type": "ranked priorities",
          "priority": "standard"
        },
        {
          "id": "29.9",
          "prompt": "Must the user record a reason when overriding or ignoring a CAP recommendation?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    },
    {
      "id": "30",
      "title": "Priorities, pilot plan, and acceptance criteria",
      "description": "Turn discovery into a bounded pilot with data, measures, blockers, training, sign-off, support, and deferred scope.",
      "roles": [
        "executive",
        "operations",
        "technology",
        "governance"
      ],
      "areas": [
        "pilot",
        "strategy"
      ],
      "questions": [
        {
          "id": "30.1",
          "prompt": "Rank the implementation priority of CRM, Selling, Stock, Buying, Accounting, Support, Maintenance, Portal, CAP, Reporting, Integrations, and other modules.",
          "response_type": "ranked priorities",
          "priority": "standard"
        },
        {
          "id": "30.2",
          "prompt": "Which branch, team, or process is best suited for the Pilot, and why?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "30.3",
          "prompt": "What minimum data is required before Pilot launch?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "30.4",
          "prompt": "Which processes may temporarily remain manual, and which cannot accept a manual workaround?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "30.5",
          "prompt": "What are the target Pilot duration, users, customers, installed systems, service cases, and transactions?",
          "response_type": "numbers / estimate",
          "priority": "standard"
        },
        {
          "id": "30.6",
          "prompt": "What are the Pilot success indicators?",
          "response_type": "decision with explanation",
          "priority": "critical"
        },
        {
          "id": "30.7",
          "prompt": "Which defects or conditions prevent Go-Live?",
          "response_type": "open response",
          "priority": "critical"
        },
        {
          "id": "30.8",
          "prompt": "What training is required for each role?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "30.9",
          "prompt": "Who signs off on acceptance of each module?",
          "response_type": "roles / owners",
          "priority": "standard"
        },
        {
          "id": "30.10",
          "prompt": "What is the post-launch support and escalation plan?",
          "response_type": "decision with explanation",
          "priority": "standard"
        },
        {
          "id": "30.11",
          "prompt": "Which customizations should be deferred to Phase 2 rather than forced into Phase 1?",
          "response_type": "decision with explanation",
          "priority": "standard"
        }
      ]
    }
  ],
  "principles": [
    "ERPNext is the System of Record for operational business transactions.",
    "CAP is the governance, evidence, provenance, recommendation, model-run, human-review, and attestation layer surrounding those transactions.",
    "A recommendation is not a decision. Receipt is not acceptance. Acceptance is not execution. Execution is not automatically entry into institutional Canon."
  ]
};
