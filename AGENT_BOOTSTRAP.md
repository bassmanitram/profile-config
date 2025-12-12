# profile-config - Agent Bootstrap

**Purpose**: Manage hierarchical configuration files with profile-based inheritance and variable interpolation
**Type**: Library
**Language**: Python 3.8+
**Repository**: https://github.com/bassmanitram/profile-config

---

## What You Need to Know

**This is**: A configuration discovery and merging library that walks up directory trees finding config files, merges them with proper precedence, resolves profile inheritance chains (with cycle detection), and applies variable interpolation via OmegaConf. Enables applications to have multiple configuration profiles (dev, staging, prod) with hierarchical overrides.

**Architecture in one sentence**: Discovery (walk up tree) → Load (multi-format) → Merge (closest wins) → Resolve Profile Chain → Apply Overrides → Interpolate Variables → Inject Environment.

**The ONE constraint that must not be violated**: Profile inheritance must be acyclic - circular inheritance detection is critical and must never be bypassed.

---

## Mental Model

- Think of this as **cascading configuration** with profiles - like CSS specificity rules
- Files closer to CWD override files higher up (./config.yaml beats ../config.yaml)
- Profiles can inherit from other profiles (staging → base), inheritance is recursive
- **OmegaConf** handles variable interpolation (`${variable}` syntax) - happens after all merging
- Environment variable injection is **optional** (set `os.environ` from config section)

---

## Codebase Organization

```
profile_config/
├── resolver.py      # ProfileConfigResolver - main API facade
├── discovery.py     # ConfigDiscovery - hierarchical file finding
├── loader.py        # ConfigLoader - multi-format parsing (YAML/JSON/TOML)
├── profiles.py      # ProfileResolver - inheritance chain resolution with cycle detection
├── merger.py        # ConfigMerger - OmegaConf-based merging and interpolation
├── exceptions.py    # Custom exceptions (ProfileNotFound, CircularInheritance, etc.)
└── tests/           # Comprehensive test suite with temporary directory fixtures
```

**Navigation Guide**:

| When you need to... | Start here | Why |
|---------------------|------------|-----|
| Change file discovery logic | `discovery.py` → `discover_configs()` | Walks up directory tree |
| Add new file format | `loader.py` → `load_config()` | Format detection and loading |
| Modify merge behavior | `merger.py` → `merge_configs()` | Uses OmegaConf, wraps it |
| Fix inheritance resolution | `profiles.py` → `resolve_profile()` | Cycle detection and chain building |
| Add configuration option | `resolver.py` → `__init__()` | Main API entry point |

**Entry points**:
- Main execution: `ProfileConfigResolver(config_name, profile).resolve()` - Returns merged config dict
- Tests: `tests/` - Use temporary directories with fixture files

---

## Critical Invariants

These rules MUST be maintained:

1. **Acyclic profile inheritance**: No circular inheritance chains allowed
   - **Why**: Prevents infinite loops during resolution, ensures deterministic config
   - **Breaks if violated**: Stack overflow or infinite loop during `resolve()`
   - **Enforced by**: `profiles.py` tracks visited profiles, raises `CircularInheritanceError`

2. **File precedence: closest to CWD wins**: Files lower in tree override higher
   - **Why**: Enables project-specific overrides of system-wide configs
   - **Breaks if violated**: Config behavior becomes unpredictable, overrides don't work
   - **Enforced by**: `discovery.py` orders files by depth, `merger.py` applies in order

3. **Interpolation happens last**: Variable substitution after all merging complete
   - **Why**: Variables might reference keys from other files in hierarchy
   - **Breaks if violated**: Variables resolve too early, get wrong values or undefined errors
   - **Enforced by**: `resolver.py` orchestrates: merge first, interpolate after

---

## Non-Obvious Behaviors & Gotchas

Things that surprise people:

1. **`defaults` section applies to ALL profiles**:
   - **Why it's this way**: Common base configuration shared across all profiles
   - **Common mistake**: Expecting `defaults` to only apply when no profile specified
   - **Correct approach**: Use `defaults` for truly global config, use inheritance for profile-specific sharing

2. **Profile "default" auto-creates if requested but not defined**:
   - **Why**: Convenience - requesting "default" profile always succeeds
   - **Watch out for**: Auto-created "default" only contains `defaults` section (no profile-specific config)
   - **Pattern**: If you define explicit "default" profile, it overrides this behavior

3. **Environment variable injection is opt-in but ON by default**:
   - **Why**: Most use cases want config to set environment (DATABASE_URL, API_KEY, etc.)
   - **Watch out for**: Sets `os.environ` globally, affects entire process
   - **Correct approach**: Use `apply_environment=False` if you don't want this, or `override_environment=True` to force overwrite existing vars

4. **Overrides can be dicts, file paths, or list of both**:
   - **Why**: Maximum flexibility for different use cases (runtime overrides, test fixtures, CI config)
   - **Pattern**: List is applied in order, later overrides earlier
   - **Gotcha**: File path overrides are loaded and merged, not just stored as strings

---

## Architecture Decisions

**Why walk up directory tree instead of explicit config path?**
- **Trade-off**: Implicit discovery is "magical" but enables hierarchical overrides without complex configuration
- **Alternative considered**: Require explicit config file path
- **Why discovery wins**: Enables system-wide config in `~/.myapp/` overridden by project-specific `./myapp/`, all automatic

**Why OmegaConf instead of simple dict merging?**
- **Trade-off**: Heavy dependency but gets variable interpolation, type safety, validation for free
- **Alternative considered**: Custom dict merge + string.Template or manual `${var}` replacement
- **Implications**: We're bound to OmegaConf's behavior (mostly good, but sometimes surprising)

**Why support multiple formats (YAML, JSON, TOML)?**
- **Trade-off**: More parsing code but maximizes adoption
- **Alternative considered**: YAML only (most common) or JSON only (stdlib)
- **Why multi-format wins**: Different teams prefer different formats, TOML is popular in Python ecosystem

---

## Key Patterns & Abstractions

**Pattern 1: Facade (ProfileConfigResolver)**
- **Used for**: Hiding complexity of discovery → load → merge → resolve → interpolate pipeline
- **Structure**: Single class orchestrates all subsystems, users call one method: `resolve()`
- **Examples in code**: `resolver.py` delegates to discovery, loader, merger, profiles modules

**Pattern 2: Template Method (resolve pipeline)**
- **Used for**: Standardizing the resolution process
- **Structure**: Fixed sequence: discover → load → merge files → resolve profile → merge profile → apply overrides → interpolate
- **Why**: Each step depends on previous, order is critical

**Anti-pattern to avoid: Mutating resolved config**
- **Don't do this**: `config = resolver.resolve(); config['key'] = 'value'`
- **Why it fails**: Changes aren't persisted, next resolve() call returns original
- **Instead**: Use `overrides` parameter: `resolver = ProfileConfigResolver(..., overrides={'key': 'value'})`

---

## State & Data Flow

**State management**:
- **Persistent state**: Configuration files on filesystem (this library reads them)
- **Runtime state**: Resolver holds configuration (immutable after resolve()), OmegaConf DictConfig objects
- **No state here**: Discovery, Loader, Merger are stateless - resolver orchestrates them

**Data flow**:
```
CWD → Discovery (walk up) → List[Path]
                              ↓
                         Loader (parse) → List[Dict]
                              ↓
                         Merger (combine) → Base Config Dict
                              ↓
                    Profile Resolver (inheritance) → Profile Config Dict
                              ↓
                         Merger (apply overrides) → Final Dict
                              ↓
                    OmegaConf (interpolate ${vars}) → Resolved Dict
                              ↓
                    Environment Injector → os.environ updated
```

**Critical paths**: Cycle detection in profile inheritance must happen before merging - circular references would cause infinite loop.

---

## Integration Points

**This project depends on** (upstream):
- **omegaconf**: Configuration merging and interpolation, tightly coupled (core functionality)
- **pyyaml**: YAML parsing, tightly coupled (primary format)
- **tomli** (Python <3.11): TOML parsing, loosely coupled (optional format)

**Projects that depend on this** (downstream):
- **yacba**: Uses profile-config for hierarchical chatbot configuration
- **Your Python applications**: Configuration management system

**Related projects** (siblings):
- **dataclass-args**: CLI args vs profile-config's files - complementary configuration sources
- **envlog**: Similar environment-based philosophy, different domain (logging vs app config)

---

## Configuration Philosophy

**What's configurable**: Search paths, file extensions, profile filename, inheritance key name, interpolation toggle, environment variable behavior

**What's hardcoded**:
- Directory walk algorithm (up from CWD, then home)
- Merge strategy (closest to CWD wins)
- OmegaConf as interpolation engine
- Profile inheritance resolution algorithm

**Configuration sources** (precedence):
1. Runtime `overrides` parameter - Highest
2. Current directory config - Project-specific
3. Parent directory configs - Intermediate
4. Home directory config - User defaults
5. `defaults` section in any file - Base values

**The trap**: Forgetting that `defaults` section merges with EVERY profile. If you put database connection in `defaults`, it's in production config too. Use profile inheritance instead.

---

## Testing Strategy

**What we test**:
- **Discovery**: File finding at various directory depths, home directory, missing configs
- **Profile resolution**: Single inheritance, multi-level chains, cycle detection, missing profiles
- **Merging**: Precedence rules, override application, interpolation
- **Environment variables**: Injection, skipping existing, override mode

**What we don't test**:
- **OmegaConf internals**: Trust upstream library works
- **Filesystem reliability**: Assume reads succeed (mocked failures covered)

**Test organization**: Each module has corresponding test file (test_discovery.py, test_profiles.py, etc.). Heavy use of `tmp_path` fixture for isolated filesystem tests.

**Mocking strategy**: Minimal mocking - use real files in temp directories (easier to debug, more realistic). Mock only when simulating errors (file permissions, I/O failures).

---

## Common Problems & Diagnostic Paths

**Symptom**: Config not found error
- **Most likely cause**: Wrong config name or no config files in directory hierarchy
- **Check**: Print `resolver.get_config_files()` to see what was discovered
- **Fix**: Create config file in `./myapp/config.yaml` or verify config_name matches directory name

**Symptom**: Profile inheritance not working
- **Likely cause**: Typo in `inherits` key or profile name
- **Diagnostic**: Call `resolver.list_profiles()` to see available profiles
- **Solution approach**: Verify profile names match exactly (case-sensitive)

**Symptom**: Variable interpolation not resolving (`${var}` appears in output)
- **Why it happens**: Variable not defined in merged config or interpolation disabled
- **Diagnostic**: Check if variable exists in final merged config before interpolation
- **Solution**: Define variable in config file or use `enable_interpolation=False` to disable

**Symptom**: Circular inheritance error
- **Why it happens**: Profile A inherits B, B inherits C, C inherits A
- **Diagnostic**: Error message shows the cycle
- **Solution**: Break the cycle - remove one inheritance link, use `defaults` for shared config instead

---

## Modification Patterns

**To add new file format** (e.g., INI):
1. Add parser in `loader.py` → `_load_ini()` function
2. Add `.ini` to default extensions list
3. Update `load_config()` to dispatch to INI parser
4. Add tests in `tests/test_loader.py` or new `tests/test_ini_support.py`

**To change precedence rules** (e.g., home directory wins instead of current):
1. Modify `discovery.py` → `discover_configs()` to change ordering
2. Update `merger.py` if merge strategy needs to change
3. **Critical**: Update all tests that assume current precedence
4. Document as breaking change (major version bump required)

**To add new resolver option** (e.g., custom interpolation syntax):
1. Add parameter to `ProfileConfigResolver.__init__()`
2. Pass to appropriate subsystem (merger for interpolation)
3. Add tests in `tests/test_resolver.py`
4. Document in README.md API section

---

## When to Update This Document

Update this bootstrap when:
- [x] Discovery algorithm changes (e.g., stop at project root, add custom search paths)
- [x] Profile inheritance mechanism changes (e.g., multiple inheritance support)
- [x] Merge strategy changes (e.g., deep merge instead of shallow)
- [x] Major dependency added/removed (e.g., replace OmegaConf)

Don't update for:
- ❌ New file format support (extends existing pattern)
- ❌ New resolver options (extends configuration)
- ❌ Bug fixes in discovery, loading, or merging
- ❌ Test additions or refactoring
- ❌ Documentation updates

---

**Last Updated**: 2025-12-03
**Last Architectural Change**: v1.3.0 - Added environment variable injection feature
