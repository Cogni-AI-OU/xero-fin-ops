"""
Shared utilities for Xero scripts.

This module provides common functionality used across multiple Xero scripts.
"""

import sys
from xero_python.identity import IdentityApi


def resolve_tenant(api_client, tenant_id_arg=None, tenant_index=None):
    """
    Resolve and return a tenant ID from available connections.

    Args:
        api_client: Xero API client instance
        tenant_id_arg: Optional specific tenant ID to use
        tenant_index: Optional 1-based index of tenant connection to use

    Returns:
        str: The resolved tenant ID

    Exits:
        If no connections are found, tenant ID is not found, or index is out of range
    """
    identity_api = IdentityApi(api_client)
    connections = identity_api.get_connections()

    if not connections:
        print("No connections found.", file=sys.stderr)
        sys.exit(1)

    if tenant_id_arg:
        for conn in connections:
            if getattr(conn, "tenant_id", None) == tenant_id_arg:
                print(
                    f"Using Tenant: {getattr(conn, 'tenant_name', tenant_id_arg)} ({tenant_id_arg})",
                    file=sys.stderr,
                )
                return tenant_id_arg
        print(f"Tenant ID {tenant_id_arg} not found among connections.", file=sys.stderr)
        sys.exit(1)

    if tenant_index:
        idx = tenant_index - 1
        if idx < 0 or idx >= len(connections):
            print(f"Tenant index {tenant_index} is out of range (1-{len(connections)}).", file=sys.stderr)
            sys.exit(1)
        chosen = connections[idx]
        print(
            f"Using Tenant: {getattr(chosen, 'tenant_name', '')} ({getattr(chosen, 'tenant_id', '')})",
            file=sys.stderr,
        )
        return chosen.tenant_id

    chosen = connections[0]
    tenant_name = getattr(chosen, "tenant_name", "")
    tenant_id = getattr(chosen, "tenant_id", "")
    print(
        f"Using Tenant: {tenant_name} ({tenant_id})",
        file=sys.stderr,
    )
    return tenant_id
