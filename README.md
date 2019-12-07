# APIキーについて
- /common 配下にlocal_settings.pyを配置し，以下のように記述
    ```python
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
    DEBUG = True
    
    SECRET_KEY = '[APIキーをここに書く]'
    ```
- local_settings.pyはgit管理外とする（.gitignore）
- settings.pyでlocal_settings.pyのimportを試み，成功すればlocal_settings.pyのKEYが読み込まれる．
- import失敗時は，settings.pyの設定からDEBUG=Falseとなるため，settings.py最下部のif文内で環境変数を読みに行く．
- 本番環境用にはHerokuで別途環境変数にAPIキーを指定すれば良い．