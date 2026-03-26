# Configured Tools

> See [Recipe Index](INDEX.md) for all recipes.

Model forensic tools with specific configurations — command-line flags, rulesets, external configuration files. Based on [CASE-Examples/configured_tool](https://github.com/casework/CASE-Examples/tree/master/examples/illustrations/configured_tool).

## Key classes

| Class | Role |
|---|---|
| `AnalyticTool` | The base tool (e.g., IDA Pro, Volatility) |
| `ConfiguredTool` | A specific configuration of the base tool |
| `Configuration` + `ConfigurationEntry` | The configuration parameters |
| `InvestigativeAction` | The analysis action using the configured tool |

## Pattern

```
AnalyticTool (base tool)
    ▲
    │ isConfigurationOf
    │
ConfiguredTool
    │
    └── usesConfiguration ──▶ Configuration
                                   └── ConfigurationEntry (flag/value pairs)
                                   └── ConfigurationEntry (itemObject → File for rulesets)
```

<details open><summary>Python</summary>

```python
from case_uco import CASEGraph
from case_uco.case.investigation import InvestigativeAction
from case_uco.uco.identity import Identity
from case_uco.uco.tool import AnalyticTool, ConfiguredTool
from case_uco.uco.configuration import Configuration, ConfigurationEntry
from case_uco.uco.observable import ObservableObject, File, FileFacet

graph = CASEGraph()

# Base tool
base_tool = graph.create(AnalyticTool,
    name="...",       # tool name from source
    version="...",    # from source
    tool_type="...",  # e.g. "Reverse Engineering"
)

# Configuration with parameter entries
config = Configuration(
    configuration_entry=[
        ConfigurationEntry(
            item_name="...",   # flag/parameter name from source
            item_value=["..."],  # value from source
        ),
        ConfigurationEntry(
            item_name="...",
            item_value=["..."],
        ),
    ],
)

# Configured variant of the tool
configured = graph.create(ConfiguredTool,
    name="...",  # descriptive name for this configuration
    is_configuration_of=base_tool,
    uses_configuration=config,
)

# For configurations that reference external files (rulesets, scripts)
ruleset = graph.create(File,
    has_facet=[FileFacet(file_name="...", file_path="...")],
)
file_config = Configuration(
    configuration_entry=[
        ConfigurationEntry(
            item_name="...",        # e.g. "ruleset"
            item_object=[ruleset],  # reference to the file
        ),
    ],
)

# Use the configured tool in an action
analyst = graph.create(Identity, name="...")  # from source
action = graph.create(InvestigativeAction,
    name="...",
    description=["..."],
    performer=analyst,
    instrument=[configured],
    object=[...],  # artifacts being analyzed
)

graph.write("configured_tool.jsonld")
```

</details>

## Notes

- `ConfiguredTool` inherits from `Tool` and adds `is_configuration_of` (points to the base `Tool`) and `uses_configuration` (points to a `Configuration`).
- `ConfigurationEntry` has `item_name` (str), `item_value` (list[str]), and `item_object` (list[UcoObject]) for referencing files or other objects.
- Create multiple `ConfiguredTool` instances for different configurations of the same base tool.
