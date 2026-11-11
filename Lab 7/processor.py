
def parse_storage_quota(quota_str):
    """Parse storage quota into GB safely."""
    if not isinstance(quota_str, str) or not quota_str.strip():
        return "Invalid quota"

    cleaned = quota_str.strip().upper()

    if len(cleaned) <= 2:
        return "Invalid quota"

    val_str = cleaned[:-2]
    unit = cleaned[-2:]

    multipliers = {
        "MB": 0.001,
        "GB": 1.0,
        "TB": 1000.0
    }

    if unit not in multipliers:
        return "Invalid quota"

    try:
        value = float(val_str)
        if value < 0:
            return "Invalid quota"
    except ValueError:
        return "Invalid quota"

    gb_total = value * multipliers[unit]
    return f"Quota: {gb_total:.2f} GB"


def compute_compression_ratio(size_metric_str):
    """Calculate compression ratio safely."""
    if not isinstance(size_metric_str, str):
        return 0.0

    try:
        parts = size_metric_str.split(':')
        if len(parts) != 2:
            return 0.0

        raw_bytes = float(parts[0])
        comp_bytes = float(parts[1])

        if comp_bytes <= 0 or raw_bytes < 0:
            return 0.0

        ratio = raw_bytes / comp_bytes

        if not float('inf') > ratio:
            return 0.0

        return round(ratio, 2)

    except (ValueError, ZeroDivisionError):
        return 0.0


def lookup_bandwidth_tier_rate(tier_descriptor):
    """Look up bandwidth tier rate safely."""
    if not isinstance(tier_descriptor, str):
        return 0.0

    prefix = tier_descriptor.strip().upper()[:3]

    tier_rates = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }

    return tier_rates.get(prefix, 0.0)
def main():
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    print(parse_storage_quota(q_input))

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    print("Compression Ratio:", compute_compression_ratio(c_input))

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    print("Rate per GB: $", lookup_bandwidth_tier_rate(t_input))


if __name__ == "__main__":
    main()
