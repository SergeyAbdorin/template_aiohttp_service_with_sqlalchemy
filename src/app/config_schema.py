from trafaret import Bool, Dict, Int, String

MINIMAL_USERSPACE_PORT = 1001


schema = Dict({
    'service': Dict({
        'name': String,
        'version': String,
        'component': String,
        'port': Int(gte=MINIMAL_USERSPACE_PORT),
        'debug': Bool,
    }),
    'logging': Dict().allow_extra('*'),
    'env_prefix': String,
})
