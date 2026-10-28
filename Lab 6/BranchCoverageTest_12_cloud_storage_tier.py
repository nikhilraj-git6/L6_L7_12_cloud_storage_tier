
import pytest
from cloud_storage_tier import (
    process_storage_tenants,
    monitor_replication_latency,
)


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_storage_tenants("invalid", 10)
    with pytest.raises(ValueError):
        process_storage_tenants([], -1)


def test_tenant_and_tier_branches():
    tenants = [
        {"account_active": False, "tier": "hot"},
        {"account_active": True, "tier": "hot",
         "buckets": [{"size_gb": 100, "egress_gb": 100}]},
        {"account_active": True, "tier": "cool",
         "buckets": [{"size_gb": 600, "egress_gb": 150}]},
        {"account_active": True, "tier": "archive",
         "buckets": [{"size_gb": 100, "corrupted": True}]},
        {"account_active": True, "tier": "invalid"},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["status"] in ("BILLED", "AUDIT_FLAGGED")


def test_bucket_size_corruption_and_egress():
    tenants = [
        {"account_active": True, "tier": "hot",
         "has_backup_vault": True,
         "buckets": [
             {"size_gb": 0},
             {"size_gb": -1},
             {"size_gb": 501, "egress_gb": 101},
             {"size_gb": 100, "corrupted": True, "egress_gb": 0},
         ]},
    ]
    result = process_storage_tenants(tenants, 5)
    assert result["status"] == "BILLED"
    assert result["total_billed"] > 0


def test_archive_corruption():
    result = process_storage_tenants(
        [{"account_active": True, "tier": "archive",
          "buckets": [{"size_gb": 100, "corrupted": True}]}],
        0,
    )
    assert result["status"] == "ZERO_USAGE"


def test_audit_and_zero_usage():
    invalid = [{"account_active": True, "tier": "hot",
                "buckets": [{"size_gb": 0}] * 5}]
    assert process_storage_tenants(invalid, 0)["status"] == "AUDIT_FLAGGED"
    assert process_storage_tenants([], 0)["status"] == "ZERO_USAGE"


def test_latency_all_branches():
    assert monitor_replication_latency([]) == "NO_DATA"
    assert monitor_replication_latency([[]]) == "SYNCED"
    assert monitor_replication_latency([[100, 201, 100]]) == "SYNCED"
    assert monitor_replication_latency([[201, 201]]) == "SYNC_LAG_ALERT"
    assert monitor_replication_latency([[201], [201, 201]]) == "SYNC_LAG_ALERT"
