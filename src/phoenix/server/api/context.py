from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import AsyncContextManager, Callable, List, Optional, Tuple, Union

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.dataloader import DataLoader

from phoenix.core.model_schema import Model
from phoenix.db import models
from phoenix.server.api.input_types.TimeRange import TimeRange
from phoenix.server.api.types.DocumentRetrievalMetrics import DocumentRetrievalMetrics
from phoenix.server.api.types.Evaluation import DocumentEvaluation, SpanEvaluation, TraceEvaluation


@dataclass
class DataLoaders:
    latency_ms_quantile: DataLoader[Tuple[int, Optional[TimeRange], float], Optional[float]]
    span_evaluations: DataLoader[int, List[SpanEvaluation]]
    document_evaluations: DataLoader[int, List[DocumentEvaluation]]
    trace_evaluations: DataLoader[int, List[TraceEvaluation]]
    document_retrieval_metrics: DataLoader[
        Tuple[int, Optional[str], int], List[DocumentRetrievalMetrics]
    ]
    span_descendants: DataLoader[str, List[models.Span]]


@dataclass
class Context:
    request: Union[Request, WebSocket]
    response: Optional[Response]
    db: Callable[[], AsyncContextManager[AsyncSession]]
    data_loaders: DataLoaders
    model: Model
    export_path: Path
    corpus: Optional[Model] = None
    streaming_last_updated_at: Callable[[], Optional[datetime]] = lambda: None
