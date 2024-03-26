class PostNotFoundError(Exception):
    pass


class PostCommentNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistError(Exception):
    pass


class AuthenticationFailedError(Exception):
    pass

class AuthorizationFailedError(Exception):
    pass

class DuplicateUserError(Exception):
    pass
