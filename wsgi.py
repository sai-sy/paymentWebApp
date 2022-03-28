if __name__=='__main__':
    from website import create_app, db
    from website.extensions_inits import load_preset_data

    def start():
        app = create_app()
        app.app_context().push()
        db.create_all()
        load_preset_data(app, db)

        return app

    app = start()
    app.run(host='0.0.0.0')
else:
    from .website import create_app, db
    from .website.extensions_inits import load_preset_data

    def start():
        app = create_app()
        app.app_context().push()
        db.create_all()
        load_preset_data(app, db)

        return app

    app = start()
    app.run(host='0.0.0.0')