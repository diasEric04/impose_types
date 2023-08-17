

class ArgsLengthDontMatch(Exception):
    def __init__(self, type, len_args, len_kwargs):
        super().__init__(
            f'args length of {type} dont match: '
            f'func len={len_args}; decorator len='
            f'{len_kwargs}'
        )


class TypesDontMatch(Exception):
    def __init__(self, type, type_args_types, value_args_types):
        super().__init__(
            f'the types of {type} dont match: '
            f'func types={type_args_types}; decorator types='
            f'{value_args_types}'
        )


class KwargsKeysDontMatch(Exception):
    def __init__(self, kwargs_keys, typed_kwargs_keys):
        super().__init__(
            f'the kwargs\'s keys dont match: '
            f'func kwargs keys={kwargs_keys}; decorator kwargs keys='
            f'{typed_kwargs_keys}'
        )
