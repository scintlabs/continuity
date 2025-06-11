from __future__ import annotations

from enum import Enum
from datetime import timedelta
from typing import Callable, List, Optional

from attrs import define, field

from base.core.helpers import timestamp
from base.schema.context import Metadata
from base.schema.messages import Content


THREAD_TIMEOUT = timedelta(minutes=30)


class ThreadTransition(Enum):
    CREATED = {"created": lambda: timestamp()}
    ENCODED = {"encoded": lambda: timestamp()}
    ARCHIVED = {"archived": lambda: timestamp()}
    PRUNED = {"pruned": lambda: timestamp()}

    def __init__(self, event):
        self.event = event

    def __call__(self, content: str = None):
        if content is not None:
            self.event["content"] = content
        return self.event


@define
class Thread:
    content: List[Content] = field(factory=list)
    prev: Optional[Thread] = field(default=None)
    next: Optional[Thread] = field(default=None)

    async def update(self, content: Content, *, embed: List[float] | None = None):
        self.content.append(content)
        if embed is not None:
            self.metadata.embedding = embed

    def transition(self):
        if self._NEXT is None or self._EVENT_AFTER is None:
            raise NotImplementedError("Subclass didn’t set _NEXT/_EVENT_AFTER")
        nxt = self._NEXT(
            metadata=self.metadata,
            prev=self.prev,
            next=self.next,
            content=self._transform_content(),
        )
        nxt._record(self._EVENT_AFTER)
        return nxt

    def _record(self, event: ThreadTransition, msg: str | None = None):
        self.metadata.events.append(event(msg) if msg else event())


@define
class Threads:
    maxlen: int = 0
    index_threshold: int = 10
    encode_threshold: int = 20
    should_index: Callable[[Thread], bool] = lambda self, t: False
    head: Optional[Thread] = None
    tail: Optional[Thread] = None
    counts: dict[str, int] = field(default=None)

    def append(self, *, metadata: Metadata = None, left: bool = False):
        node = Thread(metadata or Metadata())
        node._record(ThreadTransition.ACTIVATED)

        if self.head is None:
            self.head = self.tail = node
        elif left:
            node.next, self.head.prev = self.head, node
            self.head = node
        else:
            node.prev, self.tail.next = self.tail, node
            self.tail = node

        self._bump(Thread, +1)
        self._maybe_rollover()
        return node

    def pop(self, *, left: bool = False):
        if self.head is None:
            raise IndexError("pop from empty Threads")
        node = self.head if left else self.tail
        self._detach(node)
        self._bump(type(node).__name__, -1)
        return node

    def walk(self, *types):
        cur = self.head
        while cur:
            if not types or isinstance(cur, types):
                yield cur
            cur = cur.next

    def _bump(self, name: str, d: int):
        self.counts[name] += d

    def _detach(self, n: Thread):
        if n.prev:
            n.prev.next = n.next
        else:
            self.head = n.next
        if n.next:
            n.next.prev = n.prev
        else:
            self.tail = n.prev
        n.prev = n.next = None

    def _maybe_rollover(self):
        self._rollover(Thread, self.maxlen, self._index)
        self._rollover(Thread, self.index_threshold, self._advance_stale)

    def _rollover(self, kind, limit: int, advance: Callable[[Thread], Thread]):
        while self.counts.get(kind, 0) > limit:
            node = self._oldest(kind)
            if node is None:
                break
            nxt = advance(node)
            self._replace(node, nxt)

    def _index(self, thread: Thread):
        nxt = Thread(
            metadata=thread.metadata,
            prev=thread.prev,
            next=thread.next,
            content=thread.content,
        )
        nxt._record(ThreadTransition.TimedOut)
        self._shift_counts(Thread, Thread)
        return nxt

    def _advance_stale(self, node: Thread):
        dequeue = self.should_index(node)
        nxt = node.transition(purge=dequeue)
        self._shift_counts(Thread, type(nxt).__name__)
        if dequeue:
            return nxt

        self._replace(node, nxt)
        self._rollover(Thread, self.encode_threshold, self._purge_encoded)
        return nxt

    def _shift_counts(self, frm, to):
        self.counts[frm] -= 1
        self.counts[to] += 1

    def _oldest(self, kind):
        cls = kind if isinstance(kind, type) else globals()[kind]
        cur = self.head
        while cur and not isinstance(cur, cls):
            cur = cur.next
        return cur

    def _replace(self, old: Thread, new: Thread):
        if old.prev:
            old.prev.next = new
        else:
            self.head = new
        if old.next:
            old.next.prev = new
        else:
            self.tail = new
        new.prev, new.next = old.prev, old.next
        old.prev = old.next = None
