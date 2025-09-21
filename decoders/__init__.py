import importlib
import pkgutil
from .base import DECODER_REGISTRY

package_dir = __path__[0]
for _, name, is_pkg in pkgutil.iter_modules([package_dir]):
    if is_pkg:
        importlib.import_module(f"{__name__}.{name}.decoder")

# Adds all the supported decoders to the decoder registry.
# Allows for easy expansion of the supported makes.
# To add a new make, just add a new package and extend the base decoder class.