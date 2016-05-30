def preconfigure(config):
    # Default configuration values.
    config.GEOZONES_LEVELS = ['fr/region', 'fr/county', 'fr/town']
    config.GEOZONES_MAX_IMPORTANCE = {
        'fr/region': 11898502,
        'fr/county': 2830000,
        'fr/town': 2249975
    }
