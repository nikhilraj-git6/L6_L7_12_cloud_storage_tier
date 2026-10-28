
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


def test_inactive_and_unknown_tenants():
    tenants = [
        {"account_active": False, "tier": "hot"},
        {"account_active": True, "tier": "unknown"},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["status"] == "ZERO_USAGE"


def test_all_storage_tiers():
    tenants = [
        {"account_active": True, "tier": "hot",
         "buckets": [{"size_gb": 100, "egress_gb": 0}]},
        {"account_active": True, "tier": "cool",
         "buckets": [{"size_gb": 100, "egress_gb": 0}]},
        {"account_active": True, "tier": "archive",
         "buckets": [{"size_gb": 100, "egress_gb": 0}]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["total_billed"] == 4.5
    assert result["status"] == "BILLED"


def test_invalid_bucket_size_and_missing_values():
    tenants = [
        {"account_active": True, "tier": "hot",
         "buckets": [
             {"size_gb": 0},
             {"size_gb": -5},
             {},
         ]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["status"] == "ZERO_USAGE"


def test_large_bucket_egress_and_backup():
    tenants = [
        {"account_active": True, "tier": "hot",
         "has_backup_vault": True,
         "buckets": [
             {"size_gb": 600, "egress_gb": 150},
             {"size_gb": 100, "egress_gb": 50},
         ]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["total_billed"] == 30.0
    assert result["status"] == "BILLED"


def test_corrupted_non_archive_bucket():
    tenants = [
        {"account_active": True, "tier": "hot",
         "buckets": [
             {"size_gb": 100, "corrupted": True, "egress_gb": 0}
         ]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["total_billed"] == 0
    assert result["status"] == "ZERO_USAGE"


def test_corrupted_archive_bucket_stops_processing():
    tenants = [
        {"account_active": True, "tier": "archive",
         "buckets": [
             {"size_gb": 100, "corrupted": True, "egress_gb": 0},
             {"size_gb": 200, "egress_gb": 0},
         ]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["total_billed"] == 0
    assert result["status"] == "ZERO_USAGE"


def test_audit_flagged_after_many_invalid_buckets():
    tenants = [
        {"account_active": True, "tier": "hot",
         "buckets": [
             {"size_gb": 0},
             {"size_gb": 0},
             {"size_gb": 0},
             {"size_gb": 0},
             {"size_gb": 0},
         ]},
    ]
    result = process_storage_tenants(tenants, 10)
    assert result["status"] == "AUDIT_FLAGGED"


def test_latency_monitor():
    assert monitor_replication_latency([]) == "NO_DATA"
    assert monitor_replication_latency([[100, 250, 100]]) == "SYNCED"
    assert monitor_replication_latency([[250, 250]]) == "SYNC_LAG_ALERT"
    assert monitor_replication_latency([[250], [250, 250]]) == "SYNC_LAG_ALERT"
