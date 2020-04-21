#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


declared_permissions = db.Table(
    "declared_permissions",
    db.metadata,
    db.Column("apk_id", db.String(32), db.ForeignKey("apks.md5"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)

required_and_used_permissions = db.Table(
    "required_and_used_permissions",
    db.metadata,
    db.Column("apk_id", db.String(32), db.ForeignKey("apks.md5"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)

required_but_not_used_permissions = db.Table(
    "required_but_not_used_permissions",
    db.metadata,
    db.Column("apk_id", db.String(32), db.ForeignKey("apks.md5"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)

not_required_but_used_permissions = db.Table(
    "not_required_but_used_permissions",
    db.metadata,
    db.Column("apk_id", db.String(32), db.ForeignKey("apks.md5"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)


class Apk(db.Model):

    __tablename__ = "apks"

    md5 = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    source = db.Column(db.String(24), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    risk = db.Column(db.Float, nullable=False)

    declared_permissions = db.relationship(
        "Permission",
        secondary=declared_permissions,
        backref=db.backref("app_declaring", lazy="dynamic"),
    )

    required_and_used_permissions = db.relationship(
        "Permission",
        secondary=required_and_used_permissions,
        backref=db.backref("app_requiring_and_using", lazy="dynamic"),
    )

    required_but_not_used_permissions = db.relationship(
        "Permission",
        secondary=required_but_not_used_permissions,
        backref=db.backref("app_requiring_but_not_using", lazy="dynamic"),
    )

    not_required_but_used_permissions = db.relationship(
        "Permission",
        secondary=not_required_but_used_permissions,
        backref=db.backref("app_not_requiring_but_using", lazy="dynamic"),
    )

    def __repr__(self):
        return '<Apk (md5="{0}", name="{1}", risk="{2}")>'.format(
            self.md5, self.name, self.risk
        )


class Permission(db.Model):

    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Permission (name="{0}")>'.format(self.name)
