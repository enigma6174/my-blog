def find(_db, _id, _table):
    try:
        query = _db.query(_table).filter(_table.bid == _id)
        post = query.first()
        if not post:
            raise Exception(f"No data found for id {_id}")
    except Exception as e:
        raise e
    else:
        return post


def insert(_db, _post):
    try:
        _db.add(_post)
        _db.commit()
        _db.refresh(_post)
    except Exception as e:
        _db.rollback()
        raise e
    else:
        return _post


def update(_db, _id, _table, _payload):
    try:
        query = _db.query(_table).filter(_table.bid == _id)
        if not query.first():
            raise Exception(f"No data found for id {_id}")

        query.update(_payload, synchronize_session=False)
        _db.commit()
    except Exception as e:
        _db.rollback()
        raise e
    else:
        return query.first()


def delete(_db, _id, _table):
    try:
        query = _db.query(_table).filter(_table.bid == _id)
        if not query.first():
            raise Exception(f"No data found for id {_id}")
        query.delete(synchronize_session=False)
        _db.commit()
    except Exception as e:
        _db.rollback()
        raise e
