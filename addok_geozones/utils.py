from addok.helpers import yielder
from addok.config import config
from shapely.geometry import shape


@yielder
def prepare_document(doc):
    level = doc.get('level')
    if level not in config.GEOZONES_LEVELS:
        return
    doc['id'] = doc['_id']
    doc.update(doc.get('keys'))  # Flat doc.
    max_importance = config.GEOZONES_MAX_IMPORTANCE.get(level)
    if max_importance:
        doc['importance'] = (doc.get('population', 0) / max_importance)
    geom = shape(doc['geom'])
    doc['bounds'] = str(list(geom.bounds))
    center = geom.centroid
    doc['lat'] = center.y
    doc['lon'] = center.x
    del doc['geom']
    del doc['_id']
    del doc['keys']
    return doc
