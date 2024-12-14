import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML


def extract_lineage(sql_query: str):

    # remove comments from sql statements
    sql_query = sqlparse.format(sql_query, strip_comments=True).strip()

    parsed = sqlparse.parse(sql_query)[0]

    tables = []
    columns = []

    for statement in parsed.tokens:
        if statement.ttype is DML and statement.value.upper() in (
            "SELECT",
            "INSERT",
            "UPDATE",
            "DELETE",
        ):
            for token in statement.tokens:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        columns.append(identifier.get_name())
                elif isinstance(token, Identifier):
                    if token.value.upper() not in (
                        "FROM",
                        "WHERE",
                        "GROUP BY",
                        "ORDER BY",
                        "HAVING",
                        "SELECT",
                        "INSERT",
                        "UPDATE",
                        "DELETE",
                    ):  # added filter conditions
                        columns.append(token.get_name())
                elif token.ttype is Keyword and token.value.upper() == "FROM":

                    # table_name can be subquery. so we need to check if the next token is identifier or not
                    next_ = token.token_next(0)
                    if isinstance(next_, IdentifierList):
                        for identifier in next_.get_identifiers():
                            tables.append(str(identifier))
                    elif isinstance(next_, Identifier):
                        tables.append(str(next_))

    return {
        "tables": list(set(tables)),
        "columns": list(set(columns)),
    }  # Remove duplicates
