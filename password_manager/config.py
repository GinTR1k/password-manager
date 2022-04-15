from pathlib import Path

from dynaconf import Dynaconf

# settings = Dynaconf(
#     settings_files=['settings.toml'],
# )

# VAULT_FILE_PATH = Path(settings.vault_file_path)
VAULT_FILE_PATH = Path('./vault.gpassman')
IV = b'\x80\x1cD\xd8\xe3\xaf\xf6\x16\xf2\x98\xba\xae\xf14\x95\x00\x14\x1e\xed+vX`\x9c\xdc\x9aJ]\x1d\xe2\x1f.QV\xa7'
