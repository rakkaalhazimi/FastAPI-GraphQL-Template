from strawberry.exceptions import StrawberryGraphQLError



def create_strawberry_response_error(error: Exception, status_code: int):
    return StrawberryGraphQLError(
        message=str(error),
        extensions={
            "status_code": status_code,
        },
        original_error=error
    )