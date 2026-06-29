import os
from urllib.parse import unquote
from gi.repository import Nautilus, GObject

class KittyExtension(GObject.GObject, Nautilus.MenuProvider):

    def get_file_items(self, files):
        # API 4.0: 'window' argument removed
        return []

    def get_background_items(self, folder):
        # API 4.0: 'window' argument removed; 'file' is now 'folder'
        if folder.get_uri_scheme() != 'file':
            return []

        item = Nautilus.MenuItem(
            name='KittyExtension::OpenInKitty',
            label='Open in Kitty',
            tip='Open Kitty terminal in this directory'
        )
        item.connect('activate', self.on_item_activated, folder)
        return [item]

    def on_item_activated(self, menu, folder):
        # Convert folder URI to a local filesystem path
        filepath = unquote(folder.get_uri()[7:])
        
        # Spawn kitty directly into the directory
        os.chdir(filepath)
        os.system('kitty &')
