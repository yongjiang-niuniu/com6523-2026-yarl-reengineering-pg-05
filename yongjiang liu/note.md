# Week 2 Notes — Black (psf/black)

## 1. Key functions of the system
Black is an “uncompromising” Python code formatter. Its main function is to take Python source code and rewrite it into a consistent formatting style (e.g., line wrapping, spacing, quote normalization depending on configuration), so developers do not need to manually format code.

Typical usage:
- Command-line tool: `black <path>`
- Used in CI / pre-commit to enforce formatting automatically.

## 2. Important packages / directories
- `black-main/src/black/`: core formatter implementation (main logic lives here).
- `black-main/src/black/__init__.py` and related modules: likely expose main API / version info.
- `tests/`: test suite (ignored for class diagrams in this lab, but useful to see expected behavior).
- Project metadata files (e.g., `pyproject.toml`): configuration and packaging.

## 3. Key classes (from pyreverse output)
From the generated class diagram (`classes_black.png`), several classes appear central to the formatting pipeline. These classes look like they represent:
- The formatting engine / state (how code is transformed)
- Data structures for handling lines, tokens, and formatting decisions
- Possible configuration-related objects

(Exact class list can be read directly from the UML diagram.)

## 4. Inheritance / abstract classes / top of hierarchy
The class diagram suggests a relatively flat inheritance structure compared to large frameworks. Any base classes at the top of hierarchies are likely utility/data structure base types rather than deep OO frameworks.

## 5. Frequently used classes/functions (evidence)
- Core formatting entry points are expected to be called often (format file / format string functions).
- The CLI entry point is frequently used in normal workflows.
Evidence:
- The package diagram (`packages_black.png`) shows which modules import others, highlighting central modules.

## 6. Obvious design patterns
- Pipeline-style processing: source code -> parse -> transform -> re-render.
- Separation of concerns: CLI layer vs formatting logic vs utilities.

## 7. Potential problematic design aspects / smells (initial scan)
- Formatting tools often require complex rule logic; risk of large modules or highly coupled functions.
- Some modules may contain dense transformation logic that is harder to modify (potential maintainability hotspots).
- However, the project appears mature and well-structured, so code smells may be limited.

## 8. Recommendation to my group
Black is a good candidate because:
- Clear purpose and scope (formatting)
- Well-structured, widely used, and has clear entry points
- UML diagrams are manageable and helpful for comprehension
Possible downside: formatting rules can be intricate, but for reengineering analysis the structure is still tractable.

## Appendix: tool commands used
- `pyreverse -o png -p black --ignore=tests --filter-mode=PUB_ONLY --colorized ./black-main/src/black`
