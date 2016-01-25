from PMtools import db


class mzitemscode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'name %r' % (self.name)

    def get_name_uid(self):
        return self.name, self.uid


class ddtitemscode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    name_id = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'name %r' % (self.name)

    def get_name_uid(self):
        return self.name, self.name_id


class hxbnsitemscode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    names = db.Column(db.String(64), index=True)
    item_id = db.Column(db.String(64), index=True)

    def __repr__(self):
        return 'name %r' % (self.name)

    def get_name_names_itemid(self):
        return self.name, self.names, self.item_id
