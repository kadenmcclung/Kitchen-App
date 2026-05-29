# tests/test_imports.py

def test_kivy_import():
    import kivy
    assert kivy is not None


def test_app_modules_import():
    import main
    main.run_test_mode()