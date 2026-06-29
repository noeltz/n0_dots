import os
from urllib.parse import unquote

from gi.repository import GObject, Nautilus


class KittyExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, window, files):
        return []

    def get_background_items(self, window, file):
        if file.get_uri_scheme() != "file":
            return []

        item = Nautilus.MenuItem(
            name="KittyExtension::OpenInKitty",
            label="Open in Kitty",
            tip="Open Kitty terminal in this directory",
        )
        item.connect("activate", self.on_item_activated, file)
        return [item]

    def on_item_activated(self, menu, file):
        # Convert file URI to local path
        filepath = unquote(file.get_uri()[7:])

        # Spawn kitty in that directory
        os.chdir(filepath)
        os.system("kitty &")
