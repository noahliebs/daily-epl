from soccer_player import SoccerPlayer
from trie import TrieNode


class PlayerTypeAhead(object):
    
    def __init__(self, players: list[SoccerPlayer]):
            root = TrieNode('*')
            for p in players:
                root.add(p.get_display_name(), p.get_display_name())

                for fn in p.get_first_name().split(" "):
                    root.add(fn, p.get_display_name())

                for ln in p.get_last_name().split(" "):
                    root.add(ln, p.get_display_name())

                root.add(p.get_first_name() + " " + p.get_last_name(), p.get_display_name())

            root.add("Captain America", "Christian Pulisic") # Because why not
            root.add("Jacquelyn", "Jack Harrison")
            root.add("Randy", "That's a zero")


            self.root = root

    def search_ahead(self, prefix):
        return sorted(list(self.root.find_prefix(prefix)))