# contract_audit.py

Dataclass contract verification tool for Mercury AI V1 integrity audit.

Features:
- Extract all @dataclass/@dataclass(frozen=True) definitions
- Verify field types, defaults, and required status
- Check all consumers for contract violations
- Detect missing/extra/mismatched fields
- Identify incorrect enum usage
- Track field access patterns

Output:
- Contract violation reports
- Field type mismatches
- Missing required fields
- Enum type errors
- Unused dataclass instances
- Field access violations