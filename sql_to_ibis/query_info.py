from typing import Dict, List, Optional, Tuple

from sql_to_ibis.parsing.transformers import InternalTransformer
from sql_to_ibis.sql_objects import Aggregate, Value


class QueryInfo:
    """
    Class that holds metadata extracted / derived from a sql query
    """

    def __init__(
        self,
        having_expr,
        where_expr,
        internal_transformer: InternalTransformer,
        distinct: bool = False,
    ):
        self.columns: List[Value] = []
        self.table_names: List[str] = []
        self.all_names: List[str] = []
        self.name_order: Dict[str, int] = {}
        self.aggregates: Dict[str, Aggregate] = {}
        self.group_columns: List[str] = []
        self.where_expr = where_expr
        self.distinct = distinct
        self.having_expr = having_expr
        self.internal_transformer: InternalTransformer = internal_transformer
        self.order_by: List[Tuple[str, bool]] = []
        self.limit: Optional[int] = None

    @staticmethod
    def set_none_var(value, default):
        return default if not value else value

    def __repr__(self):
        return (
            f"Query Information\n"
            f"-----------------\n"
            f"Columns: {self.columns}\n"
            f"Tables names: {self.table_names}\n"
            f"All names: {self.all_names}\n"
            f"Name order: {self.name_order}\n"
            f"Aggregates: {self.aggregates}\n"
            f"Group columns: {self.group_columns}\n"
        )
