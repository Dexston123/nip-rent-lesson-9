import json
import random
from typing import Any

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
CONFIG = {"currency": "PLN", "tax": 0.23, "late_fee": 50}

example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(
    path: str = "data/apartments.json",
    cache: list[dict] | None = None,
) -> list[dict]:
    if path is None:
        print("No path provided")
        return []
    if cache is None:
        cache = []
    if cache:
        return cache
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            cache.extend(data)
    except FileNotFoundError:
        print(f"File {path} not found")
        return []
    return cache


class RentManager:
    def __init__(
        self,
        name: str,
        apartments: list[dict] | None = None,
        tenants: dict[str, dict] | None = None,
    ):
        self.name = name
        self.apartments = apartments or []
        self.tenants = tenants or {}
        self.history: list[dict[str, Any]] = []
        self._last_error: str | None = None

    def add_tenant(self, tenant_id: str, tenant: dict[str, Any]) -> bool:
        if tenant_id in self.tenants:
            print(f"Tenant {tenant_id} already exists")
            return False
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(
        self,
        tenant_id: str,
        month: int,
        year: int,
        discount: float = 0.0,
    ) -> float | None:
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            return None
        base = tenant.get("rent", 0)
        utilities = tenant.get("utilities", 0)
        total = base + utilities
        total -= total * discount
        # Leap year adjustment for February
        if month == 2 and year % 4 == 0:
            total += 1
        if total == 0:
            print("Warning: total bill is 0")
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id: str, days: int) -> None:
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            print(f"Tenant {tenant_id} not found")
            return
        fee = CONFIG["late_fee"] if days > 7 else 0
        tenant["overdue_days"] = days
        tenant["late_fee"] = fee

    def export_summary(self, output_file: str = "summary.txt") -> str:
        lines = [
            f"Tenant: {item['tenant']} Month: {item['month']} Year: {item['year']} Total: {item['total']}"
            for item in self.history
        ]
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return output_file


def random_adjustments(values: list[int]) -> list[int]:
    return [v + random.randint(-5, 5) for v in values if 0 <= v <= 1000]


def normalize_names(names: list[str]) -> list[str]:
    return [n.strip().title() for n in names if n.strip()]


async def fake_api_call(
    payload: Any,
    retries: int = 3,
    timeout: int = 30,
) -> dict[str, Any]:
    for i in range(retries):
        try:
            if i == 1:
                raise ValueError("network")
            return {"status": "ok", "payload": payload}
        except Exception:
            continue
    return {"status": "error"}


def pretty_print_tenants(tenants: dict[str, dict]) -> None:
    for k, v in tenants.items():
        print(k, v)


def do_many_things(
    data: dict,
    flag: bool = True,
    x: int = 10,
    y: int = 20,
    z: int = 30,
) -> dict[Any, Any]:
    output: dict[Any, Any] = {i: i * i for i in range(1, 6)}
    for name in ["alice", "bob", "charlie", "dan"]:
        output[name] = name.upper() if flag else name.lower()
    if x + y + z > 50 and x * y * z > 5000:
        print("Complex condition met")
    for i in [1, 2, 3]:
        print(i)
    print("Ambiguous vars:", 1 + 2 + 3)
    return output


def parse_amount(amount: str) -> float:
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except ValueError as e:
        print("Parse error:", e)
        return 0.0


def dead_code_example(x: int) -> str:
    if x < 0:
        return "negative"
    if x == 0:
        return "zero"
    return "positive"


def main() -> None:
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    bill = manager.calculate_bill("T1", 2, 2024, discount=0.1)
    print("Bill:", bill)

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")

    print(do_many_things({"x": 1}, True, 12, 25, 30))
    print(parse_amount(" 1234.50 PLN "))


if __name__ == "__main__":
    main()
