from soccer_player import SoccerPlayer
from trie import TrieNode


class PlayerTypeAhead(object):
    
    def __init__(self, players: list[SoccerPlayer]):
            root = TrieNode('*')
            for p in players:
                root.add(p.get_display_name(), p.get_display_name())

            last_name_root = TrieNode("*")
            for p in players:
                last_name_root.add(p.get_last_name(), p.get_display_name())

                ## Example: Cristiano Ronaldo is the "First Name" according to PremierLeague.com
                first_names = p.get_first_name().split(" ")
                if len(first_names) > 1:
                    for fn in first_names[1:]:
                        last_name_root.add(fn, p.get_display_name())

            self.root = root
            self.last_name_root = last_name_root

                        
                        
    def search_ahead(self, prefix):
        using_all = self.root.find_prefix(prefix)
        using_last = self.last_name_root.find_prefix(prefix)
        return sorted(list(using_all.union(using_last)))