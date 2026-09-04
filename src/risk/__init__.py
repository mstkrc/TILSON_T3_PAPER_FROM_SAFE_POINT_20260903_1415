"""Risk permission and concurrency models; no execution behavior."""

from .permission import PermissionResult, evaluate_permission

__all__ = ["PermissionResult", "evaluate_permission"]
