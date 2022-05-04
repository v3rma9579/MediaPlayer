import pathlib
import shutil

import PyInstaller.__main__

if __name__ == '__main__':
    APP_NAME = r'Simple Media Player'
    # APP_DIR aka ROOT DIR of the project
    APP_DIR = pathlib.PurePath(__file__).parents[1]
    # path to the main.py file
    APP_PATH = APP_DIR.joinpath('sources', 'main.py')
    ASSETS_DIR = APP_DIR.joinpath('assets')
    ICON_PATH = APP_DIR.joinpath(ASSETS_DIR, 'smp.ico')
    DIST_DIR = pathlib.Path(APP_DIR.joinpath('release'))
    try:
        DIST_DIR.mkdir(exist_ok=True)
        PyInstaller.__main__.run([
            fr'{APP_PATH}',
            '-i',
            fr'{ICON_PATH}',
            '-n',
            fr'{APP_NAME}',
            '--distpath',
            fr'{DIST_DIR}',
            '--add-data',
            f'{ASSETS_DIR};ASSETS',
            '--onedir',
            '--clean',
            '--noconsole',
            '--noconfirm'
        ])
        shutil.make_archive(fr'{APP_NAME}', 'zip', root_dir=fr'{DIST_DIR}')
    except FileExistsError as e:
        print('FAILED', e)
