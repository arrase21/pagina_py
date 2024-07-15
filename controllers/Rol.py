from models.Models import Rol, db


def initialize():
    roles = [
        {"id_rol": 1, "description": "Admin"},
        {"id_rol": 2, "description": "User"},
    ]

    for rol_data in roles:
        rol = Rol.query.get(rol_data["id_rol"])
        if not rol:
            new_rol = Rol(
                id_rol=rol_data["id_rol"], description=rol_data["description"]
            )
            db.session.add(new_rol)
    db.session.commit()
