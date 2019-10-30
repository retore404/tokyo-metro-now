# APIキーについて
-/common/common 配下にsettings_secret.pyを配置し，SECRET_API_KEYにAPIキーを格納する．（テンプレートをsettings_secret_template.pyとして配置済み．）
- settings.pyに"from .settings_secret import *"を追加することで格納したAPIキーをインポート．
- settings.pyで API_KEY = SECRET_API_KEY とする．
- views.pyなどでは，from django.conf import settingsでインポートした上でgetattr(settings, "API_KEY", None)でAPIキーを取得可能．