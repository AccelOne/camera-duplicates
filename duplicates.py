from operator import itemgetter
import re
from utils import Roman


class DataSanitization():
    def __init__(self, file_name):
        self.sorted_names_weight = []
        self.renamed = {}
        self.file_name = file_name 

    def sanitize(self):
        """
            Sanitize using a determined set or rules a text file 
            with camera names or related prodct names.
            Returns a dictionary with each original name from the file
            as key and a new -'better'- name as value.
        """
        self.weighted_names()
        self.rename_to_most_used()
        return self.renamed

    def weighted_names(self):
        """
            Look up to each registry for similar ones.
            Similarity is defined as those that by removing spaces and
            case distinction are the same.
            Those similar will be grouped and will be counted to see
            which one was the most used.
        """
        f = open(self.file_name, "r")
        names_weight = {}
        for l in f.readlines():
            striped_line = l.strip()    
            no_spaces_lower_lines = striped_line.lower().replace(" ", "")
            if no_spaces_lower_lines not in names_weight:
                names_weight[no_spaces_lower_lines] = {"count_total": 1, "lines": {striped_line: 1}}
            else:
                names_weight[no_spaces_lower_lines]["count_total"] += 1
                if striped_line in names_weight[no_spaces_lower_lines]["lines"]:
                    names_weight[no_spaces_lower_lines]["lines"][striped_line] += 1
                else:
                    names_weight[no_spaces_lower_lines]["lines"][striped_line] = 1
                        
        self.sorted_names_weight = sorted(names_weight.items(),key=lambda k_v: k_v[1]["count_total"], reverse=True)

    def rename_to_most_used(self):
        """
            Creates a dictionary with each value from
            sorted_names_weight with the most used name in each list.
            The logic used is that the majority of users will write well
            so lets use those registries as guide.
        """
        renamed = {}
        for name in self.sorted_names_weight:
            lines = name[1]['lines']
            most_used_name = max(lines.items(), key=itemgetter(1))[0].capitalize()
            most_used_name = re.sub(' {2,}', ' ', most_used_name)
            most_used_name = self.fix_mark(most_used_name) 
            for line in lines:
                renamed[line] = most_used_name
        self.renamed = renamed

    def fix_mark(self, most_used_name):
        """
            Fix a common issue with mark statements.
            eg.'MK3' -> 'Mark III'. 'markiv' -> 'Mark IV'
        """
        regex_mark = re.compile("(m(?:ar)?k\s*)([ivx\d]*)", flags=re.IGNORECASE)
        search = regex_mark.search(most_used_name)
        if search:
            replacement = 'Mark'
            version = search.group(2)
            if version:
                if version.isdigit():
                    try:
                        version = Roman.int_to_roman(int(version))
                    except ValueError as error:
                        print(error)
                else:
                    version = version.upper()
                replacement += ' ' + version
            return most_used_name.replace(search.group(0), replacement) 
        return most_used_name

    def manual_replacement(self, original, replacement):
        """
            Replace the sanitized name for the given one for all 
            the matching items.
        """
        for db_name, sanitized_name in self.renamed.items():
            if sanitized_name == original:
                self.renamed[db_name] = replacement

    def manual_delete(self, deletable):
        """
            Receives a string argument.
            Deletes all items from renamed dictionary if either 
            its key or value matched with the given string.
        """
        to_delete = []
        for db_name, sanitized_name in self.renamed.items():
            if any(deletable in name for name in (sanitized_name, db_name)):
                to_delete.append(db_name)
        if to_delete:
            for k in to_delete:
                del(self.renamed[k])

    @property
    def renamed_by_sanitized(self):
        """Return names grouped by sanitized values"""
        grouped = {}
        for db_name, sanitized_name in self.renamed.items():
            grouped.setdefault(sanitized_name, []).append(db_name)
        return grouped

