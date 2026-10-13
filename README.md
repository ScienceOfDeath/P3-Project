# P3-Project | Agentic AI Vulnerabilities

A quantitative evaluation framework assessing autonomous AI coding agents' tendency to introduce security flaws in Flask applications. The testing suite maps generated applications against **OWASP Top 25** and **CWE** taxonomies using OpenGrep and manual evaluation.

## Architecture
```
├── baseline/             # Reference implementations per scenario
├── CWE-22/               ### CWE Block 
├── CWE-.../              # Context, prompts,
├── CWE-.../              # variations and scenarios
├── CWE-502/              ### CWE Block
├── testing-suite/        # Automated test suites & verification harnesses
└── results/              # Aggregated metric outputs & vulnerability matrices
```
## Methodology
½. **Scenario**: Each scenario is developed and based on existing vulnerable code suggested by CWE, OWASP, CodeQL or OpenGrep and modified by us.
1. **Generation**: Target LLM/agent generates the Flask application code.
2. **Automated Testing**: The testing suite executes analysis and static assertions against the generated artifact.
3. **Manual Testing**: The testing suite flags app to be evaluated manually.
4. **Taxonomy Mapping**: Failures are classified using CWE identifiers and mapped to OWASP risk categories.
