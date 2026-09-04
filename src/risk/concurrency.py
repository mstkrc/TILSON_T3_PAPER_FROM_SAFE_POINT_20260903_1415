"""Per-symbol preparation lock only."""

from threading import Lock


class SymbolLockRegistry:
    def __init__(self):
        self._locks: dict[str, Lock] = {}

    def acquire(self, symbol: str) -> bool:
        lock = self._locks.setdefault(symbol, Lock())
        return lock.acquire(blocking=False)

    def release(self, symbol: str) -> None:
        lock = self._locks.get(symbol)
        if lock and lock.locked():
            lock.release()

    def is_locked(self, symbol: str) -> bool:
        lock = self._locks.get(symbol)
        if not lock:
            return False
        acquired = lock.acquire(blocking=False)
        if acquired:
            lock.release()
            return False
        return True
